"""
Gate registry for phase transitions.

Mirrors pocketops/gates/ - defines workflow phases and gates that guard transitions.
"""

from pocketswe.gates.registry import Phase, Gate, GateResult, GateRegistry

__all__ = ["Phase", "Gate", "GateResult", "GateRegistry"]
