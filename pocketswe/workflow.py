"""
PocketSWE workflow enforcement.

This module provides the ONLY valid way to start and complete work in PocketSWE.

- start_work() MUST be called before implementation begins
- complete_work() MUST be called to finish (enforces all gates)

IRON FIST: Agents declaring "done" without calling complete_work() have NOT
actually completed. The work record will remain in work/current/ as proof.
"""

import subprocess
import yaml
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional

from pocketswe.gates import Phase, GateRegistry, GateResult

# Import gate implementations so decorators register checks at module load.
import pocketswe.gates.checks  # noqa: F401


@dataclass
class WorkRecord:
    """A work record returned by start_work()."""
    work_id: str
    work_file: str
    north_star_id: str
    created_at: str


@dataclass
class CompletionResult:
    """Result of a completion attempt."""
    success: bool
    work_id: str
    message: str
    gate_results: list[GateResult] = field(default_factory=list)
    archived_to: Optional[str] = None


class WorkCreationError(Exception):
    """Raised when work creation fails."""
    def __init__(self, message: str, details: dict | None = None):
        self.message = message
        self.details = details or {}
        super().__init__(message)


class CompletionError(Exception):
    """Raised when completion is blocked by a gate."""
    def __init__(self, gate_name: str, message: str, details: dict | None = None):
        self.gate_name = gate_name
        self.message = message
        self.details = details or {}
        super().__init__(f"Completion blocked by {gate_name}: {message}")


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


def _git_revision(project_root: Path) -> str:
    """Get the current git revision."""
    return _git_output(project_root, "rev-parse", "HEAD")


def start_work(
    north_star_id: str,
    is_framework_change: bool = False,
    project_root: Optional[str | Path] = None,
) -> WorkRecord:
    """
    Create a work record before implementation.

    This MUST be called before implementing any feature. It creates the work
    record that will be validated and archived by complete_work().

    Args:
        north_star_id: ID of the North Star document (must exist)
        is_framework_change: If True, allows modifying protected paths
        project_root: Path to project root (auto-detected if not provided)

    Returns:
        WorkRecord with work_id and file path

    Raises:
        WorkCreationError: If North Star doesn't exist or validation fails
    """
    project_root = Path(project_root) if project_root else _find_project_root()
    work_dir = project_root / "work" / "current"

    # Validate North Star exists
    north_star_file = None
    for location in [
        project_root / "north-stars" / f"{north_star_id}.md",
        project_root / "north-stars" / f"{north_star_id}.yaml",
        project_root / "docs" / "north-stars" / f"{north_star_id}.md",
        project_root / "plans" / f"{north_star_id}.md",
    ]:
        if location.exists():
            north_star_file = location
            break

    if not north_star_file:
        raise WorkCreationError(
            f"North Star '{north_star_id}' not found. "
            "You must create a North Star document before implementation. "
            "Use the /planning-work skill to create one.",
            details={"north_star_id": north_star_id},
        )

    # Capture North Star snapshot for immutability check
    north_star_snapshot = north_star_file.read_text()

    # Capture git baseline for framework integrity check
    framework_baseline_revision = _git_revision(project_root)

    # Generate work ID
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    work_id = f"{timestamp}-{north_star_id}"

    # Create work record
    work_data = {
        "work_id": work_id,
        "north_star_id": north_star_id,
        "north_star_file": str(north_star_file),
        "north_star_snapshot": north_star_snapshot,
        "framework_baseline_revision": framework_baseline_revision,
        "is_framework_change": is_framework_change,
        "status": "in_progress",
        "created_at": datetime.now().isoformat(),
        "phases": {
            "planning": {"completed": True, "timestamp": datetime.now().isoformat()},
            "implementation": {"completed": False},
            "review": {"completed": False, "result": None},
            "verification": {"completed": False, "result": None},
        },
        "review": {
            "status": "not_reviewed",
            "checks": [],
        },
        "verification": {
            "status": "not_verified",
            "evidence": {},
        },
    }

    # Ensure work directory exists
    work_dir.mkdir(parents=True, exist_ok=True)

    # Write work file
    work_file = work_dir / f"{work_id}.yaml"
    with open(work_file, "w") as f:
        yaml.safe_dump(work_data, f, default_flow_style=False, sort_keys=False)

    return WorkRecord(
        work_id=work_id,
        work_file=str(work_file),
        north_star_id=north_star_id,
        created_at=work_data["created_at"],
    )


