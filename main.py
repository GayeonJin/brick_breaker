#!/usr/bin/python

import os
import sys
import csv

import pygame
import pymunk
import pymunk.pygame_util
import random
from time import sleep

from gobject import *
from gresource import *

TITLE_STR = "Brick Breaker"

SCORE_UNIT1 = 10
SCORE_UNIT2 = 30

STATUS_XOFFSET = 10
STATUS_YOFFSET = 10
STATUS_HEIGHT = 40

INFO_HEIGHT = 40
INFO_OFFSET = 10
INFO_FONT = 14

BRICK_XOFFSET = 40
BRICK_YOFFSET = 120
BRICK_HEIGHT = 20

BAR_YOFFSET = 30
BAR_WIDTH = 60

def draw_info() :
    font = pygame.font.SysFont('Verdana', INFO_FONT)
    info = font.render('F1/F2 : Load/Save file    space : toggle', True, COLOR_BLACK)

    pygame.draw.rect(gctrl.surface, COLOR_PURPLE, (0, gctrl.height - INFO_HEIGHT, gctrl.width, INFO_HEIGHT))
    gctrl.surface.blit(info, (INFO_OFFSET * 2, gctrl.height - 2 * INFO_FONT - INFO_OFFSET)) 

def draw_score(count) :
    gctrl.draw_string("Score : " + str(count), STATUS_XOFFSET, STATUS_YOFFSET, ALIGN_LEFT)

def draw_message(str) :
    gctrl.draw_string(str, 0, 0, ALIGN_CENTER, 40, COLOR_BLACK)
       
    pygame.display.update()
    sleep(2)

def terminate() :
    pygame.quit()
    sys.exit()

def start_game() :
    global score

    draw_options = pymunk.pygame_util.DrawOptions(gctrl.surface)

    centerx = gctrl.width / 2
    centery = gctrl.height / 2

    sx = 5
    sy = STATUS_HEIGHT + 5
    ex = gctrl.width - 5
    ey = gctrl.height - 5
    
    walls = []
    walls.append(wall_object((sx, sy), (sx, ey), WALL_COLLISION_TYPE))
    walls.append(wall_object((ex, ey), (ex, sy), WALL_COLLISION_TYPE))    
    walls.append(wall_object((sx, sy), (ex, sy), WALL_COLLISION_TYPE))
    walls.append(wall_object((sx, ey), (ex, ey), BOTTOM_COLLISION_TYPE))

    for wall in walls :
        gctrl.space.add(wall.body, wall.shape)
    
    brick_sx = BRICK_XOFFSET
    brick_sy = BRICK_YOFFSET

    brick_col_num = 8
    brick_row_num = 8
    brick_width = (gctrl.width - brick_sx * 2) / brick_col_num
    brick_height = BRICK_HEIGHT

    bricks = []
    for y in range(brick_row_num) :
        for x in range(brick_col_num+1) :
            bricks.append(brick_object((brick_sx, brick_sy), brick_width, brick_height))
            brick_sx += brick_width
        brick_sy += brick_height
        brick_sx = BRICK_XOFFSET

    for brick in bricks :
        gctrl.space.add(brick.body, brick.shape)

    bar_sx = centerx - (BAR_WIDTH / 2)
    bar_ex = centerx + (BAR_WIDTH / 2)
    bar_y = gctrl.height - BAR_YOFFSET
 
    bar = bar_object((bar_sx, bar_y), (bar_ex, bar_y), BAR_COLLISION_TYPE)
    gctrl.space.add(bar.body, bar.shape)

    ball = ball_object((centerx, centery))
    gctrl.space.add(ball.body, ball.shape)

    coll_handler1 = gctrl.space.add_collision_handler(BALL_COLLISION_TYPE, BOTTOM_COLLISION_TYPE)
    coll_handler1.begin = ball.coll_begin

    coll_handler2 = gctrl.space.add_collision_handler(BAR_COLLISION_TYPE, WALL_COLLISION_TYPE)
    coll_handler2.begin = bar.coll_begin

    def brick_separate(arbiter, space, data) :
        global score

        shape = arbiter.shapes[0]
        #print('brick shape :', shape)

        score += SCORE_UNIT1

        for i, brick in enumerate(bricks) :
            if brick.body == shape.body :
                brick.life -= 1
                if brick.life == 0 :
                    bricks.remove(brick)

                    gctrl.space.remove(shape.body, shape)
                    score += SCORE_UNIT2
                break
    
    coll_handler3 = gctrl.space.add_collision_handler(BRICK_COLLISION_TYPE, BALL_COLLISION_TYPE)
    coll_handler3.separate = brick_separate

    score = 0
    running = True
    while running:
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                running = False
                continue

            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_LEFT :
                    (x, y) = bar.get_position_a()
                    if x > 10 :
                        bar.set_velociy(-400, 0)
                elif event.key == pygame.K_RIGHT :
                    (x, y) = bar.get_position_b()
                    if x < gctrl.width - 10 :
                        bar.set_velociy(400, 0)
            elif event.type == pygame.KEYUP :
                if event.key == pygame.K_LEFT :
                    bar.set_velociy(0, 0)
                elif event.key == pygame.K_RIGHT :
                    bar.set_velociy(0, 0)

        gctrl.surface.fill(COLOR_BLACK)

        # do not draw pymunk debug 
        #gctrl.space.debug_draw(draw_options)

        # use object draw function
        for wall in walls :
            wall.draw()

        for brick in bricks :
            brick.draw()

        bar.draw()
        ball.draw()

        draw_score(score)

        pygame.display.flip()
        gctrl.space.step(1.0 / FPS)
        gctrl.clock.tick(FPS)

    terminate()

def init_game() :
    pad_width = 480
    pad_height = 640

    gctrl.set_surface(pygame.display.set_mode((pad_width, pad_height)))
    pygame.display.set_caption(TITLE_STR)    

if __name__ == '__main__' :
    init_game()
    start_game()
