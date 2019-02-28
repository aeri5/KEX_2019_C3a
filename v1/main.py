from tkinter import *
from classes import *

def main():
	print("I'm alive!")

	wWidth = 5
	wHeight = 5

	root = Tk()
	root.title('Warehouse sim')
	canvas = Canvas(root, bg="#afafaf", width=1280, height=720)
	canvas.pack()

	w = warehouse(canvas, wWidth, wHeight)
	w.insertObject(object(w, 0, 3, "agent", "agent1"))
	w.insertObject(object(w, 4, 0, "shelf", "shelf1"))
	w.insertObject(object(w, 3, 3, "shelf", "shelf2"))
	w.insertObject(object(w, 4, 1, "shelf", "shelf2"))
	w.updateWarehouse()
	root.mainloop()

main()