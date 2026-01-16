from typing import Tuple
from game import HeuristicFunction, Game, S, A
from helpers.utils import NotImplemented

#TODO: Import any modules you want to use

# All search functions take a problem, a state, a heuristic function and the maximum search depth.
# If the maximum search depth is -1, then there should be no depth cutoff (The expansion should not stop before reaching a terminal state) 

# All the search functions should return the expected tree value and the best action to take based on the search results

# This is a simple search function that looks 1-step ahead and returns the action that lead to highest heuristic value.
# This algorithm is bad if the heuristic function is weak. That is why we use minimax search to look ahead for many steps.
def greedy(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    agent = game.get_turn(state)
    
    terminal, values = game.is_terminal(state)
    if terminal: return values[agent], None

    actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]
    value, _, action = max((heuristic(game, state, agent), -index, action) for index, (action , state) in enumerate(actions_states))
    return value, action

# Apply Minimax search and return the game tree value and the best action
# Hint: There may be more than one player, and in all the testcases, it is guaranteed that 
# game.get_turn(state) will return 0 (which means it is the turn of the player). All the other players
# (turn > 0) will be enemies. So for any state "s", if the game.get_turn(s) == 0, it should a max node,
# and if it is > 0, it should be a min node. Also remember that game.is_terminal(s), returns the values
# for all the agents. So to get the value for the player (which acts at the max nodes), you need to
# get values[0].

#S: the type of a state
#A: the type of an action
def minimax(game: Game[S, A], state: S, heuristic: HeuristicFunction,
            max_depth: int = -1) -> Tuple[float, A]:
    # Convert -1 to a very large number for uniform recursion
    depth_limit = max_depth if max_depth != -1 else 10**9

    # a recursive function that performs a DF minimax from node s.depth
    def dfs(s: S, depth: int) -> Tuple[float, A]:
        terminal, values = game.is_terminal(s)
        # values is a list of terminal values (one per agent) when terminal.
        # Return the terminal value for player (the main one) and None as action (there is no action at terminal).
        if terminal:
            return values[0], None

        # If no more expansion possible
        if depth == 0:
            return heuristic(game, s, 0), None

        actions = game.get_actions(s)
        if not actions:
            # No moves available → evaluate as a terminal-like node
            return heuristic(game, s, 0), None

        # get which agent's turn it is, 0 is the maximizing player
        turn = game.get_turn(s)
        if turn == 0:  # MAX NODE
            best_val = float('-inf')
            best_act = None
            for action in actions:
                val, _ = dfs(game.get_successor(s, action), depth - 1)
                if val > best_val:
                    best_val = val
                    best_act = action
            return best_val, best_act
        else:  # MIN NODE
            best_val = float('inf')
            best_act = None
            for action in actions:
                val, _ = dfs(game.get_successor(s, action), depth - 1)
                if val < best_val:
                    best_val = val
                    best_act = action
            return best_val, best_act

    return dfs(state, depth_limit)

