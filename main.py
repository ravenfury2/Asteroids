# this allows us to use code from
# the open-source pygame library
# throughout this file
import pygame

from constants import *
from player import Player
from shot import Shot
from asteroid import Asteroid
from asteroidfield import AsteroidField

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    game_paused = False

    #Object grouping   
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    #Adding objects groups to containers
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, updatable, drawable)
    Player.containers = (updatable, drawable)

    #Player and play field
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()

    #Delta Time initiator
    dt = 0

    # Fonts
    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 50)

    def draw_text(text, font, color, x, y):
        text_surface = font.render(text, True, color)
        text_rect= text_surface.get_rect(center=(x, y))
        screen.blit(text_surface, text_rect)
    
    def draw_pause_menu():
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150)) # Black with 150 alpha ( transparency )
        screen.blit(overlay, (0, 0))

        draw_text("Game Paused", font, (255, 255, 255), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)

        # Resume Button
        resume_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2, 150, 50)
        pygame.draw.rect(screen, (0, 200, 0), resume_button_rect) # Green
        draw_text("Resume", small_font, (255, 255, 255), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 25)

        # Quit Button
        quit_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 + 70, 150, 50)
        pygame.draw.rect(screen, (200, 0, 0), quit_button_rect) # Red
        draw_text("Quit", small_font, (255, 255, 255), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 95)

        return resume_button_rect, quit_button_rect


    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_paused = not game_paused
            if event.type == pygame.MOUSEBUTTONDOWN and game_paused:
                mouse_pos = event.pos
                resume_rect, quit_rect = draw_pause_menu() # Re-draw to get button rects
                if resume_rect.collidepoint(mouse_pos):
                    game_paused = False
                elif quit_rect.collidepoint(mouse_pos):
                    running = False

        screen.fill("black")

        if not game_paused:
            updatable.update(dt)

            # collision detection
            for asteroid in asteroids:
                if asteroid.is_colliding(player):
                    print("Game Over!")
                    return
                for bullet in shots:
                    if bullet.is_colliding(asteroid):
                        bullet.kill()
                        asteroid.split()
            for objects in drawable:
            # Horizontal wrapping
                if objects.position.x > SCREEN_WIDTH:
                    objects.position.x = -objects.radius # Appears on the left
                elif objects.position.x < -objects.radius:
                    objects.position.x = SCREEN_WIDTH # Appears on the right
            
            # Vertical wrapping
                if objects.position.y > SCREEN_HEIGHT:
                    objects.position.y = -objects.radius # Appears at the top
                elif objects.position.y < -objects.radius:
                    objects.position.y = SCREEN_HEIGHT # Appears at the bottom
            

            for objects in drawable:
                objects.draw(screen)
        else:
            draw_pause_menu()

        pygame.display.flip()

        # limit the framerate to 60 FPS
        dt = clock.tick(60) / 1000
    pygame.quit()
        
        
if __name__ == "__main__":
    main()
