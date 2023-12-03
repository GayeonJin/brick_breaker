#!/usr/bin/python

import sys

BRICK_COLS = 9
BRICK_ROWS = 8

brick_data_example1 = [
    [2, 2, 2, 3, 3, 3, 3, 3, 3],
    [2, 2, 3, 3, 3, 3, 3, 3, 3],
    [2, 3, 3, 3, 0, 3, 3, 3, 3],
    [2, 3, 3, 0, 0, 0, 3, 3, 3],
    [2, 2, 3, 0, 0, 0, 3, 3, 3],
    [2, 2, 2, 3, 0, 3, 3, 3, 3],
    [2, 2, 2, 2, 3, 3, 3, 3, 3],
    [1, 1, 1, 1, 1, 3, 3, 3, 3],            
]

class brick_data :
    def __init__(self, rows = BRICK_ROWS, cols = BRICK_COLS) :
        self.rows = rows
        self.cols = cols

        self.bricks = []
        for y in range(self.rows) :
            row_data = []
            for x in range(self.cols) :
                row_data.append(0)

            self.bricks.append(row_data)

        self.load(brick_data_example1)

    def load(self, data_array) :
        for y in range(self.rows) :
            for x in range(self.cols) :
                self.bricks[y][x] = data_array[y][x]

        print(self.bricks)

if __name__ == '__main__' :
    print('brick_data')
    bricks = brick_data()