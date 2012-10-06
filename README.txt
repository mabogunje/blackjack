================
    CONTENTS
================

    This folder contains:
        1. Required classes for running the games of Whitejack and Greyjack
        2. The sampling program (Sampling.py) for generating markov probabilities
        3. A folder (results) of all test results using the program with varying parameters

====================
    INSTRUCTIONS
====================
    For instructions on how to use the "Sampling" program with optional arguments, do:
        `python Sampling.py -h`

    Otherwise, you may simply run Sampling.py with required arguments only. 
        `python Sampling.py -n25`

    You may also pipe the results of sampling excercise to an output file.

=====================================
    NAVIGATING THE RESULTS FOLDER
=====================================
    
    Results files are named as follows:
        `[GAME_TYPE]_[SAMPLINGS]_result.txt`
    
    For example a sampling using sets of 10 games would be:
        `whitejack_200_result.txt`

    Each results file records every play of all games played and the outcomes
    with the result markov probabilities listed last. 
    
    It is recommended that if you only want the probability table, you use the following command:
        `tail [file]`
        
    To compare multiple results you may also do:
        `tail -f [file 1] [file 2] ... [file n] 
        

=====================================
    UNDERSTANDING RESULTS OUTPUT
=====================================

The output presented at the end of each results file looks like this:

    0 => [0.0, 0.25, 0.25, 0.25, 0.25, 0.0, 0.0]
    1 => [0.0, 0.0, 0.249, 0.253, 0.25, 0.248, 0.0]
    2 => [0.0, 0.0, 0.0, 0.22138047138047137, 0.2398989898989899, 0.4612794612794613, 0.07744107744107744]
    3 => [0.0, 0.0, 0.0, 0.0, 0.20999275887038377, 0.662563359884142, 0.1274438812454743]
    4 => [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]
    5 => [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

Where each number on the left is a state pointing to its list of transitions to other states
You will notice that the list is longer than the number of remaining states. This is because
The last two entries represent win/loss probabilities In each list:

    - The very last probability, is the probability of winning  
    - The second-to-last probability, is the probability of losing  
             
            ====================================================
            |   This program was created by Damola Mabogunje   |
            ====================================================

