import pygame
import random
import time


# Initialize Pygame
pygame.init()

# Constants                   
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 50
OBJECT_WIDTH, OBJECT_HEIGHT = 50, 50
PLAYER_SPEED = 5
OBJECT_MIN_SPEED, OBJECT_MAX_SPEED = 3, 5  # Initial speed range
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
FONT = pygame.font.SysFont(None, 36)

score_multiplier = 1

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y 
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.speed = PLAYER_SPEED
        self.direction = 1  # 1 for right, -1 for left

    def change_direction(self):
        self.direction *= -1

    def move(self):
        self.x += self.direction * self.speed
        self.x = max(0, min(SCREEN_WIDTH - self.width, self.x))

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, [self.x, self.y, self.width, self.height])

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Object:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH - OBJECT_WIDTH)
        self.y = -OBJECT_HEIGHT
        global OBJECT_MIN_SPEED, OBJECT_MAX_SPEED
        self.speed = random.randint(OBJECT_MIN_SPEED, OBJECT_MAX_SPEED)

    def update(self):
        self.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, RED, [self.x, self.y, OBJECT_WIDTH, OBJECT_HEIGHT])

    def get_rect(self):
        return pygame.Rect(self.x, self.y, OBJECT_WIDTH, OBJECT_HEIGHT)

def main():
    global OBJECT_MIN_SPEED, OBJECT_MAX_SPEED, score_multiplier
    # Set up the display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Game")

    # Player setup
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - PLAYER_HEIGHT - 10)

    # Object setup
    objects = []
    start_time = time.time()

    # Game loop
    running = True
    clock = pygame.time.Clock()

    score = 0

    while running:
        screen.fill(WHITE)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.change_direction()

        # Update player position
        player.move()

        # Update objects
        for obj in objects:
            obj.update()

        # Add new object
        elapsed_time = time.time() - start_time
        # Decrease spawn threshold over time to increase spawn rate
        spawn_threshold = max(10, 30 - int(elapsed_time / 20))
        if random.randint(1, spawn_threshold) == 1:
            objects.append(Object())

        # Gradual increase in object speed
        OBJECT_MIN_SPEED = min(7, 3 + int(elapsed_time / 60))
        OBJECT_MAX_SPEED = min(10, 5 + int(elapsed_time / 45))

        # Draw player
        player.draw(screen)

        # Draw objects
        for obj in objects:
            obj.draw(screen)

        # Check for collisions
        player_rect = player.get_rect()
        for obj in objects:
            if player_rect.colliderect(obj.get_rect()):
                running = False  # End the game on collision

        # Scoring
        score += 1 * score_multiplier  # Update score

        # Display score
        score_text = FONT.render(f'Score: {int(score)}', True, BLACK)
        screen.blit(score_text, (10, 10))

        # Update the display
        pygame.display.flip()

        # Remove off-screen objects
        objects = [obj for obj in objects if obj.y < SCREEN_HEIGHT]

        # Cap the frame rate
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
