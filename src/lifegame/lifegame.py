import pygame
from pygame.locals import *
from copy import deepcopy


SIZE = (40, 30)
BOARD = """
0
1110000
0000000
0000000
0000000
0000000
000000000000000000000000000
000000000000000000000000000
000000000000000000000000000
000000000000000000000000000
000000000000000000000000010
000000000000000000011000000
000000000000000000001000111
000000000000000000000000000
000000000000000000000000000
000000000000000000000000000
000000111000000000000000000
000000011100000000000000000
010000000000000000000000000
001000000000000000000000000
111000000000000000000000000
"""
class Game(object):
	PATT_COLOR = (255, 100, 0)
	BACK_COLOR = (0, 0, 0)
	
	def __init__(self):
		pygame.init()
		vi = pygame.display.Info()
		width, height = vi.current_w, vi.current_h
		self.video_size = (width, height)
		self.screen = pygame.display.set_mode(self.video_size, FULLSCREEN)
		self.clock = pygame.time.Clock()
		self.patterns_horizontal, self.patterns_vertical = SIZE
		self.pattern_width = width/self.patterns_horizontal
		self.pattern_height = height/self.patterns_vertical
		self.init_board()
	
	def get_no_neighbours(self, x, y):
		no_neighbours = 0
		if y > 0 and x > 0:
			no_neighbours += self.board[y-1][x-1]
		if y > 0:
			no_neighbours += self.board[y-1][x]
		if y > 0 and x < (self.patterns_horizontal-1):
			no_neighbours += self.board[y-1][x+1]
		if x > 0:
			no_neighbours += self.board[y][x-1]
		if x < (self.patterns_horizontal-1):
			no_neighbours += self.board[y][x+1]
		if x > 0 and y < (self.patterns_vertical-1):
			no_neighbours += self.board[y+1][x-1]
		if y < (self.patterns_vertical-1):
			no_neighbours += self.board[y+1][x]
		if x < (self.patterns_horizontal-1) and y < (self.patterns_vertical-1):
			no_neighbours += self.board[y+1][x+1]
		return no_neighbours
		
	def init_board(self):
		self.board = [[0 for x in range(0, self.patterns_horizontal)] for y in range(0, self.patterns_vertical)]
		self.board2 = deepcopy(self.board)
		for y, row in enumerate(BOARD.split()):
			for x, cell in enumerate(row):
				if cell == '1' and x <= self.patterns_horizontal and y <= self.patterns_vertical:
					self.board[y][x] = 1

	def draw(self):
		pw, ph = self.pattern_width, self.pattern_height
		screen = self.screen
		for x in range(0, self.patterns_horizontal):
			for y in range(0, self.patterns_vertical):
				color = Game.PATT_COLOR if self.board[y][x] == 1 else Game.BACK_COLOR
				pygame.draw.rect(screen, color, pygame.Rect(x*pw, y*ph, pw-1, ph-1))
		
	def logic(self):
		for x in range(0, self.patterns_horizontal):
			for y in range(0, self.patterns_vertical):
				no_neighbours = self.get_no_neighbours(x, y)
				self.board2[y][x] = self.board[y][x]
				if not self.board[y][x] and no_neighbours == 3:
					self.board2[y][x] = 1
					print("Birth at %d,%d [%d]" % (x,y,no_neighbours))
				if self.board[y][x] and no_neighbours != 3 and no_neighbours != 2:
					self.board2[y][x] = 0
					print("Delete at %d,%d [%d]" % (x,y,no_neighbours))
		self.board = deepcopy(self.board2)
				
	def loop(self):
		
		done = False
		pygame.event.pump()
		self.screen.fill((0, 0, 0))
		
		while not done: # main game loop
			for event in pygame.event.get():
				if event.type == QUIT:
					done = True

			self.draw()
			self.logic()
			print("*** NEXT ***")
			
			pygame.display.update()
			self.clock.tick(50)
			pygame.time.wait(100)
		pygame.quit()

def main():
	game = Game()
	game.loop()

if __name__ == '__main__':
	main()
	pygame.display.quit()
	