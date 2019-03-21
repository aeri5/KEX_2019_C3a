from warehouse import *
from q import *
import random
import time
import sys
import csv

warehouseSize = [10, 10] #[coloumns, rows]
squareDim = 50 #pixels per square
w = Warehouse(warehouseSize, squareDim)
w.update()
qTables = [QTable(warehouseSize[0], warehouseSize[1]), QTable(warehouseSize[0], warehouseSize[1])]
actionsDict = {0:"up", 1:"right", 2:"down", 3:"left", 4:"stay"}

dataLog = []
episodes = 0
goalsReached = 0
oldState = [[0,9], [0,0]]
nextState = [[0,0], [0,0]]

def doStep(index):
	global episodes, goalsReached, oldState, nextState
	if episodes%250 == 0:
		time.sleep(0.05)
	while True:
		if random.uniform(0,1)<qTables[index].epsilon:
			action = random.randint(0, 4)
		else:
			action = qTables[index].findBestAction(oldState[index])
		if (oldState[index][0] == 0 and action == 3) or (oldState[index][1] == 0 and action == 0) or (oldState[index][0] == warehouseSize[0]-1 and action == 1) or (oldState[index][1] == warehouseSize[1]-1 and action == 2):
			continue
		else:
			break

	w.moveAgent(index, action)
	if episodes%250 == 0:
		w.update()
	nextState[index] = w.getAgentCoords(index)

	collision, goalReached = w.collision(index)
	reward = w.reward(index)

	qTables[index].updateQTable(oldState[index], action, reward, nextState[index])
	# print(oldState)

	if collision:
		if goalReached:
			outputStr = "Episode " + str(episodes) + ": Goal reached!"
			goalsReached += 1
		else:
			outputStr = "Episode " + str(episodes) + ": Collided by moving " + actionsDict[action] + " at coords " + str(oldState[index]) + "."
		dataLog.append([str(episodes), str(goalsReached)])
		# print(outputStr) 

	oldState[index] = nextState[index]



	return collision, goalReached

try:
	while True:
		w.restart(0)
		w.restart(1)
		episodes += 1
		oldState[0] = w.getAgentCoords(0)
		oldState[1] = w.getAgentCoords(1)

		goal0 = False
		goal1 = False
		while True:
			if not goal0:
				coll0, goal0 = doStep(0)
			if not goal1:
				coll1, goal1 = doStep(1)
			if coll0 or coll1:
				break

		if episodes%10 == 0:
			for qTable in qTables:
				qTable.updateEpsilon()
			print(str(episodes), "episodes with ", str(round(100*goalsReached/episodes)), "% of goals reached in total.")

	w.mainloop()

except KeyboardInterrupt:
		with open('data.csv', 'w', newline='') as dataFile:
		    writer = csv.writer(dataFile)
		    writer.writerow("eg")
		    writer.writerows(dataLog)
		dataFile.close()	
		# np.round(qTable.qTable, 4)
		# print(qTable.qTable)
		sys.exit(0)









