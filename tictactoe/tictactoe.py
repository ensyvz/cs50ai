"""
Tic Tac Toe Player
"""

import math
from operator import truediv
from pickle import TRUE
from queue import Empty
from copy import deepcopy

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
    turn_of = 0 # 0 if X's turn. other if O's turn.
    for row in board:
        for col in row:
            cell = col
            if cell == X:
                turn_of -= 1
            elif cell == O:
                turn_of += 1

    if turn_of == 0:
        return X
    return O
            

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()

    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == EMPTY:
                actions.add((row,col))

    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    result = deepcopy(board)
    result[action[0]][action[1]] = player(result)

    return result

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    last_player = None
    if player(board) == X:
        last_player = O
    else:
        last_player = X
        
    for row in board:
        if row[0]==last_player and row[1]==last_player and row[2]==last_player:
            return last_player
    for i in range(3):
        if board[0][i]==last_player and board[1][i]==last_player and board[2][i]==last_player:
            return last_player
    if board[0][0]==last_player and board[1][1]==last_player and board[2][2]==last_player:
        return last_player
    if board[0][2]==last_player and board[1][1]==last_player and board[2][0]==last_player:
        return last_player
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    empty_flag = False
    for row in board:
        for col in row:
            if col == EMPTY:
                empty_flag = True
                break
        if empty_flag:
            break
    if empty_flag == False or winner(board) != None:
        return True
        
    return False

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    won = winner(board)
    if won == X:
        return 1
    if won == O:
        return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    if player(board) == X:
        return max_value(board)[0]
    else:
        return min_value(board)[0]

explored_boards = list()

def max_value(board):
    best_action = None
    max_score = -2

    for action in actions(board):
        result_board = result(board,action)
        if terminal(result_board):
            score = utility(result_board)
            if max_score<score:
                max_score = score
                best_action = action

        else:
            flag=False
            for s in explored_boards:
                if(s[0]==result_board):
                    flag=True
                    if max_score < s[1]:
                        best_action = action
                        max_score = s[1]
                    break
            if flag:
                continue
            res = min_value(result_board)
            explored_boards.append((result_board,res[1]))
            if max_score < res[1]:
                best_action = action
                max_score = res[1]
        if max_score == 1:
            break

    return (best_action,max_score)

def min_value(board):
    best_action = None
    min_score = 2
    
    for action in actions(board):
        result_board = result(board,action)
        if terminal(result_board):
            score = utility(result_board)
            if min_score>score:
                min_score = score
                best_action = action
                
        else:
            flag=False
            for s in explored_boards:
                if(s[0]==result_board):
                    flag=True
                    if min_score > s[1]:
                        best_action = action
                        min_score = s[1]
                    break
            if flag:
                continue
            res = max_value(result_board)
            explored_boards.append((result_board,res[1]))
            if min_score > res[1]:
                best_action = action
                min_score = res[1]
        if min_score == -1:
            break

    return (best_action,min_score)