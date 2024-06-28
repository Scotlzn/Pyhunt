import pygame, time
from settings import *
from random import choice
from support import get_random_colour

class ParticleManager:
	def __init__(self, ds):
		self.ds = ds

		pygame.mixer.init()
		self.click_sounds = self.generate_click_sounds()

		self.particles = []

	def generate_click_sounds(self):
		out = []
		files = ['click1', 'click2', 'click3', 'click4', 'click5', 'click6', 'click7', 'click8']
		for f in files:
			out.append(pygame.mixer.Sound(f'sounds/click/{f}.wav'))
		return out

	def create_particle_directions(self):
		x = [-1, 0, 1]
		y = [-1, 0, 1]
		vectors = []
		depth = 2
		# Loop through the 8 (without [0, 0]) directions
		for i in range(len(x)):
			for j in range(len(y)):
				# Calculate the int values to check for 0, 0
				vector = [x[i], y[j]]
				# Check if vector doesn't have any movement at all
				if vector != [0, 0]:
					# If it has movement the ints will be added to the output directions
					vectors.append(vector)
					# If depth is enabled, loop for each layer of depth
					for depth_count in range(depth-1):
						# calculate both x and y independently as to not have slow messed up particles
						# adds both an int and a float based on the division of the initial number the
						# amount of times of the value of depth, +1 to avoid division by 0 error
						a = [x[i], vector[1] / (2 * (depth_count + 1))]
						b = [vector[0] / (2 * (depth_count + 1)), y[j]]
						# check for slow particles by not having a 0 and a float
						if (a[1] < 1.0 and b[1] == 0) or (b[0] < 1.0 and a[0] == 0):
							continue
						# finally, adds the x and y of the vector to the output
						vectors.append(a)
						vectors.append(b)
		return vectors

	def create_particles(self, pos):
		out = []
		mouse_position = pos
		directions = self.create_particle_directions()
		choice(self.click_sounds).play()
		for particle in range(len(directions)):
			obj = Particle(self.ds, mouse_position, directions[particle], 30, 16, 1, get_random_colour(), 'square')
			out.append(obj)
		self.particles.append(out)

	def update(self, dt):
		if self.particles != []:
			for group in self.particles:
				for particle in group:
					if particle.check_duration():
						self.particles.remove(group)
						break
					else:
						particle.update(dt)

class Particle:
	def __init__(self, ds, pos, velocity, speed, size, duration, colour, shape):
		self.ds = ds
		self.x = pos[0] - 8
		self.y = pos[1] - 8
		self.velocity = pygame.math.Vector2(velocity)
		self.speed = speed
		self.size = size
		self.colour = colour
		self.duration = duration
		self.shape = shape

		self.img = pygame.Surface((self.size, self.size))
		if self.shape == 'square':
			self.img.fill(self.colour)
		elif self.shape == 'circle':
			pygame.draw.circle(self.img, self.colour, (8, 8), 8)
			self.img.set_colorkey((0, 0, 0))

		# Get the duration and the time when fading is going to start
		# Calculate fixed float of the increment of the alpha value based on fps and time
		# Alpha starts at 255 and works it's way down to 0
		self.start_fade = self.duration * 0.5
		self.fade = 255 / (FPS * self.start_fade)
		self.alpha = 255

		self.start_time = time.time()

	def check_duration(self):
		return True if time.time() > self.start_time + self.duration else False

	def check_fade(self):
		if time.time() > self.start_time + self.start_fade:
			self.alpha -= self.fade
			self.img.set_alpha(self.alpha)

	def move(self, dt):
		self.x += self.velocity.x * self.speed * dt
		self.y += self.velocity.y * self.speed * dt

	def render(self):
		if self.shape == 'square':
			self.ds.blit(self.img, (self.x+2, self.y+2))
		elif self.shape == 'circle':
			self.ds.blit(self.img, (self.x, self.y))

	def update(self, dt):
		self.move(dt)
		self.check_fade()
		self.render()
