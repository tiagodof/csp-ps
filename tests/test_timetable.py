"""Tests for the timetable domain model and CSP builder."""

import pytest
from src.timetable import build_csp
from src.backtracking import backtracking_search


SMALL_PROBLEM = {
    "courses": [
        {"id": "CS101", "lecturer": "Dr. Murphy", "students": 25},
        {"id": "CS102", "lecturer": "Dr. Kelly",  "students": 30},
        {"id": "CS201", "lecturer": "Dr. Murphy", "students": 20},
    ],
    "rooms": [
        {"id": "A101", "capacity": 40},
        {"id": "B203", "capacity": 30},
    ],
    "slots": [
        "Mon-09:00", "Mon-11:00", "Tue-09:00", "Tue-11:00", "Wed-09:00"
    ],
    "lecturer_availability": {
        "Dr. Murphy": ["Mon-09:00", "Mon-11:00", "Tue-09:00"],
        "Dr. Kelly":  ["Mon-11:00", "Tue-09:00", "Tue-11:00", "Wed-09:00"],
    },
}

CAPACITY_PROBLEM = {
    "courses": [
        {"id": "BIG", "lecturer": "Dr. X", "students": 50},
        {"id": "SMALL", "lecturer": "Dr. Y", "students": 10},
    ],
    "rooms": [
        {"id": "LARGE", "capacity": 60},
        {"id": "TINY",  "capacity": 15},
    ],
    "slots": ["Mon-09:00", "Mon-11:00"],
    "lecturer_availability": {},
}


class TestBuildCSP:
    def test_variables_match_courses(self):
        csp, _ = build_csp(SMALL_PROBLEM)
        assert set(csp.variables) == {"CS101", "CS102", "CS201"}

    def test_domains_respect_capacity(self):
        csp, _ = build_csp(CAPACITY_PROBLEM)
        # BIG course (50 students) should only be assigned to LARGE room
        for room_id, slot in csp.domains["BIG"]:
            assert room_id == "LARGE"

    def test_domains_respect_availability(self):
        csp, _ = build_csp(SMALL_PROBLEM)
        # Dr. Murphy is only available Mon-09:00, Mon-11:00, Tue-09:00
        allowed_slots = {"Mon-09:00", "Mon-11:00", "Tue-09:00"}
        for room_id, slot in csp.domains["CS101"]:
            assert slot in allowed_slots

    def test_constraints_registered(self):
        csp, _ = build_csp(SMALL_PROBLEM)
        # All pairs should have constraints
        assert ("CS101", "CS102") in csp.constraints
        assert ("CS101", "CS201") in csp.constraints

    def test_no_room_conflict_in_solution(self):
        csp, _ = build_csp(SMALL_PROBLEM)
        solution = backtracking_search(csp)
        assert solution is not None
        # Check no two courses share the same room and slot
        seen = set()
        for course, (room, slot) in solution.items():
            key = (room, slot)
            assert key not in seen, f"Room conflict at {key}"
            seen.add(key)

    def test_no_lecturer_conflict_in_solution(self):
        csp, _ = build_csp(SMALL_PROBLEM)
        solution = backtracking_search(csp)
        assert solution is not None
        # Check Dr. Murphy is not scheduled twice in the same slot
        courses = SMALL_PROBLEM["courses"]
        lecturer_map = {c["id"]: c["lecturer"] for c in courses}
        lecturer_slots: dict = {}
        for course, (room, slot) in solution.items():
            lec = lecturer_map[course]
            key = (lec, slot)
            assert key not in lecturer_slots, f"Lecturer conflict: {key}"
            lecturer_slots[key] = course
