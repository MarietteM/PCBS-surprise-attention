#Monica Hegde
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
An experiment to assess the surprise-attention-hypothesis
"""
#%%
import expyriment
from expyriment import design, control, stimuli, io, misc
from expyriment.misc import constants
import numpy as np
import random


#################################### EXPERIMENT INITIALISATION ####################################
exp = expyriment.design.Experiment(name="Surprise Attention Task")
expyriment.control.initialize(exp)
screensize = exp.screen.surface.get_size()
screen_x, screen_y = exp.screen.surface.get_size()


### DEFINING COLORS AND CANVAS ###
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
canvas1 = stimuli.Canvas(screensize)
canvas2 = stimuli.Canvas(screensize)
canvas3 = stimuli.Canvas(screensize)


### INSTRUCTIONS ###    ##need to make instructions better...they're not clear rn
practiceinstructions = """ For this experiment, you will first see a cross, followed by a display of 12 squares in the form of a clock.
There will be a letter on each square. Your task is to determine whether there was an "H" or "U" among those letters. 
You will respond with the left and right keys, marked with "H" and "U" correspondingly.
We wil now do some practice trials! To begin press the space bar"""

expinstructions = """We will now begin the actual experiment. As a reminder:

You will first see a cross, followed by a display of 12 squares in the form of a clock. 
There will be a letter on each square. Your task is to determine whether there was an "H" or "U" among those letters.
You will respond with the left and right keys, marked with "H" and "U" correspondingly.
To begin press the space bar"""



#################################### CREATING A TRIAL FUNCTION ####################################
def trial_targetcolor(targetcolor, canvas1, canvas2, canvas3):
    ### FIXATION CROSS ###
    fixcross = stimuli.FixCross()
    fixcross.preload()
    fixcross.present()
    exp.clock.wait(1000)
    ### STIMULUS PARAMETERS ###
    coeff = 50
    s = 1.2 * coeff
    squaresides = [s,s]
    radius = 3.35 * coeff
    letterx, lettery = 0.7 * coeff, 0.8 * coeff
    letterxy = (letterx,lettery)
    targetletters = ['H','U']
    ranHU = random.randint(0, 1)
    targ_dist = [('P',0), ('L',0),('T',0), ('C',0), ('I',0), ('O',0), ('F',0), ('B',0), ('A',0), ('S',0), ('E',0), (targetletters[ranHU],1)]
    shuffledtarg_dist = random.sample(targ_dist, len(targ_dist)) 
    factor_position = shuffledtarg_dist.index((targetletters[ranHU],1)) ### POSITION OF TARGET ###
    for i in range(len(targ_dist)):
        angle = (2 * 3.1415 * i) / len(targ_dist)
        x = int(radius * np.cos(angle)) #CAH
        y = int(radius * np.sin(angle)) #SOH
        ranHU = random.randint(0, 1)
        if shuffledtarg_dist[i][1] == 1: ### IF TARGET ###
            squarestim = stimuli.Rectangle(squaresides, colour = targetcolor, position=(x,y))
            textstim = stimuli.TextBox(shuffledtarg_dist[i][0], size = letterxy , position= (x,y-5), text_colour= BLACK) #here i want the y to be in the square length 
        elif shuffledtarg_dist[i][1] == 0: ### IF DISTRACTOR ###
            squarestim = stimuli.Rectangle(squaresides, colour = RED, position=(x,y))
            textstim = stimuli.TextBox(shuffledtarg_dist[i][0], size = letterxy , position= (x,y-5), text_colour= BLACK) #here i want the y to be in the square length
        squarestim.plot(canvas1)
        squarestim.plot(canvas2)
        squarestim.plot(canvas3)
        textstim.plot(canvas2)
    canvas1.present()
    exp.clock.wait(500)
    canvas2.present()
    exp.clock.wait(86)
    canvas3.present()
    key, rt = exp.keyboard.wait([constants.K_LEFT, constants.K_RIGHT])
    trial = design.Trial()
    trial.set_factor("Target Position",factor_position)
    trial.set_factor("Target Letter", str(targetletters[ranHU]))
    trial.set_factor("Response", key)
    trial.set_factor("Reaction Time", rt)
    
    ##### Setting Target Color Factor --> red vs. green #####
    if targetcolor == (255, 0, 0):
        trial.set_factor("Target Color", "red")        
    elif targetcolor == (0, 255, 0):
        trial.set_factor("Target Color", "green")   
        
    ###### Setting Accuracy Factor --> hit vs. miss #####
    if key == 276 and str(targetletters[ranHU]) == 'H':
        trial.set_factor("Accuracy", "hit")
    elif key == 275 and str(targetletters[ranHU]) == 'U': 
        trial.set_factor("Accuracy", "hit")
    else:
        trial.set_factor("Accuracy", "miss")
    return trial


#################################### STARTING EXPERIMENT ####################################
expyriment.control.start(skip_ready_screen = True)
exp.data_variable_names = ["Target_Position", "Target_Color", "Target_Letter", "Response", "Reaction Time", "Block", "Accuracy"]
N_trials_block, N_blocks = 108, 2


for block in range(3): ### Three Blocks: Practice, Part1: Conjunction Search Segments, Part 2: Surprise Trials ###
    if block<2:
        INSTRUCTIONS = [practiceinstructions,expinstructions]
        stimuli.TextScreen('Instructions', INSTRUCTIONS[block]).present()
        exp.keyboard.wait(constants.K_SPACE)
    COLOR = [RED, RED, GREEN]
    trial = trial_targetcolor(COLOR[block], canvas1, canvas2, canvas3)
    if block == 0:
        for trials in range(12): #creating 12 practice trials per block
            trial = trial_targetcolor(COLOR[block], canvas1, canvas2, canvas3)
            trial.set_factor("Block", "Practice")
            exp.data.add([trial.get_factor("Target Position"),trial.get_factor("Target Color"),trial.get_factor("Target Letter"), trial.get_factor("Response"),trial.get_factor("Reaction Time"), trial.get_factor("Block"),trial.get_factor("Accuracy")])
    else:
        for trials in range(48): #creating 48 trials per experimental blocks [Conjunction Search Segment; Surprise Trials]
            trial = trial_targetcolor(COLOR[block], canvas1, canvas2, canvas3)
            trial.set_factor("Block", "Block " + str(block))
            exp.data.add([trial.get_factor("Target Position"),trial.get_factor("Target Color"),trial.get_factor("Target Letter"), trial.get_factor("Response"),trial.get_factor("Reaction Time"), trial.get_factor("Block"),trial.get_factor("Accuracy")])


expyriment.control.end(goodbye_text = "Thank you for participating!", confirmation = False, goodbye_delay = 1000)

