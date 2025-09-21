import pygame
from constants import *

# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        # we will be using this later
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def draw(self, screen):
        # sub-classes must override
        pass

    def update(self, dt):
        
        # Horizontal wrapping
        if self.position.x > SCREEN_WIDTH:
            self.position.x = -self.radius # Appears on the left
        elif self.position.x < -self.radius:
            self.position.x = SCREEN_WIDTH # Appears on the right
            
        # Vertical wrapping
        if self.position.y > SCREEN_HEIGHT:
            self.position.y = -self.radius # Appears at the top
        elif self.position.y < -self.radius:
            self.position.y = SCREEN_HEIGHT # Appears at the bottom

    def is_colliding(self, other):
        return self.position.distance_to(other.position) <= (self.radius + other.radius)