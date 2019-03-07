from warehouse import *
import time
import sys
import pygame

w = Warehouse()
w.update()
pygame.init()
window = pygame.display.set_mode((200,200))
pygame.display.set_caption("Window")
black = (0,0,0)
gameloop = True
while gameloop:
	for event in pygame.event.get():
		if event.type==pygame.KEYDOWN:
			if event.key==pygame.K_RIGHT:
				w.moveAgent(0, str("right"))
			elif event.key==pygame.K_LEFT:
				w.moveAgent(0, str("left"))
			elif event.key==pygame.K_UP:
				w.moveAgent(0, str("up"))
			elif event.key==pygame.K_DOWN:
				w.moveAgent(0, str("down"))
			elif event.key==pygame.K_BACKSPACE:
				print("exit")
				sys.exit(0)
		collision, goalReached = w.collision(0)
		if collision:
			w.restart(0)
			if goalReached:
				print("goal reached")
			else:
				print("restart")
		w.update()
	window.fill(black)
	pygame.display.flip()