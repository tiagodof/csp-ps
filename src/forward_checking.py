"""
forward_checking.py — Backtracking with Forward Checking.

After each assignment, prunes values from the domains of unassigned
neighbours that would become inconsistent. If any domain becomes empty,
backtracks immediately (fail-early).
"""

import copy
from typing import Any, Dict, List, Optional
from src.csp import CSP


def forward_checking_search(csp: CSP) -> Optional[Dict[str, Any]]:
    """
    Entry point for forward checking search.
    Returns a complete assignment or None if no solution exists.
    """
    csp.reset_stats()
    # Work on copies of domains so we can restore them on backtrack
    domains = {v: list(d) for v, d in csp.domains.items()}
    return _fc_backtrack({}, domains, csp)


def _fc_backtrack(
    assignment: Dict[str, Any],
    domains: Dict[str, List[Any]],
    csp: CSP,
) -> Optional[Dict[str, Any]]:
    if len(assignment) == len(csp.variables):
        return assignment

    var = _select_unassigned_variable(assignment, domains, csp)

    for value in list(domains[var]):
        if csp.is_consistent(var, value, assignment):
            csp.assign(var, value, assignment)
            saved_domains = copy.deepcopy(domains)

            # Forward check: prune neighbours
            if _forward_check(var, value, assignment, domains, csp):
                result = _fc_backtrack(assignment, domains, csp)
                if result is not None:
                    return result

            # Restore domains on failure
            domains.update(saved_domains)
            csp.unassign(var, assignment)

    return None


def _forward_check(
    var: str,
    value: Any,
    assignment: Dict[str, Any],
    domains: Dict[str, List[Any]],
    csp: CSP,
) -> bool:
    """
    Remove values from unassigned neighbours that conflict with var=value.
    Returns False if any neighbour domain becomes empty (dead end).
    """
    for neighbour in csp.neighbours.get(var, []):
        if neighbour not in assignment:
            key = (neighbour, var)
            if key in csp.constraints:
                fn = csp.constraints[key]
                domains[neighbour] = [
                    v for v in domains[neighbour] if fn(v, value)
                ]
                if not domains[neighbour]:
                    return False
    return True


def _select_unassigned_variable(
    assignment: Dict[str, Any],
    domains: Dict[str, List[Any]],
    csp: CSP,
) -> str:
    """MRV with degree tie-breaking on current (pruned) domains."""
    unassigned = [v for v in csp.variables if v not in assignment]
    return min(
        unassigned,
        key=lambda v: (
            len(domains[v]),
            -len(csp.neighbours.get(v, [])),
        ),
    )
