#!/usr/bin/python

import sys
import numpy as np

action = {'w': 0, 'a': 1, 's': 2, 'd': 3}


class Game2048:
    def __init__(self, size=4):
        self._size = size
        self._grid = np.zeros((size, size)) + np.nan
        self.score = 0
        self.status = 'running'

        self._add_random_tile()
        self._add_random_tile()

    @property
    def grid(self):
        grid = self._grid.copy()
        grid[np.isnan(grid)] = 0
        return grid

    @grid.setter
    def grid(self, new_grid):
        grid = np.array(new_grid).astype(float)
        grid[grid == 0] = np.nan
        self._grid = grid
        self.score = 0

    def _add_random_tile(self):
        isnan_idx = np.argwhere(np.isnan(self._grid))
        rand_idx = isnan_idx[np.random.randint(len(isnan_idx))]
        rand_val = 2 if np.random.random() < 0.5 else 4
        self._grid[rand_idx[0]][rand_idx[1]] = rand_val

    def _check_merge_available(self):
        if np.isnan(self._grid).any():
            return
        for i in range(2):
            grid = self._grid.copy()
            grid = np.rot90(grid, i)
            for row in grid:
                for idx in range(len(row) - 1):
                    if row[idx] == row[idx + 1]:
                        return
        self.status = 'end'
        print('GAME OVER')

    def _stack(self, direction):
        self._grid = np.rot90(self._grid, 1 - direction)
        self._grid = np.array([np.concatenate((x[~np.isnan(x)], x[np.isnan(x)])) for x in self._grid])  # move tiles to left
        self._grid = np.rot90(self._grid, direction - 1)
        return self._grid

    def _merge(self, direction):
        # merge tile to up
        self._grid = np.rot90(self._grid, direction)
        grid_nan = np.concatenate(([np.zeros(self._size) + np.nan], self._grid))
        nan_grid = np.concatenate((self._grid, [np.zeros(self._size) + np.nan]))
        merge = grid_nan - nan_grid
        merge[2][merge[1] == 0] = np.nan
        merge[3][merge[2] == 0] = np.nan
        self._grid[merge[1:] == 0] = self._grid[merge[1:] == 0] * 2
        self._grid[merge[:4] == 0] = np.nan

        self.score += sum(self._grid[merge[1:] == 0])
        self._grid = np.rot90(self._grid, -direction)

    def move(self, direction):
        """

        :param direction: 0: up, 1: left, 2:down, 3: right
        :return:
        """
        # 0: up, 1: left, 2:down, 3: right
        if self.status == 'end':
            return
        self._stack(direction)
        self._merge(direction)
        self._stack(direction)
        if np.isnan(self._grid).any():
            self._add_random_tile()
        self._check_merge_available()


def run():
    game = Game2048()
    while game.status == 'running':
        print(game.grid)
        game.move(action[input("Next move?\n")])
    print(game.score)


if __name__ == '__main__':
    sys.exit(run())
