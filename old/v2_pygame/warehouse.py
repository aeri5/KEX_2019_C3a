import tkinter
from agent import *

squareDim = 60
warehouseSize = [7,8] #[rows, columns]
windowSize = [squareDim*warehouseSize[1], squareDim*warehouseSize[0]] #[width, height]
obstacleCoords = [[2,2], [3,2], [4,2], [5,2], [7,2], [7,3], [7,4], [3,4], [4,4], [5,4]] #[[x, y], [x, y], ...]
obstacles = []
agentCoords = [[0,6]] #[[x, y], [x, y], ...]
agents = []

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

		self.canvas.pack()

	def moveAgent(self, index, action):
		if action == "up":
			self.canvas.move(agents[index].tkID, 0, -squareDim)
			agents[index].y = agents[index].y + 1
		elif action == "right":
			self.canvas.move(agents[index].tkID, squareDim, 0)
			agents[index].x = agents[index].x + 1
		elif action == "down":
			self.canvas.move(agents[index].tkID, 0, squareDim)
			agents[index].y = agents[index].y + 1
		elif action == "left":
			self.canvas.move(agents[index].tkID, -squareDim, 0)
			agents[index].x = agents[index].x - 1
		elif action == "stay":
			self.canvas.move(agents[index].tkID, 0, 0)
		else:
			raise ValueError("Incorrect movement")