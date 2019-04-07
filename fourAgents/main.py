from warehouse import *
from deepQ import *
from q import *
import random
import time
import sys
import csv

warehouseSize = [5, 5] #[coloumns, rows]
squareDim = 50 #pixels per square
w = Warehouse(warehouseSize, squareDim)
w.update()
dqn = [dqn(), dqn(), dqn(), dqn()]
actionsDict = {0:"up", 1:"right", 2:"down", 3:"left", 4:"stay"}

dataLog = []
episodes = 0
goalsReached = 0
oldState = [[0,4], [0,0], [4,1], [4,3]]
nextState = [[0,0], [0,0], [0,0], [0,0]]
totalReward = [0, 0, 0, 0]
batchSize = 128

def doStep(index):
	global episodes, goalsReached, oldState, nextState, totalReward

	if episodes%50 == 0:
		time.sleep(0.05)

	action = dqn[index].pickAction(oldState[index])
	# print("Agent:", index, " in state:", oldState[index], " makes action:", actionsDict[action])
	w.moveAgent(index, action)


	if episodes%50 == 0:
		w.update()

	nextState[index] = w.getAgentCoords(index)

	collision, goalReached = w.collision(index)
	reward = w.reward(index)
	totalReward[index] += reward

	dqn[index].remember(oldState[index], action, reward, nextState[index], collision, goalReached)

	# if collision or goalReached:
	# 	if goalReached:
	# 		outputStr = "Episode " + str(episodes) + ": Goal reached!"
	# 		goalsReached += 1
	# 	else:
	# 		outputStr = "Episode " + str(episodes) + ": Collided by moving " + actionsDict[action] + " at coords " + str(oldState[index]) + "."
	# 	dataLog.append([str(episodes), str(goalsReached)])
	#	print(outputStr) 

	oldState[index] = nextState[index]

	if len(dqn[index].memory) > batchSize:
		dqn[index].replay(batchSize)

	return collision, goalReached

try:
	while True:
		for i in range(0, len(oldState)):
			w.restart(i)
			oldState[i] = w.getAgentCoords(i)

		episodes += 1
		totalReward = [0, 0, 0, 0]
		goalReached = [False, False, False, False]
		collision = [False, False, False, False]

		while True:
			for i in range(0, len(goalReached)):
				if not goalReached[i]:
					collision[i], goalReached[i] = doStep(i)
			if all(goal == True for goal in goalReached):
				goalsReached += 1
				break
			elif any(coll == True for coll in collision):
				break


		# while True:
		# 	# print("goal 0:", goal0, "goal1:", goal1, "coll0:", coll0, "coll1", coll1)
		# 	# print("goal 0:", goal0, "   goal1:", goal1, "         coll0:", coll0, "   coll1:", coll1, "\n")
		# 	if not goal0:
		# 		coll0, goal0 = doStep(0)
		# 	if not goal1:
		# 		coll1, goal1 = doStep(1)
		# 	if (goal0 and goal1):
		# 		goalsReached += 1
		# 		break
		# 	elif coll0 or coll1:
		# 		break

		# dataLog.append([str(episodes), str(totalReward[0]), str(totalReward[1])])
		if episodes % 5 == 0:
			for network in dqn:
				network.updateEpsilon()

		if episodes%25 == 0:
			print(str(episodes), ":th episode with", str(round(100*goalsReached/episodes)), "% of goals reached in total.")
			print("Rewards: \t", totalReward[0], "\t", totalReward[1], "\t", totalReward[2], "\t", totalReward[3])
			print("Goal reached: \t", goalReached[0], "\t", goalReached[1], "\t", goalReached[2], "\t", goalReached[3],)
			print("Collison: \t", collision[0], "\t", collision[1], "\t", collision[2], "\t", collision[3])
			print("Epsilon: \t", round(dqn[0].epsilon, 4), "\n")

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









