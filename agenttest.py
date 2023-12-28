import torch
import random
import numpy as np
from collections import deque
from game import OBJECT_MAX_SPEED, SCREEN_HEIGHT, SCREEN_WIDTH, GameAI 
from model import Linear_QNet, QTrainer

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    def __init__(self, input_size, output_size):
        self.n_games = 0
        self.epsilon = 0  # randomness
        self.gamma = 0.9  # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)  # popleft()
        self.model = Linear_QNet(input_size, 256, output_size)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, game):
        # Find the nearest object
        nearest_object = None
        min_distance = float('inf')
        for obj in game.objects:
            distance = obj.y - game.player.y
            if distance > 0 and distance < min_distance:
                nearest_object = obj
                min_distance = distance
        if nearest_object is not None:
            state = [
                # Player's position (normalized)
                game.player.x / SCREEN_WIDTH,
                
                # Nearest object's horizontal position (normalized)
                nearest_object.x / SCREEN_WIDTH,
                
                # Nearest object's vertical distance from the player (normalized)
                min_distance / SCREEN_HEIGHT,

                # Nearest object's speed (normalized)
                nearest_object.speed / OBJECT_MAX_SPEED
            ]
        else:
            # Default state if no object is found
            state = [0, 0, 1, 0]
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
        # Random moves: trade-off between exploration and exploitation
        self.epsilon = 80 - self.n_games
        if random.randint(0, 200) < self.epsilon:
            action = random.randint(0, 1)
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            action = torch.argmax(prediction).item()

        return action
    
