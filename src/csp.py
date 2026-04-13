"""
csp.py — Core Constraint Satisfaction Problem engine.

Defines the CSP class that holds variables, domains, and constraints,
and provides the interface used by all search algorithms.
"""

from typing import Any, Callable, Dict, List, Optional, Tuple


class CSP:
    """
    A generic Constraint Satisfaction Problem.

    Attributes:
        variables: List of variable names.
        domains:   Mapping from variable name to its list of possible values.
        neighbours: Mapping from variable to the list of variables it shares
                    a constraint with.
        constraints: Mapping from (var1, var2) to a binary constraint function
                     f(val1, val2) -> bool.
    """

    def __init__(
        self,
        variables: List[str],
        domains: Dict[str, List[Any]],
    ) -> None:
        self.variables: List[str] = variables
        self.domains: Dict[str, List[Any]] = {v: list(d) for v, d in domains.items()}
        self.neighbours: Dict[str, List[str]] = {v: [] for v in variables}
        self.constraints: Dict[Tuple[str, str], Callable] = {}
        self._nassigns: int = 0

    def add_constraint(
        self,
        var1: str,
        var2: str,
        constraint_fn: Callable[[Any, Any], bool],
    ) -> None:
        """Register a binary constraint between var1 and var2."""
        self.constraints[(var1, var2)] = constraint_fn
        self.constraints[(var2, var1)] = lambda a, b: constraint_fn(b, a)
        if var2 not in self.neighbours[var1]:
            self.neighbours[var1].append(var2)
        if var1 not in self.neighbours[var2]:
            self.neighbours[var2].append(var1)

    def is_consistent(
        self,
        var: str,
        value: Any,
        assignment: Dict[str, Any],
    ) -> bool:
        """
        Return True if assigning value to var is consistent with the
        current partial assignment.
        """
        for neighbour in self.neighbours.get(var, []):
            if neighbour in assignment:
                key = (var, neighbour)
                if key in self.constraints:
                    if not self.constraints[key](value, assignment[neighbour]):
                        return False
        return True

    def assign(self, var: str, value: Any, assignment: Dict[str, Any]) -> None:
        """Add var=value to assignment and increment the assignment counter."""
        assignment[var] = value
        self._nassigns += 1

    def unassign(self, var: str, assignment: Dict[str, Any]) -> None:
        """Remove var from assignment if present."""
        assignment.pop(var, None)

    def num_conflicts(self, var: str, value: Any, assignment: Dict[str, Any]) -> int:
        """Count how many neighbours of var conflict with value."""
        count = 0
        for neighbour in self.neighbours.get(var, []):
            if neighbour in assignment:
                key = (var, neighbour)
                if key in self.constraints:
                    if not self.constraints[key](value, assignment[neighbour]):
                        count += 1
        return count

    def goal_test(self, assignment: Dict[str, Any]) -> bool:
        """Return True if assignment is complete and satisfies all constraints."""
        if len(assignment) != len(self.variables):
            return False
        for (v1, v2), fn in self.constraints.items():
            if v1 in assignment and v2 in assignment:
                if not fn(assignment[v1], assignment[v2]):
                    return False
        return True

    @property
    def nassigns(self) -> int:
        """Total number of variable assignments made during search."""
        return self._nassigns

    def reset_stats(self) -> None:
        """Reset the assignment counter."""
        self._nassigns = 0
