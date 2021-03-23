import unittest
import itertools

import numpy as np

from init import Board, Game


class TestBoard(unittest.TestCase):

    def test_getRowId(self):
        x = Board()
        y = ['1', '2', '3', '4', '5', '6', '7', '8']
        for i in range(8):
            self.assertEqual(x.getRowId(y[i]), i)

    def test_getRow(self):
        x = Board()
        y = ['1', '2', '3', '4', '5', '6', '7', '8']
        x.data = np.array([['B'] * 8] * 8)
        r = np.random.permutation(8)
        for i in range(8):
            x.data[i, r[i]] = 'W'
        for i in range(8):
            z = x.getRow(y[i])
            for j in range(8):
                if j == r[i]:
                    self.assertEqual(z[j], 'W')
                else:
                    self.assertEqual(z[j], 'B')

    def test_getColumnId(self):
        x = Board()
        y = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        for i in range(8):
            self.assertEqual(x.getColumnId(y[i]), i)

    def test_getColumn(self):
        x = Board()
        y = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        x.data = np.array([['B'] * 8] * 8)
        r = np.random.permutation(8)
        for i in range(8):
            x.data[r[i], i] = 'W'
        for i in range(8):
            z = x.getColumn(y[i])
            for j in range(8):
                if j == r[i]:
                    self.assertEqual(z[j], 'W')
                else:
                    self.assertEqual(z[j], 'B')

    def test_getValue(self):
        x = Board()
        x.data = np.array([['B'] * 8] * 8)
        r = np.random.choice(64, 5, replace=False)
        for i in r:
            x.data[i // 8, i % 8] = 'W'
        for i, a in enumerate(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']):
            for j, b in enumerate(['1', '2', '3', '4', '5', '6', '7', '8']):
                if i + 8 * j in r:
                    self.assertEqual(x.getValue(a + b), 'W')
                else:
                    self.assertEqual(x.getValue(a + b), 'B')

    def test_isOutOfRange(self):
        x = Board()
        for i in range(-1, 9):
            for j in range(-1, 9):
                if i < 0:
                    self.assertTrue(x.isOutOfRange(i, j))
                elif j < 0:
                    self.assertTrue(x.isOutOfRange(i, j))
                else:
                    try:
                        x.data[i, j]
                        self.assertFalse(x.isOutOfRange(i, j))
                    except:
                        self.assertTrue(x.isOutOfRange(i, j))

    def test_isDirectionPlaceable(self):
        x = Board()

        x.data = np.array([
            ['E', 'W', 'E', 'E', 'E', 'E', 'E', 'E'],
            ['E', 'B', 'W', 'E', 'E', 'E', 'E', 'E'],
            ['E', 'B', 'B', 'W', 'E', 'E', 'E', 'E'],
            ['E', 'E', 'B', 'W', 'E', 'E', 'E', 'E'],
            ['E', 'B', 'E', 'W', 'E', 'E', 'E', 'E'],
            ['E', 'B', 'E', 'B', 'W', 'E', 'E', 'E'],
            ['E', 'B', 'B', 'B', 'B', 'B', 'B', 'W'],
            ['E', 'B', 'B', 'B', 'B', 'B', 'B', 'B']
        ])
        for (r, c) in itertools.product(list('12345678'), list('abcdefgh')):
            position = c + r
            if position in ["a2", "a3", "b4", "c6", "a7"]:
                self.assertTrue(x.isDirectionPlaceable(position, (0, 1), 'W'))
            else:
                self.assertFalse(x.isDirectionPlaceable(position, (0, 1), 'W'))

    def test_isPlaceable(self):
        x = Board()

        x.data = np.array([
            ['E', 'W', 'E', 'E', 'E', 'E', 'E', 'E'],
            ['E', 'B', 'W', 'E', 'E', 'E', 'E', 'E'],
            ['E', 'B', 'B', 'W', 'E', 'E', 'E', 'E'],
            ['E', 'E', 'B', 'W', 'E', 'E', 'E', 'E'],
            ['E', 'B', 'E', 'W', 'E', 'E', 'E', 'E'],
            ['E', 'B', 'E', 'B', 'W', 'E', 'E', 'E'],
            ['E', 'B', 'B', 'B', 'B', 'B', 'B', 'W'],
            ['E', 'B', 'B', 'B', 'B', 'B', 'B', 'B']
        ])
        for (r, c) in itertools.product(list('12345678'), list('abcdefgh')):
            position = c + r
            if position in ["a1", "a2", "a3", "a4", "b4", "c5", "a6", "c6", "a7"]:
                self.assertTrue(x.isPlaceable(position, 'W'))
            else:
                self.assertFalse(x.isPlaceable(position, 'W'))

    def test_getResult(self):
        x = Board()

        x.data = np.array([
            ['E', 'W', 'E', 'E', 'E', 'E', 'E', 'E'],
            ['E', 'B', 'W', 'E', 'E', 'E', 'E', 'E'],
            ['E', 'B', 'B', 'W', 'E', 'E', 'E', 'E'],
            ['E', 'E', 'B', 'W', 'E', 'E', 'E', 'E'],
            ['E', 'B', 'E', 'W', 'E', 'E', 'E', 'E'],
            ['E', 'B', 'E', 'B', 'W', 'E', 'E', 'E'],
            ['E', 'B', 'B', 'B', 'B', 'B', 'B', 'W'],
            ['E', 'B', 'B', 'B', 'B', 'B', 'B', 'B']
        ])
        self.assertEqual(x.getResult(), (20, 7))

    def test_getDirectionFlips(self):
        x = Board()

        x.data = np.array([
            ['E', 'W', 'E', 'E', 'E', 'E', 'E', 'E'],
            ['E', 'B', 'W', 'E', 'E', 'E', 'E', 'E'],
            ['E', 'B', 'B', 'W', 'E', 'E', 'E', 'E'],
            ['E', 'E', 'B', 'W', 'E', 'E', 'E', 'E'],
            ['E', 'B', 'E', 'W', 'E', 'E', 'E', 'E'],
            ['E', 'B', 'E', 'B', 'W', 'E', 'E', 'E'],
            ['E', 'B', 'B', 'B', 'B', 'B', 'B', 'W'],
            ['E', 'B', 'B', 'B', 'B', 'B', 'B', 'B']
        ])
        for (r, c) in itertools.product(list('12345678'), list('abcdefgh')):
            position = c + r
            if position == "a2":
                self.assertEqual(set(x.getDirectionFlips(position, (0, 1), 'W')),
                                 set([(1, 1)]))
            elif position == "a3":
                self.assertEqual(set(x.getDirectionFlips(position, (0, 1), 'W')),
                                 set([(2, 1), (2, 2)]))
            elif position == "b4":
                self.assertEqual(set(x.getDirectionFlips(position, (0, 1), 'W')),
                                 set([(3, 2)]))
            elif position == "c6":
                self.assertEqual(set(x.getDirectionFlips(position, (0, 1), 'W')),
                                 set([(5, 3)]))
            elif position == "a7":
                self.assertEqual(set(x.getDirectionFlips(position, (0, 1), 'W')),
                                 set([(6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6)]))
            else:
                self.assertEqual(x.getDirectionFlips(
                    position, (0, 1), 'W'), [])

    def test_getFlips(self):
        x = Board()

        x.data = np.array([
            ['E', 'W', 'E', 'E', 'E', 'E', 'E', 'E'],
            ['E', 'B', 'W', 'E', 'E', 'E', 'E', 'E'],
            ['E', 'B', 'B', 'W', 'E', 'E', 'E', 'E'],
            ['E', 'E', 'B', 'W', 'E', 'E', 'E', 'E'],
            ['E', 'B', 'E', 'W', 'E', 'E', 'E', 'E'],
            ['E', 'B', 'E', 'B', 'W', 'E', 'E', 'E'],
            ['E', 'B', 'B', 'B', 'B', 'B', 'B', 'W'],
            ['E', 'B', 'B', 'B', 'B', 'B', 'B', 'B']
        ])
        for (r, c) in itertools.product(list('12345678'), list('abcdefgh')):
            position = c + r
            if position == "a1":
                self.assertEqual(set(x.getFlips(position, 'W')),
                                 set([(1, 1), (2, 2)]))
            elif position == "a2":
                self.assertEqual(set(x.getFlips(position, 'W')),
                                 set([(1, 1), (2, 1), (3, 2)]))
            elif position == "a3":
                self.assertEqual(set(x.getFlips(position, 'W')),
                                 set([(2, 1), (2, 2)]))
            elif position == "a4":
                self.assertEqual(set(x.getFlips(position, 'W')),
                                 set([(2, 1)]))
            elif position == "b4":
                self.assertEqual(set(x.getFlips(position, 'W')),
                                 set([(3, 2), (1, 1), (2, 1)]))
            elif position == "c5":
                self.assertEqual(set(x.getFlips(position, 'W')),
                                 set([(2, 2), (3, 2)]))
            elif position == "a6":
                self.assertEqual(set(x.getFlips(position, 'W')),
                                 set([(4, 1), (3, 2)]))
            elif position == "c6":
                self.assertEqual(set(x.getFlips(position, 'W')),
                                 set([(5, 3)]))
            elif position == "a7":
                self.assertEqual(set(x.getFlips(position, 'W')),
                                 set([(6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6)]))
            else:
                self.assertEqual(x.getFlips(position, 'W'), [])

    def test_place(self):
        x = Board()
        y = Board()

        x.data = np.array([
            ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
            ['B', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
            ['E', 'B', 'E', 'E', 'E', 'E', 'E', 'E'],
            ['E', 'E', 'B', 'E', 'B', 'E', 'E', 'E'],
            ['W', 'B', 'B', 'E', 'W', 'E', 'E', 'E'],
            ['E', 'E', 'E', 'B', 'B', 'E', 'E', 'E'],
            ['E', 'B', 'E', 'E', 'E', 'W', 'E', 'E'],
            ['W', 'E', 'E', 'W', 'E', 'E', 'E', 'E']
        ])
        y.data = np.array([
            ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
            ['B', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
            ['E', 'B', 'E', 'E', 'E', 'E', 'E', 'E'],
            ['E', 'E', 'B', 'E', 'B', 'E', 'E', 'E'],
            ['W', 'W', 'W', 'W', 'W', 'E', 'E', 'E'],
            ['E', 'E', 'E', 'B', 'W', 'E', 'E', 'E'],
            ['E', 'B', 'E', 'E', 'E', 'W', 'E', 'E'],
            ['W', 'E', 'E', 'W', 'E', 'E', 'E', 'E']
        ])
        x.place("d5", 'W')
        self.assertTrue(np.array_equal(x.data, y.data))

    def test_update(self):
        x = Board()
        y = Board()

        x.update([
            "E E E E E E E E",
            "B E E E E E E E",
            "E B E E E E E E",
            "E E B E B E E E",
            "W B B E W E E E",
            "E E E B B E E E",
            "E B E E E W E E",
            "W E E W E E E E"
        ])
        y.data = np.array([
            ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
            ['B', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
            ['E', 'B', 'E', 'E', 'E', 'E', 'E', 'E'],
            ['E', 'E', 'B', 'E', 'B', 'E', 'E', 'E'],
            ['W', 'B', 'B', 'E', 'W', 'E', 'E', 'E'],
            ['E', 'E', 'E', 'B', 'B', 'E', 'E', 'E'],
            ['E', 'B', 'E', 'E', 'E', 'W', 'E', 'E'],
            ['W', 'E', 'E', 'W', 'E', 'E', 'E', 'E']
        ])
        self.assertTrue(np.array_equal(x.data, y.data))


class TestGame(unittest.TestCase):

    def test_getNextTurn(self):
        x = Game()
        self.assertEqual(x.getNextTurn(), "BLACK")
        x.history.append("a1")
        self.assertEqual(x.getNextTurn(), "WHITE")
        x.history.append("b1")
        self.assertEqual(x.getNextTurn(), "BLACK")
        x.history.append("c1")
        self.assertEqual(x.getNextTurn(), "WHITE")
        x.history.append("d1")
        self.assertEqual(x.getNextTurn(), "BLACK")

    def test_checkGameOver(self):
        x = Game()
        self.assertFalse(x.checkGameOver())

        x = Game()
        for i in x.victory_cells:
            x.board.data[x.board.getRowId(
                i[1]), x.board.getColumnId(i[0])] = 'W'
        self.assertTrue(x.checkGameOver())
        self.assertEqual(x.getWinner(), "WHITE")

        x = Game()
        for i in x.victory_cells:
            x.board.data[x.board.getRowId(
                i[1]), x.board.getColumnId(i[0])] = 'B'
        self.assertTrue(x.checkGameOver())
        self.assertEqual(x.getWinner(), "BLACK")

        x = Game()
        for (i, j) in itertools.product(range(8), range(8)):
            if i in range(0, 3):
                x.board.data[i, j] = 'W'
            if i in range(3, 5):
                x.board.data[i, j] = 'E'
            if i in range(5, 8):
                x.board.data[i, j] = 'B'
        x.victory_cells = ["a4", "a5", "b4", "b5", "c4"]
        self.assertTrue(x.checkGameOver())
        self.assertEqual(x.getWinner(), "DRAW")
        x.winner = None
        x.board.data[3, 7] = 'W'
        self.assertTrue(x.checkGameOver())
        self.assertEqual(x.getWinner(), "WHITE")
        x.winner = None
        x.board.data[3, 6] = 'W'
        x.board.data[4, 1] = 'B'
        self.assertTrue(x.checkGameOver())
        self.assertEqual(x.getWinner(), "WHITE")
        x.winner = None
        x.board.data[4, 7] = 'B'
        self.assertTrue(x.checkGameOver())
        self.assertEqual(x.getWinner(), "BLACK")

    def test_setNextTurn(self):
        x = Game()
        y = Board()

        x.winner = "DRAW"
        self.assertFalse(x.setNextTurn("d3"))
        x.winner = None
        self.assertTrue(x.setNextTurn("d3"))
        y.data = np.array([
            ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
            ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
            ['E', 'E', 'E', 'B', 'E', 'E', 'E', 'E'],
            ['E', 'E', 'E', 'B', 'B', 'E', 'E', 'E'],
            ['E', 'E', 'E', 'B', 'W', 'E', 'E', 'E'],
            ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
            ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
            ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E']
        ])
        self.assertTrue(np.array_equal(x.board.data, y.data))
        self.assertEqual(x.history, ["d3"])
        self.assertFalse(x.setNextTurn("e6"))
        self.assertTrue(x.setNextTurn("NULL"))
        self.assertEqual(x.getWinner(), "BLACK")


if __name__ == '__main__':
    unittest.main()
