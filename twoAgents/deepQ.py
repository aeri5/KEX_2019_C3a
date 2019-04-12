import numpy as np
import keras
from random import randint, sample
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
import tensorflow as tf

sess = tf.InteractiveSession()

class dqn():
	def __init__(self):

		self.gamma = 0.95
		self.alpha = 0.001
		self.epsilon = 1.0
		self.epsilonMin = 0.01
		self.epsilonDecay = 0.995

		self.memory = deque(maxlen = 2000)

		self.model = Sequential()

		self.model.add(Dense(24, input_dim=3, activation='relu'))
		self.model.add(Dense(24, activation='relu'))
		self.model.add(Dense(5, activation='linear'))
		self.model.compile(loss='mse', optimizer=Adam(lr=self.alpha))


	def pickAction(self, state, agentCloseBy):
		global sess
		if np.random.rand() <= self.epsilon:
			randAction = randint(0, 4)
			return randAction
		else:
			actions = self.model.predict(np.reshape(np.asarray(state+[agentCloseBy]), [1, 3]))
			return np.argmax(actions[0])


	def remember(self, state, action, agentCloseBy, agentCloseBy2, reward, nextState, collision, goalReached):
		self.memory.append([state, action, agentCloseBy, agentCloseBy2, reward, nextState, collision, goalReached])


	def replay(self, batchSize):
		miniBatch = sample(self.memory, batchSize)

		for state, action, agentCloseBy, agentCloseBy2, reward, nextState, collision, goalReached in miniBatch:
			target = reward
			if not (collision or goalReached):
				networkInputNext = nextState + [agentCloseBy2]
				target = reward + self.gamma * np.amax(self.model.predict(np.reshape(np.asarray(networkInputNext), [1, 3]))[0])
			networkInput = state + [agentCloseBy]
			targetF = self.model.predict(np.reshape(np.asarray(networkInput), [1, 3]))
			targetF[0][action] = target

			self.model.fit(np.reshape(np.asarray(networkInput), [1, 3]), targetF, epochs=1, verbose=0)


	def updateEpsilon(self):
		if self.epsilon > self.epsilonMin:
			self.epsilon *= self.epsilonDecay