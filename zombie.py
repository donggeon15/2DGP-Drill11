import random
import math
import game_framework
import game_world

from pico2d import *

# zombie Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# zombie Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10.0

# zombie Action Dead
TIME_PER_ACTION_DEAD = 10.0
ACTION_DEAD_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION_DEAD = 12.0

animation_names = ['Walk']
animation_names2 = ['Dead']
animation_names3 = ['Attack']

class Zombie:
    images = None

    def load_images(self):
        if Zombie.images == None:
            Zombie.images = {}
            for name in animation_names:
                Zombie.images[name] = [load_image("./zombie/"+ name + " (%d)" % i + ".png") for i in range(1, 11)]
            for name in animation_names2:
                Zombie.images[name] = [load_image("./zombie/"+ name + " (%d)" % i + ".png") for i in range(1, 13)]
            for name in animation_names3:
                Zombie.images[name] = [load_image("./zombie/"+ name + " (%d)" % i + ".png") for i in range(1, 9)]


    def __init__(self):
        self.x, self.y = random.randint(1600-800, 1600), 150
        self.load_images()
        self.size = 200
        self.action = 0 # 0: 걷기 1: 죽음
        self.collision_size_x = 50
        self.collision_size_y = 100
        self.frame = random.randint(0, 9)
        self.dir = random.choice([-1,1])


    def update(self):
        if self.action == 0:
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        if self.action == 1:
            self.frame = (self.frame + FRAMES_PER_ACTION_DEAD * ACTION_DEAD_PER_TIME * game_framework.frame_time)
            if self.frame > FRAMES_PER_ACTION_DEAD:
                game_world.remove_object(self)
        if self.action == 2:
            self.frame = (self.frame + 8 * ACTION_PER_TIME * game_framework.frame_time)
            if self.frame >= 7:
                game_framework.quit()

        self.x += RUN_SPEED_PPS * self.dir * game_framework.frame_time
        if self.x > 1600:
            self.dir = -1
        elif self.x < 800:
            self.dir = 1
        self.x = clamp(800, self.x, 1600)
        pass


    def draw(self):
        if self.dir < 0:
            if self.action == 0:
                Zombie.images['Walk'][int(self.frame)].composite_draw(0, 'h', self.x, self.y, self.size, self.size)
            if self.action == 1:
                Zombie.images['Dead'][int(self.frame)].composite_draw(0, 'h', self.x, self.y + 15, 150, 100)
            if self.action == 2:
                Zombie.images['Attack'][int(self.frame)].composite_draw(0, 'h', self.x, self.y, self.size, self.size)
        else:
            if self.action == 0:
                Zombie.images['Walk'][int(self.frame)].draw(self.x, self.y, self.size, self.size)
            if self.action == 1:
                Zombie.images['Dead'][int(self.frame)].draw(self.x, self.y + 15, 150, 100)
            if self.action == 2:
                Zombie.images['Attack'][int(self.frame)].draw(self.x, self.y, self.size, self.size)
        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        pass

    def get_bb(self):
        return self.x - self.collision_size_x, self.y - self.collision_size_y, self.x + self.collision_size_x, self.y + self.collision_size_y

    def handle_collision(self, group, other):
        if group == 'ball:zombie':
            if self.size > 50:
                self.size //= 2
                self.y = self.y - (self.y//3)
                self.collision_size_x //= 2
                self.collision_size_y //= 2
            if self.size == 50:
                if self.action == 0:
                    self.action = 1
                    self.frame = 0
        if group == 'boy:zombie':
            if self.action != 2:
                self.frame = 0
                self.action = 2