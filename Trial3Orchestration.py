# Trial3Orchestration.py
# Come up with a pitchset for each two bar phrase, choose several beat numbers for events, then orchestrate pitches for each event
# homophonic music!

import numpy as np
from abjad import *
import math

# takes a start and end pitchset, and the number of intermediary pitchsets to use
# returns an array of length numsteps where each subsequent element transforms 
def incrementPitchset(startPitchset, endPitchset, numsteps):
	extraPitches = np.array([])
	pitchesAtStart = False # tracks where our extra pitches are
	# make sure they're the same length
	while len(endPitchset) > len(startPitchset):
		i = np.randint(0,len(endPitchset))
		extraPitches.append(endPitchset[i])
		endPitchset = np.delete(endPitchset, i)
	while len(startPitchset) > len(endPitchset):
		i = np.random.randint(0,len(startPitchset))
		np.append(extraPitches, startPitchset[i])
		startPitchset = np.delete(startPitchset, i)
		pitchesAtStart = True
	# create the list of pitchsets
	retval = np.empty((numsteps, len(startPitchset)))
	retval[0] = startPitchset
	retval[-1] = endPitchset
	# fill them in
	for i in range(1, len(startPitchset)-1):
		retval[:,i]=interpolateNumbers(startPitchset[i],endPitchset[i], numsteps)
	# insert back in the extra pitches
	for i in range(len(extraPitches)):
		if pitchesAtStart:
			n = int(np.absolute(np.random.normal(0, 1)))
			np.append(retval[0:n],extraPitches[i])
		else:
			n = len(retval)-int(np.absolute(np.random.normal(0,1)))
			np.append(retval[n:],extraPitches[i])
	return retval
	
	
# returns a list of equally-spaced integers from start to end of the specified length
def interpolateNumbers(start, end, length):
	delta = (end - start) / float(length)
	floatValues = np.arange(start, end, delta, dtype=float)
	return np.round(floatValues)
	
# assigns each pitch in pitches to an instrument such that it is as close to the center of that instrument's range
# returns an array containing arrays of pitches for each instrument
def orchestratePitches(pitches, instrumentRanges):
	retval = np.empty(len(instrumentRanges))
	remainingInstruments = range(len(instrumentRanges))
	for pitch in pitches:
		inst = remainingInstruments[np.random.randint(0, len(remainingInstruments))]
		r = instrumentRanges[inst]
		center = r[0] + (r[1]-r[0])//2
		offset = min(center%12 - pitch, pitch - center%12)
		retval[inst] = center+offset
	return retval
	
# takes a list of time locations and pitches, create a abjad representation with rests for the space in between notes
def turnToNotes(beatLocations, pitches):
	notes = [[],[],[],[]]
	# convert them all to the same denominator
	denom = np.max(beatLocations[:,1])
	for i in range(len(beatLocations)):
		if beatLocations[i,1] != denom:
			beatLocations[i,:] *= denom//beatLocations[i,1]
	# sort by numerator
	beatLocations = np.sort(beatLocations, axis=0)
	curr = 0 # counts through indices of beatLocations
	# loop through possible numerator values
	while i < beatLocations[-1,0]:
		# this shouldn't happen
		if i > beatLocations[curr,0]:
			curr += 1
			print("Error")
			continue
		# if there's no beatLocation there, add a rest to each staff
		elif i < beatLocations[curr,0]:
			for j in range(len(notes)):
				rest = Rest(Duration(1,1))
				restDenom = denom // lowerPowerOf2(beatLocations[curr,0]-i)
				rest = Rest(Duration(1, restDenom))
				notes[j].append(rest)
			i+= denom//restDenom
			continue
		# else add the corresponding pitch to each staff for the desired length
		elif i == beatLocations[curr,0]:
			for j in range(len(notes)):
				notes[j].append(Note(pitches[curr][j], Duration(1, denom)))
			curr += 1
			i+=1
			continue
	return notes
	
def lowerPowerOf2(n):
	x = 1
	while x < n:
		x = x*2
	return max(x//2,1)

def genStringQuartetOrchestratedEvents(startPitchset, endPitchset, length):
	# create instrumentation (with ranges)
	ranges = np.array([[0,0]]*4)
	# violin1
	s1 = []
	ranges[0] =[-5, 43]
	# violin2
	s2 = []
	ranges[1] = (-5, 43)
	# viola
	s3 = []
	ranges[2] = (-12, 37)
	# cello
	s4 = []
	ranges[3] = (-24, 24)
	# generate pitchsets
	pitchsets = incrementPitchset(startPitchset, endPitchset, length/2)
	# loop through them
	for i in range(len(pitchsets)):
		# choose number of events
		n = min(int(np.absolute(np.floor(np.random.normal(0, 3))+4)),8)
		if n == 0:
			continue
		# choose locations for events
		beatNumbers = np.random.choice(np.array(range(8)), n, replace=False)
		offsetpower = np.absolute(np.floor(np.random.normal(0, 1, size=(n))))
		beats = np.array([[0,0]]*n)
		beats[:,0] = beatNumbers*np.power(2, offsetpower) + 1
		beats[:,1] = np.power(2, offsetpower+2)
		# orchestrate a subset of the pitchset for each event
		pitches = np.array([[0,0,0,0]]*n)
		for j in range(n):
			pitches[j] = orchestratePitches(pitchsets[i],ranges)
		#add the pitches to each instrument
		notes = turnToNotes(beats, pitches)
		s1 = s1 + notes[0]
		s2 = s2 + notes[1]
		s3 = s3 + notes[2]
		s4 = s4 + notes[3]
	s = [s1,s2,s3,s4]
	# make sure the total duration is on a measure barrier (or else it fucks up tuplets)
	for j in range(len(s)):
		totalLength = 0
		for k in range(len(s[j])):
			totalLength += s[j][k].written_duration
		extraDuration = 0
		if totalLength % 1 != 0:
			extraDuration = Duration(1,1) - Duration(totalLength % 1)
			
			while extraDuration.numerator != 1:
				print(extraDuration)
				s[j].append(Rest(Duration(1,extraDuration.denominator)))
				extraDuration -= Duration(1,extraDuration.denominator)
			s[j].append(Rest(extraDuration))
			
	return s
	#play(Score([s1,s2,s3,s4]))
	
#main()
	
	
	
	
	
	
	
	
	
	
