from typing import Any, Dict, Set, Tuple, List
from problem import Problem
from mathutils import Direction, Point
from helpers.utils import NotImplemented

#TODO: (Optional) Instead of Any, you can define a type for the parking state

ParkingState = Tuple[Point, ...]

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
        """
    Determines whether a given state is the goal state.
    - For each car, we check if its current position corresponds to its designated slot.
    - 'self.slots' maps positions to car indices.
    - If any car is not in its correct slot, the state is not the goal.
    """
        for i, carPosition in enumerate(state):
            if self.slots.get(carPosition) != i:
                return False
            return True
        
    # This function returns a list of all the possible actions that can be applied to the given state
    def get_actions(self, state: ParkingState) -> List[ParkingAction]:
        """
    Returns a list of all valid actions that can be taken from the given state.
    - Each action is a tuple (car_index, direction).
    - A move is valid if:
        1. The direction leads to a passage cell (valid road position).
        2. The target position is not already occupied by another car.
    """ 
        #from problem we are told that the solution is a list of actions or none  
        action = []
        occupied = set(state)
        for i, carPos in enumerate(state): 
            for dir in Direction: #Enum [RIGHT, UP, LEFT, DOWN] in imported Direction from mathutils
                movedTo = carPos + dir.to_vector() # to_vector is a func int mathutils
                if movedTo in self.passages and movedTo not in occupied: #here i am checking I can move into this postion stored in passages and whether the postion is take or not 
                    #if it is not taken and exist then it is an action i can take 
                    action.append((i,dir))
        return action
                
    
    # This function returns a new state which is the result of applying the given action to the given state
    def get_successor(self, state: ParkingState, action: ParkingAction) -> ParkingState:
        #TODO: ADD YOUR CODE HERE
        """
    Returns the new state resulting from applying a given action.
    - The action is (car_index, direction).
    - We move that car one step in the given direction and update the state.
    - The state is stored as a tuple for immutability (hashable for sets/dicts).
    """
        i, direction = action 
        #make a list of new states
        newState = list(state)
        newPostion = newState[i] + direction.to_vector()
        #update the car's position 
        newState[i] = newPostion
        return tuple(newState) 
    
    # This function returns the cost of applying the given action to the given state
    def get_cost(self, state: ParkingState, action: ParkingAction) -> float:
        #TODO: ADD YOUR CODE HERE
        """
    Returns the cost of performing a given action from the given state.
    - Each car has a unique movement cost: cost = 26 - i
      (i is the car index; earlier cars are more expensive to move).
    - The cost is converted to float since the search algorithms expect numerical values.
    """
        i, dir = action
        cost = 26 - i 
        return float(cost)   
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
    
