from dungeon import DungeonProblem, DungeonState
from mathutils import Direction, Point, euclidean_distance, manhattan_distance
from helpers import utils

# This heuristic returns the distance between the player and the exit as an estimate for the path cost
# While it is consistent, it does a bad job at estimating the actual cost thus the search will explore a lot of nodes before finding a goal
def weak_heuristic(problem: DungeonProblem, state: DungeonState):
    return euclidean_distance(state.player, problem.layout.exit)

#TODO: Import any modules and write any functions you want to use
def calculate_mst_cost(points: set[Point]) -> float:
    # If there are no points or only one point in remaining_coins, 
    # there is no need for an MST, so the cost is 0.0.
    if len(points) <= 1:
        return 0.0
    
    cost = 0.0
    connected_points = {next(iter(points))}  # Start with an arbitrary point from the set
    remaining_points = set(points - connected_points)  # The rest of the points

    while len(remaining_points)>0:
        min_edge_cost = float('inf')
        nearest_point = None

        # For each point in connected_points, 
        # find the nearest point in remaining_points by calculating the Manhattan distance.
        for connected_point in connected_points:
            for point in remaining_points:
                distance = manhattan_distance(connected_point, point)
                if distance < min_edge_cost:
                    min_edge_cost = distance
                    nearest_point = point

        # Update MST cost and add the nearest point to the connected set
        cost += min_edge_cost
        connected_points.add(nearest_point)
        remaining_points.remove(nearest_point)

    return cost

def strong_heuristic(problem: DungeonProblem, state: DungeonState) -> float:
    #TODO: ADD YOUR CODE HERE
#     #IMPORTANT: DO NOT USE "problem.is_goal" HERE.
#     # Calling it here will mess up the tracking of the explored nodes count
#     # which is considered the number of is_goal calls during the search
#     #NOTE: you can use problem.cache() to get a dictionary in which you can store information that will persist between calls of this function
#     # This could be useful if you want to store the results heavy computations that can be cached and used across multiple calls of this function
#     # Check if we have already computed the distances (using the cache)
    remaining_coins = state.remaining_coins
    player = state.player
    exit_point = problem.layout.exit
    cache = problem.cache()

    # If no coins remaining, return the distance from player to the exit
    if len(remaining_coins)==0:
        return manhattan_distance(player, exit_point)

    # Total heuristic = distance from the player to the nearest coin + MST of the remaining coins + distance from the closest coin to the exit
    # Find the distance from the player to the nearest coin
    nearest_coin_distance = min(manhattan_distance(player, coin) for coin in remaining_coins)
    # Calculate an MST of the remaining coins to estimate the minimum path to collect all coins
    if remaining_coins not in cache:
        # If not in cache, calculate it 
        cache[remaining_coins] = calculate_mst_cost(remaining_coins)
    mst_cost = cache[remaining_coins]
    # Find the distance from the closest coin to the exit
    nearest_exit_distance = min(manhattan_distance(coin, exit_point) for coin in remaining_coins)

    # Total heuristic value
    return nearest_coin_distance + mst_cost + nearest_exit_distance

