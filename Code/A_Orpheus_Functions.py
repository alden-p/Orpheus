# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 14:13:10 2018

@author: Alden Porter

This program contains the necessacary functions for the Orpheus Program
"""


# =============================================================================
# Import Libraries
# =============================================================================

import winsound
import time
import random
import pandas as pd
import re
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LogisticRegressionCV

# =============================================================================
# Class Definitions
# =============================================================================

class Note:
    """
    The Note Class, a pitch and note to be assigned to a beat
    """
    
    def __init__(self, pitch, octave):
        """
        pitch: A string, corresponds to the pitch of the chromatic scale.
        octave: The octave of the note
        hertz: The hertz of the note
        """
        hertz_base = 440
        octave_base = 4
        numerical_base = 2**(1/12)
        pitch_dict = {"A": 0, "A#": 1, "Bb": 1, "B": 2, "C": 3, "C#": 4,
                      "Dd": 4, "D": 5, "D#": 6, "Eb": 6, "E": 7, "F": 8, "F#": 9,
                      "Gb": 9, "G": 10, "G#": 11, "Ab": 11}
        self.pitch = pitch
        self.octave = octave
        self.hertz =  hertz_base*(numerical_base)**(12*(octave-octave_base) + pitch_dict[pitch])
        
    def win_play(self, duration):
        """
        Play the note through the windows system sound library for a specified duration
        """
        winsound.Beep(int(self.hertz), int(duration))

class Measure:
    """
    The Measure Class, the building block of more complex musical structures
    """
    def __init__(self, bpm, measure, nbeat):
        """
        measure: A list that is the actual measure of the object 
        nbeat: how many "beats" are in the measure (say, 32 for 4/4 time with 16th notes)
        """
        self.bpm = bpm
        self.measure = measure # A list of notes
        self.nbeat = nbeat
        self.nnotes= len(measure)
        self.note_duration = (60000/self.bpm) * (self.nbeat/self.nnotes)
        
        
    def win_play(self):
        """
        Play the measure as a series of system beeps
        """

        for i in range(0,self.nnotes):
            #starttime = time.time() #display note time
            
            note = self.measure[i]
            
            if note == "rest":
                #"rest" types in the list are interpreted as rests
                
                #Rest for a duration given by the number of proceeding continuations
                continuations = 1
                next_note_i = i + 1
                    
                while next_note_i <= self.nnotes - 1 and self.measure[next_note_i] == "cont":
                    continuations += 1
                    next_note_i +=1
                    #print("hi")
                
                time.sleep(self.note_duration/1000 * continuations)
                
                #print("rest: " + str(time.time() - starttime)) #Display Rest Time
            elif note == "cont":
                
                continue
                
            else:
                #Play the note for a duration given by the number of proceeding continuations
                
                continuations = 1
                next_note_i = i + 1
                
                while next_note_i <= self.nnotes - 1 and self.measure[next_note_i] == "cont":
                    continuations += 1
                    next_note_i +=1
                    #print("hi")
                note.win_play(self.note_duration*continuations)
                
                #print("note: " + str(time.time() - starttime)) #Display Note Time
                   
# =============================================================================
# Functions
# =============================================================================


def convert_notes(note_string_list):
    """
    Convert a list of strings to the note class of a specified octave.
    """
    note_list = []
            
    for i in range(len(note_string_list)):
        if note_string_list[i] != "rest" and note_string_list[i] != "cont":
            note_list.append(Note(note_string_list[i].split('-')[0], int(note_string_list[i].split('-')[1]))) #Construct a list of note objects
        else:
            note_list.append(note_string_list[i])
        
    return note_list
    

def random_select(p_list):
    """
    Randomly select an index from an iterable list of probabilities
    Inputs:
        p_list, a list of probabilities that sums to 1
    Outputs:
        An index from p_list
    """
    target_num = random.uniform(0,1)
    cum_prob = 0
    
    #Add up probability until the first index that passes cum_prob
    # and return that index, if the probabilities do not sum to one, and the
    # target number is greater, we simply return the last index
    for i in range(0,len(p_list)):
        cum_prob += p_list[i]
        if cum_prob >= target_num:
            return i
    return len(p_list)-1

def next_note_lin(notes, p_notes):
    """
    This function runs through the decision tree with specified probabilities
    Inputs:
        notes, a list of notes must have [..., cont, rest] at the end
        p_notes, a vector of probabilities correspond to each note
    Outputs:
        A note from key
    """
    
    #Randomly returns the next beat in the sequence based on prespecified probabilities
    #According to the decision tree
    
    return notes[random_select(p_notes)]


def selection_prob(prob_list):
    """
    Given a list of probabilities "prob_list" that denotes the probability someone likes a given piece,
    compute the probabilities of selection
    """
    S = sum(prob_list)
    
    selection_probs = []
    for i in range(0, len(prob_list)):
        selection_probs.append(prob_list[i]/S)
        
    return selection_probs


def like_dislike(outfilename, music_function):
    """
    Plays a piece, asks the user if they like or dislike it, then appends the piece and
    respose to a .csv file.
    inputs:
        outfilename, the name of the csv file a string
        music_function, a function handle that plays music and returns the measure of music being played
    outputs:
        none, writes to a file
    """
    
    measure = music_function().measure
    
    critical_review = input("Did you like it <y/n>? ")
    
    if critical_review.lower() == "y":
        response = 1
    elif critical_review.lower() == "n":
        response = 0
    else:
        print("Can you read? Answer y or n.")
        raise ValueError
            
        
    with open(outfilename, mode = 'a', encoding = "utf_8") as outfile:
        outfile.write(str(response) + ",")
        for index, beat in enumerate(measure):
            if index < len(measure)-1:
                if isinstance(beat, Note):
                    outfile.write(beat.pitch + "-" + str(beat.octave) + ",")
                elif type(beat) == str:
                    outfile.write(beat + ",")
                else:
                    print("Unknown beat value")
                    raise ValueError
            elif index == len(measure)-1:
                if isinstance(beat, Note):
                    outfile.write(beat.pitch + "-" + str(beat.octave))
                elif type(beat) == str:
                    outfile.write(beat)
                else:
                    print("Unknown beat value")
                    raise ValueError
        outfile.write("\n")


def initialize_datafile(outfilename, num_beats):
    """
    Intialize the datafile to store training data on a particular measure
    inputs:
        outfilename, a string
    outputs:
        none, writes to a file
    """
    with open(outfilename, mode = 'w', encoding = "utf_8") as outfile:
        outfile.write("listener_response" + ",")
        for i in range(0,num_beats):
            outfile.write("beat" + str(i) + ",")
        outfile.write("\n")
        


def expand_datafile(infilename, outfilename, mes_len):
    """
    Expand the csv file of the listener_respond, note1, note2,...
    into all measures of length 'mes_len'
    inputs:
        infilename, a string the input filename
        outfilename, a string the output filename 
        mes_len, and integer how far back we are looking
    outputs:
        None
    """
    #Loop over every line in the input file
    with open(infilename, mode = "r", encoding = "utf_8") as infile:
        for count, line in enumerate(infile):
            
            num_notes = len(line.strip().split(",")) - 1 #The number of notes in the measure
            data = line.strip().split(",")
            
            #If it is the first line, write the first mes_len + 1 entries
            if count == 0:
                with open(outfilename, mode = "w", encoding = "utf_8") as outfile:
                    for i in range(0,mes_len + 1):
                        outfile.write(data[i])
                        if i < mes_len:
                            outfile.write(",")
                        else:
                            outfile.write("\n")
            
            #The actual data
            else:
                with open(outfilename, mode = "a", encoding = "utf_8") as outfile:
                    for j in range(1, num_notes-mes_len + 2):
                        #If we have empty data, continue
                        if data[j] == "cont":
                            continue
                        
                        outfile.write(data[0] + ",")
                        for i in range(j, mes_len + j):
                            outfile.write(data[i])
                            if i < mes_len + j-1:
                                outfile.write(",")
                        outfile.write("\n")

def powerset(s):
    """
    This function takes a set object S and returns its powerset Ps.
    Inputs:
        s, a set
    Outputs:
        Ps, a set, the powerset of s
    """
    result = [[]]
    for elem in s:
        result.extend([x + [elem] for x in result])
    return result

def create_interactions(infilename, outfilename, order):
    """
    This function creates a series of interaction variables
    inputs:
        infilename, a string, the name of the file containing the variables to be interacted
        outfilename, a stirng, the name of the file to output interactions to
        order, an integer, the maximum allowed order of interactions
    outputs:
        none, writes to a csv file
    """
    with open(infilename, mode = 'r', encoding = 'utf_8') as infile:
        with open(outfilename, mode = 'w', encoding = 'utf_8') as outfile:
            
            for index, row in enumerate(infile):
                row_data = row.strip().split(',')
                
                if index == 0:
                    header = row_data
                    interaction_orders = set(range(1, len(header))) # The different desired orders of interacitons
                    interactions = powerset(interaction_orders)
                
                outfile.write(row_data[0] + ',')
                
                for sub_num, subset in enumerate(interactions):
                    if subset == []:
                        continue
                    if len(subset) > order:
                        continue
                    for elem in subset:
                        outfile.write(row_data[elem])
                    if sub_num < len(interactions) - 1:
                        outfile.write(',')
                outfile.write('\n')    
    
def create_indicators(infilename, outfilename):
    """
    This function creates a series of indicator variables for each column beat value,
    outputs a high dimensional csv file.
    inputs:
        filename, a string the filename to read in
        outfilename, a string, the file to output to
    outputs:
        none, constructs a csv file under outfilename
    """
    
    input_df = pd.read_csv(infilename) # read the data input
    
    input_col_names = list(input_df.columns.values)
    output_df = pd.get_dummies(input_df, columns = input_col_names[1:])
    
    output_df.to_csv(outfilename, index = False)

def logit_lasso(infilename, reg_par = 1):
    """
    This function takes in a file containing csv data with dep var in the first column
    and potential covariates in the others, fits a logistic regression with a L1
    penalty to it, and returns that model.
    inputs:
        infilename, a string the name of the file containing the data
        reg_par, a float, the regularization penalty parameter for the logit. Defaults to 1
    outputs:
        A trained logit model
    """
    
    
    input_df = pd.read_csv(infilename) 
    
    y = input_df.iloc[:,0]
    X = input_df.iloc[:,1:]
    
    model = LogisticRegression(penalty = "l1", solver = "liblinear", C = reg_par, multi_class = "ovr")
#    model = LogisticRegressionCV(penalty = "l1", solver = "liblinear", multi_class = "ovr", Cs = reg_par)

    fitted_model = model.fit(X,y)
    
    return fitted_model

def create_X(note_string_list, datafilename):
    """
    This function takes a sequence of notes and returns a vector (list) of covariate
    indicators for that list.
    inputs:
        note_string_list, A list of strings indicating the sequence of notes to be played
        datafilename, a string, the name of the file containing the information on the covariates
    outputs:
        a list of indicators (1,0)s
    """
    
    X = []
    
    #Read in the header of the datafile and take everything but listerner respose into a list
    with open(datafilename, mode = 'r', encoding = 'utf_8') as infile:
        columnnames = infile.readline().strip().split(',')[1:]
    
    #Loop over columnnames, they should be of the form beat0beat2_A#-4C-5
    for col in columnnames:
        
        noteseq = '' #Intialize empty sequence of notes
        
        #Split the format into the beatorder we care about, and what the corresponding
        #Note order should be for indicator = 1
        collist = col.split('_')
        beatorder = re.sub('[^0-9]','', collist[0]) #Construct a string defining the order
        noteorder = collist[1]
        
        #Check if the note order in the list equals the note order we care about.
        for i in beatorder:
            noteseq += note_string_list[int(i)]
        if noteorder == noteseq:
            X.append(1)
        else:
            X.append(0)
    return np.array(X).reshape(1,-1)

def construc_prob(history, window, note_set, model, datafilename):
    """
    This function constructs the proabilities of seeing each next note
    Inputs:
        history, A list of strings, the note history in chronological order
        window, and integer how far back we are looking
        note_set, the set of notes to be considered
        model, the model used to construct probabilities
        datafilename,  a string, the name of the file containing the information to convert strings of notes to interaction dummies
    Outputs:
        A list of probabilities of len(note_set)
    """
    
    recent_history = history[len(history)-window + 1:len(history)]
    
    like_prob = [] # Initialize a empty list of probabilities of liking a certain sequence
    
    for note in note_set:
        potential_hist = recent_history + [note]
        X = create_X(potential_hist, datafilename)
#        print(potential_hist)
#        print(model(X))
        like_prob.append(model(X))
    
    return selection_prob(like_prob)

    
def Amajor_8beat():
    """
    This function plays an 8 beat A major scale.
    Inputs:
        None
    Outputs:
        A instance of the measure class
    """
    #Intialize teh scale and probability list for the first 3 notes
    A_major = ["A-4", "B-4", "C#-4", "D-4", "E-4", "F#-4", "G#-4", "A-5"]
    note_set = A_major + ["cont", "rest"]
    p_list = [.08, .08, .08, .08, .08, .08, .08, .08]
    scale = convert_notes(note_set)
    
    #Generate the first note, add it to the history and random measure
    first_note = A_major[random_select(p_list)] #Initialize the first note 
    history = [first_note]
    random_measure_list = [Note(first_note.split("-")[0], int(first_note.split("-")[1]))]
    
    #Allow for the possibility of rests and continues now that the first note has been added
    p_list.append(.18)
    p_list.append(.18)
    
    #Generate the next 2 notes
    for i in range(1, 3):
        #randomly select the index, using that index add a new note to the scale
        index = random_select(p_list) 
        new_note = scale[index]
        new_note_str = note_set[index]
        
        #Add the new note to the random measure and the history
        random_measure_list.append(new_note)
        history.append(new_note_str)
        
    #Fit a logit model to predict probabilities
    datafilename = "../input/A_Amajor-8beat-winsound_indicators.csv"
    fitted_model = logit_lasso(datafilename,3)
    model = lambda X: fitted_model.predict_proba(X)[0,1]
    window = 4
    
    #Intelligently generate the remainder of the measure
    for i in range(3, 8):
        #randomly select the index, using that index add a new note to the scale, where the probabilities are updated accodring to model
        p_list = construc_prob(history, window, note_set, model, datafilename)
        index = random_select(p_list) 
        new_note = scale[index]
        new_note_str = note_set[index]
        
        #Add the new note to the random measure and the history
        random_measure_list.append(new_note)
        history.append(new_note_str) 
        
    print(history)
    
    random_measure = Measure(145, random_measure_list, len(random_measure_list))
    
    starttime = time.time()
    random_measure.win_play()
    
    print("Measure Duration: " + str(time.time() - starttime))
    return random_measure

def Amajor_8beat_adddata():
    """
    Add a datapoint to the Amajor_8beat file.
    """
    
    like_dislike("../input/A_Amajor-8beat-winsound.csv",  Amajor_8beat)
    expand_datafile("../input/A_Amajor-8beat-winsound.csv", "../input/A_Amajor-8beat-winsound_expanded.csv", 4)
    create_interactions("../input/A_Amajor-8beat-winsound_expanded.csv", "../input/A_Amajor-8beat-winsound-interactions.csv", 3)
    create_indicators("../input/A_Amajor-8beat-winsound-interactions.csv", "../input/A_Amajor-8beat-winsound_indicators.csv")
    
# =============================================================================
# Testing
# =============================================================================

#Amajor_8beat()
Amajor_8beat_adddata()
