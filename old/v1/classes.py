from tkinter import *

class thing:
	def __init__(self):
		self.temp = 0

class object(object):
	def __init__(self, warehouse, x, y, objectType, id, contents = []):
		self.x = x
		self.y = y
		self.id = id
		self.objectType = objectType
		if self.objectType == "agent":
			self.image = PhotoImage(file="forklift.gif").subsample(int(256/(620/warehouse.width)), int(256/(620/warehouse.width)))
		elif self.objectType == "shelf":
			self.contents = contents
			self.image = PhotoImage(file="shelf.gif").subsample(int(256/(620/warehouse.width)), int(256/(620/warehouse.width)))

class warehouse:
	def __init__(self, canvas, width, height, objects = []):
		self.canvas = canvas
		self.width = width
		self.height = height
		self.objects = objects

		self.canvas.create_line(50, 50, 670, 50, width=2, fill="black") #Top
		self.canvas.create_line(670, 50, 670, 670, width=2, fill="black") #Right
		self.canvas.create_line(50, 670, 670, 670, width=2, fill="black") #Bottom
		self.canvas.create_line(50, 50, 50, 670, width=2, fill="black") #Left

		for i in range(1, self.width):
			self.canvas.create_line(50+i*(620/self.width), 50, 50+i*(620/self.width), 670, width=2, fill="grey")

		for j in range(1, self.height):
			self.canvas.create_line(50, 50+j*(620/self.height), 670, 50+j*(620/self.height), width=2, fill="grey")

	def insertObject(self, object):
		self.objects.append(object)

	def updateWarehouse(self):
		for i in range(0, len(self.objects)):

			self.canvas.create_image((50 + self.objects[i].x*(620/self.width), 50 + self.objects[i].y*(620/self.height)), image = self.objects[i].image, anchor = "nw")