# PCBS: Testing the Surprise-Attention Hypothesis

## Introduction

The current project is based on the work of Gernot Horstmann (2002). The study investigates the surprise attention hypothesis, which postulates that unexpected events induce surprise in subjects, which in turn elicits attention towards this surprising event. They investigated whether surprising color singletons capture attention. They measured attention in terms of target stimulus detection; a greater proportion of stimulus detection indicates a better caption of attention. The study presents a series of 12 colored squares appearing on the 12 clock positions of a circle. On 11 of the squares, distractor letters are present, on 1 of the squares, the target is presented. For the first 48 experimental trials (after a practice session of 12 trials), all 12 squares are the same color(i.e. red). These trials are denoted as 'Conjunction search segment'. Beginning from the 49th trial, the target square is green, thus possibly inducing surprise. The 49th trial is referred to as the 'surprise trial', and the 50th trial onwards is referred to as 'Featured search segment'. In Gernot's study, they found that the surprise trial yields a 90 percent correct detection rate among participants, with following feature search segment trials eliciting equally if not better correction detection rates. 


<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->
**Table of Contents**

- [PCBS: Testing the Surprise-Attention Hypothesis](#pcbs:-testing-the-surprise-attention-hypothesis)
    - [Methods](#methods)
        - [Initializing Experiment and Preparing Presets](#initializing-experiment-and-preparing-presets)
    	- [Creating Trial Function](#creating-trial-function)
    	- [Creating Stimuli](#Stimuli)
    	- [Creating Trial Structure](#trial-structure)
    	- [Creating Expyriment Trial](#creating-Expyriment-Trial)
    - [Experiment](#experiment)
    - [Future Directions](#future-directions)
    - [Class Reflection](#class-reflection)
    - [Reference](#reference)

<!-- markdown-toc end -->

## Methods

### Initializing Experiment and Preparing Presets
To begin, I imported relevant modules from expyriment, numpy, and random. Also, knowing that I would be using the colors, red, green and black, I defined said variables. I also defined two instruction variables, one to be presented before practice trials and one to be presented before experimental trials.

```
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


### INSTRUCTIONS ###  
practiceinstructions = """ For this experiment, you will first see a cross, followed by a display of 12 squares in the form of a clock.
There will be a letter on each square. Your task is to determine whether there was an "H" or "U" among those letters. 
You will respond with the left and right keys, marked with "H" and "U" correspondingly.
We wil now do some practice trials before starting the actual experiment! To begin press the space bar"""

expinstructions = """We will now begin the actual experiment. As a reminder:

You will first see a cross, followed by a display of 12 squares in the form of a clock. 
There will be a letter on each square. Your task is to determine whether there was an "H" or "U" among those letters.
You will respond with the left and right keys, marked with "H" and "U" correspondingly.
To begin press the space bar"""

```
### Creating Trial Function
I defined the following function to display my stimuli and record responses from participants. In following sections, I will detail the various aspects of this function. 

```
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
```


### Creating Stimuli
To replicate their study, using the expyriment module from python, I presented 12 colored squares appearing on the 12 clock positions of a circle. On 11 of the squares, the following distractor letters were randomly presented: B, A, S, E, P, U, L, T, C, I, O, and F. On a twelfth square, one of two target letters were presented: H or U. Half the targets were 'H', and the other half were 'U'. Stimulus parameters (i.e. square color, circle diameter, clock positions) were taken from Gernot's methods.

```
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
```
Target and distractor positions were randomly distributed among the 12 squares. 

```
shuffledtarg_dist = random.sample(targ_dist, len(targ_dist)) 
factor_position = shuffledtarg_dist.index((targetletters[ranHU],1))
```

```
        if shuffledtarg_dist[i][1] == 1: ### IF TARGET ###
            squarestim = stimuli.Rectangle(squaresides, colour = targetcolor, position=(x,y))
            textstim = stimuli.TextBox(shuffledtarg_dist[i][0], size = letterxy , position= (x,y-5), text_colour= BLACK) #here i want the y to be in the square length 
        elif shuffledtarg_dist[i][1] == 0: ### IF DISTRACTOR ###
            squarestim = stimuli.Rectangle(squaresides, colour = RED, position=(x,y))
            textstim = stimuli.TextBox(shuffledtarg_dist[i][0], size = letterxy , position= (x,y-5), text_colour= BLACK) 
```

For 12 practice trials, and 96 experimental trials, participants were asked to determine which of the two possible target letters were presented using the keyboard as quickly and as accurately as possible. 


### Creating Trial Structure
The trial structure is as follows:

![Surprise Attention](https://github.com/monicahegde/PCBS-surprise-attention/blob/master/Gernot_Presentation.png?raw=true)

For the first 48 trials(i.e. the conjunction search segment), where all squares are the same color (i.e. red),  a fixation cross is present for 1000ms, followed by a preview of the 12 squares (without letters) for 500ms, followed by the 12 squares with target and distractor letters present, and finally followed by blank squares until participant makes a response (either H or U).
###
For the 49th trial (surprise trial) and the 50th trial onwards (feature search segment), the same structure was presented. A fixation cross is present for 1000ms, followed by a preview of the 12 squares (without letters) for 500ms, followed by the 12 squares with target and distractor letters present, and finally followed by blank squares until participant makes a response (either H or U).

```
    fixcross = stimuli.FixCross()
    fixcross.preload()
    fixcross.present()
    exp.clock.wait(1000)

```


```
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
```


Here, participants would either have to press the left arrow key, corresponding to detection of an 'H' target or the right arrow key, corresponding to the 'U' target, as marked with stickers on the physical keyboard. I chose not to ask participants to use actual H and U keys because keyboards vary by country, and for right handed participants, pressing a left vs. right arrow creates less confounds.

```
 key, rt = exp.keyboard.wait([constants.K_LEFT, constants.K_RIGHT])
```

### Creating Expyriment Trial
Once I created the stimuli and mapped them to the expyriment canvas, I designed a trial and initially collected the following factors: Target Position, Target Letter, Response, Reaction Time, Target Color and Accuracy(hit: response corresponds to Target Letter; Miss: response does not correspond to Target Letter). 

Note: We measure reaction time because it is used in one of the papers follow up experiment. Knowing this before hand could be interesting in terms of understanding the degree to which participants perform better or worse on the different trials types (conjunction search v. surprise trial v. feature search)

```
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

```
Once the function collected criteria for these measures, I returned trial as a global variable. 

```
    return trial
```

## Experiment
I then started the experiment and created the variable names (which create headers for factors in .xpd file). I also defined variables indicating the number of practice and experimental trials.

```
expyriment.control.start(skip_ready_screen = True)
exp.data_variable_names = ["Target_Position", "Target Color", "Target Letter", "Response", "Reaction Time", "Block", "Accuracy"]
N_practice = 12
N_experiment = 48
```


Following, I created the following loop to run the experiment. 

```
for block in range(3): ### Three Blocks: Practice, Part1: Conjunction Search Segment, Part 2: Feature Search Segment ###
    if block<2:
        INSTRUCTIONS = [practiceinstructions,expinstructions]
        stimuli.TextScreen('Instructions', INSTRUCTIONS[block]).present()
        exp.keyboard.wait(constants.K_SPACE)
    COLOR = [RED, RED, GREEN]
    trial = trial_targetcolor(COLOR[block], canvas1, canvas2, canvas3)
    if block == 0:
        for trials in range(N_practice): #creating 12 practice trials per block
            trial = trial_targetcolor(COLOR[block], canvas1, canvas2, canvas3)
            trial.set_factor("Block", "Practice")
            exp.data.add([trial.get_factor("Target Position"),trial.get_factor("Target Color"),trial.get_factor("Target Letter"), trial.get_factor("Response"),trial.get_factor("Reaction Time"), trial.get_factor("Block"),trial.get_factor("Accuracy")])
    else:
        for trials in range(N_experiment): #creating 48 trials per experimental blocks [Conjunction Search Segment; Surprise Trials]
            trial = trial_targetcolor(COLOR[block], canvas1, canvas2, canvas3)
            trial.set_factor("Block", "Block " + str(block))
            exp.data.add([trial.get_factor("Target Position"),trial.get_factor("Target Color"),trial.get_factor("Target Letter"), trial.get_factor("Response"),trial.get_factor("Reaction Time"), trial.get_factor("Block"),trial.get_factor("Accuracy")])


expyriment.control.end(goodbye_text = "Thank you for participating!", confirmation = False, goodbye_delay = 1000)
```

Here, there are three blocks, a practice block, the conjunction search segment, and the Feature Search Segments. I then added "Block" as a factor to my trial. Here, the practice and the first block have red targets, while the second block has green targets. 

```
    COLOR = [RED, RED, GREEN]
    trial = trial_targetcolor(COLOR[block], canvas1, canvas2, canvas3)
```

For each block, using the exp.data.add and trial.get_factor commands, the program records the relevant data from responses for each trial: target position, target color, target letter, response, reaction time, block number, and accuracy. 

```
exp.data.add([trial.get_factor("Target Position"),trial.get_factor("Target Color"),trial.get_factor("Target Letter"), trial.get_factor("Response"),trial.get_factor("Reaction Time"), trial.get_factor("Block"),trial.get_factor("Accuracy")])

```
## Future Directions

From this code, participants' results are saved in the data sub-directory folder as an .xpd file. Given more time, these data could be analyzed via the pandas module in python using `pandas.read_csv()` or via R using `read.table`. Furthermore, once data from enough participants has been collected, we can use a generalized linear mixed effects model to see whether there are significant effects of trial type (Conjunction Search, Feature Search) and target placement on reaction time and on accuracy. 


## Class Reflection
Before starting this course, I had a pretty limited knowledge about experimental python. Prior to the cogmaster, I had never coded on my own. I had gone to the mois de rentrée beginners course, and the intersemestre R courses, so I knew the very basics of creating loops and 'if' statements. I did take the class AT2, which focused on using the numpy and random module. There, we did a lot of isolated exercises in spyder, using the visualizations of dataframes and matrices. Also, since the class was more focused on the reports rather than the code, I never learned how not to "bricoler" whenever I had a complex problem. 

While the principles of the 'random' module helped me understand how to randomize stimulus presention, before this class, I would not have any idea of how to code an experiment. I would say that this class taught me how to approach a problem in python. Before this class, I had a tendency to get bogged down by the complexity of a problem, but with this course, I learned to approach a larger problem in smaller steps. I also learned how to understand error messages, which I think hindered me before. After this class, I feel more equipped to code by trial and error. Though I am still a beginner, I feel more equipped to learn autonomously than I did before. 

I did, however, find the expyriment documentation pretty difficult to understand at first; at first I did not understand the difference between the backend Xpyriment and expyriment, hence struggled a lot at first. But because I started rather early on on this project, I was able to find solutions slowly but surely, and towards the end, I found it very manageable and enjoyable (when the code worked). You mentioned a strategy of writing down the problem and breaking down the solutions on paper. That, particularly, I found to be incredibly useful. I also learned how to push and pull from github, something which I think will help me out later.


I think, for the future, it would be interesting to have a brief overview of pandas and R regarding statistical analyses. I would have liked to analyse the datafiles, but I did not know exactly how to go about this. Also, I personally found that I progressed a lot quicker once I had my project in mind, so for next year I think it could be beneficial to have students pick their project within the first month, and do the shorter exercises before that. The short exercises were a good way to start the course (given that there are many different levels of exercises for different levels of students).  And I definitely found it nice to try coding a problem on my own and then seeing a more clean solution afterwards on slack/github.

## Reference

Horstmann, G. (2002). Evidence for attentional capture by a surprising color singleton in visual search. Psychological science, 13(6), 499-505.