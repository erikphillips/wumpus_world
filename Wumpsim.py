
#
# wumpsim.py a Python implementation of pywumpsim
#
# Created by Erik Phillips - ephill07@calpoly.edu
# Date: November 6th, 2017
#
# CSC 480 - Artificial Intelligence
# Professor Daniel Kauffman
# Cal Poly, San Luis Obispo
#
# https://github.com/erikphillips/wumpus_world
#


from Action import *
from Orientation import *
import PyAgent
import random
import sys


# The version of the wumpus simulator
WUMPSIM_VERSION = "v1.2"

# The size of the world, which will be a square
WORLD_SIZE = 4

# The probability that a pit will be at any given location
PIT_PROBABILITY = 0.2

# The maximum number of moves per game
MAX_MOVES_PER_GAME = 1000


class Percept(object):
    def __init__(self):
        """ __init__: create a new percept"""
        self.stench = False
        self.breeze = False
        self.glitter = False
        self.bump = False
        self.scream = False

    def initialize(self):
        """ initialize: reset the percepts to their default value at the start of a try """
        self.stench = False
        self.breeze = False
        self.glitter = False
        self.bump = False
        self.scream = False


class State(object):
    """ State: holds the information on the current state of the game """

    def __init__(self, file_information):
        """ __init__: create a new state for the wumpus world, setting locations for wumpus, pits, and gold """

        # If there is file information, then use that, otherwise setup randomly
        if file_information is None:
            self.wumpus_location = self._get_wumpus_location()
            self.gold_location = self._get_gold_location()
            self.pit_locations = self._get_pit_locations()
        else:
            self.wumpus_location = file_information.wumpus_location
            self.gold_location = file_information.gold_location
            self.pit_locations = file_information.pit_locations

        self.agent_location = Location(1, 1)
        self.agent_orientation = RIGHT
        self.agent_alive = True
        self.agent_has_arrow = True
        self.agent_has_gold = False
        self.agent_in_cave = True
        self.wumpus_alive = True

    def initialize(self):
        """ initialize: called at the start of a new try, to reset game aspects back to default """
        self.agent_location = Location(1, 1)
        self.agent_orientation = RIGHT
        self.agent_alive = True
        self.agent_has_arrow = True
        self.agent_has_gold = False
        self.agent_in_cave = True
        self.wumpus_alive = True

    def _get_gold_location(self):
        """ _get_gold_location: return a random location not (1,1) for the gold's location """
        x, y = self._get_random_location()
        return Location(x, y)

    def _get_wumpus_location(self):
        """ _get_wumpus_location: return a random location, not (1,1) for the wumpus's location """
        x, y = self._get_random_location()
        return Location(x, y)

    @staticmethod
    def _get_random_location():
        """ _get_random_location: return a random location that is not the (1,1) square """
        x = 1
        y = 1

        while (x == 1) and (y == 1):
            x = random.randint(1, WORLD_SIZE)
            y = random.randint(1, WORLD_SIZE)

        return x, y

    @staticmethod
    def _get_pit_locations():
        """ _get_pit_locations: returns an array of pit locations, randomly selected based on a probability """
        locations = []
        for x in range(1, WORLD_SIZE + 1):
            for y in range(1, WORLD_SIZE + 1):
                if (x != 1) or (y != 1):
                    # Using the PIT_PROBABILITY, randomly determine if a pit will be at this location
                    if (random.randint(0, 1000 - 1)) < (PIT_PROBABILITY * 1000):
                        locations.append(Location(x, y))
        return locations


class Location(object):
    """ Location: location object that holds an x, y coordinate in the map """

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    @staticmethod
    def adjacent(location1, location2):
        """ adjacent: returns true if the two locations and next to each other """

        x1 = location1.x
        x2 = location2.x
        y1 = location1.y
        y2 = location2.y

        if (x1 == x2) and (y1 == (y2 - 1)) or \
           (x1 == x2) and (y1 == (y2 + 1)) or \
           (x1 == (x2 - 1)) and (y1 == y2) or \
           (x1 == (x2 + 1)) and (y1 == y2):
            return True

        return False


