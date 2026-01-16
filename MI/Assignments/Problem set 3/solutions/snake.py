from typing import Dict, List, Optional, Set, Tuple
from mdp import MarkovDecisionProcess
from environment import Environment
from mathutils import Point, Direction
from helpers.mt19937 import RandomGenerator
from helpers.utils import NotImplemented
import json
from dataclasses import dataclass

"""
Environment Description:
    The snake is a 2D grid world where the snake can move in 4 directions.
    The snake always starts at the center of the level (floor(W/2), floor(H/2)) having a length of 1 and moving LEFT.
    The snake can wrap around the grid.
    The snake can eat apples which will grow the snake by 1.
    The snake can not eat itself.
    You win if the snake body covers all of the level (there is no cell that is not occupied by the snake).
    You lose if the snake bites itself (the snake head enters a cell occupied by its body).
    The action can not move the snake in the opposite direction of its current direction.
    The action can not move the snake in the same direction 
        i.e. (if moving right don't give an action saying move right).
    Eating an apple increases the reward by 1.
    Winning the game increases the reward by 100.
    Losing the game decreases the reward by 100.
"""

# IMPORTANT: This class will be used to store an observation of the snake environment
@dataclass(frozen=True)
class SnakeObservation:
    snake: Tuple[Point]     # The points occupied by the snake body 
                            # where the head is the first point and the tail is the last  
    direction: Direction    # The direction that the snake is moving towards
    apple: Optional[Point]  # The location of the apple. If the game was already won, apple will be None


