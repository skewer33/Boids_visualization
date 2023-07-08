import pygame
import math
pygame.init()
pygame.font.init()

#global constants
WIDTH = 1280  # ширина игрового окна
HEIGHT = 760  # высота игрового окна
FPS = 20  # частота кадров в секунду

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
N_birds = 80
speed = 3  # средняя скорость
size = 15
sense = 8*size
min_distance = 2 * size
turn_angle = 90 * math.pi/180
turn_angle_wall = 90 * math.pi/180
trace_length = 50

# правила Рейнольдса
first_rule = True
second_rule = True
third_rule = True