class WumpusWorld(object):
    def __init__(self, file_information=None):
        """ __init__: create a new wumpus world, randomly placing the wumpus and the gold, and multiple pits """
        self.num_actions = 0

        # Update the current state
        self.current_state = State(file_information=file_information)

        # Update current percepts
        self.current_percept = Percept()

        if Location.adjacent(self.current_state.agent_location, self.current_state.wumpus_location) or \
           (self.current_state.agent_location == self.current_state.wumpus_location):
            self.current_percept.stench = True

        for pit in self.current_state.pit_locations:
            if Location.adjacent(self.current_state.agent_location, pit):
                self.current_percept.breeze = True

        if self.current_state.gold_location.x == 1 and self.current_state.gold_location.y == 1:
            self.current_percept.glitter = True

    def initialize(self):
        """ initialize: called at the start of a new try, resets certain aspects to default """

        self.num_actions = 0
        self.current_state.initialize()
        self.current_percept.initialize()

        if Location.adjacent(self.current_state.agent_location, self.current_state.wumpus_location) or \
           (self.current_state.agent_location == self.current_state.wumpus_location):
            self.current_percept.stench = True

        for pit in self.current_state.pit_locations:
            if Location.adjacent(self.current_state.agent_location, pit):
                self.current_percept.breeze = True

        if self.current_state.gold_location.x == 1 and self.current_state.gold_location.y == 1:
            self.current_percept.glitter = True

    def get_percept(self):
        """ get_percept: return the current percept for the agent's location """
        return self.current_percept

    def execute_action(self, action):
        """ execute_action: execute the provided action, updating the agent's location and the percepts """

        self.num_actions += 1
        self.current_percept.bump = False
        self.current_percept.scream = False

        if action == GOFORWARD:
            if self.current_state.agent_orientation == RIGHT:
                if self.current_state.agent_location.x < WORLD_SIZE:
                    self.current_state.agent_location.x += 1
                else:
                    self.current_percept.bump = True
            elif self.current_state.agent_orientation == UP:
                if self.current_state.agent_location.y < WORLD_SIZE:
                    self.current_state.agent_location.y += 1
                else:
                    self.current_percept.bump = True
            elif self.current_state.agent_orientation == LEFT:
                if self.current_state.agent_location.x > 1:
                    self.current_state.agent_location.x -= 1
                else:
                    self.current_percept.bump = True
            elif self.current_state.agent_orientation == DOWN:
                if self.current_state.agent_location.y > 1:
                    self.current_state.agent_location.y -= 1
                else:
                    self.current_percept.bump = True

            # Update glitter percept
            self.current_percept.glitter = False

            if (not self.current_state.agent_has_gold) and \
                    (self.current_state.agent_location == self.current_state.gold_location):
                self.current_percept.glitter = True

            # Update stench percept
            self.current_percept.stench = False

            if Location.adjacent(self.current_state.agent_location, self.current_state.wumpus_location) or \
                    (self.current_state.agent_location == self.current_state.wumpus_location):
                self.current_percept.stench = True

            # Update breeze percept
            self.current_percept.breeze = False

            for pit in self.current_state.pit_locations:
                if Location.adjacent(self.current_state.agent_location, pit):
                    self.current_percept.breeze = True
                elif self.current_state.agent_location == pit:
                    self.current_state.agent_alive = False

            # check for death by wumpus
            if self.current_state.wumpus_alive and \
                    (self.current_state.agent_location == self.current_state.wumpus_location):
                self.current_state.agent_alive = False

        if action == TURNLEFT:
            if self.current_state.agent_orientation == RIGHT:
                self.current_state.agent_orientation = UP
            elif self.current_state.agent_orientation == UP:
                self.current_state.agent_orientation = LEFT
            elif self.current_state.agent_orientation == LEFT:
                self.current_state.agent_orientation = DOWN
            elif self.current_state.agent_orientation == DOWN:
                self.current_state.agent_orientation = RIGHT

        if action == TURNRIGHT:
            if self.current_state.agent_orientation == RIGHT:
                self.current_state.agent_orientation = DOWN
            elif self.current_state.agent_orientation == UP:
                self.current_state.agent_orientation = RIGHT
            elif self.current_state.agent_orientation == LEFT:
                self.current_state.agent_orientation = UP
            elif self.current_state.agent_orientation == DOWN:
                self.current_state.agent_orientation = LEFT

        if action == GRAB:
            if not self.current_state.agent_has_gold and \
                    (self.current_state.agent_location == self.current_state.gold_location):
                self.current_state.agent_has_gold = True
                self.current_percept.glitter = False

        if action == SHOOT:
            if self.current_state.agent_has_arrow:
                self.current_state.agent_has_arrow = False

                if self.current_state.wumpus_alive:
                    if (((self.current_state.agent_orientation == RIGHT) and
                         (self.current_state.agent_location.x < self.current_state.wumpus_location.x) and
                         (self.current_state.agent_location.y == self.current_state.wumpus_location.y)) or
                        ((self.current_state.agent_orientation == UP) and
                         (self.current_state.agent_location.x == self.current_state.wumpus_location.x) and
                         (self.current_state.agent_location.y < self.current_state.wumpus_location.y)) or
                        ((self.current_state.agent_orientation == LEFT) and
                         (self.current_state.agent_location.x > self.current_state.wumpus_location.x) and
                         (self.current_state.agent_location.y == self.current_state.wumpus_location.y)) or
                        ((self.current_state.agent_orientation == DOWN) and
                         (self.current_state.agent_location.x == self.current_state.wumpus_location.x) and
                         (self.current_state.agent_location.y > self.current_state.wumpus_location.y))):
                        self.current_state.wumpus_alive = False
                        self.current_percept.scream = True

        if action == CLIMB:
            if self.current_state.agent_location.x == 1 and self.current_state.agent_location.y == 1:
                self.current_state.agent_in_cave = False
                self.current_percept.stench = False
                self.current_percept.breeze = False
                self.current_percept.glitter = False

    def game_over(self):
        """ game_over: return True if the game is over, False otherwise"""
        return not self.current_state.agent_in_cave or not self.current_state.agent_alive

    def get_score(self):
        """ get_score: return the score for the current state of the game """

        score = 0

        # -1 for each action
        score -= self.num_actions

        if not self.current_state.agent_has_arrow:
            # -10 for shooting the arrow (already lost 1 for the action)
            score -= 9

        if self.current_state.agent_has_gold and not self.current_state.agent_in_cave:
            # +1000 for leaving the cave with the gold
            score += 1000

        if not self.current_state.agent_alive:
            # -1000 for dying
            score -= 1000

        return score

    def print_world(self):
        """ print_world: print the current wumpus world"""

        print("World size = {}x{}".format(WORLD_SIZE, WORLD_SIZE))

        # print out the first horizontal line
        out = "+"
        for x in range(1, WORLD_SIZE + 1):
            out += "---+"
        print(out)

        for y in range(WORLD_SIZE, 0, -1):  # print starting from the 'bottom' up

            # print out the first row, containing pits + gold + wumpus
            out = "|"

            for x in range(1, WORLD_SIZE + 1):
                if self.current_state.wumpus_location == Location(x, y):
                    if self.current_state.wumpus_alive:
                        out += "W"
                    else:
                        out += "x"
                else:
                    out += " "

                if not self.current_state.agent_has_gold and self.current_state.gold_location == Location(x, y):
                    out += "G"
                else:
                    out += " "

                _has_pit = False
                for pit in self.current_state.pit_locations:
                    if pit == Location(x, y):
                        _has_pit = True
                if _has_pit:
                    out += "P"
                else:
                    out += " "

                out += "|"

            print(out)

            # print out the second row, containing the agent
            out = "|"

            for x in range(1, WORLD_SIZE + 1):
                if self.current_state.agent_alive and self.current_state.agent_location == Location(x, y):
                    if self.current_state.agent_orientation == RIGHT:
                        out += " A>|"
                    elif self.current_state.agent_orientation == UP:
                        out += " A^|"
                    elif self.current_state.agent_orientation == LEFT:
                        out += " A<|"
                    else:
                        out += " Av|"
                else:
                    out += "   |"

            print(out)
            out = "+"

            # print out the final horizontal line
            for x in range(1, WORLD_SIZE + 1):
                out += "---+"

            print(out)

        # print the current percepts for the agent's location
        print("Current percept = [stench={},breeze={},glitter={},bump={},scream={}]".format(
            self.current_percept.stench,
            self.current_percept.breeze,
            self.current_percept.glitter,
            self.current_percept.bump,
            self.current_percept.scream))

        print("Agent has gold = {}, agent has arrow = {}".format(
            self.current_state.agent_has_gold,
            self.current_state.agent_has_arrow))

        print("Current score = {}".format(self.get_score()))
        print()


