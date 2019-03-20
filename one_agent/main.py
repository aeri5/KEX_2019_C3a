from warehouse import *
from q import *
import random
import time
import sys
import csv
import matplotlib.pyplot as plt

warehouseSize = [10, 10] #[coloumns, rows]
squareDim = 50 #pixels per square
w = Warehouse(warehouseSize, squareDim)
w.update()
qTable = QTable(warehouseSize[0]+2, warehouseSize[1]+2)
actionsDict = {0:"up", 1:"right", 2:"down", 3:"left", 4:"stay"}

try:

	dataLog = []
	episodes = 0
	goalsReached = 0
	while True:
		w.restart(0)
		episodes += 1
		oldState = w.getAgentCoords(0)

		while True:
			# print("state:", oldState)
			if random.uniform(0,1)<qTable.epsilon:
				action = random.randint(0, 4)
			else:
				action = qTable.findBestAction(oldState)
			w.moveAgent(0, action)
			nextState = w.getAgentCoords(0)

			collision, goalReached = w.collision(0)
			reward = w.reward(0)

			qTable.updateQTable(oldState, action, reward, nextState)

			if collision:
				if goalReached:
					outputStr = "Episode " + str(episodes) + ": Goal reached!"
					goalsReached += 1
				else:
					outputStr = "Episode " + str(episodes) + ": Collided by moving " + actionsDict[action] + " at coords " + str(oldState) + "."
				dataLog.append([str(episodes), str(goalsReached)])
				# print(outputStr)
				break

			oldState = nextState

		if episodes%10 == 0:
			qTable.updateEpsilon()
			print(str(qTable.epsilon))
			print(str(episodes), "episodes with ", str(goalsReached), "goals reached")

	w.mainloop()




	# for i in range(1,100001):
	# 	w.restart(0)
	# 	x_cord, y_cord = w.getAgentCoords(0)
	# 	state =[x_cord,y_cord]
	# 	epochs, penalty, reward = 0,0,0
	# 	done = False

	# 	while not done:  #Main loop
	# 		if random.uniform(0,1)<qTable.epsilon:
	# 			action = random.randint(0, 4)
	# 		else:
	# 			# print(state)
	# 			action = qTable.findBestAction(state)
	# 			if action > 4:
	# 				action = 4
	# 			#print("state:", state)
	# 			#print("action:", action)
	# 			#print(qTable.qTable)
	# 		w.moveAgent(0, action)
	# 		x_cord, y_cord = w.getAgentCoords(0)
	# 		next_state = [x_cord,y_cord]
	# 		reward = w.reward(0)
	# 		collision, goalReached = w.collision(0)

	# 		qTable.updateQTable(state, action, reward, next_state)

	# 		time.sleep(0.2)
			



	# 		if reward < - 40:
	# 			penalty += 1
	# 			print("suger ju")
	# 			break



	# 		state = next_state

	# 		epochs +=1

	# #qTable.updateEpsilon()
	# 		if i%100 == 0:
	# 			w.update()
	# 			print(qTable.qTable)


	# 	# 	if collision:
	# 	# 		w.restart(0)
	# 	# 		if goalReached:
	# 	# 			print("Goal reached")
	# 	# 		else:
	# 	# 			print("Restart")
	# 	# 	time.sleep(0.1)
	# 	# 	w.update()
	# w.mainloop()

except KeyboardInterrupt:
	with open('data.csv', 'w', newline='') as dataFile:
	    writer = csv.writer(dataFile)
	    writer.writerow("eg")
	    writer.writerows(dataLog)
	dataFile.close()	
	sys.exit(0)