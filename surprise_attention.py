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


### INSTRUCTIONS ###          ##need to make instructions better...they're not clear rn
instructions = """after every cross, you will see 12 squares displayed 
in the form of a clock, you will need to respond, using the keys marked below,
whether the letter sequence contains an H or a U. Press space to continue. """


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
    exp.keyboard.wait()
    trial = design.Trial()
    trial.set_factor("Position",factor_position)
    trial.set_factor("Target Letter", str(targetletters[ranHU]))
    trial.set_factor("Target Color", str(targetcolor))
    return trial

    
    #need to measure RT here
    ##first 48 targets will be RED, second 48 targets will be GREEN---target colors
    ##first 12 trials--practice
    ##if keyboard press is the same as targetletters[ranHU]--> HIT, if not, MISS
    

#################################### STARTING EXPERIMENT ####################################
expyriment.control.start(skip_ready_screen = True)
exp.data_variable_names = ["Position", "Target Letter", "Target Color"]
N_trials_block, N_blocks = 108, 2

###PRESENTING STIMULI###
stimuli.TextScreen('Experiment 1', instructions).present()
exp.keyboard.wait(expyriment.misc.constants.K_SPACE)

for block in range(N_blocks):#creating 2 blocks and then 
    COLOR = [RED, GREEN]
    #adding 108 trials per block
    for trials in range(2): #creating 12 practice trials per block
        trial = trial_targetcolor(COLOR[block], canvas1, canvas2, canvas3)
        exp.data.add([trial.get_factor("Position"),trial.get_factor("Target Color"),trial.get_factor("Target Letter")])

                
    
expyriment.control.end()

#To-do
##now need to have it so that the last canvas--squares w/o text AND WAIT!!!
##figure out how to WAIT until either < or > is pressed
##figure out how to record responses

##DONE
### need to make first 48 trials RED and second 48 trials GREEN