class WumpusWorldFileInformation(object):
    def __init__(self, filename):
        self.world_size = WORLD_SIZE
        self.wumpus_location = None
        self.gold_location = None
        self.pit_locations = []

        with open(filename, "r") as infile:
            lines = infile.readlines()

            if len(lines) < 3:  # there must be at least 3 lines for size, wumpus, and gold
                print("Invalid world file; required: size, wumpus, and gold locations.")
                sys.exit(1)

            self._process_size(lines[0])
            self._process_wumpus(lines[1])
            self._process_gold(lines[2])

            if len(lines) > 3:  # only process the pits (optional) if there are more lines
                self._process_pits(lines[3:])

    def _process_size(self, line):
        global WORLD_SIZE  # if the size of the map is different than 4, then the world size will need updating.

        size_tokens = line.strip().split(" ")
        if len(size_tokens) != 2 or size_tokens[0] != "size":
            print("Incorrect token in world file '{}', expected 'size'".format(size_tokens[0]))
            sys.exit(1)

        self.world_size = int(size_tokens[1])
        if self.world_size < 2:
            print("Invalid world size, size < 2.")
            sys.exit(1)

        WORLD_SIZE = self.world_size  # update the global world size

    def _process_wumpus(self, line):
        tokens = line.strip().split(" ")
        if len(tokens) != 3 or tokens[0] != "wumpus":
            print("Incorrect token in world file '{}', expected 'wumpus'".format(tokens[0]))
            sys.exit(1)

        loc_x = int(tokens[1])
        loc_y = int(tokens[2])

        if (1 > loc_x > self.world_size) or (1 > loc_y > self.world_size) or (loc_x == 1 and loc_y == 1):
            print("Bad wumpus location in world file for location ({}, {}).".format(loc_x, loc_y))
            sys.exit(1)

        # Create a new location object and set it to the wumpus location
        self.wumpus_location = Location(loc_x, loc_y)

    def _process_gold(self, line):
        tokens = line.strip().split(" ")
        if len(tokens) != 3 or tokens[0] != "gold":
            print("Incorrect token in world file '{}', expected 'gold'".format(tokens[0]))
            sys.exit(1)

        loc_x = int(tokens[1])
        loc_y = int(tokens[2])

        if (1 > loc_x > self.world_size) or (1 > loc_y > self.world_size) or (loc_x == 1 and loc_y == 1):
            print("Bad gold location in world file for location ({}, {}).".format(loc_x, loc_y))
            sys.exit(1)

        # Create a new location object and set it to the gold location
        self.gold_location = Location(loc_x, loc_y)

    def _process_pits(self, lines):
        for line in lines:
            tokens = line.strip().split(" ")
            if len(tokens) != 3 or tokens[0] != "pit":
                print("Incorrect token in world file '{}', expected 'pit'".format(tokens[0]))
                sys.exit(1)

            loc_x = int(tokens[1])
            loc_y = int(tokens[2])

            if (1 > loc_x > self.world_size) or (1 > loc_y > self.world_size) or (loc_x == 1 and loc_y == 1):
                print("Bad pit location in world file for location ({}, {}).".format(loc_x, loc_y))
                sys.exit(1)

            # Create a new location object and append it to the pit locations
            self.pit_locations.append(Location(loc_x, loc_y))


