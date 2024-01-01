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
OBJECT_MIN_SPEED, OBJECT_MAX_SPEED = 4, 4
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
        self.speed = 4
        self.to_remove = False
        # self.speed = random.randint(OBJECT_MIN_SPEED, OBJECT_MAX_SPEED)

    def update(self):
        self.y += self.speed
        if self.y > SCREEN_HEIGHT:  # Condition to flag the object for removal
            self.to_remove = True

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

        # Initial reward for surviving this step
        survival_reward = 0.1
        reward = survival_reward

        # Perform the action decided by the agent
        if action == 1:
            self.player.change_direction()

        # Save the previous X before the player moves
        previous_x = self.player.x
        self.player.move()

        # Update the positions of the objects
        for obj in self.objects:
            obj.update()

        # Remove objects that have been flagged for removal
        self.objects = [obj for obj in self.objects if not obj.to_remove]

        game_over = False
        player_rect = self.player.get_rect()

        # Check for collision with any of the objects
        for obj in self.objects:
            if player_rect.colliderect(obj.get_rect()):
                game_over = True
                reward = -10  # Large penalty for collision
                break

        # Check if the player has moved, apply idle penalty if not
        idle_penalty = 0.01
        if self.player.x == previous_x:
            reward -= idle_penalty
        
        # Check for close calls and apply rewards or penalties
        close_avoidance_bonus = 0.5
        close_call_threshold = OBJECT_WIDTH  # This threshold determines what is considered a close call
        near_miss_penalty = 0.2
        NEAR_MISS_THRESHOLD = OBJECT_WIDTH / 2  # Threshold for a near miss
        for obj in self.objects:
            distance_x = abs(obj.x - self.player.x)
            if obj.y > self.player.y and obj.y < SCREEN_HEIGHT:
                if distance_x < close_call_threshold:
                    reward += close_avoidance_bonus
                if distance_x < NEAR_MISS_THRESHOLD:
                    reward -= near_miss_penalty

        # Increment the score for surviving this step
        self.score += 1

        # Bonus for high scores at certain milestones
        high_score_bonus = 1
        if self.score % 100 == 0:
            reward += high_score_bonus

        # Spawn new objects if needed, adjust as necessary for your game's difficulty
        elapsed_time = time.time() - self.start_time
        spawn_threshold = max(10, 60 - int(elapsed_time / 20))
        if random.randint(1, spawn_threshold) == 1 and len(self.objects) < 2:
            self.objects.append(Object())

        # Update the UI
        self._update_ui()

        # Return the reward, game over status, and score
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