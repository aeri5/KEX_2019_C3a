import numpy
import random

class QTable():
	def __init__(self):
		self.qTable = numpy.zeros([100, len(actions)])

actions = ["up", "right", "down", "left", "stay"]
states = 100

gamma = 0.9
alpha = 0.1

epsilon = 0.1
epsilonMax = 1.0
epsilonMin = 0.1
decayRate = 0.01

allEpochs = []
allPenalties = []
penalties = 0