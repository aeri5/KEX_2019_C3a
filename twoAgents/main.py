from warehouse import *
from deepQ import *
from q import *
import random
import time
import sys
import csv

warehouseSize = [4, 4] #[coloumns, rows]
squareDim = 50 #pixels per square
w = Warehouse(warehouseSize, squareDim)
w.update()
dqn = [dqn(), dqn()]
actionsDict = {0:"up", 1:"right", 2:"down", 3:"left", 4:"stay"}

dataLog = []
episodes = 0
goalsReached = 0
oldState = [[0,9], [0,0]]
nextState = [[0,0], [0,0]]
totalReward = [0, 0]
batchSize = 64

def doStep(index):
	global episodes, goalsReached, oldState, nextState, totalReward
	agentCloseBy = w.agentCloseBy(index, oldState[index])

	action = dqn[index].pickAction(oldState[index], agentCloseBy)

	nextState[index] = w.nextCoords(index, action)
	agentCloseBy2 = w.agentCloseBy(index, nextState[index])

	collision, goalReached, reward = w.collision(index, nextState[index])
	totalReward[index] += reward

	dqn[index].remember(oldState[index], action, agentCloseBy, agentCloseBy2, reward, nextState[index], collision, goalReached)

	if len(dqn[index].memory) > batchSize:
		dqn[index].replay(batchSize)

	if not collision:
		oldState[index] = nextState[index]
		w.moveAgent(index, action)
		# if episodes%1==0:
		# 	time.sleep(0.1)
		# 	w.update()

	return collision, goalReached

try:
	while True:
		w.restart(0)
		w.restart(1)
		episodes += 1
		oldState[0] = w.getAgentCoords(0)
		oldState[1] = w.getAgentCoords(1)
		totalReward = [0, 0]
		goal0 = False
		goal1 = False
		coll0 = False
		coll1 = False

		while True:
			# print("goal 0:", goal0, "goal1:", goal1, "coll0:", coll0, "coll1", coll1)
			# print("goal 0:", goal0, "   goal1:", goal1, "         coll0:", coll0, "   coll1:", coll1, "\n")
			if not goal0:
				coll0, goal0 = doStep(0)
			if not goal1:
				coll1, goal1 = doStep(1)
			if goal0 and goal1:
				goalsReached += 1
				break
			elif (coll0 and coll1) or (coll0 and goal1) or (coll1 and goal0):
				break
		
		for network in dqn:
			network.updateEpsilon()

		if episodes%1 == 0:
			print("epsilon: ", round(dqn[0].epsilon, 4), round(dqn[1].epsilon, 4))
			print(str(episodes), ":th episode with a collective accumulated reward of", str(totalReward[0] + totalReward[1]))
			print("goal 0:", goal0, "   goal1:", goal1, "         coll0:", coll0, "   coll1:", coll1, "\n")

	w.mainloop()

except KeyboardInterrupt:
		with open('data.csv', 'w', newline='') as dataFile:
		    writer = csv.writer(dataFile)
		    writer.writerow("err")
		    writer.writerows(dataLog)
		dataFile.close()	
		# np.round(qTable.qTable, 4)
		# print(qTable.qTable)
		sys.exit(0)









