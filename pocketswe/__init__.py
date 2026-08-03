"""
PocketSWE Iron Fist enforcement module.

This module provides runtime enforcement of the PocketSWE work protocol.
Agents CANNOT bypass these constraints - they are enforced at the tool level.

Usage:
    from pocketswe import start_work, complete_work

    # BEFORE implementation
    work = start_work(north_star_id="feature-x")

    # ... implement, review, verify ...

    # AFTER verification
    result = complete_work(work_id=work.work_id)
    # Only if result.success can you tell user "done"
"""

from pocketswe.workflow import (
    start_work,
    complete_work,
    mark_phase_complete,
    check_completion_ready,
    WorkRecord,
    CompletionResult,
    WorkCreationError,
    CompletionError,
)

__all__ = [
    "start_work",
    "complete_work",
    "mark_phase_complete",
    "check_completion_ready",
    "WorkRecord",
    "CompletionResult",
    "WorkCreationError",
    "CompletionError",
]
