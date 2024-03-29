import numpy as np
import random

from depth_limited_search import *

ACTIONS = ["up", "right", "down", "left"]

def apply_action(board,action):
    """
    Move the "blank" tile of the 8 puzzle
    :param board:
    the board to manipulate
    :param action:
    the direction to move the blank tile
    :return:
    """
    deltas = np.array([[-1,0,1,0],[0,1,0,-1]])
    action_2_index = {'up':0,'right':1,'down':2,'left':3}
    # dictionary matching direction to number value
    posx,posy = np.where(np.isin(board, [0]))
    # find position of element 0, the blank tile
    (x,y) = (posx[0],posy[0])
    # set this tuple to x, y of 0

    (new_x,new_y) = (x + deltas[0,action_2_index[action]],y + deltas[1,action_2_index[action]])
    # generate new position for blank tile
    try:
        # generate a new board and try to replace the old one
        new_board = np.copy(board)
        # swap the old val at new_x, new_y with 0
        el = new_board[new_x,new_y]
        new_board[x,y] = el
        new_board[new_x,new_y] = 0

        # print(new_x, new_y)
        # print(board)
        return new_board
    except IndexError:
        # if the solution is invalid, return the old board
        return board


def goal_test(board):
    """
    Check if board is in goal state
    :param board:
    The board to check
    :return:
    True if in goal state
    False otherwise
    """
    goal = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
    return np.array_equal(board,goal)


def n_out_of_order(board):
    """
    Counts the number of pieces not in their proper positions
    in the out of order board
    :param board:
    The board to check
    :return:
    The number of out of place tiles in the board
    """
    goal = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
    return np.count_nonzero(np.subtract(board,goal))


def mess_up(board,actions,moves):
    """
    Mess up the order of board
    :param board:
    Board to mess up
    :param actions:
    the moves to mess up the board with
    :param moves:
    the number of moves to mess up the board
    """
    for iter in range(0,moves):
        board = apply_action(board,actions[random.randint(0,3)])
    return board

class EightPuzzleProblem(Problem):
    def __init__(self):
        # create a board then mess it up for end state
        # start_state = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
        # start_state = mess_up(start_state, ACTIONS, 10)
        # start_state = np.array([[1, 2, 3], [4, 5, 6], [7, 0, 8]])
        # start_state = np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8]])
        start_state = np.array([[1, 2, 3], [4, 5, 6], [7, 0, 8]])

        start_node = Node(start_state)
        # end goal is normal
        goal_state = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
        goal_node = Node(goal_state)

        # feed the super init the start and end state
        super().__init__(start_node, goal_node)

    def actions(self, state):
        """
        Generates possible solutions for an 8-tile puzzle
        :param state:
        The current layout of the tile puzzle
        :return:
        an iterable representing possible solutions for an 8-tile puzzle
        """

        # try all possible moves for the tile puzzle
        for action in ACTIONS:
            # try to make a new board from the current action
            new_state = apply_action(state, action)

            # an invalid solution is one that returns the original board
            if np.array_equal(new_state, state):
                continue

            # if the solution is valid, yield it as a result

            yield new_state

    def goal_test(self, state):
        # use the predefined goal test for 8-Puzzle
        return goal_test(state)

    def node_comparison(self, a, b):
        """
        Returns true if the two nodes are equal
        :param a:
        First node
        :param b:
        Second node
        :return:
        True if two nodes are equal
        False otherwise
        """
        return np.array_equal(a, b)

def random_search(board):
    # create a sequce of 32 random moves and keep going until it is solved.
    # this may take a long time to return

    new_board = np.copy(board)
    actions = ACTIONS
    while True:
        sequence = []
        new_board = np.copy(board)
        for iteration in range(0,32):
            action = actions[random.randint(0,3)]
            sequence.append(action)
            new_board=apply_action(new_board, action)
            if goal_test(new_board):
                return sequence
    pass
