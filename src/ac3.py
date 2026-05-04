"""
ac3.py — AC-3 Arc Consistency algorithm.

Enforces arc consistency by iteratively removing values from domains
that have no support in neighbouring variables. Can be used as a
preprocessing step or interleaved with backtracking search.
"""

import copy
from collections import deque
from typing import Any, Dict, List, Optional, Tuple
from src.csp import CSP


def ac3(csp: CSP, domains: Optional[Dict[str, List[Any]]] = None) -> bool:
    """
    Run AC-3 on the CSP.

    Args:
        csp:     The CSP instance.
        domains: Optional domain dict to prune (uses csp.domains if None).

    Returns:
        True if arc consistency is achieved, False if any domain becomes empty.
    """
    if domains is None:
        domains = csp.domains

    queue: deque[Tuple[str, str]] = deque(csp.constraints.keys())

    while queue:
        xi, xj = queue.popleft()
        if _revise(csp, xi, xj, domains):
            if not domains[xi]:
                return False  # Domain wiped out — no solution possible
            for xk in csp.neighbours.get(xi, []):
                if xk != xj:
                    queue.append((xk, xi))

    return True


def _revise(
    csp: CSP,
    xi: str,
    xj: str,
    domains: Dict[str, List[Any]],
) -> bool:
    """
    Remove values from domains[xi] that have no support in domains[xj].
    Returns True if any value was removed.
    """
    revised = False
    fn = csp.constraints.get((xi, xj))
    if fn is None:
        return False

    to_remove = []
    for vx in domains[xi]:
        if not any(fn(vx, vy) for vy in domains[xj]):
            to_remove.append(vx)

    for v in to_remove:
        domains[xi].remove(v)
        revised = True

    return revised


def ac3_search(csp: CSP) -> Optional[Dict[str, Any]]:
    """
    Backtracking search with AC-3 preprocessing and interleaved propagation.
    Returns a complete assignment or None if no solution exists.
    """
    csp.reset_stats()
    domains = {v: list(d) for v, d in csp.domains.items()}

    if not ac3(csp, domains):
        return None  # Problem is unsatisfiable

    return _ac3_backtrack({}, domains, csp)


def _ac3_backtrack(
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
            new_domains = copy.deepcopy(domains)
            new_domains[var] = [value]

            if ac3(csp, new_domains):
                result = _ac3_backtrack(assignment, new_domains, csp)
                if result is not None:
                    return result

            csp.unassign(var, assignment)

    return None


def _select_unassigned_variable(
    assignment: Dict[str, Any],
    domains: Dict[str, List[Any]],
    csp: CSP,
) -> str:
    """MRV with degree tie-breaking."""
    unassigned = [v for v in csp.variables if v not in assignment]
    return min(
        unassigned,
        key=lambda v: (
            len(domains[v]),
            -len(csp.neighbours.get(v, [])),
        ),
    )
