#!/usr/bin/python

import pygame
import pymunk
import pymunk.pygame_util
import random

from gresource import *
from brick_data import *

BALL_COLLISION_TYPE = 1
BRICK_COLLISION_TYPE = 2
WALL_COLLISION_TYPE = 3
BAR_COLLISION_TYPE = 4
BOTTOM_COLLISION_TYPE = 5

class ball_object :
    LEFT_DIR = 0
    RIGHT_DIR = 1

    def __init__(self, pos, dir = LEFT_DIR, radius = 10) :
        self.body = pymunk.Body()
        self.body.position = pos

        self.shape = pymunk.Circle(self.body, radius)
        self.shape.density = 1
        self.shape.elasticity = 1
        self.shape.collision_type = BALL_COLLISION_TYPE

        if dir == self.LEFT_DIR :
            self.set_velociy(random.randrange(-400, 0), 200)
        else :
            self.set_velociy(random.randrange(0, 400), 200)

    def set_position(self, pos) :
        self.body.position = pos

    def set_velociy(self, vel_x, vel_y) :
        self.body.velocity = (vel_x, vel_y)

    def draw(self) :
        center = self.body.local_to_world((0, 0))
        pygame.draw.circle(gctrl.surface, COLOR_BLUE, center, 10)

class wall_object :
    def __init__(self, pos1, pos2, collision_type = None, radius = 2) :
        self.body = pymunk.Body(body_type = pymunk.Body.STATIC)
        self.shape = pymunk.Segment(self.body, pos1, pos2, radius)
        self.shape.elasticity = 1
        if collision_type != None :
            self.shape.collision_type = collision_type

    def draw(self) :
        pos_a = self.body.local_to_world(self.shape.a)
        pos_b = self.body.local_to_world(self.shape.b)
        pygame.draw.line(gctrl.surface, COLOR_WHITE, pos_a, pos_b, 4)            

class bar_object :
    def __init__(self, pos1, pos2, collision_type = None, radius = 4) :
        self.body = pymunk.Body(body_type = pymunk.Body.KINEMATIC)
        self.shape = pymunk.Segment(self.body, pos1, pos2, radius)
        self.shape.density = 1
        self.shape.elasticity = 1
        if collision_type != None :
            self.shape.collision_type = collision_type

    def set_velociy(self, vel_x, vel_y) :
        self.body.velocity = (vel_x, vel_y)
        
    def get_position_a(self) :
        return self.body.local_to_world(self.shape.a)

    def get_position_b(self) :
        return self.body.local_to_world(self.shape.b)
    
    def get_position_center(self) :
        (x1, y1) = self.get_position_a()
        (x2, y2) = self.get_position_b()
        x = (x1 + x2) / 2
        y = (y1 + y2) / 2
        return (x, y)

    def coll_begin(self, arbiter, space, data) :
        self.set_velociy(0, 0)

        return False

    def draw(self) :
        pos_a = self.body.local_to_world(self.shape.a)
        pos_b = self.body.local_to_world(self.shape.b)
        pygame.draw.line(gctrl.surface, COLOR_PURPLE, pos_a, pos_b, 8)  

brick_color = [
    COLOR_RED,
    COLOR_ORANGE,
    COLOR_MAGENTA,
    COLOR_GREEN,
]

class brick_object :
    def __init__(self, pos, width = 40, height= 20, life = 3) :
        self.body = pymunk.Body(body_type = pymunk.Body.STATIC)
        self.body.position = pos
        self.shape = pymunk.Poly.create_box(self.body, (width, height))
        self.shape.density = 1
        self.shape.elasticity = 1
        self.shape.collision_type = BRICK_COLLISION_TYPE
        self.rect = pygame.Rect(0, 0, width, height)
        self.life = life

    def draw(self) :
        vertices = self.shape.get_vertices()
        self.rect.topleft = self.body.local_to_world(vertices[3])
        self.rect.bottomright = self.body.local_to_world(vertices[1])
        #print(self.rect)
        pygame.draw.rect(gctrl.surface, brick_color[self.life], self.rect, 0, 1)
        pygame.draw.rect(gctrl.surface, COLOR_WHITE, self.rect, 1, 1)

BRICK_XOFFSET = 40
BRICK_YOFFSET = 120
BRICK_HEIGHT = 20

class brick_group :
    def __init__(self, col, row, brick_data) :
        brick_sx = BRICK_XOFFSET
        brick_sy = BRICK_YOFFSET

        brick_col_num = col
        brick_row_num = row
        brick_width = (gctrl.width - brick_sx * 2) / (brick_col_num - 1)
        brick_height = BRICK_HEIGHT

        self.bricks = []
        for y in range(brick_row_num) :
            for x in range(brick_col_num) :
                life = brick_data[y][x]
                if life > 0 :
                    self.bricks.append(brick_object((brick_sx, brick_sy), brick_width, brick_height, life))
                brick_sx += brick_width
            brick_sy += brick_height
            brick_sx = BRICK_XOFFSET

    def remove(self, shape) :
        for i, brick in enumerate(self.bricks) :
            if brick.body == shape.body :
                brick.life -= 1
                if brick.life == 0 :
                    self.bricks.remove(brick)

                    return True
                break

        return False

    def is_clear(self) :
        if len(self.bricks) == 0 :
            return True
        else :
            return False

    def draw(self) :
        for brick in self.bricks :
            brick.draw()

if __name__ == '__main__' :
    print('pymunk object')