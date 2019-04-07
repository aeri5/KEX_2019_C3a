import tkinter
from agent import *

obstacleCoords = [] #[[x, y], [x, y], ...]
obstacles = []
agentCoords = [[0,3], [0,0]] #[[x, y], [x, y], ...] (agent start locations)
agents = []
goalCoords = [[3, 0], [3,3]]
goals = []

class Warehouse(tkinter.Tk, object):
	def __init__(self, warehouseSize, squareDim):
		super(Warehouse, self).__init__()
		self.warehouseSize = warehouseSize
		self.squareDim = squareDim
		self.windowSize = [self.squareDim*self.warehouseSize[0], self.squareDim*self.warehouseSize[1]] #[width, height]
		self.title("Warehouse sim with one agent")
		self.canvas = tkinter.Canvas(self, bg="#b7b7b7", width = self.windowSize[0], height = self.windowSize[1])
		
		#draw grid
		for i in range(1, int(self.windowSize[0]/self.squareDim)): #vertical lines
			self.canvas.create_line(i*self.squareDim, 0, i*self.squareDim, self.windowSize[1], fill="#444444")
		for i in range(1, int(self.windowSize[1]/self.squareDim)): #horizontal lines
			self.canvas.create_line(0, i*self.squareDim, self.windowSize[0], i*self.squareDim, fill="#444444")

		#init shelves
		for obstacle in obstacleCoords:
			obstacles.append(self.canvas.create_rectangle(obstacle[0]*self.squareDim+1, obstacle[1]*self.squareDim+1, (obstacle[0]+1)*self.squareDim-1, (obstacle[1]+1)*self.squareDim-1, fill="#444444", outline="#444444"))

		#init goal
		goals.append(self.canvas.create_rectangle(goalCoords[0][0]*self.squareDim+1, goalCoords[0][1]*self.squareDim+1, (goalCoords[0][0]+1)*self.squareDim-1, (goalCoords[0][1]+1)*self.squareDim-1, fill="#db3b23", outline="#db3b23", tags="goal0"))
		goals.append(self.canvas.create_rectangle(goalCoords[1][0]*self.squareDim+1, goalCoords[1][1]*self.squareDim+1, (goalCoords[1][0]+1)*self.squareDim-1, (goalCoords[1][1]+1)*self.squareDim-1, fill="#2455b7", outline="#2455b7", tags="goal1"))	

		#init agent
		agents.append(Agent(agentCoords[0][0], agentCoords[0][1], self.canvas.create_rectangle(agentCoords[0][0]*self.squareDim+1, agentCoords[0][1]*self.squareDim+1, (agentCoords[0][0]+1)*self.squareDim-1, (agentCoords[0][1]+1)*self.squareDim-1, fill="#eda061", outline="#eda061", tags="agent0")))			
		agents.append(Agent(agentCoords[1][0], agentCoords[1][1], self.canvas.create_rectangle(agentCoords[1][0]*self.squareDim+1, agentCoords[1][1]*self.squareDim+1, (agentCoords[1][0]+1)*self.squareDim-1, (agentCoords[1][1]+1)*self.squareDim-1, fill="#91cbf7", outline="#91cbf7", tags="agent1")))


		self.canvas.pack()

	def moveAgent(self, index, action):
		if action == 0:
			self.canvas.move(agents[index].tkID, 0, -self.squareDim)
			agents[index].y = agents[index].y - 1
		elif action == 1:
			self.canvas.move(agents[index].tkID, self.squareDim, 0)
			agents[index].x = agents[index].x + 1
		elif action == 2:
			self.canvas.move(agents[index].tkID, 0, self.squareDim)
			agents[index].y = agents[index].y + 1
		elif action == 3:
			self.canvas.move(agents[index].tkID, -self.squareDim, 0)
			agents[index].x = agents[index].x - 1
		elif action == 4:
			self.canvas.move(agents[index].tkID, 0, 0)
		else:
			raise ValueError("Incorrect movement")
		# print(agents[index].x, "x", agents[index].y)

	def restart(self, index):
		agents[index].x = agentCoords[index][0]
		agents[index].y = agentCoords[index][1]
		self.canvas.coords(agents[index].tkID, agentCoords[index][0]*self.squareDim+1, agentCoords[index][1]*self.squareDim+1, (agentCoords[index][0]+1)*self.squareDim-1, (agentCoords[index][1]+1)*self.squareDim-1)
		# print("restart")

	def collision(self, index):
		if ([agents[index].x, agents[index].y] in obstacleCoords) or ([agents[index].x, agents[index].y] == [agents[(index+1)%2].x, agents[(index+1)%2].y]) or (agents[index].x < 0 or agents[index].x > self.warehouseSize[0]-1 or agents[index].y < 0 or agents[index].y > self.warehouseSize[1]-1): #Agent collided with obstacle, wall, or another agent
			return True, False
		elif [agents[index].x, agents[index].y] == goalCoords[index]:	#Agent reached its goal
			return False, True
		else:	#No collision and goal not reached
			return False, False

	def reward(self, index):
		reward = -1
		collision, goalReached = self.collision(index)
		if collision:
				reward = -50		
		elif goalReached:
				reward = 50

		return reward

	def getAgentCoords(self, index):
		return [agents[index].x, agents[index].y]

