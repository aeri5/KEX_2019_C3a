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
		self.model.add(Dense(24, input_dim=2, activation='relu'))
		self.model.add(Dense(24, activation='relu'))
		self.model.add(Dense(5, activation='linear'))
		self.model.compile(loss='mse', optimizer=Adam(lr=self.alpha))


	def pickAction(self, state):
		global sess
		if np.random.rand() <= self.epsilon:
			randAction = randint(0, 4)
			return randAction
		else:
			actions = self.model.predict(np.reshape(np.asarray(state), [1, 2]))
			return np.argmax(actions[0])


	def remember(self, state, action, reward, nextState, collision, goalReached):
		self.memory.append([state, action, reward, nextState, collision, goalReached])


	def replay(self, batchSize):
		miniBatch = sample(self.memory, batchSize)

		for state, action, reward, nextState, collision, goalReached in miniBatch:
			target = reward
			if not (collision or goalReached):
			  target = reward + self.gamma * np.amax(self.model.predict(np.reshape(np.asarray(nextState), [1, 2]))[0])
			targetF = self.model.predict(np.reshape(np.asarray(state), [1, 2]))
			targetF[0][action] = target

			self.model.fit(np.reshape(np.asarray(state), [1, 2]), targetF, epochs=1, verbose=0)

		if self.epsilon > self.epsilonMin:
			self.epsilon *= self.epsilonDecay



	def stateToRowIndex(self, state):
		rowIndex = state[1]*10 + state[0]
		return rowIndex