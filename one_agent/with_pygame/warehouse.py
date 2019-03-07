import tkinter
from agent import *

squareDim = 40
warehouseSize = [10, 10] #[maxX, maxY]
windowSize = [squareDim*warehouseSize[0], squareDim*warehouseSize[1]] #[width, height]
obstacleCoords = [[2,2], [3,2], [4,2], [5,2], [7,2], [7,3], [7,4], [3,4], [4,4], [5,4]] #[[x, y], [x, y], ...]
obstacles = []
agentCoords = [[0,6]] #[[x, y], [x, y], ...] (agent start locations)
agents = []
actions = ["up", "right", "down", "left", "stay"]
goalCoords = [[9, 0]]
goals = []

class Warehouse(tkinter.Tk, object):
	def __init__(self):
		super(Warehouse, self).__init__()
		self.title("Warehouse sim with one agent")
		self.canvas = tkinter.Canvas(self, bg="#b7b7b7", width = windowSize[0], height = windowSize[1])
		
		#draw grid
		for i in range(1, int(windowSize[0]/squareDim)): #vertical lines
			self.canvas.create_line(i*squareDim, 0, i*squareDim, windowSize[1], fill="#444444")
		for i in range(1, int(windowSize[1]/squareDim)): #horizontal lines
			self.canvas.create_line(0, i*squareDim, windowSize[0], i*squareDim, fill="#444444")

		#init shelves
		for obstacle in obstacleCoords:
			obstacles.append(self.canvas.create_rectangle(obstacle[0]*squareDim+1, obstacle[1]*squareDim+1, (obstacle[0]+1)*squareDim-1, (obstacle[1]+1)*squareDim-1, fill="#444444", outline="#444444"))

		#init agent
		agentCounter = 0
		for agent in agentCoords:
			agents.append(Agent(agent[0], agent[1], self.canvas.create_rectangle(agent[0]*squareDim+1, agent[1]*squareDim+1, (agent[0]+1)*squareDim-1, (agent[1]+1)*squareDim-1, fill="#eda061", outline="#eda061", tags=str(agentCounter))))
			agentCounter += 1

		#init goal
		for goal in goalCoords:
			goals.append(self.canvas.create_rectangle(goal[0]*squareDim+1, goal[1]*squareDim+1, (goal[0]+1)*squareDim-1, (goal[1]+1)*squareDim-1, fill="#a8e298", outline="#a8e298"))	

		self.canvas.pack()

	def moveAgent(self, index, action):
		if action == actions[0]:
			self.canvas.move(agents[index].tkID, 0, -squareDim)
			agents[index].y = agents[index].y - 1
		elif action == actions[1]:
			self.canvas.move(agents[index].tkID, squareDim, 0)
			agents[index].x = agents[index].x + 1
		elif action == actions[2]:
			self.canvas.move(agents[index].tkID, 0, squareDim)
			agents[index].y = agents[index].y + 1
		elif action == actions[3]:
			self.canvas.move(agents[index].tkID, -squareDim, 0)
			agents[index].x = agents[index].x - 1
		elif action == actions[4]:
			self.canvas.move(agents[index].tkID, 0, 0)
		else:
			raise ValueError("Incorrect movement")
		print(agents[index].x, "x", agents[index].y)

	def getActions(self):
		return actions

	def restart(self, index):
		agents[index].x = agentCoords[index][0]
		agents[index].y = agentCoords[index][1]
		self.canvas.coords(agents[index].tkID, agentCoords[index][0]*squareDim+1, agentCoords[index][1]*squareDim+1, (agentCoords[index][0]+1)*squareDim-1, (agentCoords[index][1]+1)*squareDim-1)
		# print("restart")

	def collision(self, index):
		if [agents[index].x, agents[index].y] in obstacleCoords or agents[index].x < 0 or agents[index].x > warehouseSize[0]-1 or agents[index].y < 0 or agents[index].y > warehouseSize[1]-1:
			return True, False
		elif [agents[index].x, agents[index].y] in goalCoords:
			return True, True
		else:
			return False, False

	def reward(self, index):
		reward = -1
		collision, goalReached = self.collision(index)
		if collision:
			if goalReached:
				reward = 100
			else:
				reward = -100

		return reward