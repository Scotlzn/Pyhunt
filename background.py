import pygame, time
from random import randint
from pygame import mixer

class BackgroundManager:
    def __init__(self, ds):
        self.ds = ds

        pygame.mixer.init()
        mixer.music.load("sounds/wind.wav")
        mixer.music.set_volume(0.05)
        mixer.music.play(-1)

        self.clouds = []

        self.start_time = time.time()
        self.timers = {
            'timer_cloud': self.start_time,
            'timer_cloud_particle': self.start_time
        }

        self.sun = pygame.image.load('assets/sun.png').convert()
        self.sun.set_colorkey((0, 0, 0))
        self.sun.set_alpha(6)

        self.wind_particles = []

    def check_time(self):
        current_time = time.time()
        if current_time > self.timers['timer_cloud'] + 1:
            self.clouds.append(Cloud(self.ds, (640, randint(10, 310))))
            self.timers['timer_cloud'] = current_time
        if current_time > self.timers['timer_cloud_particle'] + 1:
            self.wind_particles.append(WindParticle(self.ds, (640, 180), [randint(-100, -20), randint(-40, 40)]))
            self.timers['timer_cloud_particle'] = current_time

    def update_sun(self):
        self.ds.blit(self.sun, (8, 8))

    def update_clouds(self, dt):
        for cloud in self.clouds:
            cloud.update(dt)
            if cloud.x < -cloud.width:
                self.clouds.remove(cloud)

    def update_wind_particles(self, dt):
        for particle in self.wind_particles:
            particle.update(dt)
            if particle.x < -particle.size:
                if particle.y < 0 or particle.y > 644:
                    self.wind_particles.remove(particle)

    def update(self, dt):
        self.check_time()
        self.ds.fill('#ADD8E6')
        self.update_sun()
        self.update_clouds(dt)
        self.update_wind_particles(dt)

class Cloud:
    def __init__(self, ds, pos):
        self.ds = ds

        self.x = pos[0]
        self.y = pos[1]
        self.width = 200
        self.height = 100
        self.speed = -50
        self.img = self.generate_cloud()

    def generate_cloud(self):
        out = pygame.Surface((self.width, self.height))
        for i in range(1, 16):
            size = randint(20, 70)
            xOffset = randint(-40, 40)
            yOffset = randint(-30, 30)
            pygame.draw.ellipse(out, (255, 255, 255), (100 + xOffset, 50 + yOffset, size, size))
        out.set_colorkey((0, 0, 0))
        return out

    def move(self, dt):
        self.x += self.speed * dt

    def render(self):
        self.ds.blit(self.img, (self.x, self.y))

    def update(self, dt):
        self.move(dt)
        self.render()

class WindParticle:
    def __init__(self, ds, pos, velocity):
        self.ds = ds

        self.x, self.y = pos
        self.size = 4
        self.velocity = velocity

    def move(self, dt):
        self.x += self.velocity[0] * dt
        self.y += self.velocity[1] * dt

    def render(self):
        pygame.draw.rect(self.ds, (255,255,255), (self.x, self.y, self.size, self.size))

    def update(self, dt):
        self.move(dt)
        self.render()