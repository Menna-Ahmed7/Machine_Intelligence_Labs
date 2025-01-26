from typing import Tuple
from game import HeuristicFunction, Game, S, A
from helpers.utils import NotImplemented

#TODO: Import any built in modules you want to use
from typing import Optional
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
def minimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: Complete this function
    def recursive_minimax(state: S, depth: int) -> Tuple[float, Optional[A]]:
        # Check for terminal state
        terminal, values = game.is_terminal(state)
        if terminal:
            # Return the player's value (index 0)   
            return values[0], None  

        # if depth cutoff -> use heuristic at depth limit
        if max_depth != -1 and depth == max_depth:
            return heuristic(game, state, 0), None  

        turn = game.get_turn(state)
        actions = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]
        # if player 0 -> max node
        if turn==0:
            best_value=float("-inf")
            best_action=None
            for action,successor in actions:
                value, _=recursive_minimax(successor,depth+1)
                if value>best_value:
                    best_value=value
                    best_action=action
            return best_value,best_action
        else:
        # Otherwise -> min node
            best_value=float("inf")
            best_action=None
            for action,successor in actions:
                value, _=recursive_minimax(successor,depth+1)
                if value<best_value:
                    best_value=value
                    best_action=action
            return best_value,best_action
    return recursive_minimax(state,0)

        

# Apply Alpha Beta pruning and return the tree value and the best action
# Hint: Read the hint for minimax.
def alphabeta(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: Complete this function
    def recursive_alphabeta(state: S, depth: int,alpha,beta) -> Tuple[float, Optional[A]]:
        # Check for terminal state
        terminal, values = game.is_terminal(state)
        if terminal:
            # Return the player's value (index 0)   
            return values[0], None  

        # if depth cutoff -> use heuristic at depth limit
        if max_depth != -1 and depth == max_depth:
            return heuristic(game, state, 0), None  

        turn = game.get_turn(state)
        actions = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]
        # if player 0 -> max node
        if turn==0:
            best_value=float("-inf")
            best_action=None
            for action,successor in actions:
                value, _=recursive_alphabeta(successor,depth+1,alpha,beta)
                if value>best_value:
                    best_value=value
                    best_action=action
                # once you find value >= beta prune the rest of children
                if best_value>=beta:
                    return best_value,best_action
                alpha=max(alpha,best_value)
            return best_value,best_action
        else:
            best_value=float("inf")
            best_action=None
            for action,successor in actions:
                value, _=recursive_alphabeta(successor,depth+1,alpha,beta)
                if value<best_value:
                    best_value=value
                    best_action=action
                # once you find value <= alpha prune the rest of children
                if best_value<=alpha:
                    return best_value,best_action
                beta=min(best_value,beta)
            return best_value,best_action

    return recursive_alphabeta(state,0,float("-inf"),float("inf"))

# Apply Alpha Beta pruning with move ordering and return the tree value and the best action
# Hint: Read the hint for minimax.
def alphabeta_with_move_ordering(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: Complete this function
    def recursive_alphabeta(state: S, depth: int,alpha,beta) -> Tuple[float, Optional[A]]:
        # Check for terminal state
        terminal, values = game.is_terminal(state)
        if terminal:
            # Return the player's value (index 0)   
            return values[0], None  

        # if depth cutoff -> use heuristic at depth limit
        if max_depth != -1 and depth == max_depth:
            return heuristic(game, state, 0), None  

        turn = game.get_turn(state)
        actions = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]

        #** Order actions **
        # For each action, calculates the heuristic value for the successor state.
        # And Order descending for maximizer, ascending for minimizer
        actions = sorted(
            actions,
            key=lambda action: heuristic(game, action[1], 0),
            reverse=(turn == 0),  
        )
        if turn==0:
            best_value=float("-inf")
            best_action=None
            for action,successor in actions:
                value, _=recursive_alphabeta(successor,depth+1,alpha,beta)
                if value>best_value:
                    best_value=value
                    best_action=action
                # once you find value >= beta prune the rest of children
                if best_value>=beta:
                    return best_value,best_action
                alpha=max(alpha,best_value)
            return best_value,best_action
        else:
            best_value=float("inf")
            best_action=None
            for action,successor in actions:
                value, _=recursive_alphabeta(successor,depth+1,alpha,beta)
                if value<best_value:
                    best_value=value
                    best_action=action
                # once you find value <= alpha prune the rest of children
                if best_value<=alpha:
                    return best_value,best_action
                beta=min(best_value,beta)
            return best_value,best_action
    return recursive_alphabeta(state,0,float("-inf"),float("inf"))

# Apply Expectimax search and return the tree value and the best action
# Hint: Read the hint for minimax, but note that the monsters (turn > 0) do not act as min nodes anymore,
# they now act as chance nodes (they act randomly).
def expectimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: Complete this function
    def recursive_minimax(state: S, depth: int) -> Tuple[float, Optional[A]]:
        # Check for terminal state
        terminal, values = game.is_terminal(state)
        if terminal:
            # Return the player's value (index 0)
            return values[0], None  

        # if depth cutoff -> use heuristic at depth limit
        if max_depth != -1 and depth == max_depth:
            return heuristic(game, state, 0), None  

        turn = game.get_turn(state)
        actions = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]
        if turn==0:
            best_value=float("-inf")
            best_action=None
            for action,successor in actions:
                value, _=recursive_minimax(successor,depth+1)
                if value>best_value:
                    best_value=value
                    best_action=action
            return best_value,best_action
        else:
            best_action=None
            accumulative_value=0
            num_actions = len(actions)
            for action,successor in actions:
                value, _=recursive_minimax(successor,depth+1)
                # Average value for chance nodes
                accumulative_value += value / num_actions  
            return accumulative_value,best_action
    return recursive_minimax(state,0)
        