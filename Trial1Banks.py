# A trial to see if I can use Abjad to make music procedurally
# Takes rhythm and melody from banks of choices specified by me
# As of now, voices are written independently, this isn't a very sophisticated composition

from abjad import *
import sys
import random

rhythm = []
melody = []

def generateVoice(length):
	notes = []
	pitches = melody[random.randint(0, len(melody)-1)]
	rhythms = rhythm[random.randint(0, len(rhythm)-1)]
	j = 0
	k = 0
	i = 0.0
	while i < length:
		if j >= len(pitches):
			pitches = melody[random.randint(0, len(melody)-1)]
			j = 0
		if k >= len(rhythms):
			rhythms = rhythm[random.randint(0, len(rhythm)-1)]
			k = 0
		notes.append(Note(pitches[j], Duration(1, rhythms[k])))
		i += 1.0/(rhythms[k])
		j += 1
		k += 1
	return Staff(notes)

# args[1] is the number of voices
# args[2] is the length in bars
# args[3] is the bank of rhythms
# args[4] is the bank of melodies
def main():
	# parse rhythm bank
	rfile = open(sys.argv[3])
	for line in rfile:
		rhythm.append(map(int, line.split()))
	mfile = open(sys.argv[4])
	for line in mfile:
		melody.append(map(int, line.split()))
	instruments = []
	for i in range(int(sys.argv[1])):
		instruments.append(generateVoice(int(sys.argv[2])))
		
	score = Score(instruments)
	show(score)
	play(score)
	lilypond_file = lilypondfiletools.make_basic_lilypond_file(score)
	print(format(lilypond_file))
main()
