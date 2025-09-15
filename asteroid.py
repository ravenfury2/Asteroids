import pygame
from constants import *
from circleshape import *
import math
import random

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

        self.lumpy_points = []
        num_segments = random.randint(ASTEROID_MIN_NUM_SEGMENTS, ASTEROID_MAX_NUM_SEGMENTS)
        base_angle_increment = (2 * math.pi) / num_segments

        for i in range(num_segments):
            angle = i * base_angle_increment
            
            perturbed_radius = self.radius * random.uniform(ASTEROID_MIN_LUMP_FACTOR, ASTEROID_MAX_LUMP_FACTOR)
                        
            px_offset = perturbed_radius * math.cos(angle)
            py_offset = perturbed_radius * math.sin(angle)

            self.lumpy_points.append(pygame.Vector2(px_offset, py_offset))
    

    def draw(self, screen):
        if len(self.lumpy_points) > 2:
            transformed_points = []
            for p_offset in self.lumpy_points:
                transformed_points.append(self.position + p_offset)
            pygame.draw.polygon(screen, "white", transformed_points, width=2)


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
