# First serious composition
# Chooses pitches stochastically from a pitch set for a specified amount of time (+- some amount decided by gaussian distribution)
# Each voice should switch from pitchset to pitchset at similar but not necessarily the same time

# what i want is to specify the rhythms for each voice, then generate the melody stochastically
# that's what I've got here, it's just that I want to make the rhythm nonrandom
# then, I'll call it on a set 

# TODO Change rhythms to take in lists of Durations, rather than numbers

from abjad import *
from abjad.tools.mathtools import *
import sys
import random
import numpy as np
import math
import copy



# generates a part of the specified length (in measures) out of the specified pitches
# rhythm should be an ordering of note lengths, we won't start at the beginning, but we will loop through it]
def generatePassage(length, pitchset, rhythm):
	rhythmLength = np.sum(rhythm)
	# get the full array of note lengths, rhythms
	rhythms = rhythm
	length -= rhythmLength
	while length > rhythmLength:
		rhythms = np.append(rhythms, rhythm)
		length-=rhythmLength
	# figure out pitches
	pitchIndexes = np.floor(np.abs(np.random.normal(0, len(pitchset)/2, len(rhythms))))
	pitches = np.vectorize(lambda x: pitchset[x%pitchset.size])(pitchIndexes)
	notes = []
	for i in range(len(pitches)):
		notes.append(Note(pitches[i], rhythms[i]))
	return notes

# start with a set of pitches and rational note lengths (8/3 is 3 eigth notes, or a dotted quarter)
# Change the pitchset's octave based on voice
# generate a passage
# increment the pitch of one note
# cut the length of one rhythmic value in half
# then change the pitch and rhythmic content gradually (2 voices at first, then 4)
# repeat the process with the new pitches and note lengths
def generateStringQuartet(pitches, rhythms, lengths):
	# if we don't have four different rhythms specified
	if rhythms.shape[0] == 1:
		r = np.zeros((4,len(rhythms)))
		r[:] = rhythms
		rhythms = r
	#create staffs
	s1 = []
	s2 = []
	s3 = []
	s4 = []
	
	instruments = [s1,s2,s3,s4]
	pitchesbackup = np.copy(pitches)
	# generate music
	for i in range(len(pitches)):
		for j in range(len(instruments)):
			if j == 0:
				pitches[:]+=12
			if j == 2:
				pitches[:]-=12
			elif j == 3: 
				pitches[:]-=24
			instruments[j] = instruments[j] + generatePassage(lengths[j], pitches, rhythms[j])
			pitches = np.copy(pitchesbackup)
			#pitches[0:j*2]-=12
		pitches[i]+=1
		#rhythms[j][i]= rhythms[j][i]*2
		
	return instruments
	"""pitches = np.array([0, 7, 4, 2, 9])
	rhythms = np.array([16/3, 16, 16/3, 16, 8, 8])	
	
	instruments[1].extend(generatePassage(4, pitches[:]-12, rhythms))
	instruments[3].extend(generatePassage(4, pitches[:]-24, rhythms))
	# generate music
	for i in range(len(pitches)):
		for j in range(len(instruments)):
			pitches[0:(len(pitches)-j*2)]+=12
			if j == 0:
				pitches[:]+=12
			if j == 2:
				pitches[:]-=12
			elif j == 3: 
				pitches[:]-=24
			instruments[j].extend(generatePassage(4, pitches, rhythms))
			pitches[0:(len(pitches)-j*2)]-=12
			if j == 0:
				pitches[:]-=12
			if j == 2:
				pitches[:]+=12
			elif j == 3:
				pitches[:] += 24
		pitches[i]+=1
		rhythms[i]= rhythms[i]*2
	score = Score(instruments)
	show(score)
	play(score)
	#lilypond_file = lilypondfiletools.make_basic_lilypond_file(score)
	#print(format(lilypond_file))
main()"""

def applyTuplets(staff, mul):
	num = mul.numerator
	denom = mul.denominator
	tuplets = Tuplet.from_duration_and_ratio(Duration(1,denom), Ratio([1]*num)) * (len(staff)/num)
	i = 0
	for t in tuplets:
		for note in t.select_leaves():
			note.written_pitch = staff[i].written_pitch;
			i+=1
	"""
	stf = copy.deepcopy(staff[1:])
	for n in stf:
		n.written_duration = Duration(1,8)
	
	i = 0
	while i < len(stf):
		tuplets.append(Tuplet(mul, stf[i:i+num]).to_fixed_duration_tuplet())
		#show(tuplets[-1])
		i+=num"""
	return tuplets


def main():

	pitches = np.array([0, 10, 2, 8, 4, 6])
	#pitches[:] -=12
	rhythms = np.array([[Duration(1,4)] * 4,[Duration(1,8)] * 8,[Duration(1,4), Duration(1,4), Duration(1,8), Duration(1,8), Duration(1,8), Duration(1,8),], [Duration(1,2), Duration(1,2)]])
	s = generateStringQuartet(pitches, rhythms, [3, 4, 4, 4])
	show(s)
	applyTuplets(s[0][1:], Multiplier(3,2))
	show(s)
	#play(s)
#main()
