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
OBJECT_MIN_SPEED, OBJECT_MAX_SPEED = 3, 5
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
FONT = pygame.font.SysFont(None, 36)

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

class GameAI:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Game")
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - PLAYER_HEIGHT - 10)
        self.objects = []
        self.score = 0
        self.start_time = time.time()
        self.running = True

    def play_step(self, action):
        if not self.running:
            self.reset()

        if action == 1:
            self.player.change_direction()

        self.player.move()

        for obj in self.objects:
            obj.update()

        reward = 0
        game_over = False
        player_rect = self.player.get_rect()
        for obj in self.objects:
            if player_rect.colliderect(obj.get_rect()):
                game_over = True
                reward = -10
                break

        self.score += 1
        elapsed_time = time.time() - self.start_time
        spawn_threshold = max(10, 30 - int(elapsed_time / 20))
        if random.randint(1, spawn_threshold) == 1:
            self.objects.append(Object())

        self._update_ui()
        return reward, game_over, self.score

    def _update_ui(self):
        self.screen.fill(WHITE)
        self.player.draw(self.screen)
        for obj in self.objects:
            obj.draw(self.screen)
        score_text = FONT.render('Score: {}'.format(int(self.score)), True, BLACK)
        self.screen.blit(score_text, (10, 10))
        pygame.display.flip()
        self.clock.tick(60)