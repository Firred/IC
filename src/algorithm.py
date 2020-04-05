import numpy as np
import queue
import utils


class Board:
    def __init__(self, rows, cols):
        self.board = np.zeros((rows, cols))

        self.goal = None
        self.start = None

    def is_inbounds(self, x, y):
        if x >= len(self.board) or x < 0:
            if y >= len(self.board[0]) or y < 0:
                return False

        return True

    def set_cell(self, x, y, value):
        if self.is_inbounds(x, y):
            self.board[x][y] = value

            if value == 0:
                if self.goal is not None and x == self.goal[0] and y == self.goal[1]:
                    self.goal = None
                elif self.start is not None and x == self.start[0] and y == self.start[1]:
                    self.start = None

            old = None

            if value == -1:
                if self.goal is not None:
                    self.board[self.goal[0]][self.goal[1]] = 0

                    if self.goal != (x, y):
                        old = self.goal

                if self.start is not None and x == self.start[0] and y == self.start[1]:
                    self.start = None

                self.goal = x, y

                return old

            if value == -2:
                if self.start is not None:
                    self.board[self.start[0]][self.start[1]] = 0

                    if self.start != (x, y):
                        old = self.start

                if self.goal is not None and x == self.goal[0] and y == self.goal[1]:
                    self.goal = None

                self.start = x, y

                return old

        return None

    def get_cell(self, x, y):
        if self.is_inbounds(x, y):
            return self.board[x][y]

    def get_size(self):
        return self.board.shape

    def get_cells(self, min_row, max_row, min_col, max_col):
        if min_row < 0:
            min_row = 0

        if min_col < 0:
            min_col = 0

        return self.board[min_row:max_row, min_col:max_col]

    def get_adjacents(self, pos):
        row, col = pos
        return np.copy(self.get_cells(row - 1, row + 2, col - 1, col + 2))

    def get_goal(self):
        return self.goal

    def get_start(self):
        return self.start


class Cell:
    def __init__(self, pos, **kwargs):
        self.g = 0
        self.pos = np.array(pos)

        if 'father' in kwargs:
            self.father = kwargs['father']

            self.g = self.father.get_g() + utils.calculate_dist(self.father.get_pos(), self.pos)
        else:
            self.father = None

        if 'h' in kwargs:
            self.h = kwargs['h']
        else:
            self.h = 0

        self.pos = np.array(pos)
        self.f = self.h + self.g

    def set_h(self, h):
        self.h = h
        self.f = self.h + self.g

    def set_g(self, g):
        self.g = g
        self.f = self.h + self.g

    def get_h(self):
        return self.h

    def get_g(self):
        return self.g

    def get_f(self):
        return self.f

    def get_pos(self):
        return self.pos

    def get_father(self):
        return self.father

    def __repr__(self):
        return str(self.pos) + " father: " + ("None " if self.father is None else str(self.father.get_pos())) \
               + " h: " + str(self.h) + " g: " + str(self.g) + " f: " + str(self.f)


class AStar:
    def __init__(self, board):
        self.board = board

    def set_board(self, board):
        self.board = board

    def get_board(self):
        return self.board

    def exec(self):
        goal = self.board.get_goal()
        start = self.board.get_start()

        if goal is None or start is None:
            return -1

        h = utils.calculate_dist(goal, start)

        current = Cell(self.board.get_start(), h=h)
        goal = tuple(self.board.get_goal())

        open_list = []
        close_list = {tuple(current.get_pos()): current}

        last_insert = tuple(current.get_pos())

        adj = self.board.get_adjacents(current.get_pos())
        cells = get_adj_cells(adj, current, -1 if last_insert[0] == 0 else 0, -1 if last_insert[1] == 0 else 0)
        calculate_h(cells, goal)

        open_list.extend(cells)

        while last_insert != goal and len(open_list) != 0:
            open_list.sort(key=lambda c: c.get_f(), reverse=True)

            current = open_list.pop()
            close_list[tuple(current.get_pos())] = current
            last_insert = tuple(current.get_pos())

            adj = self.board.get_adjacents(current.get_pos())
            cells = get_adj_cells(adj, current, -1 if last_insert[0] == 0 else 0, -1 if last_insert[1] == 0 else 0)

            cells = discard_closed_cells(close_list, open_list, cells)

            calculate_h(cells, goal)

            open_list.extend(cells)

        if last_insert == goal:
            path = get_path(close_list[last_insert])
        else:
            path = None

        return path, goal, start

    def add_start(self, x, y):
        return self.board.set_cell(x, y, -2)

    def add_goal(self, x, y):
        return self.board.set_cell(x, y, -1)

    def add_obstacle(self, x, y):
        return self.board.set_cell(x, y, 1)

    def clear_cell(self, x, y):
        return self.board.set_cell(x, y, 0)


def get_path(cell):
    current = cell
    path = queue.LifoQueue()

    while current is not None:
        path.put(current.get_pos())

        current = current.get_father()

    return path


def calculate_h(cells, goal):
    for cell in cells:
        cell.set_h(utils.calculate_dist(cell.pos, goal))


def calculate_g(cell):
    cell.set_g(cell.get)


''' rows and cols indicates whenever cell collides with the limits of the board.
    rows/cols=0 means no limits, 
    =-1 means that the 'upper'/'left' row/col is out bounds 
    and =1 means that the 'lower'/'right' row/col is out bounds
'''


def get_adj_cells(board, cell, rows=0, cols=0):
    """Internal function"""
    pos = cell.get_pos()

    if rows == -1:
        x = 0
        i = 0
    else:
        x = 1
        i = -1

    if cols == -1:
        y = 0
        reset_j = 0
    else:
        y = 1
        reset_j = -1

    board[x][y] = 1
    cells = []

    for row in board:
        j = reset_j

        for col in row:
            if col != 1:
                cells.append(Cell(pos + (i, j), father=cell))

            j += 1
        i += 1

    return cells


def discard_closed_cells(closed_list, open_list, cells):
    new_list = []

    for cell in cells:
        if tuple(cell.get_pos()) not in closed_list:
            if tuple(cell.get_pos()) in open_list:
                print("ya existe: " + str(cell.get_pos()))

            new_list.append(cell)

    return new_list
