# Wumpus World Simulator #
A driver for the wumpus world which allows for students to create their own Wumpus World agent to navigate the cave.

## Python Agent ##
You will make all your changes to the PyAgent.py file. You will see five
functions in the file: PyAgent_Constructor, PyAgent_Destructor,
PyAgent_Initialize, PyAgent_Process, and PyAgent_GameOver. These five functions
are called by their counterparts in the simulator.  You can
see how this is done in the Wumpsim.py file, BUT DO NOT MODIFY THIS
FILE.  The only file you should change is PyAgent.py. Note that the
PyAgent_Process function takes the five separate percepts, rather than a
Percept class instance, and the PyAgent_Process function should return one of
the six actions defined in the Action.py file.

Once you've finished your PyAgent.py file, simply run the `python Wumpsim.py` program
to test your agent. The PyAgent.py file and the `Wumpsim.py` script must be
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

## Future Work ## 
Currently this version of the simulator does not support importing a predefined world from a text file like the original verson of the wumpus simulator. All the worlds will have to be randomly generated.
