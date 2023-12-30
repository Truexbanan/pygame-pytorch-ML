from game import GameAI
from agent import Agent
from helper import plot

def train():
    # Define game and agent parameters
    input_size = 4 # Define based on your state representation
    output_size = 2  # Two actions: left or right
    agent = Agent(input_size, output_size)
    game = GameAI()

    scores = []
    mean_scores = []
    total_score = 0
    record = 0

    while True:
        state_old = agent.get_state(game)

        # Decide action
        action = agent.get_action(state_old)

        # Perform action in the game
        reward, done, score = game.play_step(action)
        state_new = agent.get_state(game)

        # Train short memory
        agent.train_short_memory(state_old, action, reward, state_new, done)

        # Store the experience
        agent.remember(state_old, action, reward, state_new, done)

        if done:
            # Train long memory, plot result
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            print('Game', agent.n_games, 'Score', score, 'Record:', record)

            scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            mean_scores.append(mean_score)
            plot(scores, mean_scores)

if __name__ == '__main__':
    train()