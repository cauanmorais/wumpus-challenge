# Action Constants
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

# CLASS CONSTANT: Master reference for all movement.
# Format -> action_number: (change_in_x, change_in_y)
# 0: Up, 1: Right, 2: Down, 3: Left
# Movement Modifiers (dx, dy)
DIRECTIONS = {
    UP: (0, -1),
    RIGHT: (1, 0),
    DOWN: (0, 1),
    LEFT: (-1, 0)
}