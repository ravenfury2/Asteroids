# this allows us to use code from
# the open-source pygame library
# throughout this file
import pygame

# import everything from the module
# constants.py into the current file
from constants import *

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill("black")

        pygame.display.flip()


if __name__ == "__main__":
    main()
