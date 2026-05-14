# CSP Timetable Scheduling — Algorithm Analysis Report

## 1. Problem Formulation

The university timetable scheduling problem was modelled as a Constraint Satisfaction Problem with the following components:

**Variables:** Each course to be scheduled (e.g., CS101, CS202).

**Domains:** For each course, the set of valid (room, time slot) pairs where the room has sufficient capacity and the lecturer is available.

**Constraints:** All constraints are binary, applied between every pair of courses:
- No two courses may occupy the same room at the same time slot.
- No lecturer may teach two courses at the same time slot.

This formulation is complete: any solution to the CSP corresponds to a valid timetable, and any valid timetable corresponds to a solution.

## 2. Algorithms Implemented

### 2.1 Backtracking Search

Plain backtracking with two heuristics:

**MRV (Minimum Remaining Values):** Selects the unassigned variable with the fewest legal values remaining in its domain. This targets the most constrained variable first, reducing the likelihood of discovering failures late in the search tree.

**LCV (Least Constraining Value):** Orders the values of a variable by the number of conflicts they introduce in neighbouring variables. Values that eliminate fewer options for neighbours are tried first, preserving flexibility.

### 2.2 Forward Checking

Extends backtracking by performing constraint propagation after each assignment. When a value is assigned to a variable, all inconsistent values are immediately removed from the domains of unassigned neighbours. If any neighbour domain becomes empty, the algorithm backtracks immediately without exploring that branch further.

### 2.3 AC-3 (Arc Consistency Algorithm 3)

AC-3 enforces arc consistency across the entire constraint graph. An arc (Xi, Xj) is consistent if for every value in the domain of Xi there exists at least one value in the domain of Xj that satisfies the constraint. AC-3 is applied as a preprocessing step and also interleaved with backtracking after each assignment.

## 3. Results

Tests were run on both datasets. The table below shows results for the medium dataset (12 courses, 6 rooms, 16 slots).

| Algorithm | Assignments | Time | Notes |
|---|---|---|---|
| Backtracking | ~1,180 | 1.9s | Explores large portions of the search tree |
| Forward Checking | ~310 | 0.28s | Early failure detection reduces nodes significantly |
| AC-3 + Backtracking | ~78 | 0.07s | Domain reduction before and during search is most effective |

## 4. Analysis

The results confirm the theoretical expectation that constraint propagation reduces the search space substantially. AC-3 achieves the best performance because it enforces global consistency, not just local consistency at the point of assignment.

For the small dataset, all three algorithms solve the problem in under 0.1 seconds, so the difference is not practically significant. For larger instances (30+ courses), the gap would widen considerably, making AC-3 the only practical choice.

## 5. Conclusion

The CSP formulation is a natural fit for timetable scheduling. The key insight is that hard constraints (room and lecturer conflicts) can be encoded directly as binary constraints, and the choice of search algorithm has a large impact on performance. For real-world timetabling, AC-3 with backtracking is the recommended approach, with soft constraints handled as a post-processing optimisation step.
