# PyAgent.py

import Action
import Orientation


def PyAgent_Constructor():
    """ PyAgent_Constructor: called at the start of a new trial """
    print "PyAgent_Constructor"


def PyAgent_Destructor():
    """ PyAgent_Destructor: called after all tries for a trial are complete """
    print "PyAgent_Destructor"


def PyAgent_Initialize():
    """ PyAgent_Initialize: called at the start of a new try """
    print "PyAgent_Initialize"


def PyAgent_Process(stench, breeze, glitter, bump, scream):
    """ PyAgent_Process: called with new percepts after each action to return the next action """

    percept_str = ""
    if stench == 1:
        percept_str += "Stench=True,"
    else:
        percept_str += "Stench=False,"
    if breeze == 1:
        percept_str += "Breeze=True,"
    else:
        percept_str += "Breeze=False,"
    if glitter == 1:
        percept_str += "Glitter=True,"
    else:
        percept_str += "Glitter=False,"
    if bump == 1:
        percept_str += "Bump=True,"
    else:
        percept_str += "Bump=False,"
    if scream == 1:
        percept_str += "Scream=True"
    else:
        percept_str += "Scream=False"
    
    print "PyAgent_Process: " + percept_str

    return Action.GOFORWARD


def PyAgent_GameOver(score):
    """ PyAgent_GameOver: called at the end of each try """
    print "PyAgent_GameOver: score = " + str(score)

