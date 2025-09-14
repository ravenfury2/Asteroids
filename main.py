# this allows us to use code from
# the open-source pygame library
# throughout this file
import pygame

# import everything from the module
# constants.py into the current file
from constants import *

# import everything from the module
# player.py into the current file
from player import *

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill("black")
        player.update(dt)
        player.draw(screen)
        pygame.display.flip()

        dt = clock.tick(60) / 1000
        
        
        


if __name__ == "__main__":
    main()
