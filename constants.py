import pygame
import math
import random
pygame.init()
pygame.font.init()

#global constants
WIDTH = 1920  # ширина игрового окна
HEIGHT = 1000  # высота игрового окна
FPS = 25  # частота кадров в секунду

# Системные параметры
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont('Calibri', 16) # шрифт

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY1 = (75, 75, 75)
GRAY2 = (105, 105, 105)
GRAY3 = (135, 135, 135)
GRAY4 = (50, 50, 50)
LIGHT_GRAY = (150, 150, 150)

palette = [WHITE, RED, YELLOW, BLUE, GREEN]

bg_color = BLACK # цвет фона

# параметры мира
DirectMove = {'UP': (0, 100),
              'DOWN': (0, -100),
              'LEFT': (100, 0),
              'RIGHT': (-100, 0)
            }
WORLD_WIDTH = 2*WIDTH
WORLD_HEIGHT = 2*HEIGHT


# параметры птиц
N_birds = 170
speed = 7  # средняя скорость
bird_size = 15
eagle_size = 30
sense = 25 * bird_size
min_distance_friend = 3 * bird_size
min_distance_enemy = 13 * bird_size
turn_angle = 90 * math.pi/180
turn_angle_wall = 90 * math.pi/180
trace_length = 30
# weights matrix
# for friends 0: [1st rule, 2nd rule, 3rd rule]
# for  enemy  1: [1st rule, 2nd rule, 3rd rule]
rule_weights = {0: [abs(random.gauss(0.2, 0.001))*10/FPS,  # for friends
                                 abs(random.gauss(0.2, 0.005))*10/FPS,
                                 abs(random.gauss(0.1, 0.002))*10/FPS],
                1: [0.4*15/FPS, 0*10/FPS, 0*10/FPS]}                                # for enemy

# правила Рейнольдса
first_rule = True  # не сталкивайся
second_rule = True  # держись одного направления с соседями
third_rule = True # летите рядом с соседями

