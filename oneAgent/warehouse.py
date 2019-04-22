import tkinter
from agent import *

obstacleCoords = [] #[[2,2], [3,2], [4,2], [5,2], [7,2], [7,3], [7,4], [3,4], [4,4], [5,4]] #[[x, y], [x, y], ...]
obstacles = []
agentCoords = [[0,3]] #[[x, y], [x, y], ...] (agent start locations)
agents = []
goalCoords = [[3, 0]]
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
		if len(obstacleCoords) > 0:
			for obstacle in obstacleCoords:
				obstacles.append(self.canvas.create_rectangle(obstacle[0]*self.squareDim+1, obstacle[1]*self.squareDim+1, (obstacle[0]+1)*self.squareDim-1, (obstacle[1]+1)*self.squareDim-1, fill="#444444", outline="#444444"))

		#init agent
		agentCounter = 0
		for agent in agentCoords:
			agents.append(Agent(agent[0], agent[1], self.canvas.create_rectangle(agent[0]*self.squareDim+1, agent[1]*self.squareDim+1, (agent[0]+1)*self.squareDim-1, (agent[1]+1)*self.squareDim-1, fill="#eda061", outline="#eda061", tags=str(agentCounter))))
			agentCounter += 1


		#init goal
		for goal in goalCoords:
			goals.append(self.canvas.create_rectangle(goal[0]*self.squareDim+1, goal[1]*self.squareDim+1, (goal[0]+1)*self.squareDim-1, (goal[1]+1)*self.squareDim-1, fill="#a8e298", outline="#a8e298"))	

		self.canvas.pack()

	def nextCoords(self, index, action):
		nextCoords = self.getAgentCoords(index)
		if action == 0:
			nextCoords[1] -= 1
		elif action == 1:
			nextCoords[0] += 1
		elif action == 2:
			nextCoords[1] += 1
		elif action == 3:
			nextCoords[0] -= 1
		elif action == 4:
			nextCoords = nextCoords
		else:
			raise ValueError("Incorrect movement")
		return nextCoords

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

	def collision(self, index, coords):
		if coords in obstacleCoords or coords[0] < 0 or coords[0] > self.warehouseSize[0]-1 or coords[1] < 0 or coords[1] > self.warehouseSize[1]-1: #Agent collided with obstacle or moved in to a wall
			return True, False, -20
		elif coords in goalCoords:	#Agent reached its goal
			return False, True, 100
		else:	#No collision and goal not reached
			return False, False, -1

	def getAgentCoords(self, index):
		return [agents[index].x, agents[index].y]

