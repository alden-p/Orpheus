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
        self.measure = measure
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
        

def next_note(key, p_continue, p_rest, p_notes):
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
    
    






# =============================================================================
# Testing
# =============================================================================


#major_scale = convert_notes(["A", "B", "C#", "D", "E", "F#", "G#", "A"], [4, 4, 4, 4, 4, 4, 4, 5] )
#maj_scale_mes = Measure(150, major_scale, 8)
#maj_scale_mes.win_play()

#smoke_on_the_water = convert_notes(["E", "rest", "G", "rest", "A", "E", "rest", "G", "A#", "A", "E", "rest" ,"G", "rest", "A", "G", "E"],
#                                    [3,"rest",3,"rest",4,3,"rest",3,4,4,3,"rest",3,"rest",4,3,3])
#smoke_mes = Measure(200, smoke_on_the_water, len(smoke_on_the_water))
#smoke_mes.win_play()

#beat_test = convert_notes(["A", "A", "rest", "A", "A", "rest", "A", "A", "C"])
#beat_test_mes = Measure(200, beat_test, len(beat_test))
#beat_test_mes.win_play()

p_list = (.125, .125, .125, .125, .125, .125, .125, .125)
#avg = 0
#for i in range(1,100000):
#    #print(random_select(p_list))
#    avg += random_select(p_list)/100000
#    
#print(avg)
#
random_measure_list = [Note("A",4)]
scale = convert_notes(["A", "B", "C", "D", "E", "F", "G", "A"], [4,4,4,4,4,4,4,5])

for i in range(0, 7):
    new_note = next_note(scale, .2, .2, p_list)
    #print(new_note)
    random_measure_list.append(new_note)
    
random_measure = Measure(145, random_measure_list, len(random_measure_list))


starttime = time.time()
random_measure.win_play()

print("Measure Duration: " + str(time.time() - starttime))