class Agent(object):
    @staticmethod
    def construct():
        """ construct: call the agent's constructor method """
        PyAgent.PyAgent_Constructor()

    @staticmethod
    def initialize():
        """ initialize: call the agent's initialize method """
        PyAgent.PyAgent_Initialize()

    @staticmethod
    def process(percept):
        """ process: call the agent's process method, passing to it the percepts """
        return PyAgent.PyAgent_Process(percept.stench, percept.breeze, percept.glitter, percept.bump, percept.scream)

    @staticmethod
    def game_over(score):
        """ game_over: call the agent's game over method, passing to it the final score """
        PyAgent.PyAgent_GameOver(score)

    @staticmethod
    def destructor():
        """ deconstructor: call the agent's destructor """
        PyAgent.PyAgent_Destructor()


def action_to_string(action):
    """ action_to_string: return a string from the given action """
    if action == GOFORWARD:
        return "GOFORWARD"
    if action == TURNRIGHT:
        return "TURNRIGHT"
    if action == TURNLEFT:
        return "TURNLEFT"
    if action == SHOOT:
        return "SHOOT"
    if action == GRAB:
        return "GRAB"
    if action == CLIMB:
        return "CLIMB"
    return "UNKNOWN ACTION"


def main(args):
    """ main: the main driver for the wumpus simulator
              iterates over each trial, creating a new wumpus world
              then allows for the given number of tries for that world """

    print("Welcome to the Python Wumpus World Simulator {} by Erik Phillips. Happy Hunting!\n".format(WUMPSIM_VERSION))

    total_score = 0

    # Set random number generator seed
    # If no seed is given, args.seed is None, therefore the seed will be random
    random.seed(args.seed)

    for trials in range(1, args.trials + 1):
        file_information = None
        if args.world is not None:
            file_information = WumpusWorldFileInformation(args.world)

        wumpus_world = WumpusWorld(file_information=file_information)  # init a new wumpus world
        Agent.construct()  # call the constructor on the imported agent

        trial_score = 0

        for tries in range(1, args.tries + 1):
            wumpus_world.initialize()  # call initialize on the wumpus world, resetting for the try
            Agent.initialize()  # call the initialize method for the imported agent

            num_moves = 0

            print("Trial {}, Try {} begin".format(trials, tries))
            print()

            while (not wumpus_world.game_over()) and (num_moves < MAX_MOVES_PER_GAME):
                wumpus_world.print_world()
                percept = wumpus_world.get_percept()  # get the percepts for the current location
                action = Agent.process(percept)  # and pass the percepts to the imported agent, expecting an action

                print("Action = {}".format(action_to_string(action)))
                print()

                wumpus_world.execute_action(action)  # execute the action in the wumpus world
                num_moves += 1

            score = wumpus_world.get_score()  # get the final score for the world
            Agent.game_over(score)  # and pass that score to the imported agent, signaling game over
            trial_score += score

            print("Trial {}, Try {} complete: score = {}\n".format(trials, tries, score))

        Agent.destructor()  # call the deconstructor on the imported agent for this trial is over
        average_score = trial_score / args.tries
        total_score += trial_score

        print("Trial {} complete: Average score for trial = {}, total score for trial = {}\n".format(trials,
                                                                                                     average_score,
                                                                                                     trial_score))

    average_score = total_score / (args.trials * args.tries)
    print("All trials completed: Average score for all trials = {}, " \
          "Total score for all trials = {}".format(average_score, total_score))
    print("Thanks for playing!")
    print()

    # Return the average_score and the total_score
    return average_score, total_score


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-tries', type=int, default=1)
    parser.add_argument('-trials', type=int, default=1)
    parser.add_argument('-seed', type=int)
    parser.add_argument('-world', type=str)
    args = parser.parse_args()

    if args.tries <= 0:
        raise argparse.ArgumentTypeError("Minimum tries is 1")

    if args.trials <= 0:
        raise argparse.ArgumentTypeError("Minimum trials is 1")

    if args.seed and args.seed <= 0:
        raise argparse.ArgumentTypeError("Seed must be a positive integer")

    main(args)
