from problem import HeuristicFunction, Problem, S, A, Solution
from collections import deque
from helpers.utils import NotImplemented
import heapq
import itertools
#TODO: Import any modules you want to use
import heapq

# All search functions take a problem and a state
# If it is an informed search function, it will also receive a heuristic function
# S and A are used for generic typing where S represents the state type and A represents the action type

# All the search functions should return one of two possible type:
# 1. A list of actions which represent the path from the initial state to the final state
# 2. None if there is no solution

def BreadthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    #TODO: ADD YOUR CODE HERE
    # The "frontier" is a queue (FIFO) that holds states waiting to be explored.
    # Each element is a tuple (state, path), where 'path' is the list of actions leading to this state.
    frontier = deque()
    frontier.append((initial_state,[]))
    # visited keeps track of all states that have already been explored
    # to avoid revisiting them and entering infinite loops.
    visited = set()
    visited.add(initial_state)
    
    # If the starting state is already a goal, return an empty path.
    if problem.is_goal(initial_state):
        return []
    
    # Continue exploring until there are no more nodes in the frontier.
    while len(frontier) > 0:
        currentNode = frontier.popleft() #the node is (state, path)
        currentState = currentNode[0]
        currentPath = currentNode[1]
        
         # Get all possible actions from the current state.
        availableActions = problem.get_actions(currentState)
        
        for action in availableActions:
            nextState = problem.get_successor(currentState,action)
            # Only process unvisited states
            if nextState not in visited:
                newPath = currentPath + [action]
                if problem.is_goal(nextState):
                    return newPath
                # Mark this state as visited and add to the frontier to explore later.
                visited.add(nextState)
                frontier.append((nextState, newPath))
    # If no path is found, return None.
    return None
        

def DepthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    #TODO: ADD YOUR CODE HERE
    
    # The "frontier" is a stack that stores unexplored states.
    frontier = [(initial_state,[])] 
    visited = {initial_state}
    
    # If the initial state is already the goal, return immediately.
    if problem.is_goal(initial_state):
        return []
    # Loop while there are still nodes to explore.
    while frontier:
        # Pop the most recent (deepest) node.
        currentNode = frontier.pop()
        currentState = currentNode[0]
        currentPath = currentNode[1]
        # Pop the most recent (deepest) node.
        if problem.is_goal(currentState):
            return currentPath
    
        availabeActions = problem.get_actions(currentState)
        # We reverse the actions to maintain consistent order with the expected output.
        for actions in reversed(availabeActions):
            nextState = problem.get_successor(currentState, actions)
            if nextState not in visited:
                visited.add(nextState)
                newPath = currentPath+[actions]
                # Push the new state onto the stack for deeper exploration.
                frontier.append((nextState,newPath))
    # If no path found, return None.
    return None
    

def UniformCostSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    #TODO: ADD YOUR CODE HERE
    # The "frontier" is a priority queue containing tuples:
    # (path cost so far, unique tie-breaker, state, path)
    frontier = []
    counter = itertools.count()
    heapq.heappush(frontier,(0,next(counter),initial_state,[]))
    
    # The 'visited' dictionary stores the cheapest known cost to reach each state.
    visited = {initial_state:0}
    while frontier:
        currentCost, _,currentState, currentPath = heapq.heappop(frontier)
        
        # Skip if we've already seen a cheaper path to this state
        if currentCost > visited[currentState]:
            continue
        
        # If this is the goal, return the path.
        if problem.is_goal(currentState):
            return currentPath
        
        # Get all possible actions from this state.
        availabeActions = problem.get_actions(currentState)
        for action in availabeActions :
            nextState = problem.get_successor(currentState,action)
            nextCost = currentCost + problem.get_cost(currentState,action)
            
            # If this is the first time we reach 'nextState' OR
            # we found a cheaper path to it, update and push to the frontier.
            if nextState not in visited or nextCost < visited[nextState]:
                visited[nextState] = nextCost
                heapq.heappush(frontier,(nextCost,next(counter),nextState, currentPath+[action]))
    # If the goal is not reachable, return None.
    return None

def AStarSearch(problem, initial_state, heuristic):
    """
    Optimized A* Search with dynamic programming (graph-search version).

    Improvements:
    - Maintains best known g(n) per state (DP memoization)
    - Avoids re-expanding worse paths to same state
    - Uses consistent, admissible heuristic for optimality

    f(n) = g(n) + h(n)
    """

    # Early goal check
    if problem.is_goal(initial_state):
        return []

    frontier = []
    counter = 0

    # Initial costs
    h_initial = heuristic(problem, initial_state)
    f_initial = 0 + h_initial
    heapq.heappush(frontier, (f_initial, counter, 0, initial_state, []))
    counter += 1

    # DP table: best g(n) per visited state
    best_g = {initial_state: 0}

    while frontier:
        f_cost, _, g_cost, current_state, path = heapq.heappop(frontier)

        # DP pruning: skip if we’ve seen a cheaper path
        if g_cost > best_g.get(current_state, float("inf")):
            continue
         # Goal test
        if problem.is_goal(current_state):
            return path

        # Expand successors
        for action in problem.get_actions(current_state):
            successor = problem.get_successor(current_state, action)
            step_cost = problem.get_cost(current_state, action)
            new_g = g_cost + step_cost

            # Only proceed if new_g is better
            if new_g < best_g.get(successor, float("inf")):
                best_g[successor] = new_g
                new_h = heuristic(problem, successor)
                new_f = new_g + new_h
                heapq.heappush(frontier, (new_f, counter, new_g, successor, path + [action]))
                counter += 1

    return None

def BestFirstSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    """
    Implements Greedy Best First Search using h(n) only.
    
    Algorithm explanation:
    - Similar to A* but uses ONLY heuristic h(n) for priority (no g(n))
    - Always expands node that appears closest to goal (greedy)
    - Faster than A* but doesn't guarantee optimal solution
    - For tie-breaking when h(n) equal, uses FIFO (insertion order)
    
    Use case: When speed matters more than optimality
    The greedy approach can be misled by heuristic but explores fewer nodes
    """
    
    # Check if initial state is already the goal
    if problem.is_goal(initial_state):
        return []
    
    # Priority queue: (h_cost, counter, state, path)
    # Only h(n) matters for priority (no g(n) tracking)
    frontier = []
    counter = 0  # Insertion order for FIFO tie-breaking
    
    # Calculate initial heuristic
    h_initial = heuristic(problem, initial_state)
    
    heapq.heappush(frontier, (h_initial, counter, initial_state, []))
    counter += 1
    
    # Explored set tracks visited states
    explored = set()
    # Main Greedy BFS loop
    while frontier:
        # Pop node with minimum h(n) (and earliest insertion if tied)
        h_cost, _, current_state, path = heapq.heappop(frontier)
        
        # Skip if already explored
        if current_state in explored:
            continue
        
        # Mark as explored
        explored.add(current_state)
        
        # Check goal AFTER marking as explored to match expected node count
        if problem.is_goal(current_state):
            return path
        
        # Get available actions - ONLY called when retrieved from frontier
        available_actions = problem.get_actions(current_state)
        
        # Expand current node
        for action in available_actions:
            # Get successor (no cost tracking in Greedy BFS)
            successor_state = problem.get_successor(current_state, action)
            
            # Skip if already explored
            if successor_state in explored:
                continue
            
             # Calculate heuristic for successor
            new_h_cost = heuristic(problem, successor_state)
            new_path = path + [action]
            
            # Add to frontier (priority by h(n) only)
            heapq.heappush(frontier, (new_h_cost, counter, successor_state, new_path))
            counter += 1
    
    # No solution found
    return None
