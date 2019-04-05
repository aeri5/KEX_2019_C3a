import numpy as np
import random

class QTable():
	def __init__(self, tableWidth, tableHeight):
		self.tableWidth = tableWidth
		self.tableHeight = tableHeight
		self.qTable = np.zeros((tableWidth*tableHeight, 5))
		#print(self.qTable)
		self.gamma = 0.9
		self.alpha = 0.1

		self.epsilon = 0.9
		self.epsilonMin = 0.1

		# for i in range(0, tableHeight):
		# 	for j in range(0, tableWidth):
		# 		if i == 0:
		# 			self.qTable[self.stateToRowIndex([j, i]), 0] = -1000
		# 		if j == 0:
		# 			self.qTable[self.stateToRowIndex([j, i]), 3] = -1000
		# 		if j == tableWidth-1:
		# 			self.qTable[self.stateToRowIndex([j, i]), 1] = -1000
		# 		if i == tableHeight-1:
		# 			self.qTable[self.stateToRowIndex([j, i]), 2] = -1000

	def updateQTable(self, oldState, action, reward, nextState):
			nextMax = np.max(self.qTable[self.stateToRowIndex(nextState)])
			oldStateIndex = self.stateToRowIndex(oldState)
			self.qTable[oldStateIndex, action] = self.qTable[oldStateIndex,action] + self.alpha * ( reward + self.gamma * nextMax - self.qTable[oldStateIndex,action])
		# try:
		# 	nextMax = np.max(self.qTable[self.stateToRowIndex(nextState)])
		# 	self.qTable[oldState, action] = self.qTable[oldState,action] + self.alpha * ( reward + self.gamma * nextMax - self.qTable[oldState,action])
		# except IndexError:
			# print(nextState)
			# np.round(self.qTable, 4)
			# print(self.qTable)


	def findBestAction(self, state):
		bestAction = random.choice(np.argwhere(self.qTable[self.stateToRowIndex(state)] == np.max(self.qTable[self.stateToRowIndex(state)])).flatten().tolist()) #np.argmax(self.qTable[self.stateToRowIndex(state)])
		# print("bestAction:", bestAction)
		return bestAction

	def stateToRowIndex(self, state):
		rowIndex = state[1]*10 + state[0]
		return rowIndex

	def updateEpsilon(self):
		if self.epsilon > self.epsilonMin:
			self.epsilon = self.epsilon*0.95
