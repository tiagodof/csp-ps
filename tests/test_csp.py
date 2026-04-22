"""Tests for the core CSP engine."""

import pytest
from src.csp import CSP


def make_simple_csp():
    """A simple 3-variable CSP: X, Y, Z each with domain [1, 2, 3]."""
    csp = CSP(
        variables=["X", "Y", "Z"],
        domains={"X": [1, 2, 3], "Y": [1, 2, 3], "Z": [1, 2, 3]},
    )
    csp.add_constraint("X", "Y", lambda x, y: x != y)
    csp.add_constraint("Y", "Z", lambda y, z: y != z)
    csp.add_constraint("X", "Z", lambda x, z: x != z)
    return csp


class TestCSPInit:
    def test_variables_stored(self):
        csp = make_simple_csp()
        assert csp.variables == ["X", "Y", "Z"]

    def test_domains_copied(self):
        original = {"X": [1, 2], "Y": [1, 2]}
        csp = CSP(["X", "Y"], original)
        original["X"].append(99)
        assert 99 not in csp.domains["X"]

    def test_neighbours_populated(self):
        csp = make_simple_csp()
        assert "Y" in csp.neighbours["X"]
        assert "Z" in csp.neighbours["X"]
        assert "X" in csp.neighbours["Y"]


class TestConsistency:
    def test_consistent_assignment(self):
        csp = make_simple_csp()
        assert csp.is_consistent("X", 1, {"Y": 2, "Z": 3})

    def test_inconsistent_same_value(self):
        csp = make_simple_csp()
        assert not csp.is_consistent("X", 2, {"Y": 2})

    def test_consistent_empty_assignment(self):
        csp = make_simple_csp()
        assert csp.is_consistent("X", 1, {})


class TestAssignUnassign:
    def test_assign_increments_counter(self):
        csp = make_simple_csp()
        assignment = {}
        csp.assign("X", 1, assignment)
        assert assignment["X"] == 1
        assert csp.nassigns == 1

    def test_unassign_removes_variable(self):
        csp = make_simple_csp()
        assignment = {"X": 1}
        csp.unassign("X", assignment)
        assert "X" not in assignment

    def test_unassign_missing_variable_is_safe(self):
        csp = make_simple_csp()
        csp.unassign("X", {})  # Should not raise


class TestGoalTest:
    def test_complete_valid_assignment(self):
        csp = make_simple_csp()
        assert csp.goal_test({"X": 1, "Y": 2, "Z": 3})

    def test_incomplete_assignment(self):
        csp = make_simple_csp()
        assert not csp.goal_test({"X": 1, "Y": 2})

    def test_invalid_assignment(self):
        csp = make_simple_csp()
        assert not csp.goal_test({"X": 1, "Y": 1, "Z": 2})


class TestNumConflicts:
    def test_no_conflicts(self):
        csp = make_simple_csp()
        assert csp.num_conflicts("X", 1, {"Y": 2, "Z": 3}) == 0

    def test_one_conflict(self):
        csp = make_simple_csp()
        assert csp.num_conflicts("X", 2, {"Y": 2, "Z": 3}) == 1

    def test_two_conflicts(self):
        csp = make_simple_csp()
        assert csp.num_conflicts("X", 2, {"Y": 2, "Z": 2}) == 2
