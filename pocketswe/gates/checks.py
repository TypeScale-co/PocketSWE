"""
Gate check implementations.

These are the actual gate functions that enforce constraints
at phase transitions. Mirrors pocketops/gates/checks.py.
"""

import subprocess
from pathlib import Path

from pocketswe.gates.registry import GateRegistry, GateResult, Phase


_PROTECTED_FRAMEWORK_PATHS = (
    "AGENTS.md",
    ".agents/",
    "pocketswe/",
    "docs/architecture.md",
    "docs/work-protocol.md",
    "docs/code-review.md",
    "docs/verification.md",
)


def _find_project_root() -> Path:
    """Find the PocketSWE project root."""
    cwd = Path.cwd()
    current = cwd
    while current != current.parent:
        if (current / "AGENTS.md").exists() and (current / ".agents").exists():
            return current
        current = current.parent
    return cwd


def _git_output(project_root: Path, *args: str) -> str:
    """Run a read-only Git command, returning an empty string on failure."""
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=project_root,
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return ""
    return result.stdout.rstrip("\n")


def _is_protected_framework_path(path: str) -> bool:
    """Check if a path is a protected framework path."""
    normalized = path.strip().replace("\\", "/")
    return any(
        normalized == protected.rstrip("/") or normalized.startswith(protected)
        for protected in _PROTECTED_FRAMEWORK_PATHS
    )


def _changed_paths(project_root: Path, baseline_revision: str) -> list[str]:
    """Collect committed and working-tree changes made since work started."""
    paths: set[str] = set()

    if baseline_revision:
        current_revision = _git_output(project_root, "rev-parse", "HEAD")
        if current_revision and current_revision != baseline_revision:
            paths.update(
                line
                for line in _git_output(
                    project_root,
                    "diff",
                    "--name-only",
                    f"{baseline_revision}..{current_revision}",
                ).splitlines()
                if line
            )

    status = _git_output(
        project_root,
        "status",
        "--porcelain",
        "--untracked-files=all",
    )
    for line in status.splitlines():
        if len(line) < 4:
            continue
        path = line[3:]
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        paths.add(path.strip('"'))

    return sorted(paths)


@GateRegistry.register(
    name="north-star-required",
    from_phase=Phase.PLAN,
    to_phase=Phase.BUILD,
    description="North Star document must exist before building",
)
def check_north_star_exists(context: dict) -> GateResult:
    """
    Verify a North Star document exists before allowing BUILD phase.

    Context should contain:
        - north_star_id: ID of the North Star to check
        - project_root: Optional path to project root
    """
    north_star_id = context.get("north_star_id")
    project_root = Path(context.get("project_root", _find_project_root()))

    if not north_star_id:
        return GateResult(
            passed=False,
            gate_name="north-star-required",
            message="No north_star_id provided. Use /planning-work skill first.",
        )

    # Check various locations for North Star
    for location in [
        project_root / "north-stars" / f"{north_star_id}.md",
        project_root / "north-stars" / f"{north_star_id}.yaml",
        project_root / "docs" / "north-stars" / f"{north_star_id}.md",
    ]:
        if location.exists():
            return GateResult(
                passed=True,
                gate_name="north-star-required",
                message=f"North Star found: {location.name}",
                details={"path": str(location)},
            )

    return GateResult(
        passed=False,
        gate_name="north-star-required",
        message=f"North Star '{north_star_id}' not found. Create one with /planning-work skill.",
    )


@GateRegistry.register(
    name="review-required",
    from_phase=Phase.REVIEW,
    to_phase=Phase.VERIFY,
    description="Code review must pass before verification",
)
def check_review_completed(context: dict) -> GateResult:
    """
    Verify code review was completed before allowing VERIFY phase.

    Context should contain:
        - work_id: ID of the current work
        - project_root: Optional path to project root
    """
    work_id = context.get("work_id")
    project_root = Path(context.get("project_root", _find_project_root()))
    work_dir = project_root / "work" / "current"

    if not work_id:
        return GateResult(
            passed=False,
            gate_name="review-required",
            message="No work_id provided in context",
        )

    work_file = work_dir / f"{work_id}.yaml"
    if not work_file.exists():
        work_file = work_dir / f"{work_id}.yml"

    if not work_file.exists():
        return GateResult(
            passed=False,
            gate_name="review-required",
            message=f"Work file not found: {work_id}",
        )

    import yaml
    with open(work_file) as f:
        work_data = yaml.safe_load(f) or {}

    phases = work_data.get("phases", {})
    review_phase = phases.get("review", {})

    if not review_phase.get("completed"):
        return GateResult(
            passed=False,
            gate_name="review-required",
            message="Code review not completed. Use /reviewing-code skill.",
        )

    result = review_phase.get("result")
    if result == "PASS":
        return GateResult(
            passed=True,
            gate_name="review-required",
            message="Code review passed",
        )
    elif result == "REVISE":
        return GateResult(
            passed=False,
            gate_name="review-required",
            message="Code review returned REVISE - blocking findings remain",
        )
    else:
        return GateResult(
            passed=False,
            gate_name="review-required",
            message=f"Code review result unclear: {result}",
        )


