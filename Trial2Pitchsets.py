# First serious composition
# Chooses pitches stochastically from a pitch set for a specified amount of time (+- some amount decided by gaussian distribution)
# Each voice should switch from pitchset to pitchset at similar but not necessarily the same time

from abjad import *
import sys
import random
import numpy as np
import math



# generates a part of the specified length (in measures) out of the specified pitches
# rhythm should be an ordering of note lengths, we won't start at the beginning, but we will loop through it]
def generatePassage(length, pitchset, rhythm):
	rhythmlength = np.sum(np.ones(rhythm.size)/rhythm)
	length = np.random.normal(length, 1)
	# get the full array of note lengths, rhythms
	rhythms = rhythm[np.random.randint(rhythm.size):]
	length -= np.sum(np.ones(rhythms.size)/rhythms)
	while length > rhythmlength:
		rhythms = np.append(rhythms, rhythm)
		length-=rhythmlength
	rhythms = np.append(rhythms, rhythm[:np.random.randint(rhythm.size)])
	# figure out pitches
	pitchIndexes = np.floor(np.abs(np.random.normal(0, len(pitchset)/2, rhythms.size)))
	pitches = np.vectorize(lambda x: pitchset[x%pitchset.size])(pitchIndexes)
	notes = []
	for i in range(len(pitches)):
		# numerator = second value, denominator = first value
		f = Fraction(rhythms[i])
		if math.log(f.numerator, 2) % 1 != 0: 
			f*= math.pow(2, math.ceil(math.log(f.numerator,2)))/f.numerator
			f = Fraction(f)
		notes.append(Note(pitches[i], Duration(f.denominator, f.numerator)))
	return notes

# start with a set of pitches and rational note lengths (8/3 is 3 eigth notes, or a dotted quarter)
# Change the pitchset's octave based on voice
# generate a passage
# increment the pitch of one note
# cut the length of one rhythmic value in half
# then change the pitch and rhythmic content gradually (2 voices at first, then 4)
# repeat the process with the new pitches and note lengths
def main():
	pitches = np.array([0, 10, 2, 8, 4, 6])
	pitches[:] -=12
	rhythms = np.array([8, 8, 8, 8, 8, 4, 8, 8/3, 8])
	#create staffs
	s1 = Staff([Note(12, Duration(1, 1))])
	s2 = Staff([Note(8, Duration(1, 1))])
	s3 = Staff([Note(4, Duration(1, 1))])
	s4 = Staff([Note(-12, Duration(1,1))])
	instruments = [s1,s2,s3,s4]
	
	# generate music
	for i in range(len(pitches)):
		for j in range(len(instruments)):
			if j == 0:
				pitches[:]+=12
			if j == 2:
				pitches[:]-=12
			elif j == 3: 
				pitches[:]-=24
			instruments[j].extend(generatePassage(4, pitches, rhythms))
			pitches[0:j*2]-=12
			if j == 0:
				pitches[:]-=12
			if j == 2:
				pitches[:]+=12
			elif j == 3:
				pitches[:] += 24
		pitches[i]+=1
		rhythms[i]= rhythms[i]*2
		
	# switch up the values for pitches and rhythms
	
	instruments[0].extend(generatePassage(4, pitches[:]+12, rhythms))
	instruments[2].extend(generatePassage(4, pitches, rhythms))
	
	pitches = np.array([0, 7, 4, 2, 9])
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
main()
