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

====================================
    NAVIGATING THE RESULTS FOLDER
====================================
    
    Results files are named as follows:
        `result_[sample_size].txt`
    
    For example a sampling using sets of 10 games would be:
        `result_10.txt`

    Each results file records every play of all games played and the outcomes
    with the result markov probabilities listed last. 
    
    It is recommended that if you only want the probability table, you use the following command:
        `tail [file]`
        
    To compare multiple results you may also do:
        `tail -f [file 1] [file 2] ... [file n] 

             
            ====================================================
            |   This program was created by Damola Mabogunje   |
            ====================================================