@GateRegistry.register(
    name="verification-required",
    from_phase=Phase.VERIFY,
    to_phase=Phase.COMPLETE,
    description="Verification with evidence must pass before completion",
)
def check_verification_passed(context: dict) -> GateResult:
    """
    Verify the feature was verified with evidence before allowing COMPLETE phase.

    Context should contain:
        - work_id: ID of the current work
        - project_root: Optional path to project root
    """
    work_id = context.get("work_id")
    project_root = Path(context.get("project_root", _find_project_root()))
    work_dir = project_root / "work" / "current"

    if not work_id:
        return GateResult(
            passed=False,
            gate_name="verification-required",
            message="No work_id provided in context",
        )

    work_file = work_dir / f"{work_id}.yaml"
    if not work_file.exists():
        work_file = work_dir / f"{work_id}.yml"

    if not work_file.exists():
        return GateResult(
            passed=False,
            gate_name="verification-required",
            message=f"Work file not found: {work_id}",
        )

    import yaml
    with open(work_file) as f:
        work_data = yaml.safe_load(f) or {}

    phases = work_data.get("phases", {})
    verify_phase = phases.get("verification", {})

    if not verify_phase.get("completed"):
        return GateResult(
            passed=False,
            gate_name="verification-required",
            message="Verification not completed. Use /verifying-features skill.",
        )

    result = verify_phase.get("result")
    if result == "VERIFIED":
        return GateResult(
            passed=True,
            gate_name="verification-required",
            message="Verification passed",
        )
    else:
        return GateResult(
            passed=False,
            gate_name="verification-required",
            message=f"Verification result: {result}. Must be VERIFIED.",
        )


@GateRegistry.register(
    name="framework-integrity",
    from_phase=Phase.VERIFY,
    to_phase=Phase.COMPLETE,
    description="Ordinary work must not modify protected framework paths",
)
def check_framework_integrity(context: dict) -> GateResult:
    """
    Verify that protected framework paths were not modified during ordinary work.

    Protected paths: AGENTS.md, .agents/, pocketswe/, docs/*.md

    Context should contain:
        - work_id: ID of the current work
        - project_root: Optional path to project root
    """
    work_id = context.get("work_id")
    project_root = Path(context.get("project_root", _find_project_root()))
    work_dir = project_root / "work" / "current"

    if not work_id:
        return GateResult(
            passed=True,
            gate_name="framework-integrity",
            message="No work context - skipping framework check",
        )

    work_file = work_dir / f"{work_id}.yaml"
    if not work_file.exists():
        work_file = work_dir / f"{work_id}.yml"

    if not work_file.exists():
        return GateResult(
            passed=True,
            gate_name="framework-integrity",
            message="No work file - skipping framework check",
        )

    import yaml
    with open(work_file) as f:
        work_data = yaml.safe_load(f) or {}

    # Check if this is a framework change (allowed to modify protected paths)
    if work_data.get("is_framework_change"):
        return GateResult(
            passed=True,
            gate_name="framework-integrity",
            message="Framework change - protected path modifications allowed",
        )

    # Get baseline revision from work record
    baseline_revision = work_data.get("framework_baseline_revision", "")

    # Check for protected path changes
    changed_paths = _changed_paths(project_root, baseline_revision)
    protected_changes = [
        path for path in changed_paths if _is_protected_framework_path(path)
    ]

    if protected_changes:
        return GateResult(
            passed=False,
            gate_name="framework-integrity",
            message=(
                "Ordinary work modified protected framework files: "
                + ", ".join(protected_changes)
            ),
            details={"protected_changes": protected_changes},
        )

    return GateResult(
        passed=True,
        gate_name="framework-integrity",
        message="No protected framework changes detected",
    )


@GateRegistry.register(
    name="north-star-integrity",
    from_phase=Phase.VERIFY,
    to_phase=Phase.COMPLETE,
    description="North Star must not change after work started",
)
def check_north_star_integrity(context: dict) -> GateResult:
    """
    Verify the North Star was not modified after work started.

    The North Star snapshot is captured at start_work() and compared
    at complete_work(). Changes indicate scope creep or goal drift.

    Context should contain:
        - work_id: ID of the current work
        - project_root: Optional path to project root
    """
    work_id = context.get("work_id")
    project_root = Path(context.get("project_root", _find_project_root()))
    work_dir = project_root / "work" / "current"

    if not work_id:
        return GateResult(
            passed=True,
            gate_name="north-star-integrity",
            message="No work context - skipping North Star check",
        )

    work_file = work_dir / f"{work_id}.yaml"
    if not work_file.exists():
        work_file = work_dir / f"{work_id}.yml"

    if not work_file.exists():
        return GateResult(
            passed=True,
            gate_name="north-star-integrity",
            message="No work file - skipping North Star check",
        )

    import yaml
    with open(work_file) as f:
        work_data = yaml.safe_load(f) or {}

    north_star_file = work_data.get("north_star_file")
    north_star_snapshot = work_data.get("north_star_snapshot")

    if not north_star_file or not north_star_snapshot:
        return GateResult(
            passed=True,
            gate_name="north-star-integrity",
            message="No North Star snapshot to compare",
        )

    # Read current North Star content
    north_star_path = Path(north_star_file)
    if not north_star_path.exists():
        return GateResult(
            passed=False,
            gate_name="north-star-integrity",
            message="North Star file was deleted during work",
        )

    current_content = north_star_path.read_text()

    if current_content != north_star_snapshot:
        return GateResult(
            passed=False,
            gate_name="north-star-integrity",
            message=(
                "North Star was modified after work started. "
                "This indicates scope creep. Create a new work record if goals changed."
            ),
        )

    return GateResult(
        passed=True,
        gate_name="north-star-integrity",
        message="North Star unchanged since work started",
    )
