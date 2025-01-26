from typing import Any, Dict, Set, Tuple, List
from problem import Problem
from mathutils import Direction, Point
from helpers import utils

#TODO: (Optional) Instead of Any, you can define a type for the parking state
ParkingState = Tuple[Point]
# An action of the parking problem is a tuple containing an index 'i' and a direction 'd' where car 'i' should move in the direction 'd'.
ParkingAction = Tuple[int, Direction]

# This is the implementation of the parking problem
class ParkingProblem(Problem[ParkingState, ParkingAction]):
    passages: Set[Point]    # A set of points which indicate where a car can be (in other words, every position except walls).
    cars: Tuple[Point]      # A tuple of points where state[i] is the position of car 'i'. 
    slots: Dict[Point, int] # A dictionary which indicate the index of the parking slot (if it is 'i' then it is the lot of car 'i') for every position.
                            # if a position does not contain a parking slot, it will not be in this dictionary.
    width: int              # The width of the parking lot.
    height: int             # The height of the parking lot.

    # This function should return the initial state
    def get_initial_state(self) -> ParkingState:
        #TODO: ADD YOUR CODE HERE
        return self.cars
    
    # This function should return True if the given state is a goal. Otherwise, it should return False.
    def is_goal(self, state: ParkingState) -> bool:
        #TODO: ADD YOUR CODE HERE
        #looping on all cars if all the cars positions is the same as mentioned in slots 
        # then we reached the goal state
        for i in range(len(state)):
            if i !=self.slots.get(state[i]):
                return False
        return True
    
    # This function returns a list of all the possible actions that can be applied to the given state
    def get_actions(self, state: ParkingState) -> List[ParkingAction]:
        #TODO: ADD YOUR CODE HERE
        actions = []
        directions = [
        (Point(-1, 0), 'L'),  # Left
        (Point(1, 0), 'R'),   # Right
        (Point(0, 1), 'D'),   # Down
        (Point(0, -1), 'U')   # Up
    ]
        # for each car get possible actions
        for i,car in enumerate(state):
            # trying LEFT, RIGHT, UP, DOWN
            for direction_vector, action in directions:
                position = car + direction_vector   
                # If the position contains another car or is a wall then continue
                if position in state or position not in self.passages: continue
                actions.append((i,action))
        return actions
    
    # This function returns a new state which is the result of applying the given action to the given state
    def get_successor(self, state: ParkingState, action: ParkingAction) -> ParkingState:
        #TODO: ADD YOUR CODE HERE
        car_index,direction=action
        # Calculating the new position
        action_result=state[car_index]+ direction.to_vector()
        # not a wall and doesn't contain a car -> take the action
        if action_result in self.passages and action_result not in state:
            # Convert the tuple to a list to allow modification
            new_state = list(state)
            # Update the car's position in the list
            new_state[car_index] = action_result
            # Convert the list back to a tuple 
            return tuple(new_state)    
        return state
    
    # This function returns the cost of applying the given action to the given state
    def get_cost(self, state: ParkingState, action: ParkingAction) -> float:
        #TODO: ADD YOUR CODE HERE
        car_index,direction=action
        # Calculating the new position
        action_result=state[car_index]+ direction.to_vector()
        # If the given action will move the car to slot of another car
        if action_result in self.slots and self.slots.get(action_result) != car_index:
            return 101
        return 1
    
    # Read a parking problem from text containing a grid of tiles
    @staticmethod
    def from_text(text: str) -> 'ParkingProblem':
        passages =  set()
        cars, slots = {}, {}
        lines = [line for line in (line.strip() for line in text.splitlines()) if line]
        width, height = max(len(line) for line in lines), len(lines)
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char != "#":
                    passages.add(Point(x, y))
                    if char == '.':
                        pass
                    elif char in "ABCDEFGHIJ":
                        cars[ord(char) - ord('A')] = Point(x, y)
                    elif char in "0123456789":
                        slots[int(char)] = Point(x, y)
        problem = ParkingProblem()
        problem.passages = passages
        problem.cars = tuple(cars[i] for i in range(len(cars)))
        problem.slots = {position:index for index, position in slots.items()}
        problem.width = width
        problem.height = height
        return problem

    # Read a parking problem from file containing a grid of tiles
    @staticmethod
    def from_file(path: str) -> 'ParkingProblem':
        with open(path, 'r') as f:
            return ParkingProblem.from_text(f.read())
    
