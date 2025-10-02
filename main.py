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
    asteroids = pygame.sprite.Group()   
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    #Adding objects groups to containers
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, updatable, drawable)
    Player.containers = (updatable, drawable)

    #Lives and game state
    lives = 3
    game_over = False

    #Player and play field
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()
    player.reset_to_spawn(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    #Delta Time initiator
    dt = 0

    # Fonts
    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 50)

    def draw_hud():
        draw_text(f"Lives: {lives}", small_font, (255, 255, 255), 90, 30)
    
    def draw_game_over():
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        draw_text("Game Over", font, (255, 255, 255), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40)
        draw_text("Press R to Restart or ESC to Quit", small_font, (200, 200, 200), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)

    def handle_player_death():
        nonlocal lives, game_over
        lives -= 1
        if lives > 0:
            player.reset_to_spawn(SCREEN_WIDTH / 2, SCREEN_HEIGHT /2)
        else:
            game_over = True

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
                if game_over:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_r and game_over:
                        # restart
                        lives = 3
                        game_over = False
                        # clear entities
                        for a in list(asteroids): a.kill()
                        for s in list(shots): s.kill()
                        player.reset_to_spawn(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                else:
                    if event.key == pygame.K_ESCAPE:
                        game_paused = not game_paused
            if event.type == pygame.MOUSEBUTTONDOWN and game_paused and not game_over:
                mouse_pos = event.pos
                resume_rect, quit_rect = draw_pause_menu() # Re-draw to get button rects
                if resume_rect.collidepoint(mouse_pos):
                    game_paused = False
                elif quit_rect.collidepoint(mouse_pos):
                    running = False

        screen.fill("black")

        if game_over:
            draw_game_over()
            pygame.display.flip()
            continue

        if not game_paused:
            # limit the framerate to 60 FPS
            dt = clock.tick(60) / 1000

            # Spawn asteroid if able to from asteroidfield timer
            if asteroid_field.update(dt):
                asteroid_field.spawn_random()
  
            # Updates all objects  
            updatable.update(dt)
                        
            # Draw all objects
            for objects in drawable:
                objects.draw(screen)
            
            draw_hud()            
            # collision detection
            for asteroid in asteroids:
                # skip collision if invincible
                if not player.is_invincible() and asteroid.is_colliding(player):
                    handle_player_death()
                    break
                for bullet in shots:
                    if bullet.is_colliding(asteroid):
                        bullet.kill()
                        asteroid.split()
        else:
            draw_pause_menu()

        pygame.display.flip()

        
    pygame.quit()
        
        
if __name__ == "__main__":
    main()
