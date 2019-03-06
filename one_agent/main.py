from warehouse import *
import random
import time
import sys

w = Warehouse()
w.update()

try:
	while True:
		w.update()
		nextAction = w.getActions()[random.randrange(0, 5, 1)]
		w.moveAgent(0, nextAction)				
		if w.collision(0):
			w.restart(0)
		time.sleep(0.5)

	w.mainloop()

except KeyboardInterrupt:
	sys.exit(0)