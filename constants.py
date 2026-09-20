# Action Constants
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

DIRECTIONS = {
    UP: (0, -1),
    RIGHT: (1, 0),
    DOWN: (0, 1),
    LEFT: (-1, 0)
}

DEBUG_MODE = False

# --- Hyperparameters ---
NUM_EPISODES = 100000
MAX_STEPS = 40
LEARNING_RATE = 0.05     

# --- Exploration parameters ---
INITIAL_EXPLORATION_RATE = 1.0     
MIN_EXPLORATION = 0.05     
DECAY_RATE = 0.99