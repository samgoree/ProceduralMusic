# Trial5_2.py

from Trial5_1 import *
from Trial3Orchestration import *
import copy


pitches = np.array([0, 10, 2, 8, 4, 6])
endPitches = np.array([11, 9, 7, 5, 3, 1])
#pitches[:] -=12
rhythms = np.array([[Duration(1,4)],[Duration(1,4)], [Duration(1,4)], [Duration(1,2)]])
# made edit so that s is an array
s = generateStringQuartet(pitches, rhythms, [3, 5, 7, 2])
stuplets = []
stuplets.append(applyTuplets(s[0], Multiplier(3, 2)))
stuplets.append(applyTuplets(s[1], Multiplier(5,2)))
stuplets.append(applyTuplets(s[2], Multiplier(7,2)))
stuplets.append(s[3])#applyTuplets(s[3], Multiplier(1,1)))
s2 = genStringQuartetOrchestratedEvents(pitches, endPitches, 16)

#TODO this isn't working, test s2

rhythms = np.array([[Duration(1,4)],[Duration(1,4)], [Duration(1,4)], [Duration(1,2)]])
s3 = generateStringQuartet(endPitches, rhythms, [7, 5, 3, 2])
s3tuplets = []
s3tuplets.append(applyTuplets(s3[0], Multiplier(7,2)))
s3tuplets.append(applyTuplets(s3[1], Multiplier(5,2)))
s3tuplets.append(applyTuplets(s3[2], Multiplier(3,2)))
s3tuplets.append(s3[3])


sc = []
for i in range(4):
	#print(s[i])
	#print(s2[i])
	sc.append(Staff(stuplets[i] + s2[i] + s3tuplets[i]))

		
attach(Clef('alto'), sc[2])
attach(Clef('bass'), sc[3])
#show(s[0])
#show(s[1])
#show(s[2])
sc = Score(sc[:])
#play(sc)
show(sc)

