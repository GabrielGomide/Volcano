import pygame
from pygame.sndarray import use_arraytype
import random

surface = pygame.display.set_mode((500, 500))

pygame.display.set_caption("Experiencia")

manto = pygame.Rect(0, 250, 500, 250)
placa1 = pygame.Rect(0, 220, 250, 50)
placa2 = pygame.Rect(250, 220, 250, 50)
grama1 = pygame.Rect(0, 215, 250, 5)
grama2 = pygame.Rect(250, 215, 250, 5)

ORANGE = (255, 180, 0)
BROWN = (155, 100, 60)
GREEN = (80, 255, 0)
RED = (255, 0, 0)

class Particula:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.temp = self.get_temp()
		self.state = self.get_state()
		self.rect = self.get_rect()
		self.been_cold = 0
		self.been_warm = 230
		self.has_moved = False
		self.erupting = False
		self.moving_down = False
		if self.x <= 245:
			self.dir = 'L'
		else:
			self.dir = 'R'

	def  get_temp(self):
		return self.y * 4

	def get_rect(self):
		return pygame.Rect(self.x, self.y, 10, 10)

	def get_state(self):
		if self.temp < 1080:
			return "F"
		elif self.temp > 1900:
			return "Q"
		else:
			try:
				return self.state
			except:
				return "Q"


def draw_window(p_list):
	surface.fill((0, 100, 255))
	pygame.draw.rect(surface, ORANGE, manto)
	for p in p_list:
		pygame.draw.rect(surface, RED, p.rect)

	pygame.draw.rect(surface, BROWN, placa1)
	pygame.draw.rect(surface, BROWN, placa2)
	pygame.draw.rect(surface, GREEN, grama1)
	pygame.draw.rect(surface, GREEN, grama2)

	pygame.draw.polygon(surface, BROWN, [(250, 100), (150, 250), (350, 250)])

	pygame.display.update()


def main():
	run = True

	p_list = []
	
	for i in range(25):
		p_list.append(Particula(random.randrange(210, 245), random.randrange(400, 490)))

	for i in range(25):
		p_list.append(Particula(random.randrange(255, 280), random.randrange(400, 490)))

	clock = pygame.time.Clock()

	can_erupt = False

	while run:
		clock.tick(60)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		draw_window(p_list)

		for p in p_list:
			if p.state == "Q":
				p.been_warm += 1
				if can_erupt:
					p.erupting = True

				if p.been_warm > 230:
					p.been_cold = 0
					p.y -= 1
					p.rect = p.get_rect()
					p.temp = p.get_temp()
					p.state = p.get_state()
				else:			
					p.has_moved = False
					if p.dir == "L":
						p.x += 1
					else:
						p.x -= 1
					p.rect = p.get_rect()
			elif p.state == "F":
				p.been_cold += 1
				if p.x < random.randrange(10, 40) or p.x > random.randrange(450, 480):
					p.been_warm = 0
					p.y += 1
					p.rect = p.get_rect()
					p.temp = p.get_temp()
					p.state = p.get_state()
				else:
					if p.erupting:
						p.y -= 2

						if p.y < 150:
							p.x = random.randrange(235, 255)

						if p.y < 30:
							p.moving_down = True
							p.erupting = False
						p.rect = p.get_rect()
					elif p.moving_down:
						if p.moving_down:
							p.y += 1

							if p.dir == "L":
								p.x -= 1
							else:
								p.x += 1

							if p.y >= 210:
								p_list.remove(p)
								if len(p_list) == 0:
									run = False
							p.rect = p.get_rect()
					else:
						if p.dir == "L":
							p.x -= 1
						else:
							p.x += 1
						p.rect = p.get_rect()
					if p.rect.colliderect(placa1) and not p.has_moved:
						p.has_moved = True
						placa1.x -= 2
						grama1.x -= 2
					if p.rect.colliderect(placa2) and not p.has_moved:
						p.has_moved = True
						placa2.x += 2
						grama2.x += 2
					else:
						if placa1.x < -80 and placa2.x > 330:
							can_erupt = True

if __name__ == "__main__":
	main()

