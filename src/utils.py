"""
utils.py — Display and export utilities for timetable solutions.
"""

import csv
import time
from typing import Any, Callable, Dict, Optional, Tuple
from src.csp import CSP


def print_timetable(
    assignment: Dict[str, Tuple[str, str]],
    meta: Dict,
) -> None:
    """Print a formatted timetable from a solved assignment."""
    if not assignment:
        print("No solution found.")
        return

    course_map = meta["course_map"]
    slots = meta["slots"]

    # Group by slot
    by_slot: Dict[str, list] = {s: [] for s in slots}
    for course_id, (room_id, slot) in assignment.items():
        course = course_map[course_id]
        by_slot[slot].append(
            f"{course_id} ({course['lecturer']}) in {room_id}"
        )

    print()
    print(f"{'TIME SLOT':<20} {'CLASSES'}")
    print("-" * 70)
    for slot in slots:
        classes = by_slot[slot]
        if classes:
            print(f"{slot:<20} {classes[0]}")
            for cls in classes[1:]:
                print(f"{'':20} {cls}")
    print()


def export_csv(
    assignment: Dict[str, Tuple[str, str]],
    meta: Dict,
    path: str,
) -> None:
    """Export the timetable to a CSV file."""
    course_map = meta["course_map"]
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Course", "Lecturer", "Students", "Room", "Slot"])
        for course_id, (room_id, slot) in sorted(assignment.items()):
            c = course_map[course_id]
            writer.writerow([
                course_id,
                c["lecturer"],
                c.get("students", ""),
                room_id,
                slot,
            ])
    print(f"Timetable exported to {path}")


def run_solver(
    name: str,
    solver_fn: Callable[[CSP], Optional[Dict]],
    csp: CSP,
    meta: Dict,
    verbose: bool = True,
) -> Tuple[Optional[Dict], float, int]:
    """
    Run a solver function, measure time and assignments, and print results.

    Returns:
        (assignment, elapsed_seconds, num_assignments)
    """
    start = time.perf_counter()
    result = solver_fn(csp)
    elapsed = time.perf_counter() - start

    if verbose:
        status = "SOLVED" if result else "NO SOLUTION"
        print(f"[{name}] {status} | "
              f"Time: {elapsed:.4f}s | "
              f"Assignments: {csp.nassigns}")
        if result:
            print_timetable(result, meta)

    return result, elapsed, csp.nassigns


def print_comparison(results: Dict[str, Tuple[Optional[Dict], float, int]]) -> None:
    """Print a side-by-side comparison table of solver results."""
    print("\n" + "=" * 60)
    print(f"{'ALGORITHM':<25} {'TIME':>10} {'ASSIGNMENTS':>14} {'SOLVED':>8}")
    print("=" * 60)
    for name, (solution, elapsed, nassigns) in results.items():
        solved = "Yes" if solution else "No"
        print(f"{name:<25} {elapsed:>9.4f}s {nassigns:>14} {solved:>8}")
    print("=" * 60)
