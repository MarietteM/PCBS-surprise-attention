#Monica Hegde
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
An experiment to assess the surprise-attention-hypothesis
"""
#%%
import expyriment
from expyriment import design, control, stimuli, io, misc
import numpy as np
import random

exp = expyriment.design.Experiment(name="Surprise Attention Task")
expyriment.control.initialize(exp)

#DEFINING COLORS AND CANVAS
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
screensize = exp.screen.surface.get_size()
screen_x, screen_y = exp.screen.surface.get_size()
canvas1 = stimuli.Canvas(screensize)
canvas2 = stimuli.Canvas(screensize)
canvas3 = stimuli.Canvas(screensize)

instructions_eng = """after every cross, you will see 12 squares displayed 
in the form of a clock, you will need to respond, using the keys marked below,
whether the letter sequence contains an H or a U. Press space to continue. """

def fixcross1000():
    fixcross = stimuli.FixCross()
    fixcross.preload()
    fixcross.present()
#plotting distractor and target circles(target: red for first 48 trials; green for second 48 trials)
def trial_targetcolor(targetcolor, canvas1, canvas2, canvas3, text_colortarg, text_colordist):
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
    for i in range(len(targ_dist)):
        angle = (2 * 3.1415 * i) / len(targ_dist)
        x = int(radius * np.cos(angle)) #CAH
        y = int(radius * np.sin(angle)) #SOH
        ranHU = random.randint(0, 1)
        if shuffledtarg_dist[i][1] == 1:#target
            squarestim = stimuli.Rectangle(squaresides, colour = targetcolor, position=(x,y))
            textstim = stimuli.TextBox(shuffledtarg_dist[i][0], size = letterxy , position= (x,y-5), text_colour= text_colortarg) #here i want the y to be in the square length 
        elif shuffledtarg_dist[i][1] == 0: #distractors
            squarestim = stimuli.Rectangle(squaresides, colour = RED, position=(x,y))
            textstim = stimuli.TextBox(shuffledtarg_dist[i][0], size = letterxy , position= (x,y-5), text_colour= text_colordist) #here i want the y to be in the square length
        squarestim.plot(canvas1)
        squarestim.plot(canvas2)
        squarestim.plot(canvas3)
        textstim.plot(canvas2)
    canvas1.present()
    exp.clock.wait(500)
    canvas2.present()
    exp.clock.wait(86)
    canvas3.present()
    exp.keyboard.wait()
    

numbertrials_per_block = 108
numbe_of_blocks = 2


expyriment.control.start(skip_ready_screen = True)
fixation_cross = stimuli.FixCross()
stimuli.TextScreen('Experiment 1', instructions_eng).present()
exp.keyboard.wait(expyriment.misc.constants.K_SPACE)

for block in range(numbe_of_blocks):#creating 2 blocks and then 
    temp_block = design.Block (name = str(block + 1 )) #naming blocks by their numbers
    COLOR = [RED, GREEN]
    for trial in range(numbertrials_per_block): #creating 12 practice trials per block
        temp_trial = design.Trial()
        fixcross1000()#fixation cross for 1000ms 
        trial_targetcolor(COLOR[block], canvas1, canvas2, canvas3, BLACK, BLACK)
        exp.add_block(temp_block)
        
        
exp.data_variable_names = ["block", "targetletter", "targetletterresponse", "targetlettercolor", "squareposition", "trial", "RT", "accuracy", "trialtype(exp/prac)"]


expyriment.control.end()


##now need to have it so that the last canvas--squares w/o text AND WAIT!!!
##figure out how to WAIT until either < or > is pressed

###then need to make first 48 trials RED and second 48 trials GREEN
