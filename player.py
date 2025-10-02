from constants import *
from circleshape import *
from shot import Shot

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_timer = 0
        self.invincible_until = 0.0

    # in the player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        if not self.blinking_on():
            return # skip drawing this frame to "hide"
        color = "gray" if self.is_invincible() else "white"
        pygame.draw.polygon(screen, color, self.triangle(), width=2)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt):
        super().update(dt)
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()
        self.shoot_timer -= dt
    
    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt
    
    def shoot(self):
        if self.shoot_timer > 0:
            return
        self.shoot_timer = PLAYER_SHOOT_COOLDOWN
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
    
    def reset_to_spawn(self, x, y):
        self.position.update(x, y)
        self.velocity.update(0, 0)
        self.rotation = 0
        self.invincible_until = pygame.time.get_ticks() / 1000 + 2.0

    def is_invincible(self):
        return (pygame.time.get_ticks() / 1000) < self.invincible_until
    
    def blinking_on(self):
        if not self.is_invincible():
            return True
        tick = pygame.time.get_ticks() / 1000
        phase = (tick // PLAYER_BLINK_PERIOD) % 2 # 0 or 1
        return phase == 0 # visible half the time        
        

