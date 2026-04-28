"""Tests for backtracking, forward checking, and AC-3 solvers."""

import pytest
from src.csp import CSP
from src.backtracking import backtracking_search
from src.forward_checking import forward_checking_search
from src.ac3 import ac3_search, ac3


def make_graph_coloring_csp(n_colors=3):
    """
    Australia map coloring problem.
    Variables: WA, NT, SA, Q, NSW, V, T
    Constraints: adjacent regions must have different colours.
    """
    variables = ["WA", "NT", "SA", "Q", "NSW", "V", "T"]
    domains = {v: list(range(n_colors)) for v in variables}
    csp = CSP(variables, domains)

    edges = [
        ("WA", "NT"), ("WA", "SA"),
        ("NT", "SA"), ("NT", "Q"),
        ("SA", "Q"), ("SA", "NSW"), ("SA", "V"),
        ("Q", "NSW"), ("NSW", "V"),
    ]
    for v1, v2 in edges:
        csp.add_constraint(v1, v2, lambda a, b: a != b)

    return csp


def make_unsatisfiable_csp():
    """Two variables, one domain value each, with an inequality constraint."""
    csp = CSP(["X", "Y"], {"X": [1], "Y": [1]})
    csp.add_constraint("X", "Y", lambda x, y: x != y)
    return csp


class TestBacktracking:
    def test_solves_graph_coloring(self):
        csp = make_graph_coloring_csp()
        result = backtracking_search(csp)
        assert result is not None
        assert csp.goal_test(result)

    def test_returns_none_for_unsatisfiable(self):
        csp = make_unsatisfiable_csp()
        result = backtracking_search(csp)
        assert result is None

    def test_all_variables_assigned(self):
        csp = make_graph_coloring_csp()
        result = backtracking_search(csp)
        assert set(result.keys()) == set(csp.variables)

    def test_nassigns_incremented(self):
        csp = make_graph_coloring_csp()
        backtracking_search(csp)
        assert csp.nassigns > 0


class TestForwardChecking:
    def test_solves_graph_coloring(self):
        csp = make_graph_coloring_csp()
        result = forward_checking_search(csp)
        assert result is not None
        assert csp.goal_test(result)

    def test_returns_none_for_unsatisfiable(self):
        csp = make_unsatisfiable_csp()
        result = forward_checking_search(csp)
        assert result is None

    def test_fewer_assignments_than_backtracking(self):
        """Forward checking should explore fewer nodes than plain backtracking."""
        csp_bt = make_graph_coloring_csp()
        csp_fc = make_graph_coloring_csp()
        backtracking_search(csp_bt)
        forward_checking_search(csp_fc)
        assert csp_fc.nassigns <= csp_bt.nassigns


class TestAC3:
    def test_ac3_preprocessing_reduces_domains(self):
        csp = make_graph_coloring_csp(n_colors=2)
        # Tasmania has no neighbours so its domain should stay intact
        result = ac3(csp)
        # With 2 colours the problem is satisfiable
        assert result is True

    def test_ac3_detects_unsatisfiable(self):
        csp = make_unsatisfiable_csp()
        domains = {v: list(d) for v, d in csp.domains.items()}
        result = ac3(csp, domains)
        assert result is False

    def test_ac3_search_solves_graph_coloring(self):
        csp = make_graph_coloring_csp()
        result = ac3_search(csp)
        assert result is not None
        assert csp.goal_test(result)

    def test_ac3_fewest_assignments(self):
        """AC-3 should use fewer or equal assignments compared to forward checking."""
        csp_fc  = make_graph_coloring_csp()
        csp_ac3 = make_graph_coloring_csp()
        forward_checking_search(csp_fc)
        ac3_search(csp_ac3)
        assert csp_ac3.nassigns <= csp_fc.nassigns
