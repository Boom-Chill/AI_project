import itertools
import random

from init import Board

UNStable_lst = [
    'a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'b1', 'b2', 'b3', 'b4',
    'b5', 'b6', 'b7', 'b8', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8',
    'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'e1', 'e2', 'e3', 'e4',
    'e5', 'e6', 'e7', 'e8', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8',
    'g1', 'g2', 'g3', 'g4', 'g5', 'g6', 'g7', 'g8', 'h1', 'h2', 'h3', 'h4',
    'h5', 'h6', 'h7', 'h8'
]
stable_lst = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]

corner = ['a1', 'a8', 'h1', 'h8']

h_weight = [[120, -20, 20, 5, 5, 20, -20, 120],
            [-20, -40, -5, -5, -5, -5, -40, -20],
            [20, -5, 15, 3, 3, 15, -5, 20], [5, -5, 3, 3, 3, 3, -5, 5],
            [5, -5, 3, 3, 3, 3, -5, 5], [20, -5, 15, 3, 3, 15, -5, 20],
            [-20, -40, -5, -5, -5, -5, -40, -20],
            [120, -20, 20, 5, 5, 20, -20, 120]]


def getRowId(numeric_character):
    return ord(numeric_character) - ord('1')


def getColumnId(alphabet_character):
    return ord(alphabet_character) - ord('a')


def getTakenVCell(victory_cell, cell):
    v_b = v_w = 0
    for c in victory_cell:
        if cell.getValue(c) == 'W':
            v_b += 1
        if cell.getValue(c) == 'B':
            v_w += 1
    return v_b, v_w


def getWeightSquares(cell, color):
    cell_lines = cell.getCellLineList()
    total = 0
    for i in range(8):
        cell_lines[i] = cell_lines[i].replace(' ', '')
        for j in range(8):
            if cell_lines[i][j] == color:
                total += h_weight[i][j]
            elif cell_lines[i][j] != 'E':
                total -= h_weight[i][j]
    return total


def stableCount(cell, color):
    count = 0
    unstable_list_fake = UNStable_lst.copy()
    stable_lst_fake = stable_lst.copy()
    for i in range(len(unstable_list_fake)):
        stable = False
        if cell.getValue(unstable_list_fake[i]) == color:
            stable = isStableVertical(unstable_list_fake[i], stable_lst_fake) and \
                isStableHorizontal(unstable_list_fake[i], stable_lst_fake) and \
                isStableLeftDiagonal(unstable_list_fake[i], stable_lst_fake) and \
                isStableRightDiagonal(unstable_list_fake[i], stable_lst_fake)
            if stable:
                alphabet_character, numeric_character = tuple(
                    unstable_list_fake[i])
                stable_lst_fake[getRowId(numeric_character)][getColumnId(
                    alphabet_character)] = 1
                count += 1
    return count


def isStableLeftDiagonal(position, stable_lst_fake):
    alphabet_character, numeric_character = tuple(position)
    rowUP = getRowId(numeric_character) + 1
    rowDown = getRowId(numeric_character) - 1
    colUp = getColumnId(alphabet_character) + 1
    colDown = getColumnId(alphabet_character) - 1

    if (rowDown < 0 or colDown < 0):
        return True
    if (rowUP > 7 or colUp > 7):
        return True
    if (stable_lst_fake[rowDown][colDown]
            == 1) or (stable_lst_fake[rowUP][colUp] == 1):
        return True
    return False


def isStableRightDiagonal(position, stable_lst_fake):
    alphabet_character, numeric_character = tuple(position)
    rowUP = getRowId(numeric_character) + 1
    rowDown = getRowId(numeric_character) - 1
    colUp = getColumnId(alphabet_character) + 1
    colDown = getColumnId(alphabet_character) - 1

    if (rowDown < 0 or colUp > 7):
        return True
    if (rowUP > 7 or colDown < 0):
        return True
    if (stable_lst_fake[rowDown][colUp]
            == 1) or (stable_lst_fake[rowUP][colDown] == 1):
        return True
    return False


def isStableVertical(position, stable_lst_fake):
    alphabet_character, numeric_character = tuple(position)
    rowUP = getRowId(numeric_character) + 1
    rowDown = getRowId(numeric_character) - 1
    col = getColumnId(alphabet_character)

    if (rowDown < 0):
        return True
    if (rowUP > 7):
        return True
    if (stable_lst_fake[rowDown][col] == 1) or (stable_lst_fake[rowUP][col]
                                                == 1):
        return True
    return False


def isStableHorizontal(position, stable_lst_fake):
    alphabet_character, numeric_character = tuple(position)
    row = getRowId(numeric_character)
    colUp = getColumnId(alphabet_character) + 1
    colDown = getColumnId(alphabet_character) - 1

    if (colUp > 7):
        return True
    if (colDown < 0):
        return True
    if (stable_lst_fake[row][colUp] == 1) or (stable_lst_fake[row][colDown]
                                              == 1):
        return True
    return False


