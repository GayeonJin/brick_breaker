#!/usr/bin/python

import os
import sys

import pygame
import pymunk
import pymunk.pygame_util
import random
from time import sleep

from brick_data import *
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

BAR_YOFFSET = 30
BAR_WIDTH = 60

def draw_info() :
    font = pygame.font.SysFont('Verdana', INFO_FONT)
    info = font.render('F1/F2 : Load/Save file    space : start', True, COLOR_BLACK)

    pygame.draw.rect(gctrl.surface, COLOR_PURPLE, (0, gctrl.height - INFO_HEIGHT, gctrl.width, INFO_HEIGHT))
    gctrl.surface.blit(info, (INFO_OFFSET * 2, gctrl.height - 2 * INFO_FONT - INFO_OFFSET)) 

def draw_score(count) :
    gctrl.draw_string("Score : " + str(count), STATUS_XOFFSET, STATUS_YOFFSET, ALIGN_LEFT)

def draw_life(count) :
    gctrl.draw_string("Life : " + str(count), STATUS_XOFFSET, STATUS_YOFFSET, ALIGN_RIGHT)

def draw_message(str) :
    gctrl.draw_string(str, 0, 0, ALIGN_CENTER, 40, COLOR_WHITE)
       
    pygame.display.update()
    sleep(2)

def terminate() :
    pygame.quit()
    sys.exit()

def start_game() :
    global score, player_life, snd_shot, mute, ball

    mute = False
    snd_shot = pygame.mixer.Sound(get_snd_resource('snd_shot'))

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
    
    game_bricks = brick_data()
    game_bricks.load_file()
    stage = 1

    stage_bricks = brick_group(BRICK_COLS, BRICK_ROWS, game_bricks.stage_data.get(stage))
    for brick in stage_bricks.bricks :
        gctrl.space.add(brick.body, brick.shape)

    bar_sx = centerx - (BAR_WIDTH / 2)
    bar_ex = centerx + (BAR_WIDTH / 2)
    bar_y = gctrl.height - BAR_YOFFSET
 
    bar = bar_object((bar_sx, bar_y), (bar_ex, bar_y), BAR_COLLISION_TYPE)
    gctrl.space.add(bar.body, bar.shape)

    ball = None

    def ball_kill(arbiter, space, data) :
        global player_life, ball

        shape = arbiter.shapes[0]

        gctrl.space.remove(shape.body, shape)
        ball = None
        player_life -= 1

        return True

    coll_handler1 = gctrl.space.add_collision_handler(BALL_COLLISION_TYPE, BOTTOM_COLLISION_TYPE)
    coll_handler1.separate = ball_kill

    coll_handler2 = gctrl.space.add_collision_handler(BAR_COLLISION_TYPE, WALL_COLLISION_TYPE)
    coll_handler2.begin = bar.coll_begin

    def brick_separate(arbiter, space, data) :
        global score, snd_shot, mute

        shape = arbiter.shapes[0]
        #print('brick shape :', shape)

        if mute == False :
            snd_shot.play()
        score += SCORE_UNIT1

        if stage_bricks.remove(shape) == True :
            gctrl.space.remove(shape.body, shape)
            score += SCORE_UNIT2

        return True
    
    coll_handler3 = gctrl.space.add_collision_handler(BRICK_COLLISION_TYPE, BALL_COLLISION_TYPE)
    coll_handler3.separate = brick_separate

    score = 0
    player_life = 3
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
                elif event.key == pygame.K_SPACE :
                    if ball == None :
                        (x, y) = bar.get_position_center()
                        y -= 10
                        if x < gctrl.centerx :
                            ball = ball_object((x , y), ball_object.LEFT_DIR)
                        else :
                            ball = ball_object((x , y), ball_object.RIGHT_DIR)

                        gctrl.space.add(ball.body, ball.shape)

                elif event.key == pygame.K_F10 :
                    gctrl.save_scr_capture(TITLE_STR)
                elif event.key == pygame.K_F12 :
                    mute = True if mute == False else False 

        gctrl.surface.fill(COLOR_BLACK)

        if stage_bricks.is_clear() == True :
            stage += 1

            gctrl.space.remove(ball.body, ball.shape)
            ball = None

            stage_bricks = brick_group(BRICK_COLS, BRICK_ROWS, game_bricks.stage_data.get(stage))
            for brick in stage_bricks.bricks :
                gctrl.space.add(brick.body, brick.shape)

        # do not draw pymunk debug 
        #gctrl.space.debug_draw(draw_options)

        # use object draw function
        for wall in walls :
            wall.draw()

        stage_bricks.draw()

        bar.draw()

        if ball != None :
            ball.draw()
        else :
            str = 'Stage %d'%stage
            gctrl.draw_string(str, 0, 0, ALIGN_CENTER, 30, COLOR_GRAY)

        draw_score(score)
        draw_life(player_life)

        if player_life == 0 :
            draw_message('Game Over')
            score = 0
            player_life = 3

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
