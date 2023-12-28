import torch
from model import Linear_QNet, QTrainer

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    def __init__(self, input_size, output_size):
        self.n_games = 0
        self.epsilon = 0  # randomness
        self.gamma = 0.9  # discount rate
        self.model = Linear_QNet(input_size, 256, output_size)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)