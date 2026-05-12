"""
main.py — Entry point for the CSP Timetable Scheduler.

Runs all three solvers on a dataset and prints a comparison table.

Usage:
    python main.py
    python main.py --solver backtracking
    python main.py --solver forward_checking
    python main.py --solver ac3
    python main.py --data data/sample_medium.json --solver ac3
"""

import argparse
import copy

from src.timetable import load_problem, build_csp
from src.backtracking import backtracking_search
from src.forward_checking import forward_checking_search
from src.ac3 import ac3_search
from src.utils import run_solver, print_comparison


SOLVERS = {
    "backtracking":     backtracking_search,
    "forward_checking": forward_checking_search,
    "ac3":              ac3_search,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="CSP University Timetable Scheduler"
    )
    parser.add_argument(
        "--data",
        default="data/sample_small.json",
        help="Path to the problem JSON file (default: data/sample_small.json)",
    )
    parser.add_argument(
        "--solver",
        choices=list(SOLVERS.keys()) + ["all"],
        default="all",
        help="Solver to use (default: all)",
    )
    parser.add_argument(
        "--export",
        default=None,
        help="Export solution to CSV file (only for single solver mode)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    print(f"Loading problem from: {args.data}")
    problem = load_problem(args.data)
    n_courses = len(problem["courses"])
    n_rooms   = len(problem["rooms"])
    n_slots   = len(problem["slots"])
    print(f"Problem: {n_courses} courses, {n_rooms} rooms, {n_slots} slots\n")

    if args.solver == "all":
        results = {}
        for name, solver_fn in SOLVERS.items():
            csp, meta = build_csp(problem)
            solution, elapsed, nassigns = run_solver(
                name, solver_fn, csp, meta, verbose=True
            )
            results[name] = (solution, elapsed, nassigns)
        print_comparison(results)
    else:
        csp, meta = build_csp(problem)
        solver_fn = SOLVERS[args.solver]
        solution, elapsed, nassigns = run_solver(
            args.solver, solver_fn, csp, meta, verbose=True
        )
        if solution and args.export:
            from src.utils import export_csv
            export_csv(solution, meta, args.export)


if __name__ == "__main__":
    main()
