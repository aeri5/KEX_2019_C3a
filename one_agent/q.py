import numpy as np
import random

class QTable():
	def __init__(self, tableWidth, tableHeight):
		self.qTable = np.zeros((tableWidth*tableHeight, 5))
		#print(self.qTable)
		self.gamma = 0.9
		self.alpha = 0.1

		self.epsilon = 0.9
		self.epsilonMax = 1.0
		self.epsilonMin = 0.1

	def updateQTable(self, oldState, action, reward, nextState):
		nextMax = np.max(self.qTable[self.stateToRowIndex(nextState)])
		self.qTable[oldState, action] = self.qTable[oldState,action] + self.alpha * ( reward + self.gamma * nextMax - self.qTable[oldState,action])


	def findBestAction(self, state):
		bestAction = np.argmax(self.qTable[self.stateToRowIndex(state)])
		# print("bestAction:", bestAction)
		return bestAction

	def stateToRowIndex(self, state):
		return state[1]*10 + state[0]

	def updateEpsilon(self):
		if self.epsilon > self.epsilonMin:
			self.epsilon = self.epsilon*0.95
states = 100
