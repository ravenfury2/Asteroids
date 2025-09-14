import pygame
from constants import *
from circleshape import *
import random

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, width=2)

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        self.kill()

        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        
        # randomize the angle of the split
        random_angle = random.uniform(20, 50)

        new_vector1 = self.velocity.rotate(random_angle)
        new_vector2 = self.velocity.rotate(-random_angle)

        new_radius = self.radius - ASTEROID_MIN_RADIUS
        smaller_asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        smaller_asteroid1.velocity = new_vector1 * 1.2
        smaller_asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
        smaller_asteroid2.velocity = new_vector2 * 1.2
