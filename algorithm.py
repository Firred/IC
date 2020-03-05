import numpy as np


class Board:
    def __init__(self, rows, cols):
        self.board = np.zeros((rows, cols))

    def is_inbounds(self, x, y):
        if x >= len(self.board) or x < 0:
            if y >= len(self.board[0]) or y < 0:
                return False

        return True

    def set_cell(self, x, y, value):
        if self.is_inbounds(x, y):
            self.board[x][y] = value

    def get_cell(self, x, y):
        if self.is_inbounds(x, y):
            return self.board[x][y]

    def get_size(self):
        return self.board.shape


class Cell:
    def __init__(self, father, h, g):
        self.father = father
        self.h = h
        self.g = g
        self.f = h + g

    def get_h(self):
        return self.h

    def get_g(self):
        return self.g


class AStar:
    def __init__(self, rows, cols):
        '''Ejecución del algoritmo'''
