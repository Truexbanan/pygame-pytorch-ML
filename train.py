from matplotlib import pyplot as plt
from game import GameAI
from agent import Agent
from helper import plot

def train():
    # Define game and agent parameters
    input_size = 8
    output_size = 2
    agent = Agent(input_size, output_size)
    game = GameAI()

    scores = []
    mean_scores = []
    total_score = 0
    record = 0

    plt.ion()  # Interactive mode on
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))  # Two subplots

    while True:
        state_old = agent.get_state(game)
        action = agent.get_action(state_old)
        reward, done, score = game.play_step(action)
        state_new = agent.get_state(game)

        agent.train_short_memory(state_old, action, reward, state_new, done)
        agent.remember(state_old, action, reward, state_new, done)

        if done:
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

            # Plot scores
            ax1.clear()
            plot(scores, mean_scores, ax=ax1)  # Pass ax to the plot function

            # Plot Q values
            ax2.clear()
            ax2.plot(agent.q_values_history)
            ax2.set_title('Q values over Time')
            ax2.set_xlabel('Step')
            ax2.set_ylabel('Q value')

            plt.tight_layout()

            plt.pause(0.1)  # Pause to update the plots

            agent.q_values_history.clear()  # Clear Q values history

    plt.ioff()  # Turn interactive mode off
    plt.show()  # Show plots at the end

if __name__ == '__main__':
    train()