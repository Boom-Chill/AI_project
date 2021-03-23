import itertools
import random
import numpy
from init import Board
from init import Game

victory_cell = []


def isMovesLeft(cell, color):
    for (r, c) in itertools.product(list('12345678'), list('abcdefgh')):
        if cell.isPlaceable(c + r, color):
            return True
    return False


def validSteps(cell, color):
    posible_positions = []
    for (r, c) in itertools.product(list('12345678'), list('abcdefgh')):
        if cell.isPlaceable(c + r, color):
            posible_positions.append(c + r)
    return posible_positions 


def evaluated(victory_cells, cell, color, force=False):
    v_b = v_w = 0
    for c in victory_cells:
        v_b += 1 if cell.getValue(c) == 'W' else 0
        v_w += 1 if cell.getValue(c) == 'B' else 0
    if v_b == 5:
        return "BLACK"
    if v_w == 5:
        return "White"

    color = 'W' if color == 'WHITE' else 'B'
    check_playable = False
    if not force:
        check_playable = cell.isPlayable(color)
    if not check_playable:
        b, w = cell.getResult()
        if b > w:
            return "BLACK"
        elif b < w:
            return "WHITE"
        if b == w:
            if v_b > v_w:
                return "BLACK"
            elif v_b < v_w:
                return "WHITE"
            else:
                return "DRAW"

    return None


def heuristic(victory_cell, cell, color, max=True):
    result = evaluated(victory_cell, cell, color)
    opponent = 'W' if color != "BLACK" else 'B'
    if len(validSteps(cell, opponent)) == 0:
        return 9999 if max else -9999
    if result != color and result != None:
        return -9999 if max else 9999
    num_steps = len(validSteps(cell, color))
    op_num_steps = len(validSteps(cell, opponent))
    possibal_move = num_steps - op_num_steps
    return possibal_move*10 if max else -possibal_move*10


def minimax(victory_cell, cur_state, you, depth, isMax, alpha, beta):
    game = Board()
    game.update(cur_state)
    color = 'W' if you == "BLACK" else 'B'
    final = evaluated(victory_cell, game, color)

    if final == you:
        return 9999
    elif final != 'DRAW' and final != None:
        return -9999
    elif final == 'DRAW':
        return 0

    if depth == 0 and game.isPlayable(color):
        if isMax:
            return heuristic(victory_cell, game, you, True)
        else:
            return heuristic(victory_cell, game, you, False)
    if isMovesLeft(game, color) == False:
        return 0

    if isMax:
        best = -9999
        for (x, y) in itertools.product(list('12345678'), list('abcdefgh')):
            if game.isPlaceable(y + x, color):
                new_game = Board()
                new_game.update(cur_state)
                new_game.place(y + x, color)
                new_state = new_game.getCellLineList()

                best = max(best, minimax(victory_cell, new_state,
                                         you, depth - 1, False, alpha, beta))
                alpha = max(alpha, best)
                if beta <= alpha:
                    break
                # print('max:', best)
        return best
    else:
        best = 9999
        for (x, y) in itertools.product(list('12345678'), list('abcdefgh')):
            if game.isPlaceable(y + x, color):
                new_game = Board()
                new_game.update(cur_state)
                new_game.place(y + x, color)
                new_state = new_game.getCellLineList()

                best = min(best, minimax(victory_cell, new_state,
                                         you, depth - 1, True, alpha, beta))
                beta = min(beta, best)
                if beta <= alpha:
                    break
                # print('min:', best)
        return best


def prior_spot(spot):
    global victory_cell
    score = 0
    list_12 = ['a1', 'h1', 'a8', 'h8']
    list_2 = ['c1', 'f1', 'c8', 'f8', 'a3', 'h3', 'a6', 'h6']
    list_1_5 = ['c3', 'f3', 'c6', 'f6']
    list_0_5 = ['a4', 'h4', 'a5', 'h5', 'd1', 'e1', 'd8', 'e8']
    list_minus0_5 = ['c2', 'd2', 'e2', 'f2', 'b3', 'b4', 'b5', 'b6', 'g3'
                     'g4', 'g5', 'g6', 'c7', 'd7', 'e7', 'f7']
    list_minus2 = ['b1', 'g1', 'b8', 'g8', 'a2', 'h8', 'a7', 'h7']
    list_minus4 = ['b2', 'g2', 'b7', 'g7']
    if spot in list_12:
        score += 12
    elif spot in list_2:
        score += 2
    elif spot in list_1_5:
        score += 1.5
    elif spot in list_minus2:
        score += -2
    elif spot in list_minus4:
        score += -4
    elif spot in list_0_5:
        score += 0.5
    elif spot in list_minus0_5:
        score += -0.5
    elif spot in victory_cell:
        score += 20
    else:
        score += 0.3
    return score


def BestMove(victory_cell, cur_state, you, depth):
    global best
    game = Board()
    game.update(cur_state)
    color = 'W' if you == "BLACK" else 'B'
    px = None
    py = None
    bestVal = -9999
    for (x, y) in itertools.product(list('12345678'), list('abcdefgh')):
        if game.isPlaceable(y + x, color):
            global best
            best = 0
            new_game = Board()
            new_game.update(cur_state)
            new_game.place(y + x, color)
            new_state = new_game.getCellLineList()
            moveVal = minimax(victory_cell, new_state, you,
                              depth, True, -9999, 9999) + prior_spot(y+x)/2
            if moveVal > bestVal:
                px = x
                py = y
                bestVal = moveVal
    return px, py


def callBot(game_info):
    global victory_cell
    lines = game_info.split('\n')
    victory_cell = lines[1].split(' ')
    you = lines[-2]
    lines = lines[3:11]
    (px, py) = BestMove(victory_cell, lines, you, 2)
    if px == None or py == None:
        return "NULL"
    return py + px
