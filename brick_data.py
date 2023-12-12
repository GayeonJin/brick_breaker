#!/usr/bin/python

import sys
import csv

BRICK_COLS = 9
BRICK_ROWS = 8

brick_data_example0 = [
#    [0, 0, 0, 0, 1, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1],            
]

brick_data_example1 = [
    [1, 2, 2, 3, 3, 3, 2, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1],            
]

brick_data_example2 = [
    [2, 2, 2, 3, 3, 3, 3, 3, 3],
    [2, 2, 3, 3, 3, 3, 3, 3, 3],
    [2, 3, 3, 3, 0, 3, 3, 3, 3],
    [2, 3, 3, 0, 0, 0, 3, 3, 3],
    [2, 2, 3, 0, 0, 0, 3, 3, 3],
    [2, 2, 2, 3, 0, 3, 3, 3, 3],
    [2, 2, 2, 2, 3, 3, 3, 3, 3],
    [1, 1, 1, 1, 1, 3, 3, 3, 3],            
]

class brick_stage :
    def __init__(self) :
        self.db = {}

    def add(self, stage, brick_data) :
        self.db[stage] = brick_data

    def get(self, stage) :
        return self.db[stage]

class brick_data :
    def __init__(self) :
        self.stage_data = brick_stage()

    def load_file(self, filename = 'brick_data.csv') :
        file = open(filename, 'r')
        rows = csv.reader(file)

        bricks = []
        for row in rows :
            if row == [] :
                if len(bricks) > 0 :
                    self.stage_data.add(stage, bricks)
                    # print(bricks)
                continue
            if '#' in row[0] and 'Stage' in row[0] :
                stage = int(row[1])
                bricks = []
                # print('STAGE : ', stage)
            else :
                row_data = []
                for value in row :
                    row_data.append(int(value))

                bricks.append(row_data)

if __name__ == '__main__' :
    print('brick stage')
    bricks = brick_stage()
    bricks.add(0, brick_data_example0)
    bricks.add(1, brick_data_example1)
    bricks.add(2, brick_data_example2)
    data = bricks.get(1)
    print(data)

    print('brick data')
    br_data = brick_data()
    br_data.load_file()