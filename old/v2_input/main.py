from warehouse import *
import time
import sys

w = Warehouse()
w.update()

try:
	while True:
		action = input()
		if action != "stop":
			w.moveAgent(0, str(action))
			w.update()
		else:
			break
	w.mainloop()

except KeyboardInterrupt:
	sys.exit(0)