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
import re
import random

# =============================================================================
# Class Definitions
# =============================================================================

#class Beat:
#    """
#    The beat class, the basic box to be filled with notes or rests, NOT CURRENTLY USED
#    """
#    def __init__(self, note):
#        """
#        note: A member of the note class, or "rest" which indicates a rest
#        """
#        self.note = note

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


def convert_notes(note_string_list, octaves = "rest"):
    """
    Convert a list of strings to the note class of a specified octave.
    """
    note_list = []
    
    #If octaves are not specified assume all octaves to be the fourth octave
    if octaves == "rest":
        octaves =  [4]*len(note_string_list)
        
    for i in range(len(note_string_list)):
        if note_string_list[i] != "rest":
            note_list.append(Note(note_string_list[i], octaves[i])) #Construct a list of note objects
        else:
            note_list.append("rest")
        
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
        

def next_note_tree(key, p_continue, p_rest, p_notes):
    """
    This function runs through the decision tree with specified probabilities
    Inputs:
        key, the possible notes that can be selected
        p_continue, float in [0,1] the probability of continuing
        p_rest, the probability of resting
        p_notes, a vector of probabilities that is of dim = len(key)
    Outputs:
        A note from key
    """
    
    #Randomly returns the next beat in the sequence based on prespecified probabilities
    #According to the decision tree
    
    if random_select( (1-p_continue, p_continue) ) == 1:
        return "cont"
    
    elif random_select( (1-p_rest, p_rest) ) == 1:
        return "rest"
    
    else:
        return key[random_select(p_notes)]


def next_note_lin(key, p_continue, p_rest, p_notes):
    """
    This function runs through the decision tree with specified probabilities
    Inputs:
        key, the possible notes that can be selected
        p_continue, float in [0,1] the probability of continuing
        p_rest, the probability of resting
        p_notes, a vector of probabilities that is of dim = len(key)
    Outputs:
        A note from key
    """
    
    #Randomly returns the next beat in the sequence based on prespecified probabilities
    #According to the decision tree
    
    p_beat_options = p_notes
    p_beat_options.append(p_continue)
    p_beat_options.append(p_rest)
    
    beat_options = key
    beat_options.append("cont")
    beat_options.append("rest")
    
    return beat_options[random_select(p_beat_options)]


def selection_prob(prob_list):
    """
    Given a list of probabilities "prob_list" that denotes the probability someone likes a given piece,
    compute the probabilities of selection
    """
    S = sum(prob_list)
    
    selection_probs = []
    for i in range(0, len(prob_list)):
        selection_probs.append(prob_list(i)/S)
        
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
        


def expand_datafile(outfilename, infilename, mes_len):
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


def Amajor_8beat():
    """
    This function plays an 8 beat A major scale.
    Inputs:
        None
    Outputs:
        A instance of the measure class
    """
    A_major = ["A", "B", "C#", "D", "E", "F#", "G#", "A"]
    p_list = [.125, .125, .125, .125, .125, .125, .125, .125]
    random_measure_list = [Note(A_major[random_select(p_list)],4)]
    scale = convert_notes(A_major, [4,4,4,4,4,4,4,5])
    
    for i in range(0, 7):
        new_note = next_note_tree(scale, .1, .25, p_list)
        random_measure_list.append(new_note)
        
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


# =============================================================================
# Testing
# =============================================================================

Amajor_8beat_adddata()
expand_datafile("../input/A_Amajor-8beat-winsound_expanded.csv","../input/A_Amajor-8beat-winsound.csv", 4)
