import numpy as np
import random

gamma = 0.9
alpha = 0.1

epsilon = 0.9
epsilonMax = 1.0
epsilonMin = 0.1
decayRate = 0.01

allEpochs = []
allPenalties = []
penalties = 0

class QTable():
	def __init__(self):
		self.qTable = np.zeros([100, 5])
		#print(self.qTable)
		self.gamma = 0.9
		self.alpha = 0.1

		self.epsilon = 0.1
		self.epsilonMax = 1.0
		self.epsilonMin = 0.1
		self.decayRate = 0.01

		self.allEpochs = []
		self.allPenalties = []
		self.penalties = 0

	def updateQTable(self, state, action, reward, next_state):
		next_max = np.max(self.qTable[next_state])

		self.qTable[state, action] = self.qTable[state,action] + self.alpha * ( reward + self.gamma * next_max - self.qTable[state,action])



	def updateEpsilon(self):
		self.epsilon = self.epsilonMin + (self.epsilonMax-self.epsilonMin)*np.exp(-0.1*self.epsilon)
states = 100
