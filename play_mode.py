import random

from pico2d import *

import game_framework

import game_world
from grass import Grass
from boy import Boy
from ball import Ball
from zombie import Zombie

# boy = None

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            boy.handle_event(event)

def init():
    global boy
    global balls
    global zombies

    grass = Grass()
    game_world.add_object(grass, 0)

    boy = Boy()
    game_world.add_object(boy, 1)

    # fill here
    balls = [Ball(random.randint(0,1600),60, 0) for _ in range(50)]
    game_world.add_objects(balls, 1)

    game_world.add_collision_pair('boy:ball', boy, None)
    game_world.add_collision_pair('boy:zombie', boy, None)
    for ball in balls:
        game_world.add_collision_pair('boy:ball', None, ball)

    # 좀비 5마리
    zombies = [Zombie() for _ in range(5)]
    game_world.add_objects(zombies, 1)
    for zombie in zombies:
        game_world.add_collision_pair('ball:zombie', None, zombie)
        game_world.add_collision_pair('boy:zombie', None, zombie)

def finish():
    game_world.clear()
    pass


def update():
    game_world.update() #소년과 볼에 위치가 다 업데이트 됬음
    game_world.handle_collisions()
    # fill here
    #아마추어적인 방법
    #for ball in balls:
        #if game_world.collide(boy, ball):
         #  boy.ball_count += 1
         #   game_world.remove_object(ball)
         #   balls.remove(ball)

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass

