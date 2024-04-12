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
GRAY = (75, 75, 75)
LIGHT_GRAY = (150, 150, 150)

# параметры птиц
N_birds = 120
speed = 7  # средняя скорость
bird_size = 15
eagle_size = 30
sense = 15 * bird_size
min_distance_friend = 2 * bird_size
min_distance_enemy = 10 * bird_size
turn_angle = 90 * math.pi/180
turn_angle_wall = 90 * math.pi/180
trace_length = 25
# weights matrix
# for friends 0: [1st rule, 2nd rule, 3rd rule]
# for  enemy  1: [1st rule, 2nd rule, 3rd rule]
rule_weights = {0: [abs(random.gauss(0.3, 0.001))*10/FPS,  # for friends
                                 abs(random.gauss(0.1, 0.05))*10/FPS,
                                 abs(random.gauss(0.1, 0.02))*10/FPS],
                1: [0.6*15/FPS, 0*10/FPS, 0*10/FPS]}                                # for enemy

# правила Рейнольдса
first_rule = True  # не сталкивайся
second_rule = True  # держись одного направления с соседями
third_rule = True # летите рядом с соседями

