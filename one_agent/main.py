from warehouse import *
from q import *
import random
import time
import sys

w = Warehouse()
w.update()
qTable = QTable()

try:
	for i in range(1,100001):
		w.restart(0)
		x_cord, y_cord = w.getAgentCoords(0)
		state =[x_cord,y_cord]
		epochs, penalty, reward = 0,0,0
		done = False
		while not done:  #Main loop
			if random.uniform(0,1)<qTable.epsilon:
				action = random.randint(0, 4)
				#print("random")
				#print("state:", state)
				#print("action_random:", action)
			else:
				# print(state)
				action = np.argmax(qTable.qTable[state])
				if action > 4:
					action = 4
				#print("state:", state)
				#print("action:", action)
				#print(qTable.qTable)
			w.moveAgent(0, action)
			x_cord, y_cord = w.getAgentCoords(0)
			next_state = [x_cord,y_cord]
			reward = w.reward(0)
			collision, goalReached = w.collision(0)

			qTable.updateQTable(state, action, reward, next_state)

			time.sleep(0.2)
			



			if reward < - 40:
				penalty += 1
				print("suger ju")
				break



			state = next_state

			epochs +=1

	#qTable.updateEpsilon()
			if i%100 == 0:
				w.update()
				print(qTable.qTable)


		# 	if collision:
		# 		w.restart(0)
		# 		if goalReached:
		# 			print("Goal reached")
		# 		else:
		# 			print("Restart")
		# 	time.sleep(0.1)
		# 	w.update()
	w.mainloop()

except KeyboardInterrupt:
	sys.exit(0)