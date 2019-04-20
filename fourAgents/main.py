from warehouse import *
from deepQ import *
import random
import time
import sys
import csv

numberOfAgents = 1
warehouseSize = [4,4] #[coloumns, rows]
squareDim = 50 #pixels per square
w = Warehouse(warehouseSize, squareDim)
w.update()
dqn = [dqn() for n in range(numberOfAgents)]
actionsDict = {0:"up", 1:"right", 2:"down", 3:"left", 4:"stay"}

dataLog = []
episodes = 0
oldState = [[0,0] for i in range(numberOfAgents)]
nextState = [[0,0] for i in range(numberOfAgents)]
totalReward = [0 for i in range(numberOfAgents)]
batchSize = 500

def doStep(index):
	global episodes, oldState, nextState, totalReward
	agentsCloseBy = w.agentsCloseBy(index, oldState[index])

	action = dqn[index].pickAction(oldState[index], agentsCloseBy)

	nextState[index] = w.nextCoords(index, action)
	agentsCloseBy2 = w.agentsCloseBy(index, nextState[index])

	collision, goalReached, reward = w.collision(index, nextState[index])
	totalReward[index] += reward

	dqn[index].remember(oldState[index], action, agentsCloseBy, agentsCloseBy2, reward, nextState[index], collision, goalReached)

	if len(dqn[index].memory) > batchSize:
		dqn[index].replay(batchSize)

	if not collision:
		oldState[index] = nextState[index]
		w.moveAgent(index, action)
		# if episodes%10==0:
		# 	time.sleep(0.1)
		# 	w.update()

	return collision, goalReached

try:
	while True:
		episodes += 1
		coll = [False for i in range(numberOfAgents)]
		goal = [False for i in range(numberOfAgents)]
		for i in range(numberOfAgents):
			w.restart(i)
			oldState[i] = w.getAgentCoords(i)
			totalReward[i] = 0

		while True:
			for i in range(numberOfAgents):
				if not (coll[i] or goal[i]):
					coll[i], goal[i] = doStep(i)

			if all(bool == True for bool in goal):		#All agents reached their goals
				break
			elif all(bool == True for bool in coll):	#All agents have collided
				break
			elif all(item == True for item in [True if any(collOrGoal == True for collOrGoal in [coll[i], goal[i]]) else False for i in range(numberOfAgents)]):					  #All agents have either collided or reached their goals
				break

		for network in dqn:
			network.updateEpsilon()

		if episodes%10 == 0:
			print("epsilon: ", round(dqn[0].epsilon, 4))
			print(str(episodes), ":th episode with a total accumulated reward of", str(sum(totalReward)))
			print("Goals reached: \t", "\t".join([str(g) for g in goal]))
			print("Collisions: \t", "\t".join([str(c) for c in coll]), "\n")

		dataLog.append([str(episodes), str(sum(totalReward))])

	w.mainloop()

except KeyboardInterrupt:
		with open('data.csv', 'w', newline='') as dataFile:
		    writer = csv.writer(dataFile)
		    writer.writerow("er")
		    writer.writerows(dataLog)
		dataFile.close()	
		# np.round(qTable.qTable, 4)
		# print(qTable.qTable)
		sys.exit(0)