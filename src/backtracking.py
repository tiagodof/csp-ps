"""
backtracking.py — Backtracking search for CSP.

Implements recursive backtracking with:
  - MRV (Minimum Remaining Values) heuristic for variable ordering
  - LCV (Least Constraining Value) heuristic for value ordering
"""

from typing import Any, Dict, List, Optional
from src.csp import CSP


def backtracking_search(csp: CSP) -> Optional[Dict[str, Any]]:
    """
    Entry point for backtracking search.
    Returns a complete assignment or None if no solution exists.
    """
    csp.reset_stats()
    return _backtrack({}, csp)


def _backtrack(
    assignment: Dict[str, Any],
    csp: CSP,
) -> Optional[Dict[str, Any]]:
    if len(assignment) == len(csp.variables):
        return assignment

    var = _select_unassigned_variable(assignment, csp)

    for value in _order_domain_values(var, assignment, csp):
        if csp.is_consistent(var, value, assignment):
            csp.assign(var, value, assignment)
            result = _backtrack(assignment, csp)
            if result is not None:
                return result
            csp.unassign(var, assignment)

    return None


def _select_unassigned_variable(
    assignment: Dict[str, Any],
    csp: CSP,
) -> str:
    """
    MRV heuristic: choose the unassigned variable with the fewest
    remaining legal values. Ties are broken by degree (most constraints).
    """
    unassigned = [v for v in csp.variables if v not in assignment]
    return min(
        unassigned,
        key=lambda v: (
            len(csp.domains[v]),
            -len(csp.neighbours.get(v, [])),
        ),
    )


def _order_domain_values(
    var: str,
    assignment: Dict[str, Any],
    csp: CSP,
) -> List[Any]:
    """
    LCV heuristic: order values by the number of conflicts they introduce
    in neighbouring variables (ascending — least constraining first).
    """
    return sorted(
        csp.domains[var],
        key=lambda val: csp.num_conflicts(var, val, assignment),
    )