def alphabeta(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    """
    Alpha-beta search wrapper. max_depth == -1 means no cutoff (search until terminals).
    The cutoff evaluation uses heuristic(game, node, 0) (player 0's perspective), and
    terminal states return values[0] (value for player 0).
    """

    neg_infinty = float("-inf")
    post_infinty = float("inf")

    def ab(node: S, depth: int, alpha: float, beta: float) -> Tuple[float, A]:
        # Call is_terminal exactly once per node (returns (bool, Optional[List[float]]))
        terminal, values = game.is_terminal(node)
        if terminal:
            # return the value for player 0 and no action
            return values[0], None

        # If max_depth is set, treat depth as the current depth from root (0-based),
        # and cutoff when depth >= max_depth.
        if max_depth != -1 and depth >= max_depth:
            return heuristic(game, node, 0), None

        turn = game.get_turn(node)
        actions = list(game.get_actions(node))
        # If there are no actions, treat as terminal-like and evaluate with heuristic
        if not actions:
            return heuristic(game, node, 0), None

        if turn == 0:
            # maximizing player 0
            best_value = neg_infinty
            best_action = None
            for action in actions:
                succ = game.get_successor(node, action)
                val, _ = ab(succ, depth + 1, alpha, beta)
                if val > best_value:
                    best_value = val
                    best_action = action
                # update alpha and prune if possible
                alpha = max(alpha, best_value)
                if alpha >= beta:
                    break
            return best_value, best_action
        else:
            # MIN node minimizing players
            best_value = post_infinty
            best_action = None
            for action in actions:
                succ = game.get_successor(node, action)
                val, _ = ab(succ, depth + 1, alpha, beta)
                if val < best_value:
                    best_value = val
                    best_action = action
                # update beta and prune if possible
                beta = min(beta, best_value)
                if alpha >= beta:
                    break
            return best_value, best_action

    return ab(state, 0, neg_infinty, post_infinty)



# Apply Alpha Beta pruning with move ordering and return the tree value and the best action
def alphabeta_with_move_ordering(game: Game[S, A], state: S,
                                 heuristic: HeuristicFunction,
                                 max_depth: int = -1) -> Tuple[float, A]:

    NEG_INF = float("-inf")
    POS_INF = float("inf")

    def ab(node: S, depth: int, alpha: float, beta: float):

        terminal, values = game.is_terminal(node)
        if terminal:
            return values[0], None

        if max_depth != -1 and depth >= max_depth:
            return heuristic(game, node, 0), None

        turn = game.get_turn(node)
        actions = list(game.get_actions(node))

        # Ordering: evaluate each successor heuristic before recursion
        scored_actions = []
        for action in actions:
            succ = game.get_successor(node, action)
            h = heuristic(game, succ, 0)
            scored_actions.append((h, action, succ))

        # MAX sort descending
        if turn == 0:
            scored_actions.sort(key=lambda x: x[0], reverse=True)
            best_value = NEG_INF
            best_action = None

            for h, action, succ in scored_actions:
                val, _ = ab(succ, depth + 1, alpha, beta)
                if val > best_value:
                    best_value = val
                    best_action = action

                alpha = max(alpha, best_value)
                if alpha >= beta:
                    break  # prune

            return best_value, best_action

        # MIN sort ascending 
        else:
            scored_actions.sort(key=lambda x: x[0])
            best_value = POS_INF
            best_action = None

            for h, action, succ in scored_actions:
                val, _ = ab(succ, depth + 1, alpha, beta)
                if val < best_value:
                    best_value = val
                    best_action = action

                beta = min(beta, best_value)
                if alpha >= beta:
                    break  # prune

            return best_value, best_action

    return ab(state, 0, NEG_INF, POS_INF)



# Apply Expectimax search and return the tree value and the best action
# Hint: Read the hint for minimax, but note that the monsters (turn > 0) do not act as min nodes anymore,
# they now act as chance nodes (they act randomly).
def expectimax(game: Game[S, A], state: S, heuristic: HeuristicFunction,
               max_depth: int = -1) -> Tuple[float, A]:

    # Convert -1 to a very large number for uniform recursion
    depth_limit = max_depth if max_depth != -1 else 10**9

    # a recursive function that performs a DF expectimax from node s.depth
    def dfs(s: S, depth: int) -> Tuple[float, A]:
        terminal, values = game.is_terminal(s)
        # Return terminal value for player 0 and None as action
        if terminal:
            return values[0], None

        # If no more expansion possible
        if depth == 0:
            return heuristic(game, s, 0), None

        actions = game.get_actions(s)
        if not actions:
            # No moves available → evaluate as a terminal-like node
            return heuristic(game, s, 0), None

        # get which agent's turn it is
        turn = game.get_turn(s)
        if turn == 0:  # MAX NODE (maximizing player)
            best_val = float('-inf')
            best_act = None
            for action in actions:
                val, _ = dfs(game.get_successor(s, action), depth - 1)
                if val > best_val:
                    best_val = val
                    best_act = action
            return best_val, best_act
        else:  # CHANCE NODE (monsters act randomly)
            total = 0
            for action in actions:
                val, _ = dfs(game.get_successor(s, action), depth - 1)
                total += val
            # equal probability for all children
            return total / len(actions), None

    return dfs(state, depth_limit)