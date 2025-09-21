import pygame
import random
from asteroid import Asteroid
from constants import *


class AsteroidField(pygame.sprite.Sprite):

    edges = {
        "right": (pygame.Vector2(1, 0),  lambda y: pygame.Vector2(SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT)),
        "left":  (pygame.Vector2(-1, 0), lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT)),
        "bottom":(pygame.Vector2(0, 1),  lambda x: pygame.Vector2(x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS)),
        "top":   (pygame.Vector2(0, -1), lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS)),
    }

    def __init__(self):
        pygame.sprite.Sprite.__init__(self.containers)
        self.spawn_timer = 0.0

    def spawn(self, radius, position, velocity):
        asteroid = Asteroid(position.x, position.y, radius)
        asteroid.velocity = velocity
        return asteroid
    
    def spawn_random(self):

        # Choose a random side to spawn from
        edge = random.choice(list(self.edges.keys()))
        normal_vector, position_func = self.edges[edge]

        # Get a random position on that edge
        position = position_func(random.uniform(-2, 2))

        # Calculate a velocity vector pointing inwards
        center = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        direction_to_center = center - position

        # Normalize the vector and add a random angle offset for variety
        if direction_to_center.length() > 0:
            direction_to_center.normalize_ip()

        random_angle = random.uniform(-30, 30)
        direction_to_center.rotate_ip(random_angle)

        # Set a random speed
        speed = random.randint(40, 100)
        velocity = direction_to_center * speed

        # Determine the size of the asteroid
        kind = random.randint(1, ASTEROID_KINDS)
        radius = ASTEROID_MIN_RADIUS * kind

        return self.spawn(radius, position, velocity)

        #return new_asteroid

    def update(self, dt):
        self.spawn_timer += dt
        if self.spawn_timer > ASTEROID_SPAWN_RATE:
            self.spawn_timer = 0
            return True
        return False