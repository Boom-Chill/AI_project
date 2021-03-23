import itertools

import numpy as np


class Board:
    def __init__(self):
        self.data = np.array([['E'] * 8] * 8)
        self.data[3, 3] = self.data[4, 4] = 'W'
        self.data[3, 4] = self.data[4, 3] = 'B'

    # numeric_character: "12345678"
    # return: index of row
    def getRowId(self, numeric_character):
        return ord(numeric_character) - ord('1')

    # numeric_character: "12345678"
    # return: values of row
    def getRow(self, numeric_character):
        return self.data[self.getRowId(numeric_character), :]

    # alphabet_character: "abcdefgh"
    # return: index of column
    def getColumnId(self, alphabet_character):
        return ord(alphabet_character) - ord('a')

    # alphabet_character: "abcdefgh"
    # return: values of column
    def getColumn(self, alphabet_character):
        return self.data[:, self.getColumnId(alphabet_character)]

    # position: "^\w\d$"
    # return: value at position
    def getValue(self, position):
        alphabet_character, numeric_character = tuple(position)
        return self.data[self.getRowId(numeric_character),
                         self.getColumnId(alphabet_character)]

    # r, c: int
    # return: {True, False}
    def isOutOfRange(self, r, c):
        return (r < 0) or (r > 7) or (c < 0) or (c > 7)

    # position: "^\w\d$"
    # direction: (int, int) ~ (r, c)
    # color: {'B', 'W'}
    # return: {True, False}
    def isDirectionPlaceable(self, position, direction, color):
        if self.getValue(position) != 'E':
            return False

        alphabet_character, numeric_character = tuple(position)
        row_id = self.getRowId(numeric_character)
        column_id = self.getColumnId(alphabet_character)
        row_direction, column_direction = direction

        for i in range(1, 9):
            r = row_id + i * row_direction
            c = column_id + i * column_direction
            if self.isOutOfRange(r, c) or (self.data[r, c] == 'E'):
                return False
            if self.data[r, c] == color:
                if i == 1:
                    return False
                else:
                    return True

    # position: "^\w\d$"
    # color: {'B', 'W'}
    # return: {True, False}
    def isPlaceable(self, position, color):
        return self.isDirectionPlaceable(position, (1,  0), color) or    \
            self.isDirectionPlaceable(position, (1,  1), color) or    \
            self.isDirectionPlaceable(position, (0,  1), color) or    \
            self.isDirectionPlaceable(position, (-1,  1), color) or    \
            self.isDirectionPlaceable(position, (-1,  0), color) or    \
            self.isDirectionPlaceable(position, (-1, -1), color) or    \
            self.isDirectionPlaceable(position, (0, -1), color) or    \
            self.isDirectionPlaceable(position, (1, -1), color)

    # color: {'B', 'W'}
    # return: {True, False}
    def isPlayable(self, color):
        for (r, c) in itertools.product(list('12345678'), list('abcdefgh')):
            if self.isPlaceable(c + r, color):
                return True
        return False

    # return: (int, int) ~ (b, w)
    def getResult(self):
        b, w = 0, 0
        for (r, c) in itertools.product(range(8), range(8)):
            b += 1 if self.data[r, c] == 'B' else 0
            w += 1 if self.data[r, c] == 'W' else 0
        return b, w

    # position: "^\w\d$"
    # direction: (int, int) ~ (r, c)
    # color: {'B', 'W'}
    # return: list of cells which will change color
    def getDirectionFlips(self, position, direction, color):
        if self.getValue(position) != 'E':
            return []

        ret = []
        alphabet_character, numeric_character = tuple(position)
        row_id = self.getRowId(numeric_character)
        column_id = self.getColumnId(alphabet_character)
        row_direction, column_direction = direction

        for i in range(1, 9):
            r = row_id + i * row_direction
            c = column_id + i * column_direction
            if (r < 0) or (r > 7) or (c < 0) or (c > 7) or (self.data[r, c]
                                                            == 'E'):
                return []
            if self.data[r, c] == color:
                return ret
            ret.append((r, c))

    # position: "^\w\d$"
    # color: {'B', 'W'}
    # return: list of cells which will change color
    def getFlips(self, position, color):
        return self.getDirectionFlips(position, (1,  0), color) +    \
            self.getDirectionFlips(position, (1,  1), color) +    \
            self.getDirectionFlips(position, (0,  1), color) +    \
            self.getDirectionFlips(position, (-1,  1), color) +    \
            self.getDirectionFlips(position, (-1,  0), color) +    \
            self.getDirectionFlips(position, (-1, -1), color) +    \
            self.getDirectionFlips(position, (0, -1), color) +    \
            self.getDirectionFlips(position, (1, -1), color)

    # Assume that the 'color' player can place a piece at the 'position' cell of the board
    # color: {'B', 'W'}
    # return: list of cells which will change color
    def place(self, position, color):
        alphabet_character, numeric_character = tuple(position)
        row_id = self.getRowId(numeric_character)
        column_id = self.getColumnId(alphabet_character)

        changing_cells = self.getFlips(position, color) + [(row_id, column_id)]
        for (r, c) in changing_cells:
            self.data[r, c] = color

    # cell_lines: only lines of the 'cell' variable in the string which
    #             is returned by Game.getInfo function
    def update(self, cell_lines):
        for r in range(8):
            cells = cell_lines[r].split(' ')
            for c in range(8):
                self.data[r, c] = cells[c]

    def getCellLineList(self):
        line_list = []
        str_tmp = ""
        for r in range(8):
            for c in range(8):
                if c < 7:
                    str_tmp += self.data[r, c] + ' '
                else:
                    str_tmp += self.data[r, c]
            line_list.append(str_tmp)
            str_tmp = ""
        return line_list


class Game:
    def __init__(self):
        random_numbers = np.random.choice(64, 5, replace=False)

        self.victory_cells = [
            chr(x // 8 + ord('a')) + chr(x % 8 + ord('1'))
            for x in random_numbers
        ]
        self.board = Board()
        self.history = []
        self.winner = None

    # return: {"BLACK", "WHITE"} ~ who will play next
    def getNextTurn(self):
        return "BLACK" if len(self.history) % 2 == 0 else "WHITE"

    # return: {True, False} ~ check if the game is over
    def checkGameOver(self):
        if self.winner is not None:
            return True

        v_b, v_w = 0, 0
        for cell in self.victory_cells:
            v_b += 1 if self.board.getValue(cell) == 'B' else 0
            v_w += 1 if self.board.getValue(cell) == 'W' else 0
        if v_b == 5:
            self.winner = "BLACK"
            return True
        if v_w == 5:
            self.winner = "WHITE"
            return True

        color = 'B' if self.getNextTurn() == "BLACK" else 'W'
        if not self.board.isPlayable(color):
            b, w = self.board.getResult()
            self.winner = "BLACK" if b > w else self.winner
            self.winner = "WHITE" if b < w else self.winner
            if b == w:
                self.winner = "BLACK" if v_b > v_w else self.winner
                self.winner = "WHITE" if v_b < v_w else self.winner
                self.winner = "DRAW" if v_b == v_w else self.winner
            return True

        return False

    def setNextTurn(self, position):
        if self.checkGameOver():
            return False

        if position == "NULL":
            self.winner = "WHITE" if self.getNextTurn() == "BLACK" else 'BLACK'
            return True

        color = 'B' if self.getNextTurn() == "BLACK" else 'W'

        if not self.board.isPlaceable(position, color):
            return False

        self.board.place(position, color)
        self.history.append(position)
        self.checkGameOver()
        return True

    def getWinner(self):
        return self.winner

    def getInfo(self):
        s = ""

        s += "victory_cell\n"
        s += " ".join(self.victory_cells) + "\n"

        s += "cell\n"
        s += "\n".join(" ".join(self.board.getRow(r))
                       for r in "12345678") + "\n"

        s += "you\n"
        s += self.getNextTurn() + "\n"

        return s

    def getFinalResult(self):
        s = ""

        if not self.checkGameOver():
            return s

        s += "history\n"
        s += " ".join(self.history) + "\n"

        s += "winner\n"
        s += self.getWinner() + "\n"

        return s
