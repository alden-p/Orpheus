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

# =============================================================================
# Class Definitions
# =============================================================================

#class Beat:
#    """
#    The beat class, the basic box to be filled with notes or rests, NOT CURRENTLY USED
#    """
#    def __init__(self, note):
#        """
#        note: A member of the note class, or none which indicates a rest
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

        for note in self.measure:
            starttime = time.time() #display note time
            if note == None:
                #None types in the list are interpreted as rests
                
                time.sleep(self.note_duration/1000)
                
                print("rest: " + str(time.time() - starttime)) #Display Rest Time
            else:
                #Play the note
                
                note.win_play(self.note_duration)
                
                print("note: " + str(time.time() - starttime)) #Display Note Time
            
                


# =============================================================================
# Functions
# =============================================================================



def convert_notes(note_string_list, octaves = None):
    """
    Convert a list of strings to the note class of a specified octave.
    """
    note_list = []
    
    #If octaves are not specified assume all octaves to be the fourth octave
    if octaves == None:
        octaves =  [4]*len(note_string_list)
        
    for i in range(len(note_string_list)):
        if note_string_list[i] != None:
            note_list.append(Note(note_string_list[i], octaves[i])) #Construct a list of note objects
        else:
            note_list.append(None)
        
    return note_list
        


# =============================================================================
# Testing
# =============================================================================


major_scale = convert_notes(["A", "B", "C#", "D", "E", "F#", "G#", "A"], [4, 4, 4, 4, 4, 4, 4, 5] )
maj_scale_mes = Measure(150, major_scale, 8)
maj_scale_mes.win_play()


#beat_test = convert_notes(["A", "A", None, "A", "A", None, "A", "A", "C"])
#beat_test_mes = Measure(200, beat_test, len(beat_test))
#beat_test_mes.win_play()
