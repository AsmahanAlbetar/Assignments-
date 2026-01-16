from sokoban import SokobanProblem, SokobanState
from mathutils import Direction, Point, manhattan_distance
from helpers.utils import NotImplemented
from functools import lru_cache


# This heuristic returns the distance between the player and the nearest crate as an estimate for the path cost
# While it is consistent, it does a bad job at estimating the actual cost thus the search will explore a lot of nodes before finding a goal
def weak_heuristic(problem: SokobanProblem, state: SokobanState):
    return min(manhattan_distance(state.player, crate) for crate in state.crates) - 1

#TODO: Import any modules and write any functions you want to use


def strong_heuristic(problem: SokobanProblem, state: SokobanState) -> float:
    """
    Strong admissible and consistent heuristic for Sokoban.
    
    Heuristic Design:
    This heuristic is based on the sum of minimum Manhattan distances from each
    misplaced crate to its nearest goal, with corner deadlock detection.
    
    Key insight for consistency:
    - When we push a crate, exactly one crate moves by exactly 1 cell
    - The minimum distance to nearest goal for that crate changes by at most 1
    - All other crates' distances remain the same
    - Therefore, the sum decreases by at most 1 per action
    - This guarantees consistency: h(n) - h(n') ≤ cost(action) = 1
    
    Admissibility:
    - Manhattan distance is a lower bound on actual path length
    - We ignore conflicts between crates (which only increases actual cost)
    - Therefore, the heuristic never overestimates
    
    Corner deadlock detection:
    - Returns infinity for unsolvable states
    - Consistent because deadlocks are permanent (inf → inf)
    """
    crates = state.crates
    goals = problem.layout.goals
    walkable = problem.layout.walkable

    # Goal test
    if crates == goals:
        return 0

    # Identify misplaced crates (not on goals)
    misplaced_crates = crates - goals
    if not misplaced_crates:
        return 0

    # Corner Deadlock Detection 
    for crate in misplaced_crates:
        wall_up = crate + Direction.UP.to_vector() not in walkable
        wall_down = crate + Direction.DOWN.to_vector() not in walkable
        wall_left = crate + Direction.LEFT.to_vector() not in walkable
        wall_right = crate + Direction.RIGHT.to_vector() not in walkable

        # Crate is stuck between two perpendicular walls (no way out)
        if (wall_up and wall_left) or (wall_up and wall_right) or \
           (wall_down and wall_left) or (wall_down and wall_right):
            return float('inf')

    #Sum of minimum distances from crates to nearest goals 
    total_distance = 0
    for crate in crates:
        min_dist = min(manhattan_distance(crate, goal) for goal in goals)
        total_distance += min_dist

    return total_distance