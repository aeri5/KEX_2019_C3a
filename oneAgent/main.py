from warehouse import *
from q import *
from deepQ import *
import random
import time
import sys
import csv

warehouseSize = [4,4] #[coloumns, rows]
squareDim = 50 #pixels per square
w = Warehouse(warehouseSize, squareDim)
w.update()
dqn = dqn()
actionsDict = {0:"up", 1:"right", 2:"down", 3:"left", 4:"stay"}
batchSize = 128
tatalReward = 0

try:
	dataLog = []
	episodes = 0
	goalsReached = 0
	while True:
		w.restart(0)
		episodes += 1
		totalReward = 0
		oldState = w.getAgentCoords(0)

		while True:
			

			if episodes % 1000 == 0:
				print("innan:", w.getAgentCoords(0))
				action = dqn.pickAction(oldState)
				print("action:", actionsDict[action])
				nextState = w.nextCoords(0, action)				
				print("efter:", nextState)
				w.update()
				time.sleep(0.1)

			else:				
				action = dqn.pickAction(oldState)
				nextState = w.nextCoords(0, action)

			collision, goalReached, reward = w.collision(0, nextState)
			totalReward += reward

			dqn.remember(oldState, action, nextState, collision, goalReached, reward)

			dataLog.append([str(episodes), str(totalReward)])

			if not collision:
				oldState = nextState
				w.moveAgent(0, action)
				if goalReached:
					goalsReached += 1
					break

		if len(dqn.memory) > batchSize:
			dqn.replay(batchSize)

		
		dqn.updateEpsilon()

		if episodes % 1 == 0:
			print("epsilon:", dqn.epsilon)
			print(str(episodes), "episodes with the latest reward of", str(totalReward), "\n")

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