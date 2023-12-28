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