def complete_work(
    work_id: str,
    project_root: Optional[str | Path] = None,
    force: bool = False,
) -> CompletionResult:
    """
    Complete a work session, enforcing all gates.

    This is the ONLY valid way to complete work in PocketSWE.
    It runs all VERIFY → COMPLETE gates and validates phases completed.

    Review is ALWAYS regenerated. Prewritten approvals are discarded.

    Args:
        work_id: ID of the work to complete
        project_root: Path to project root (auto-detected if not provided)
        force: Deprecated. Gate overrides are prohibited.

    Returns:
        CompletionResult with success status and details

    Raises:
        CompletionError: If completion is blocked
    """
    project_root = Path(project_root) if project_root else _find_project_root()
    work_dir = project_root / "work" / "current"
    archive_dir = project_root / "work" / "archive"

    if force:
        raise CompletionError(
            gate_name="gate-integrity",
            message=(
                "force completion is disabled. Fix the issues instead of "
                "weakening completion gates."
            ),
        )

    # Load work file
    work_file = work_dir / f"{work_id}.yaml"
    if not work_file.exists():
        work_file = work_dir / f"{work_id}.yml"

    if not work_file.exists():
        raise CompletionError(
            gate_name="work-exists",
            message=f"Work file not found: {work_id}",
        )

    with open(work_file) as f:
        work_data = yaml.safe_load(f) or {}

    # Build context for gate checks
    context = {
        "work_id": work_id,
        "project_root": str(project_root),
        "north_star_id": work_data.get("north_star_id"),
    }

    # Check all VERIFY → COMPLETE gates
    can_complete, gate_results = GateRegistry.can_transition(
        Phase.VERIFY,
        Phase.COMPLETE,
        context,
    )

    # Update work data with gate results
    work_data["review"] = {
        "status": "pending",
        "timestamp": datetime.now().isoformat(),
        "gate_results": [
            {"gate": r.gate_name, "passed": r.passed, "message": r.message}
            for r in gate_results
        ],
    }

    failed_gates = [r for r in gate_results if not r.passed]

    if not can_complete:
        work_data["review"]["status"] = "rejected"
        with open(work_file, "w") as f:
            yaml.safe_dump(work_data, f, default_flow_style=False, sort_keys=False)

        first_failure = failed_gates[0] if failed_gates else None
        raise CompletionError(
            gate_name=first_failure.gate_name if first_failure else "unknown",
            message=first_failure.message if first_failure else "Gate check failed",
            details={
                "gate_results": [
                    {"gate": r.gate_name, "passed": r.passed, "message": r.message}
                    for r in gate_results
                ],
            },
        )

    # All gates passed - approve and archive
    work_data["review"]["status"] = "approved"
    work_data["status"] = "complete"
    work_data["completed_at"] = datetime.now().isoformat()
    work_data["completion"] = {
        "method": "pocketswe.workflow.complete_work",
        "gates_passed": True,
        "forced": False,
        "gate_results": [
            {"gate": r.gate_name, "passed": r.passed, "message": r.message}
            for r in gate_results
        ],
    }

    # Save updated work file
    with open(work_file, "w") as f:
        yaml.safe_dump(work_data, f, default_flow_style=False, sort_keys=False)

    # Archive the work
    archive_subdir = archive_dir / datetime.now().strftime("%Y-%m-%d")
    archive_subdir.mkdir(parents=True, exist_ok=True)
    archived_path = archive_subdir / work_file.name

    # Move to archive
    work_file.rename(archived_path)

    return CompletionResult(
        success=True,
        work_id=work_id,
        message="Work completed successfully",
        gate_results=gate_results,
        archived_to=str(archived_path),
    )


def mark_phase_complete(
    work_id: str,
    phase: str,
    result: Optional[str] = None,
    project_root: Optional[str | Path] = None,
) -> None:
    """
    Mark a phase as complete in the work record.

    Args:
        work_id: ID of the work record
        phase: One of: implementation, review, verification
        result: Result of the phase (e.g., PASS, REVISE, VERIFIED)
        project_root: Path to project root
    """
    project_root = Path(project_root) if project_root else _find_project_root()
    work_dir = project_root / "work" / "current"

    work_file = work_dir / f"{work_id}.yaml"
    if not work_file.exists():
        work_file = work_dir / f"{work_id}.yml"

    if not work_file.exists():
        return  # Silently ignore if no active work

    with open(work_file) as f:
        work_data = yaml.safe_load(f) or {}

    phases = work_data.setdefault("phases", {})
    phase_data = phases.setdefault(phase, {})
    phase_data["completed"] = True
    phase_data["timestamp"] = datetime.now().isoformat()
    if result:
        phase_data["result"] = result

    with open(work_file, "w") as f:
        yaml.safe_dump(work_data, f, default_flow_style=False, sort_keys=False)


def check_completion_ready(
    work_id: str,
    project_root: Optional[str | Path] = None,
) -> tuple[bool, list[GateResult]]:
    """
    Check if work is ready for completion (without completing it).

    Returns:
        (ready, gate_results)
    """
    project_root = Path(project_root) if project_root else _find_project_root()
    work_dir = project_root / "work" / "current"

    work_file = work_dir / f"{work_id}.yaml"
    if not work_file.exists():
        work_file = work_dir / f"{work_id}.yml"

    if not work_file.exists():
        return False, [GateResult(
            passed=False,
            gate_name="work-exists",
            message=f"Work file not found: {work_id}",
        )]

    with open(work_file) as f:
        work_data = yaml.safe_load(f) or {}

    context = {
        "work_id": work_id,
        "project_root": str(project_root),
        "north_star_id": work_data.get("north_star_id"),
    }

    return GateRegistry.can_transition(Phase.VERIFY, Phase.COMPLETE, context)
