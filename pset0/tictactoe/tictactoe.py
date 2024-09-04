"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """

    # get number of empty cells
    noEmpty = 0

    for row in range(3):
        for column in range(3):
            if board[row][column] == EMPTY:
                noEmpty += 1

    # if number is even then 'O' else 'X'
    if noEmpty % 2 == 0:
        return O
    else:
        return X

    # raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    # an empty set for actions
    actions = set()

    # add every empty cell to actions
    for row in range(3):
        for column in range(3):
            if board[row][column] == EMPTY:
                actions.add(tuple([row, column]))

    return actions

    # raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # make sure cell is empty
    if board[action[0]][action[1]] is not EMPTY:
        raise Exception("Invalid action.")
    else:
        # fill cell with symbol of current player
        result = copy.deepcopy(board)
        result[action[0]][action[1]] = X if player(board) == X else O

        return result

    # raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # check diagonal cells
    if (board[0][0] == board[1][1] == board[2][2] == X):
        return X

    if (board[0][2] == board[1][1] == board[2][0] == X):
        return X

    if (board[0][0] == board[1][1] == board[2][2] == O):
        return O

    if (board[0][2] == board[1][1] == board[2][0] == O):
        return O

    # check horizontal cells
    if (board[0][0] == board[0][1] == board[0][2] == X):
        return X

    if (board[1][0] == board[1][1] == board[1][2] == X):
        return X

    if (board[2][0] == board[2][1] == board[2][2] == X):
        return X

    if (board[0][0] == board[0][1] == board[0][2] == O):
        return O

    if (board[1][0] == board[1][1] == board[1][2] == O):
        return O

    if (board[2][0] == board[2][1] == board[2][2] == O):
        return O

    # check vertical cells
    if (board[0][0] == board[1][0] == board[2][0] == X):
        return X

    if (board[0][1] == board[1][1] == board[2][1] == X):
        return X

    if (board[0][2] == board[1][2] == board[2][2] == X):
        return X

    if (board[0][0] == board[1][0] == board[2][0] == O):
        return O

    if (board[0][1] == board[1][1] == board[2][1] == O):
        return O

    if (board[0][2] == board[1][2] == board[2][2] == O):
        return O

# def winner(board):
#     """
#     Returns the winner of the game, if there is one.
#     """
#     winning_combinations = [
#         # Rows
#         [(0, 0), (0, 1), (0, 2)],
#         [(1, 0), (1, 1), (1, 2)],
#         [(2, 0), (2, 1), (2, 2)],
#         # Columns
#         [(0, 0), (1, 0), (2, 0)],
#         [(0, 1), (1, 1), (2, 1)],
#         [(0, 2), (1, 2), (2, 2)],
#         # Diagonals
#         [(0, 0), (1, 1), (2, 2)],
#         [(0, 2), (1, 1), (2, 0)]
#     ]

#     for combination in winning_combinations:
#         symbols = [board[row][col] for row, col in combination]
#         if symbols == ['X', 'X', 'X']:
#             return 'X'
#         elif symbols == ['O', 'O', 'O']:
#             return 'O'

#     return None
    # raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    if winner(board) is not None:
        return True

    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                return False

    return True

    #raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0

    # raise NotImplementedError


def max_value(board):
    """
    Returns the highest value of the board
    if the maximizing player plays optimally
    """
    if terminal(board):
        return utility(board)

    v = -math.inf

    for action in actions(board):
        v = max(v, min_value(result(board, action)))

    return v


def min_value(board):
    """
    Returns the lowest value of the board
    if the minimizing player plays optimally
    """

    if terminal(board):
        return utility(board)

    v = math.inf

    for action in actions(board):
        v = min(v, max_value(result(board, action)))

    return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if terminal(board):
        return None

    if player(board) == X:

        u = max_value(board)
        v = -math.inf

        for action in actions(board):
            v = max(v, min_value(result(board, action)))

            if v == u:
                return action

    if player(board) == O:

        u = min_value(board)
        v = math.inf

        for action in actions(board):
            v = min(v, max_value(result(board, action)))

            if v == u:
                return action

    # raise NotImplementedError