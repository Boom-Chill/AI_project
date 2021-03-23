import itertools
import random

from init import Board
from init import Game

victory_cells = []
bot = str
competitor = str
color = str
c_color = str


def posiblePositions(game, color):
    posible_positions = []
    for (r, c) in itertools.product(list('12345678'), list('abcdefgh')):
        if game.isPlaceable(c + r, color):
            posible_positions.append(c + r)
    return posible_positions


def numberOfStep(game, color):
    c_color = str
    if (color == 'B'):
        c_color = 'W'
    else:
        c_color = 'B'
    b_step = len(posiblePositions(game, color))
    c_step = len(posiblePositions(game, c_color))
    return b_step, c_step


def evaluated(game):
    global bot
    global color
    global victory_cells

    v_b = v_w = 0
    for c in victory_cells:
        v_b += 1 if game.getValue(c) == 'W' else 0
        v_w += 1 if game.getValue(c) == 'B' else 0
    if v_b == 5:
        return "BLACK"
    if v_w == 5:
        return "WHITE"

    if not game.isPlayable(color):
        b, w = game.getResult()
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
    return "CONTINUE"


def positionScore(game, color):
    c_color = str
    if (color == 'B'):
        c_color = 'W'
    else:
        c_color = 'B'
    b_score = 0
    c_score = 0
    for (r, c) in itertools.product(list('12345678'), list('abcdefgh')):
        if game.getValue(c + r) == color:
            b_score += 10
        if game.getValue(c + r) == c_color:
            c_score += 10
    t_score = b_score + c_score
    return t_score, b_score, c_score


def findScoreCalculator(game, color):
    score = 0
    for (r, c) in itertools.product(list('12345678'), list('abcdefgh')):
        if game.getValue(c + r) == color:
            score += findScore(c + r, game, color)
    return score


def findScore(position, game, color):
    global victory_cells
    score = 0

    positionScoreBoard = [[30, -20, 20, 5, 5, 20, -20, 30],
                          [-20, -40, -5, -5, -5, -5, -40, -20],
                          [20, -5, 15, 3, 3, 15, -5, 20],
                          [5, -5, 3, 3, 3, 3, -5, 5],
                          [5, -5, 3, 3, 3, 3, -5, 5],
                          [20, -5, 15, 3, 3, 15, -5, 20],
                          [-20, -40, -5, -5, -5, -5, -40, -20],
                          [30, -20, 20, 5, 5, 20, -20, 30]]

    cell_lines = game.getCellLineList()
    for i in range(8):
        cell_lines[i] = cell_lines[i].replace(' ', '')
        for j in range(8):
            if cell_lines[i][j] == color:
                score += positionScoreBoard[i][j]
            elif cell_lines[i][j] != 'E':
                score -= positionScoreBoard[i][j]
    return score


def minimax(curState, depth, alpha, beta, isMax):
    global bot
    global color
    global competitor
    global c_color
    game = Board()
    game.update(curState)

    result = evaluated(game)

    if (result != 'CONTINUE'):
        if (result == bot):
            return 9999
        elif result == 'DRAW':
            return 0
        else:
            return -9999

    score = 0
    if (depth == 0):
        if isMax:
            b_nstep, c_nstep = numberOfStep(game, color)
            t_p, b_p, c_p = positionScore(game, color)
            score = findScoreCalculator(game, color)
            if (b_p > c_p):
                score += 100
                if (t_p < 20):
                    if (b_nstep > c_nstep):
                        score += 150
                        return score
                    else:
                        score += 100
                        return score
                else:
                    if (b_nstep > c_nstep):
                        score += 300
                        return score
                    else:
                        score += 100
                        return score
            else:
                score -= 100
                if (t_p < 200):
                    if (b_nstep > c_nstep):
                        score -= 100
                        return score
                    else:
                        score -= 150
                        return score
                else:
                    if (b_nstep > c_nstep):
                        score -= 200
                        return score
                    else:
                        score -= 300
                        return score

    if isMax:
        best = -9999
        listPosiblePositions = posiblePositions(game, color)
        for step in listPosiblePositions:
            newGame = Board()
            newGame.update(curState)
            newGame.place(step, color)
            newState = newGame.getCellLineList()

            best = max(best, minimax(newState, depth - 1, alpha, beta, False))
            alpha = max(alpha, best)
            if (beta <= alpha):
                break
        # print('max:', best)
        return best
    else:
        best = 9999
        listPosiblePositions = posiblePositions(game, c_color)
        for step in listPosiblePositions:
            newGame = Board()
            newGame.update(curState)
            newGame.place(step, c_color)
            newState = newGame.getCellLineList()

            best = min(best, minimax(newState, depth - 1, alpha, beta, True))
            beta = min(beta, best)
            if (beta <= alpha):
                break
        # print('min:', best)
        return best


def findBestMove(state, depth):
    global best
    global color
    global victory_cells

    game = Board()
    game.update(state)

    bestMoveVal = -9999

    listPosiblePositions = posiblePositions(game, color)
    bestStep = listPosiblePositions[0]
    for step in listPosiblePositions:
        global best
        best = 0
        # create new game
        newGame = Board()
        newGame.update(state)
        newGame.place(step, color)
        # get state
        newState = newGame.getCellLineList()
        # get score of move
        moveVal = minimax(newState, depth, -9999, 9999, True)
        # update step
        if (moveVal > bestMoveVal):
            bestMoveVal = moveVal
            bestStep = step
    print('step:', bestStep)
    return bestStep


def callBot(game_info):
    global bot
    global competitor
    global color
    global c_color
    global victory_cells

    lines = game_info.split('\n')
    # color
    bot = lines[12]
    if (bot == 'BLACK'):
        color = 'B'
        c_color = 'W'
        competitor = 'WHITE'
    else:
        color = 'W'
        c_color = 'B'
        competitor = 'BLACK'

    victory_cells = lines[1].split(' ')
    state = lines[3:11]
    step = findBestMove(state, 2)

    if step == None:
        return "NULL"
    return step