class SnakeEnv(Environment[SnakeObservation, Direction]):

    rng: RandomGenerator  # A random generator which will be used to sample apple locations

    snake: List[Point]
    direction: Direction
    apple: Optional[Point]

    def __init__(self, width: int, height: int) -> None:
        super().__init__()
        assert width > 1 or height > 1, "The world must be larger than 1x1"
        self.rng = RandomGenerator()
        self.width = width
        self.height = height
        self.snake = []
        self.direction = Direction.LEFT
        self.apple = None

    def generate_random_apple(self) -> Point:
        """
        Generates and returns a random apple position which is not on a cell occupied 
        by the snake's body.
        """
        snake_positions = set(self.snake)
        possible_points = [Point(x, y) 
            for x in range(self.width) 
            for y in range(self.height) 
            if Point(x, y) not in snake_positions
        ]
        return self.rng.choice(possible_points)

    def reset(self, seed: Optional[int] = None) -> Point:
        """
        Resets the Snake environment to its initial state and returns the starting state.
        Args:
            seed (Optional[int]): An optional integer seed for the random
            number generator used to generate the game's initial state.

        Returns:
            The starting state of the game, represented as a Point object.
        """
        if seed is not None:
            self.rng.seed(seed) # Initialize the random generator using the seed
        # TODO add your code here
        # IMPORTANT NOTE: Define the snake before calling generate_random_apple
        # Initialize the snake in center, direction left and generate apple
        center_x = self.width // 2
        center_y = self.height // 2
        self.snake = [Point(center_x, center_y)]
        self.direction = Direction.LEFT
        # If the board has only one free cell (rarely), generate_random_apple will handle it
        # If snake occupies entire board (width*height == 1), no apple left
        if len(self.snake) >= self.width * self.height:
            self.apple = None
        else:
            self.apple = self.generate_random_apple()

        return SnakeObservation(tuple(self.snake), self.direction, self.apple)

    def actions(self) -> List[Direction]:
        """
        Returns a list of the possible actions that can be taken from the current state of the Snake game.
        Returns:
            A list of Directions, representing the possible actions that can be taken from the current state.

        """
        # The action can not move the snake in the opposite direction of its current direction.
        # The action can not move the snake in the same direction 
        possible = [Direction.NONE]
        
        # Only perpendicular moves are allowed
        # Cannot move in current direction (that's what NONE is for)
        # Cannot move in opposite direction (would reverse or hit body)
        opposite = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT,
        }
        
        for d in [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]:
            # Exclude current direction and opposite direction
            if d != self.direction and d != opposite.get(self.direction):
                possible.append(d)
        
        return possible

    def step(self, action: Direction) -> \
            Tuple[SnakeObservation, float, bool, Dict]:
        
        # TODO Complete the following function
        # Determine new direction: only change if action is an allowed orthogonal action (or NONE)
        """
        Updates the state of the Snake game by applying the given action.

        Validation rules for the incoming `action`:
          - If action == Direction.NONE -> keep moving in current direction.
          - If action == current direction -> treat as NONE (no-op).
          - If action == opposite(current direction) and snake length > 1 -> illegal, treat as NONE.
          - Otherwise accept the action (this allows reversing only when length == 1).

        Returns:
            (observation, reward, done, info)
        """
        # Determine allowed/treated action (don't call self.actions() here)
        opposite = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT,
        }

        # Normalize/validate action without relying on self.actions()
        if action == Direction.NONE:
            used_action = Direction.NONE
        elif action == self.direction:
            # same as NONE
            used_action = Direction.NONE
        elif action == opposite.get(self.direction) and len(self.snake) > 1:
            # reversing into body (illegal) -> treat as NONE
            used_action = Direction.NONE
        else:
            # allowed perpendicular action or (opposite when length == 1)
            used_action = action

        # apply action: change direction only if it's an explicit directional action
        if used_action != Direction.NONE:
            self.direction = used_action

        # compute new head with wrap-around
        head = self.snake[0]
        vec = self.direction.to_vector()
        new_x = (head.x + vec.x) % self.width
        new_y = (head.y + vec.y) % self.height
        new_head = Point(new_x, new_y)

        ate = (self.apple is not None and new_head == self.apple)

        # collision check: moving into existing body is losing unless it's the tail being vacated this move
        tail = self.snake[-1]
        will_vacate_tail = not ate  # if we don't eat, tail will be removed ; vacated
        collision = False
        if new_head in self.snake:
            if new_head == tail and will_vacate_tail:
                collision = False
            else:
                collision = True

        if collision:
            # lose: put head for consistent observation then finish
            self.snake.insert(0, new_head)
            reward = -100
            done = True
            observation = SnakeObservation(tuple(self.snake), self.direction, self.apple)
            return observation, reward, done, {}

        # move snake: insert new head
        self.snake.insert(0, new_head)

        if ate:
            # grow: do not remove tail
            reward = 1
            # check for win (snake covers all cells)
            if len(self.snake) == self.width * self.height:
                # winning
                reward += 100
                self.apple = None
                done = True
            else:
                # generate a new apple
                self.apple = self.generate_random_apple()
                done = False
        else:
            # normal move: remove tail
            self.snake.pop()
            reward = 0
            done = False

        observation = SnakeObservation(tuple(self.snake), self.direction, self.apple)
        return observation, reward, done, {}        


    ###########################
    #### Utility Functions ####
    ###########################

    def render(self) -> None:
        # render the snake as * (where the head is an arrow < ^ > v) and the apple as $ and empty space as .
        for y in range(self.height):
            for x in range(self.width):
                p = Point(x, y)
                if p == self.snake[0]:
                    char = ">^<v"[self.direction]
                    print(char, end='')
                elif p in self.snake:
                    print('*', end='')
                elif p == self.apple:
                    print('$', end='')
                else:
                    print('.', end='')
            print()
        print()

    # Converts a string to an observation
    def parse_state(self, string: str) -> SnakeObservation:
        snake, direction, apple = eval(str)
        return SnakeObservation(
            tuple(Point(x, y) for x, y in snake), 
            self.parse_action(direction), 
            Point(*apple)
        )
    
    # Converts an observation to a string
    def format_state(self, state: SnakeObservation) -> str:
        snake = tuple(tuple(p) for p in state.snake)
        direction = self.format_action(state.direction)
        apple = tuple(state.apple)
        return str((snake, direction, apple))
    
    # Converts a string to an action
    def parse_action(self, string: str) -> Direction:
        return {
            'R': Direction.RIGHT,
            'U': Direction.UP,
            'L': Direction.LEFT,
            'D': Direction.DOWN,
            '.': Direction.NONE,
        }[string.upper()]
    
    # Converts an action to a string
    def format_action(self, action: Direction) -> str:
        return {
            Direction.RIGHT: 'R',
            Direction.UP:    'U',
            Direction.LEFT:  'L',
            Direction.DOWN:  'D',
            Direction.NONE:  '.',
        }[action]