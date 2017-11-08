# Wumpus World Simulator #
A driver for the wumpus world which allows for students to create their own Wumpus World agent to navigate the cave.

## Simulator Details ##
The simulator works by generating a new world and a new agent for each trial.
Before each try on this world, the agent's `Initialize()` method is called, which
you can use to perform any pre-game preparation. Then, the game starts.  The
agent's `Process()` method is called with the current *Percept*, and the agent
should return an action, which is performed in the simulator. This continues
until the game is over (agent dies or leaves cave) or the maximum number of
moves (1000) is exceeded. When the game is over, the Agent's `GameOver()` method
is called. If additional tries are left for this world, then the world is
re-initialized, and the agent's `Initialize()` method is called again, and play
proceeds on another instance of the same game.

After the number of tries is completed, the agent is deleted. So, you may want
to store some information in the agent's destructor method to be reloaded
during the agent's constructor method when reborn for the next trial. If
additional trials have been requested, then a new wumpus world is generated,
and the process continues as described above.

Scoring information is output at the end of each try, each trial and at the end
of the simulation.

## Agent Details ##
Your agent must include at least five methods: `constructor`, `destructor`,
`Initialize`, `Process`, and `GameOver`. You may change any or all of these methods
to implement your agent. And you may include additional methods as you see fit.

## Python Agent ##
You will make all your changes to the `PyAgent.py` file. You will see five
functions in the file: `PyAgent_Constructor`, `PyAgent_Destructor`,
`PyAgent_Initialize`, `PyAgent_Process`, and `PyAgent_GameOver`. These five functions
are called by their counterparts in the simulator.  You can
see how this is done in the `Wumpsim.py` file, **BUT DO NOT MODIFY THIS
FILE**.  The only file you should change is `PyAgent.py`. Note that the
`PyAgent_Process` function takes the five separate percepts, rather than a
`Percept` class instance, and the `PyAgent_Process` function should return one of
the six actions defined in the `Action.py` file.

Once you've finished your `PyAgent.py` file, simply run the `python Wumpsim.py` program
to test your agent. The `PyAgent.py` file and the `Wumpsim.py` script must be
in the same directory. The `Wumpsim.py` program accepts all the options
described described below.

### Simulator Options ### 
The following options are allowed and provided to the simulator as arguments:

```
usage: MyWumpsim.py [-h] [-tries TRIES] [-trials TRIALS] [-seed SEED]

Optional Arguments:
  -trials TRIALS
    The number of trials to attempt. Each trial will generate a new world
    to test the agent on. Default is 1.
  
  -tries TRIES
    The number of tries attempted for each trial which will give the agent
    multiple tries for eahc world that is created. Default is 1.
  
  -seed SEED
    The seed to specify to the random number generator. Specifying a seed 
    allows for the simulator to run the same random worlds.
    Default is None which uses a random component from the system time.
```

## Acknowledgments ##
This project was based on the wumpus simulator by Larry Holder:

```
Wumpus Simulator v2.9 (released 09/15/2017)
Copyright (c) 2017. Washington State University.
Written by Larry Holder (holder@wsu.edu).
```

The Python version of this simulator project was written for the CPE 480 class in Artificial Intelligence at Cal Poly, San Luis Obispo, CA to replace the C++ implementation.

## Future Work and Known Issues ## 
Currently this version of the simulator does not support importing a predefined world from a text file like the original verson of the wumpus simulator. All the worlds will have to be randomly generated.

Version 1.0 only supports Python 2.7
