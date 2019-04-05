from warehouse import *
from q import *
from deepQ import *
import random
import time
import sys
import csv

warehouseSize = [4, 4] #[coloumns, rows]
squareDim = 50 #pixels per square
w = Warehouse(warehouseSize, squareDim)
w.update()
dqn = dqn()
actionsDict = {0:"up", 1:"right", 2:"down", 3:"left", 4:"stay"}
batchSize = 32

try:
	dataLog = []
	episodes = 0
	goalsReached = 0

	while True:
		w.restart(0)
		episodes += 1
		oldState = w.getAgentCoords(0)
		totalReward = 0

		while True:
			

			if episodes % 25 == 0:
				print("innan:", w.getAgentCoords(0))
				action = dqn.pickAction(oldState)
				print("action:", actionsDict[action])
				w.moveAgent(0, action)
				print("efter:", w.getAgentCoords(0))
				w.update()
				time.sleep(0.1)

			else:				
				action = dqn.pickAction(oldState)
				w.moveAgent(0, action)

			nextState = w.getAgentCoords(0)

			collision, goalReached = w.collision(0)
			reward = w.reward(0)
			totalReward += reward

			dqn.remember(oldState, action, reward, nextState, collision, goalReached)

			# qTable.updateQTable(oldState, action, reward, nextState)
			# print(oldState)

			if collision:
				if goalReached:
					outputStr = "Episode " + str(episodes) + ": Goal reached!"
					goalsReached += 1
				else:
					outputStr = "Episode " + str(episodes) + ": Collided by moving " + actionsDict[action] + " at coords " + str(oldState) + "."
<<<<<<< HEAD
				dataLog.append([str(episodes), str(goalsReached)])
				# print(outputStr, "\n")
=======
				dataLog.append([str(episodes), str(totalReward)])
				# print(outputStr)
>>>>>>> 0069383b58f7c69a54d1dec009a8f260cc382eda
				break

			oldState = nextState

<<<<<<< HEAD
			if len(dqn.memory) > batchSize:
				dqn.replay(batchSize)
=======
		if episodes%10 == 0:
			qTable.updateEpsilon()
			print(str(qTable.epsilon))
			print(str(episodes), "episodes with a total reward of", str(totalReward))

		# if episodes%250 == 0:
		# 	w.restart(0)
		# 	episodes += 1
		# 	oldState = w.getAgentCoords(0)

		# 	while True:
		# 		time.sleep(0.1)
		# 		while True:
		# 			if random.uniform(0,1)<qTable.epsilon:
		# 				action = random.randint(0, 4)
		# 			else:
		# 				action = qTable.findBestAction(oldState)
		# 			if (oldState[0] == 0 and action == 3) or (oldState[1] == 0 and action == 0) or (oldState[0] == warehouseSize[0]-1 and action == 1) or (oldState[1] == warehouseSize[1]-1 and action == 2):
		# 				continue
		# 			else:
		# 				break

		# 		w.moveAgent(0, action)
		# 		w.update()
		# 		nextState = w.getAgentCoords(0)

		# 		collision, goalReached = w.collision(0)
		# 		reward = w.reward(0)

		# 		qTable.updateQTable(oldState, action, reward, nextState)
		# 		# print(oldState)

		# 		if collision:
		# 			if goalReached:
		# 				outputStr = "Episode " + str(episodes) + ": Goal reached!"
		# 				goalsReached += 1
		# 			else:
		# 				outputStr = "Episode " + str(episodes) + ": Collided by moving " + actionsDict[action] + " at coords " + str(oldState) + "."
		# 			dataLog.append([str(episodes), str(goalsReached)])
		# 			# print(outputStr)
		# 			break

		# 		oldState = nextState

>>>>>>> 0069383b58f7c69a54d1dec009a8f260cc382eda

		if episodes % 25 == 0:
			print("epsilon:", dqn.epsilon)
			print(str(episodes), "episodes with ", str(round(100*goalsReached/episodes)), "% of goals reached in total.")

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