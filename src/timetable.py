"""
timetable.py — University timetable domain model.

Builds a CSP instance from a timetable problem definition.
Each variable is a course. Each value is a (room, slot) tuple.
Constraints enforce no room conflicts, no lecturer conflicts,
and room capacity.
"""

import json
from typing import Any, Dict, List, Tuple
from src.csp import CSP


# A slot value is a tuple: (room_id, time_slot)
Slot = Tuple[str, str]


def load_problem(path: str) -> Dict:
    """Load a timetable problem definition from a JSON file."""
    with open(path, "r") as f:
        return json.load(f)


def build_csp(problem: Dict) -> Tuple[CSP, Dict]:
    """
    Build a CSP from a timetable problem definition.

    Problem format:
    {
        "courses":  [{"id": "CS101", "lecturer": "Dr. Smith", "students": 30}],
        "rooms":    [{"id": "A101", "capacity": 40}],
        "slots":    ["Mon-09:00", "Mon-11:00", ...],
        "lecturer_availability": {"Dr. Smith": ["Mon-09:00", ...]}
    }

    Returns:
        csp:  The CSP instance.
        meta: Metadata dict for display purposes.
    """
    courses = problem["courses"]
    rooms = problem["rooms"]
    slots = problem["slots"]
    availability = problem.get("lecturer_availability", {})

    variables = [c["id"] for c in courses]
    course_map = {c["id"]: c for c in courses}
    room_map = {r["id"]: r for r in rooms}

    # Domain: all (room, slot) pairs where the room fits the course
    # and the lecturer is available
    domains: Dict[str, List[Slot]] = {}
    for course in courses:
        lecturer = course["lecturer"]
        n_students = course.get("students", 0)
        avail = set(availability.get(lecturer, slots))

        domain = []
        for room in rooms:
            if room["capacity"] >= n_students:
                for slot in slots:
                    if slot in avail:
                        domain.append((room["id"], slot))
        domains[course["id"]] = domain

    csp = CSP(variables, domains)

    # Add pairwise constraints between all courses
    for i in range(len(variables)):
        for j in range(i + 1, len(variables)):
            c1 = variables[i]
            c2 = variables[j]
            lec1 = course_map[c1]["lecturer"]
            lec2 = course_map[c2]["lecturer"]

            def make_constraint(lecturer1, lecturer2):
                def constraint(val1: Slot, val2: Slot) -> bool:
                    room1, slot1 = val1
                    room2, slot2 = val2
                    # No room conflict
                    if room1 == room2 and slot1 == slot2:
                        return False
                    # No lecturer conflict
                    if lecturer1 == lecturer2 and slot1 == slot2:
                        return False
                    return True
                return constraint

            csp.add_constraint(c1, c2, make_constraint(lec1, lec2))

    meta = {
        "course_map": course_map,
        "room_map": room_map,
        "slots": slots,
    }
    return csp, meta
