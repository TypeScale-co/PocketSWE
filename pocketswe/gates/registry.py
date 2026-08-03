"""
Gate registry for phase transitions.

Defines workflow phases and the gates that guard transitions between them.
Mirrors pocketops/gates/registry.py.
"""

from enum import Enum
from dataclasses import dataclass
from typing import Callable, Optional


class Phase(str, Enum):
    """
    Workflow phases in PocketSWE.

    The workflow progresses through these phases,
    with gates enforcing requirements at each transition.
    """
    PLAN = "plan"
    BUILD = "build"
    REVIEW = "review"
    VERIFY = "verify"
    COMPLETE = "complete"

    @property
    def next(self) -> Optional["Phase"]:
        """Get the next phase in the workflow."""
        phases = list(Phase)
        idx = phases.index(self)
        if idx < len(phases) - 1:
            return phases[idx + 1]
        return None

    @property
    def previous(self) -> Optional["Phase"]:
        """Get the previous phase in the workflow."""
        phases = list(Phase)
        idx = phases.index(self)
        if idx > 0:
            return phases[idx - 1]
        return None


@dataclass
class GateResult:
    """Result of a gate check."""
    passed: bool
    gate_name: str
    message: str
    details: Optional[dict] = None

    def __bool__(self) -> bool:
        return self.passed


@dataclass
class Gate:
    """A gate that guards a phase transition."""
    name: str
    from_phase: Phase
    to_phase: Phase
    check: Callable[..., GateResult]
    description: str


class GateRegistry:
    """
    Registry of all gates in the system.

    Gates are registered at module load time and checked
    when transitioning between phases.
    """

    _gates: dict[tuple[Phase, Phase], list[Gate]] = {}

    @classmethod
    def register(
        cls,
        name: str,
        from_phase: Phase,
        to_phase: Phase,
        description: str,
    ) -> Callable:
        """
        Decorator to register a gate function.

        Usage:
            @GateRegistry.register(
                name="north-star-required",
                from_phase=Phase.PLAN,
                to_phase=Phase.BUILD,
                description="North Star must exist before building"
            )
            def check_north_star_exists(context: dict) -> GateResult:
                ...
        """
        def decorator(func: Callable[..., GateResult]) -> Callable[..., GateResult]:
            gate = Gate(
                name=name,
                from_phase=from_phase,
                to_phase=to_phase,
                check=func,
                description=description,
            )
            key = (from_phase, to_phase)
            if key not in cls._gates:
                cls._gates[key] = []
            cls._gates[key].append(gate)
            return func
        return decorator

    @classmethod
    def check_transition(
        cls,
        from_phase: Phase,
        to_phase: Phase,
        context: dict,
    ) -> list[GateResult]:
        """
        Check all gates for a phase transition.

        Returns a list of GateResults. All must pass for
        the transition to be allowed.
        """
        key = (from_phase, to_phase)
        gates = cls._gates.get(key, [])

        results = []
        for gate in gates:
            try:
                result = gate.check(context)
                results.append(result)
            except Exception as e:
                results.append(GateResult(
                    passed=False,
                    gate_name=gate.name,
                    message=f"Gate check failed with error: {e}",
                ))

        return results

    @classmethod
    def can_transition(
        cls,
        from_phase: Phase,
        to_phase: Phase,
        context: dict,
    ) -> tuple[bool, list[GateResult]]:
        """
        Check if a phase transition is allowed.

        Returns (allowed, results) tuple.
        """
        results = cls.check_transition(from_phase, to_phase, context)
        allowed = all(r.passed for r in results)
        return allowed, results

    @classmethod
    def get_gates(cls, from_phase: Phase, to_phase: Phase) -> list[Gate]:
        """Get all gates for a transition."""
        return cls._gates.get((from_phase, to_phase), [])

    @classmethod
    def list_all_gates(cls) -> list[Gate]:
        """List all registered gates."""
        all_gates = []
        for gates in cls._gates.values():
            all_gates.extend(gates)
        return all_gates

    @classmethod
    def clear(cls) -> None:
        """Clear all registered gates (for testing)."""
        cls._gates = {}
