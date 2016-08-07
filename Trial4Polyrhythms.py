# Trial4Polyrhythms.py
# Mostly just for me to figure out how to do more complicated things with Abjad containers

# Read in a melody, a rhythm and a ratio between four numbers and orchestrate it for four voices with different meters according to that ratio

# takes in a list of numbers, returns a list of lambda expressions that convert a list of notes in 4/4 to durations in that ratio (for instance, 3:4 would return a function that converts three quarter notes into a half note triplet, etc. and an identity function)
import math
from abjad import *

def solveRatio(ratios):
	functions = []
	for i in range(len(ratios)):
		if not isPowerOf2(ratios[i]):
			def f(vals):
				tuplets = []
				j = 0
				while j < len(vals):
					tuplets.append(Tuplet(Multiplier(ratios[i], 8), vals[j:min(j+ratios[i],len(vals))]))
					j = min(j+ratios[i],len(vals))
				return tuplets
			functions.append(f)
		else:
			def f(vals):
				notes = []
				for j in range(len(vals)):
					notes.append(Note(vals[j].written_pitch,vals[j].written_duration *(ratios[i]/4)))
				return notes
			functions.append(f)
	return functions
	
				
def isPowerOf2(n):
	return math.log(n, 2) % 1.0 == 0
	
def main():
	notes = [Note("c'4"), Note("d'2"), Note("e'8"), Note("f'8"), Note("g'2")]
	functions = solveRatio([3])
	s1 = Staff(functions[0](notes))
	show(s1)
	print(s1)
	return s1
	#s2 = Staff(functions[1](notes))
	#show(s2)
	#print(s2)
	#s3 = Staff(functions[2](notes)[0])
	#show(s3)
	#print(s3)
	#s = Score([s1,s2,s3])
	#show(s)

s1 = main()



