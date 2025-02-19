from typing import Dict, Optional
from agents import Agent
from environment import Environment
from mdp import MarkovDecisionProcess, S, A
import json
from helpers.utils import NotImplemented

# This is a class for a generic Value Iteration agent
class ValueIterationAgent(Agent[S, A]):
    mdp: MarkovDecisionProcess[S, A] # The MDP used by this agent for training 
    utilities: Dict[S, float] # The computed utilities
                                # The key is the string representation of the state and the value is the utility
    discount_factor: float # The discount factor (gamma)

    def __init__(self, mdp: MarkovDecisionProcess[S, A], discount_factor: float = 0.99) -> None:
        super().__init__()
        self.mdp = mdp
        self.utilities = {state:0 for state in self.mdp.get_states()} # We initialize all the utilities to be 0
        self.discount_factor = discount_factor
    
    # Given a state, compute its utility using the bellman equation
    # if the state is terminal, return 0
    def compute_bellman(self, state: S) -> float:
        #TODO: Complete this function
        if self.mdp.is_terminal(state):
            return 0
        max_utility= float('-inf')
        for action in self.mdp.get_actions(state):
            sum=0
            # Sum over the next state
            for next_S,probability in self.mdp.get_successor(state,action).items():
                # print("p=",probability)
                sum+=probability*(self.mdp.get_reward(state,action,next_S)+(self.discount_factor*self.utilities.get(next_S, 0)))
            if (sum>max_utility):
                max_utility=sum

        return max_utility        
    
    # Applies a single utility update
    # then returns True if the utilities has converged (the maximum utility change is less or equal the tolerance)
    # and False otherwise
    def update(self, tolerance: float = 0) -> bool:
        #TODO: Complete this function
        new_utilities = {}
        max_change = 0  # To track the maximum change in utility

        # Iterate over all states in the MDP
        for s in self.mdp.get_states():
            # Compute the new utility for the state using Bellman update
            new_utility = self.compute_bellman(s)
            new_utilities[s] = new_utility

            # Calculate the change in utility
            change = abs(new_utility - self.utilities[s])
            if change>max_change:
                max_change=change
        
        # Update the utilities with the newly computed values
        self.utilities=new_utilities

        # Check for convergence
        return max_change <= tolerance

    # This function applies value iteration starting from the current utilities stored in the agent and stores the new utilities in the agent
    # NOTE: this function does incremental update and does not clear the utilities to 0 before running
    # In other words, calling train(M) followed by train(N) is equivalent to just calling train(N+M)
    def train(self, iterations: Optional[int] = None, tolerance: float = 0) -> int:
        #TODO: Complete this function to apply value iteration for the given number of iterations
        iteration_count = 0
        # If iterations is None or a number, the loop runs until convergence.
        while iterations is None or iteration_count < iterations:
            # Perform a single update and check for convergence
            converged = self.update(tolerance)
            iteration_count += 1

            # Stop if converged with no fixed number of iterations required
            if converged:
                break

        # to know how many iterations were needed to converge.
        return iteration_count
            
    # Given an environment and a state, return the best action as guided by the learned utilities and the MDP
    # If the state is terminal, return None
    def act(self, env: Environment[S, A], state: S) -> A:
        #TODO: Complete this function
        if (self.mdp.is_terminal(state)):
            return None

        max_utility= float('-inf')
        best_action = None
        for action in self.mdp.get_actions(state):
            sum=0
            for next_S,probability in self.mdp.get_successor(state,action).items():
                sum+=probability*(self.mdp.get_reward(state,action,next_S)+self.discount_factor*self.utilities.get(next_S, 0))
            if (sum>max_utility):
                max_utility=sum
                best_action = action
        return best_action
    # Save the utilities to a json file
    def save(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'w') as f:
            utilities = {self.mdp.format_state(state): value for state, value in self.utilities.items()}
            json.dump(utilities, f, indent=2, sort_keys=True)
    
    # loads the utilities from a json file
    def load(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'r') as f:
            utilities = json.load(f)
            self.utilities = {self.mdp.parse_state(state): value for state, value in utilities.items()}