def is_end(victory_cells, cell, color):
    v_b = v_w = 0
    count = 0

    v_b, v_w = getTakenVCell(victory_cells, cell)
    if v_b == 5:
        return "BLACK"
    if v_w == 5:
        return "WHITE"

    if count == 5:
        if v_w > v_b:
            return "WHITE"
        return "BLACK"

    check_playable = cell.isPlayable(color)
    if not check_playable:
        return "BLACK" if color == 'B' else 'WHITE'
    return None


def Heuristic(victory_cell, cell, color, max=True):
    op_color = 'W' if color != 'W' else 'B'
    cornerv, op_cornerv = 0, 0
    my_stb = stableCount(cell, color)
    op_stb = stableCount(cell, op_color)
    hstep = 0
    hcorner = 0
    hcoin = 0
    hstb = 0
    hweight = getWeightSquares(cell, color)

    if color == 'W':
        coinv, op_coinv = getTakenVCell(victory_cell, cell)
    else:
        op_coinv, coinv = getTakenVCell(victory_cell, cell)
    if coinv + op_coinv != 0:
        hcoin = 100 * (coinv - op_coinv) / (coinv + op_coinv)
        if hcoin != 100 and hcoin != -100:
            hcoin = 0
    stepv = validSteps(cell, color)
    op_stepv = validSteps(cell, op_color)

    cornerv = len(set(corner) & set(stepv))
    op_cornerv = len(set(corner) & set(op_stepv))

    if len(stepv) + len(op_stepv) != 0:
        hstep = 100 * (len(stepv) - len(op_stepv)) / \
            (len(stepv) + len(op_stepv))
        if hstep == 100 or hstep == -100:
            hstep *= 11 / 4
    if cornerv + op_cornerv != 0:
        hcorner = 100 * (cornerv - op_cornerv) / (cornerv + op_cornerv)
    if my_stb + op_stb != 0:
        hstb = 100 * (my_stb - op_stb) / (my_stb + op_stb)

    score = 4 * hstep + hweight + hcorner * 10 + 8 * hstb + 5 * hcoin
    score = -score if not max else score
    return score, None, None


def maxBot(victory_cell, cell_line, you, alpha, beta, depth):
    cell = Board()
    cell.update(cell_line)

    color = 'W' if you == "BLACK" else 'B'
    result = is_end(victory_cell, cell, color)
    if depth == 0 or result != None and result != you:
        return Heuristic(victory_cell, cell, color)
    # elif result != None and result != you:
    #     return -999998, None, None
    elif result == you:
        return 999998, None, None

    maxv = -999999

    px = None
    py = None
    cur_weight = getWeightSquares(cell, color)

    for (x, y) in itertools.product(list('12345678'), list('abcdefgh')):
        if cell.isPlaceable(y + x, color):
            new_cell = Board()
            new_cell.update(cell_line)
            new_cell.place(y + x, color)

            new_state = new_cell.getCellLineList()
            competitior = 'BLACK' if you != "BLACK" else 'WHITE'
            (m, min_x, min_y) = minBot(victory_cell, new_state, competitior,
                                       alpha, beta, depth - 1)
            m += cur_weight
            if m > maxv:
                maxv = m
                px = x
                py = y
            if maxv >= beta:
                return (maxv, px, py)

            if maxv > alpha:
                alpha = maxv
    return maxv, px, py


def minBot(victory_cell, cell_line, you, alpha, beta, depth):
    cell = Board()
    cell.update(cell_line)

    color = 'W' if you == "BLACK" else 'B'
    result = is_end(victory_cell, cell, color)
    if depth == 0 or result != None and result != you:
        return Heuristic(victory_cell, cell, color, False)
    # elif result != None and result != you:
    #     return 999998, None, None
    elif result == you:
        return -999998, None, None

    minv = 999999

    px = None
    py = None
    cur_weight = getWeightSquares(cell, color)

    for (x, y) in itertools.product(list('12345678'), list('abcdefgh')):
        if cell.isPlaceable(y + x, color):
            new_cell = Board()
            new_cell.update(cell_line)
            new_cell.place(y + x, color)

            new_state = new_cell.getCellLineList()
            competitior = 'BLACK' if you != "BLACK" else 'WHITE'
            (m, max_x, max_y) = maxBot(victory_cell, new_state, competitior,
                                       alpha, beta, depth - 1)
            m -= cur_weight
            if m < minv:
                minv = m
                px = x
                py = y
            if minv <= alpha:
                return (minv, px, py)

            if minv < beta:
                beta = minv
    return minv, px, py


def callBot(game_info):
    lines = game_info.split('\n')
    victory_cell = lines[1].split(' ')
    you = lines[-2]
    lines = lines[3:11]
    (m, px, py) = maxBot(victory_cell, lines, you, -999999, 999999, 2)
    if px == None or py == None:
        return "NULL"
    return py + px


def validSteps(cell, color):
    posible_positions = []
    for (r, c) in itertools.product(list('12345678'), list('abcdefgh')):
        if cell.isPlaceable(c + r, color):
            posible_positions.append(c + r)
    return posible_positions
