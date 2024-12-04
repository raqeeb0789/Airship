import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A Game By Raqeeb")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load images
spaceship_img = pygame.image.load('images/rb_49950.png')
asteroid_img = pygame.image.load('images/asteroid.png')
bullet_img = pygame.image.load('images/bullet.png')

# Scale images
spaceship_img = pygame.transform.scale(spaceship_img, (50, 50))
asteroid_img = pygame.transform.scale(asteroid_img, (50, 50))
bullet_img = pygame.transform.scale(bullet_img, (10, 20))

# Sprite setup
class Spaceship(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = spaceship_img
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        bullets.add(bullet)
        all_sprites.add(bullet)

class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = asteroid_img
        self.rect = self.image.get_rect(center=(random.randint(20, WIDTH - 20), -50))
        self.speed = random.randint(3, 7)

    def update(self):
        global score
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            score = max(0, score - 5)  # Reduce score by 5, ensuring it doesn't go below 0
            self.kill()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

# Groups
all_sprites = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Instantiate spaceship
spaceship = Spaceship()
all_sprites.add(spaceship)

# Game variables
score = 0
highest_score = 0  # Track highest score
FPS = 70
clock = pygame.time.Clock()
asteroid_spawn_rate = 50

# Font
font = pygame.font.Font(None, 36)

def reset_game():
    """Reset the game state to the initial conditions."""
    global score, asteroid_spawn_rate
    score = 0
    asteroid_spawn_rate = 40
    all_sprites.empty()
    asteroids.empty()
    bullets.empty()
    spaceship.rect.center = (WIDTH // 2, HEIGHT - 50)
    all_sprites.add(spaceship)

def show_game_over_screen():
    """Display the game over screen and handle restart/quit."""
    global highest_score
    if score > highest_score:  # Update the highest score if the current score is greater
        highest_score = score

    screen.fill(BLACK)
    game_over_text = font.render("Game Over!", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    high_score_text = font.render(f"Highest Score: {highest_score}", True, WHITE)
    restart_text = font.render("Press R to Restart or Q to Quit", True, WHITE)
    
    screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 80))
    screen.blit(score_text, (WIDTH // 2 - 100, HEIGHT // 2 - 30))
    screen.blit(high_score_text, (WIDTH // 2 - 100, HEIGHT // 2 + 20))
    screen.blit(restart_text, (WIDTH // 2 - 150, HEIGHT // 2 + 70))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                    waiting = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

# Main game loop
running = True
while running:
    reset_game()
    in_game = True
    while in_game:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_game = False
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    spaceship.shoot()

        # Spawn new asteroids
        if random.randint(1, asteroid_spawn_rate) == 1:
            asteroid = Asteroid()
            asteroids.add(asteroid)
            all_sprites.add(asteroid)

        # Update all sprites
        all_sprites.update()

        # Check for bullet-asteroid collisions
        hits = pygame.sprite.groupcollide(asteroids, bullets, True, True)
        for hit in hits:
            score += 10

        # Check for asteroid-spaceship collisions
        if pygame.sprite.spritecollideany(spaceship, asteroids):
            in_game = False

        # Draw everything
        screen.fill(BLACK)
        all_sprites.draw(screen)
        score_text = font.render(f"Score: {score}", True, WHITE)
        high_score_text = font.render(f"Highest Score: {highest_score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(high_score_text, (10, 40))  # Display highest score at the top
        pygame.display.flip()
        clock.tick(FPS)

    # Show game over screen after inner loop ends
    if running:
        show_game_over_screen()

pygame.quit()
sys.exit()
