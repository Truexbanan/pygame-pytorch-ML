import matplotlib.pyplot as plt
from IPython import display

plt.ion()

def plot(scores, mean_scores, ax=None):
    if ax is None:
        ax = plt.gca()  # Get current axes if not provided
    ax.clear()
    ax.set_title('Training...')
    ax.set_xlabel('Number of Games')
    ax.set_ylabel('Score')
    ax.plot(scores, label='Score per Game')
    ax.plot(mean_scores, label='Mean Score')
    ax.set_ylim(ymin=0)
    ax.legend(loc='upper left')
    ax.text(len(scores)-1, scores[-1], str(scores[-1]))
    ax.text(len(mean_scores)-1, mean_scores[-1], str(mean_scores[-1]))