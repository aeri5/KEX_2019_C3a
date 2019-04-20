import tkinter
from agent import *

obstacleCoords = [] # [[x, y], [x, y], ...]
obstacles = []
agentCoords = [[0,3]] # [[x, y], [x, y], ...] (agent start locations)  [[0,4], [0,0], [4,1], [4,3]]
agents = []
goalCoords = [[3,0]] # [[0,4], [0,0], [4,1], [4,3]]
goals = []

class Warehouse(tkinter.Tk, object):
	def __init__(self, warehouseSize, squareDim):
		super(Warehouse, self).__init__()
		self.warehouseSize = warehouseSize
		self.squareDim = squareDim
		self.windowSize = [self.squareDim*self.warehouseSize[0], self.squareDim*self.warehouseSize[1]] #[width, height]
		self.title("Warehouse sim")
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
		# goals.append(self.canvas.create_rectangle(goalCoords[1][0]*self.squareDim+1, goalCoords[1][1]*self.squareDim+1, (goalCoords[1][0]+1)*self.squareDim-1, (goalCoords[1][1]+1)*self.squareDim-1, fill="#2455b7", outline="#2455b7", tags="goal1"))	
		# goals.append(self.canvas.create_rectangle(goalCoords[2][0]*self.squareDim+1, goalCoords[2][1]*self.squareDim+1, (goalCoords[2][0]+1)*self.squareDim-1, (goalCoords[2][1]+1)*self.squareDim-1, fill="#8cc160", outline="#8cc160", tags="goal2"))
		# goals.append(self.canvas.create_rectangle(goalCoords[3][0]*self.squareDim+1, goalCoords[3][1]*self.squareDim+1, (goalCoords[3][0]+1)*self.squareDim-1, (goalCoords[3][1]+1)*self.squareDim-1, fill="#ce618e", outline="#ce618e", tags="goal3"))	

		#init agent
		agents.append(Agent(agentCoords[0][0], agentCoords[0][1], self.canvas.create_rectangle(agentCoords[0][0]*self.squareDim+1, agentCoords[0][1]*self.squareDim+1, (agentCoords[0][0]+1)*self.squareDim-1, (agentCoords[0][1]+1)*self.squareDim-1, fill="#eda061", outline="#eda061", tags="agent0")))			
		# agents.append(Agent(agentCoords[1][0], agentCoords[1][1], self.canvas.create_rectangle(agentCoords[1][0]*self.squareDim+1, agentCoords[1][1]*self.squareDim+1, (agentCoords[1][0]+1)*self.squareDim-1, (agentCoords[1][1]+1)*self.squareDim-1, fill="#91cbf7", outline="#91cbf7", tags="agent1")))
		# agents.append(Agent(agentCoords[2][0], agentCoords[2][1], self.canvas.create_rectangle(agentCoords[2][0]*self.squareDim+1, agentCoords[2][1]*self.squareDim+1, (agentCoords[2][0]+1)*self.squareDim-1, (agentCoords[2][1]+1)*self.squareDim-1, fill="#8ce29c", outline="#8ce29c", tags="agent2")))			
		# agents.append(Agent(agentCoords[3][0], agentCoords[3][1], self.canvas.create_rectangle(agentCoords[3][0]*self.squareDim+1, agentCoords[3][1]*self.squareDim+1, (agentCoords[3][0]+1)*self.squareDim-1, (agentCoords[3][1]+1)*self.squareDim-1, fill="#f9b8d3", outline="#f9b8d3", tags="agent3")))


		self.canvas.pack()


	def nextCoords(self, index, action):
		nextCoords = self.getAgentCoords(index)
		if action == 0:
			nextCoords[1] = nextCoords[1] - 1
		elif action == 1:
			nextCoords[0] = nextCoords[0] + 1
		elif action == 2:
			nextCoords[1] = nextCoords[1] + 1
		elif action == 3:
			nextCoords[0] = nextCoords[0] - 1
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
		otherAgents = agents[:index] + agents[index+1:]
		if (coords in obstacleCoords) or (coords in [[otherAgent.x, otherAgent.y] for otherAgent in otherAgents]) or (coords[0] < 0 or coords[0] > self.warehouseSize[0]-1 or coords[1] < 0 or coords[1] > self.warehouseSize[1]-1): #Agent collided with obstacle, another agent, or a wall
			return True, False, -50

		elif coords == goalCoords[index]:	#Agent reached its goal
			return False, True, 50

		else:	#No collision, goal not reached
			return False, False, -1


	def getAgentCoords(self, index):
		return [agents[index].x, agents[index].y]


	def agentsCloseBy(self, index, coords):
		otherAgentWhere = [0, 0, 0, 0]
		otherAgents = agents[:index] + agents[index+1:]
		for otherAgent in otherAgents:
			if otherAgent.y == coords[1]-1: #another agent above
				otherAgentWhere[0] = 1
			elif otherAgent.x == coords[0]+1: #another agent to the right
				otherAgentWhere[1] = 1
			elif otherAgent.y == coords[1]+1: #another agent below
				otherAgentWhere[2] = 1
			elif otherAgent.x == coords[0]-1: #another agent to the left
				otherAgentWhere[3] = 1
		return otherAgentWhere