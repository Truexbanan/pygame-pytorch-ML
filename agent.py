import time
import torch
import random
import numpy as np
from collections import deque
from game import OBJECT_MAX_SPEED, SCREEN_HEIGHT, SCREEN_WIDTH, GameAI 
from model import Linear_QNet, QTrainer

MAX_MEMORY = 10000
BATCH_SIZE = 64
LR = 0.0005

class Agent:
    def __init__(self, input_size, output_size):
        self.n_games = 0
        self.epsilon = 1  # randomness
        self.gamma = 0.9  # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)  # popleft()
        self.model = Linear_QNet(input_size, 256, output_size)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)
        self.last_direction_change_time = time.time()
    
    def change_direction(self):
        # Call this method when the player changes direction
        self.last_direction_change_time = time.time()

    def get_state(self, game):
        # Sort objects based on their distance to the player
        sorted_objects = sorted(game.objects, key=lambda obj: (obj.y - game.player.y)**2 + (obj.x - game.player.x)**2)

        # Initialize state with default values
        state = [
            # Player's normalized position
            game.player.x / SCREEN_WIDTH,
            # Player's distance from screen edges
            min(game.player.x, SCREEN_WIDTH - game.player.x) / SCREEN_WIDTH,
            # Player's current direction
            game.player.direction
        ]

        # If there are at least one object, get the relative position of the nearest object
        if sorted_objects:
            nearest_object = sorted_objects[0]
            state.extend([
                (nearest_object.x - game.player.x) / SCREEN_WIDTH,
                (nearest_object.y - game.player.y) / SCREEN_HEIGHT
            ])
        else:
            state.extend([0, 0])  # No objects, so we add zeros

        # If there are at least two objects, get the relative position of the second nearest object
        if len(sorted_objects) > 1:
            second_nearest_object = sorted_objects[1]
            state.extend([
                (second_nearest_object.x - game.player.x) / SCREEN_WIDTH,
                (second_nearest_object.y - game.player.y) / SCREEN_HEIGHT
            ])
        else:
            state.extend([0, 0])  # Less than two objects, so we add zeros

        # Number of objects directly above the player
        objects_above_player = sum(1 for obj in game.objects if obj.x == game.player.x)
        state.append(objects_above_player)

        return np.array(state, dtype=float)


    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # Decay epsilon with a lower bound to ensure some level of exploration
        self.epsilon = max(self.epsilon * 0.99, 0.1)  # for example, decay epsilon by 1% each game, with a minimum of 0.1
        
        # Exploration vs exploitation
        if random.random() < self.epsilon:
            # Random move
            action = random.randint(0, 1)
        else:
            # Exploitation (choose the best action according to the model)
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            action = torch.argmax(prediction).item()
        
        return action