from problem import HeuristicFunction, Problem, S, A, Solution
from collections import deque
from helpers import utils
from queue import PriorityQueue
#TODO: Import any modules you want to use

# All search functions take a problem and a state
# If it is an informed search function, it will also receive a heuristic function
# S and A are used for generic typing where S represents the state type and A represents the action type

# All the search functions should return one of two possible type:
# 1. A list of actions which represent the path from the initial state to the final state
# 2. None if there is no solution

def BreadthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    #TODO: ADD YOUR CODE HERE
    frontier= deque([(initial_state, [])]) # Initial path is empty
    explored=[]
    while(True):
        # frontier is empty then we can't find a path to the goal
        if len(frontier)==0:
            return None
        # Dequeue the leftmost (first) node in queue and the path leading to it
        node, path = frontier.popleft()
        # If the goal is reached, return the path
        if problem.is_goal(node):
            return path
        # Add the node to the explored list
        explored.append(node)
        # Expand the node by getting possible actions
        actions=problem.get_actions(node)
        for action in actions:
            # Given the state and the action, return the next state 
            child=problem.get_successor(node,action)
            # Add child node to the frontier end if not explored and not already in frontier
            if child not in explored and all(c[0] != child for c in frontier):
                frontier.append((child, path + [action])) 


def DepthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    #TODO: ADD YOUR CODE HERE
    frontier= deque([(initial_state, [])]) # Initial path is empty
    explored=[]
    while(True):
        # frontier is empty then we can't find a path to the goal
        if len(frontier)==0:
            return None
        # Pop the rightmost (last) node inserted and the path leading to it
        node, path = frontier.pop()
        # If the goal is reached, return the path
        if problem.is_goal(node):
            return path
        # Add the node to the explored list
        explored.append(node)
        # Expand the node by getting possible actions
        actions=problem.get_actions(node)
        for action in actions:
            # Given the state and the action, return the next state 
            child=problem.get_successor(node,action)
            # Add child node to the frontier end if not explored and not already in frontier
            if child not in explored and all(c[0] != child for c in frontier):
                frontier.append((child, path + [action])) 
    
def UniformCostSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    #TODO: ADD YOUR CODE HERE
    #frontier: S, path, g(S)
    frontier= [(initial_state, [],0)] # Initial path is empty and g(source)=0
    explored=set()
    while(True):
        # frontier is empty then we can't find a path to the goal
        if len(frontier)==0:
            return None
        # Pop the first node and the path leading to it
        node, path,cost = frontier.pop(0)
        # If the goal is reached, return the path
        if problem.is_goal(node):
            return path
        # Add the node to the explored list
        explored.add(node)
        # Expand the node by getting possible actions
        actions=problem.get_actions(node)
        for action in actions:
            # Get the successor state and its cost
            child = problem.get_successor(node, action)
            child_g_value = cost + problem.get_cost(node, action)
            # Check if child is not in explored and not in frontier -> add it
            if child not in explored and all(c[0] != child for c in frontier):
                frontier.append((child, path + [action],child_g_value))
            else:   
                # Check if child is in frontier
                for i, (frontier_child, frontier_path, frontier_cost) in enumerate(frontier):
                    if frontier_child == child:
                        # If the cost is lower, replace it
                        if child_g_value < frontier_cost:
                            frontier[i] = (child, path + [action], child_g_value) 
                        break
            
        # Sort by the cost: g
        # if two elements have the same priority, the sort will automatically maintain 
        # their relative order based on their original order of insertion in the list
        frontier = sorted(frontier, key=lambda x: (x[2]))

def AStarSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    #TODO: ADD YOUR CODE HERE
    #frontier: S, path, g(S), f(S)
    frontier= [(initial_state, [],0,heuristic(problem, initial_state))] # Initial path is empty and g(source)=0, f(source)=g(source)+h(source)
    explored=set()
    while(True):
        # frontier is empty then we can't find a path to the goal
        if len(frontier)==0:
            return None
        # Pop the first node and the path leading to it
        node, path,cost_g,cost_f = frontier.pop(0)
        # If the goal is reached, return the path
        if problem.is_goal(node):
            return path
        # Add the node to the explored list
        explored.add(node)
        # Expand the node by getting possible actions
        actions=problem.get_actions(node)
        for action in actions:
            # Get the successor state and its cost
            child = problem.get_successor(node, action)
            child_g_value = cost_g+problem.get_cost(node,action)
            child_f_value=child_g_value+heuristic(problem,child)
            # Check if child is not in explored and not in frontier -> add it
            if child not in explored and all(c[0] != child for c in frontier):
                frontier.append((child, path + [action],child_g_value,child_f_value))
            else:   
                # Check if child is in frontier
                for i, (frontier_child, frontier_path, frontier_g,frontier_f) in enumerate(frontier):
                    if frontier_child == child:
                        # If the cost is lower, replace it
                        if child_f_value < frontier_f:
                            frontier[i] = (child, path + [action], child_g_value,child_f_value)  
                        break
            
        # Sort by the cost+heuristic: f
        # if two elements have the same priority, the sort will automatically maintain 
        # their relative order based on their original order of insertion in the list
        frontier = sorted(frontier, key=lambda x: (x[3]))

def BestFirstSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    #TODO: ADD YOUR CODE HERE
    #frontier: S, path, h(S)
    frontier= [(initial_state, [],heuristic(problem, initial_state))] # Initial path is empty and h(source)
    explored=set()
    while(True):
        # frontier is empty then we can't find a path to the goal
        if len(frontier)==0:
            return None
        # Pop the first node and the path leading to it
        node, path,cost_h = frontier.pop(0)
        # If the goal is reached, return the path
        if problem.is_goal(node):
            return path
        # Add the node to the explored list
        explored.add(node)
        # Expand the node by getting possible actions
        actions=problem.get_actions(node)
        for action in actions:
            # Get the successor state and its cost
            child = problem.get_successor(node, action)
            child_h_value=heuristic(problem,child)
            # Check if child is not in explored and not in frontier -> add it
            if child not in explored and all(c[0] != child for c in frontier):
                frontier.append((child, path + [action],child_h_value))
            else:   
                # Check if child is in frontier
                for i, (frontier_child, frontier_path, frontier_h) in enumerate(frontier):
                    if frontier_child == child:
                        # If the cost is lower, replace it
                        if child_h_value < frontier_h:
                            frontier[i] = (child, path + [action], child_h_value)  
                        break
            
        # Sort by the heuristic: h
        # if two elements have the same priority, the sort will automatically maintain 
        # their relative order based on their original order of insertion in the list
        frontier = sorted(frontier, key=lambda x: (x[2]))