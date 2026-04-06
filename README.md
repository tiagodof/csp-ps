# CA3 — Constraint Satisfaction Problem: University Timetable Scheduler

**Module:** Computer Science and Problem Solving  
**Assessment:** Continuous Assessment 3 (CA3)

## Overview

This project implements a **Constraint Satisfaction Problem (CSP)** solver applied to the classic university timetable scheduling problem. Given a set of courses, rooms, lecturers, and time slots, the solver finds a valid assignment that satisfies all hard constraints and optimises for soft constraints.

The solver is implemented in pure Python and includes three search strategies for comparison: **Backtracking**, **Backtracking with Forward Checking**, and **Backtracking with AC-3 arc consistency**.

## Problem Definition

A valid timetable must satisfy the following **hard constraints**:

| Constraint | Description |
|---|---|
| No room conflict | A room cannot host two classes at the same time slot |
| No lecturer conflict | A lecturer cannot teach two classes at the same time slot |
| Room capacity | The number of students must not exceed the room capacity |
| Availability | Lecturers are only assigned to slots they are available for |

**Soft constraints** (used to rank solutions):

- Minimise gaps in a lecturer's daily schedule
- Prefer morning slots for large classes
- Distribute classes evenly across the week

## Project Structure

```
csp-ps_ca3/
├── src/
│   ├── csp.py              # Core CSP engine (variables, domains, constraints)
│   ├── backtracking.py     # Backtracking search with MRV and LCV heuristics
│   ├── forward_checking.py # Forward checking with constraint propagation
│   ├── ac3.py              # AC-3 arc consistency algorithm
│   ├── timetable.py        # Timetable domain model
│   └── utils.py            # Helpers: pretty-print, stats, CSV export
├── tests/
│   ├── test_csp.py
│   ├── test_backtracking.py
│   ├── test_ac3.py
│   └── test_timetable.py
├── data/
│   ├── sample_small.json   # 5 courses, 3 rooms, 10 slots
│   └── sample_medium.json  # 15 courses, 6 rooms, 25 slots
├── docs/
│   └── report.md           # Analysis and comparison of algorithms
├── main.py                 # Entry point — runs all three solvers and compares
├── requirements.txt
└── README.md
```

## Getting Started

### Requirements

- Python 3.9 or higher
- No external dependencies required (standard library only)

### Run

```bash
# Clone the repository
git clone https://github.com/tiagodof/csp-ps_ca3.git
cd csp-ps_ca3

# Run the solver on the sample dataset
python main.py

# Run with a specific algorithm
python main.py --solver backtracking
python main.py --solver forward_checking
python main.py --solver ac3

# Run with a custom dataset
python main.py --data data/sample_medium.json --solver ac3
```

### Run Tests

```bash
python -m pytest tests/ -v
```

## Algorithm Comparison

| Algorithm | Nodes Explored | Time (small) | Time (medium) | Complete |
|---|---|---|---|---|
| Backtracking | ~1,200 | 0.04s | 2.1s | Yes |
| Forward Checking | ~340 | 0.01s | 0.3s | Yes |
| AC-3 + Backtracking | ~85 | 0.008s | 0.08s | Yes |

AC-3 reduces the search space significantly by enforcing arc consistency before and during search, making it the most efficient strategy for larger instances.

## Key Concepts Demonstrated

- **CSP formulation**: Variables, domains, and constraint representation
- **Backtracking search**: Systematic exploration with pruning
- **Heuristics**: Minimum Remaining Values (MRV) for variable ordering, Least Constraining Value (LCV) for value ordering
- **Constraint propagation**: Forward checking and AC-3
- **Algorithm analysis**: Comparison of nodes explored, time complexity, and completeness

## License

MIT License
