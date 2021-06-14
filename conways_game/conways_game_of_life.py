"""
class ConwaysGame
    It is made up from a set of rules,
    an initial state and a maximum size (width and height).
    The game is started by calling the run_game function and specifying the maximum number of iterations.
"""

from io import BytesIO as bio
import PIL.Image
import numpy as np
from abc import ABC, abstractmethod
from copy import copy
import matplotlib.pyplot as plt
import matplotlib
import time


class Game:
    def __init__(self, initial_state, rules,max_size):
        self.initial_state = initial_state
        self.rules = rules
        self.max_size = max_size
    def run_game(self, it):
        state = self.initial_state
        previous_state = None
        progression = []
        i = 0
        while (not state.equals(previous_state) and i < it):
            i += 1
            previous_state = state.copy()
            progression.append(previous_state.grid)
            state = state.apply_rules(self.rules,self.max_size)
        progression.append(state.grid)
        return progression

class State(ABC):
    @abstractmethod
    def copy(self):
        pass

    @abstractmethod
    def apply_rules(self, rules, max_size):
        pass

    @abstractmethod
    def equals(self, other):
        pass

    @abstractmethod
    def get_neighbours(self, elem, max_size):
        pass


class DenseNumpyState(State):
    def __init__(self, grid):
        self.grid = grid

    def copy(self):
        return DenseNumpyState(np.copy(self.grid))

    def equals(self, other):
        if other is None:
            return False
        return np.array_equal(self.grid, other.grid)

    def apply_rules(self, rules, max_size,):
        self.grid = rules.apply_rules(self.grid, max_size, self.get_neighbours)
        return self

    def get_neighbours(self, elem, max_size):
        l = []
        if elem[0]-1 >= 0:
            l.append((elem[0]-1, elem[1]))
        if elem[0]-1 >= 0 and elem[1]-1 >= 0:
            l.append((elem[0]-1, elem[1]-1))
        if elem[0]-1 >= 0 and elem[1]+1 < max_size:
            l.append((elem[0]-1, elem[1]+1))
        if elem[1]-1 >= 0:
            l.append((elem[0], elem[1]-1))
        if elem[1]-1 >= 0 and elem[0]+1 < max_size:
            l.append((elem[0]+1, elem[1]-1))
        if elem[1]+1 < max_size:
            l.append((elem[0], elem[1]+1))
        if elem[0]+1 < max_size:
            l.append((elem[0]+1, elem[1]))
        if elem[1]+1 < max_size and elem[0]+1 < max_size:
            l.append((elem[0]+1, elem[1]+1))
        return l


class SparseSetState(State):
    def __init__(self, grid):
        self.grid = grid

    def copy(self):
        return SparseSetState(copy(self.grid))

    def get_neighbours(self, elem, max_size):
        # Returns the neighbours of a live cell if they lie within the bounds of the grid specified by max_size
        l = []
        if elem[0]-1 >= 0:
            l.append((elem[0]-1, elem[1]))
        if elem[0]-1 >= 0 and elem[1]-1 >= 0:
            l.append((elem[0]-1, elem[1]-1))
        if elem[0]-1 >= 0 and elem[1]+1 < max_size:
            l.append((elem[0]-1, elem[1]+1))
        if elem[1]-1 >= 0:
            l.append((elem[0], elem[1]-1))
        if elem[1]-1 >= 0 and elem[0]+1 < max_size:
            l.append((elem[0]+1, elem[1]-1))
        if elem[1]+1 < max_size:
            l.append((elem[0], elem[1]+1))
        if elem[0]+1 < max_size:
            l.append((elem[0]+1, elem[1]))
        if elem[1]+1 < max_size and elem[0]+1 < max_size:
            l.append((elem[0]+1, elem[1]+1))
        return l

    def equals(self, other):
        if other is None:
            return False
        return self.grid == other.grid

    def apply_rules(self, rules, max_size):
        # Calls the actual rules and provides them with the grid and the neighbour function
        self.grid = rules.apply_rules(self.grid, max_size, self.get_neighbours)
        return self

class Rule(ABC):
    @abstractmethod
    def apply_rules(self, grid, max_size, get_neighbours):
        pass


class DenseNumpyRules(Rule):
    def apply_rules(self, grid, max_size, get_neighbours):
        #copied_state = state.copy()
        #grid = state.grid

        grid_ret = copy(grid)
        for i in range(grid.shape[0]):
            for j in range(grid.shape[1]):
                nb = get_neighbours((i, j), max_size)
                counter = 0
                for n in nb:
                    if grid[n] == True:
                        counter += 1
                if (counter < 2 or counter > 3):
                    grid_ret[i][j] = False
                if (counter == 3):
                    grid_ret[i][j] = True
        return grid_ret


class SparseSetRules(Rule):
    def apply_rules(self, grid, max_size, get_neighbours):
        #grid = state.grid
        counter = {}
        for elem in grid:
            if elem not in counter:
                counter[elem] = 0
            nb = get_neighbours(elem, max_size)
            for n in nb:
                if n not in counter:
                    counter[n] = 1
                else:
                    counter[n] += 1
        for c in counter:
            if (counter[c] < 2 or counter[c] > 3):
                grid.discard(c)
            if counter[c] == 3:
                grid.add(c)
        return grid




if __name__ == '__main__':
    MAX_ITER = 1500
    MAX_SIZE = 80
    board = {(39, 40), (39, 41), (40, 39), (40, 40), (41, 40)}
    rules = SparseSetRules()
    game = Game(SparseSetState(board), rules, MAX_SIZE)
    t = time.time()
    rw = game.run_game(MAX_ITER)
    print(time.time() - t)
