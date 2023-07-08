import pygame
import random
import constants as const
import math


WIDTH = const.WIDTH
HEIGHT = const.HEIGHT
FPS = const.FPS


class Birds(pygame.sprite.Sprite):

    i = 0
    def __init__(self, x, y,
                 speed = const.speed,
                 trace_length = const.trace_length,
                 screen = const.screen):
        #инициализация бактерии
        pygame.sprite.Sprite.__init__(self) #инициализатор встроенных классов Sprite
        # движение
        self.speed = speed
        self.move_angle = math.pi * random.random()

        # объект и его локализация на поле симуляции
        self.image_orig = pygame.image.load('bird1.png') # храним исходное изображение, это нужно для rotate()
        self.image_orig = pygame.transform.scale(self.image_orig, (const.size, const.size))
        self.image = self.image_orig
        self.rect = self.image.get_rect()
        self.screen = screen
        self.rect.centerx = x
        self.rect.centery = y

        #след от движения
        self.trace_length = trace_length
        self.trace_coord = [(self.rect.centerx, self.rect.centery)] * self.trace_length
        self.trace_color = random.choice([const.WHITE, const.BLUE, const.GREEN, const.YELLOW, const.RED])

        # Соседи
        self.neighbours_list = [] # будет содержать списки с информацией о соседях:
                                    # [0] квадрат расстояния между этой птицей и соседом
                                    # [1] угол между этой птицей и соседом
                                    # [2] скорость соседа
                                    # [3] направление движения соседа
                                    # [4] координата соседа (x, y)

        # весовые коэффициенты для правил
        self.rule_weights = [abs(random.gauss(0.2, 0.05)), abs(random.gauss(0.2, 0.05)), abs(random.gauss(0.1, 0.025))]
        
    def __del__(self):
        print('vmer')

# ДВИЖЕНИЕ
    def rotate(self):
        self.image = pygame.transform.rotate(self.image_orig, - self.move_angle * 180/math.pi - 90)
        self.rect = self.image.get_rect(center = self.rect.center)

    def change_direction(self, angle): # изменение направления
        self.move_angle += angle
        self.rotate()

    def trace(self):
        self.trace_coord = self.trace_coord[1:] + [(self.rect.centerx, self.rect.centery)]
        for i in range(self.trace_length-1):
            pygame.draw.line(self.screen, self.trace_color, self.trace_coord[i], self.trace_coord[i+1])

    def limited_world(self, WIDTH, HEIGHT): # зацикленный мир
        if self.rect.left > WIDTH:
            self.move_angle += const.turn_angle
        if self.rect.right < 0:
            self.move_angle += const.turn_angle
        if self.rect.top < 0:
            self.move_angle += const.turn_angle
        if self.rect.bottom > HEIGHT:
            self.move_angle += const.turn_angle

    def cycle_world(self, WIDTH, HEIGHT):
        if self.rect.centerx > WIDTH:
            self.rect.centerx = 0
           # self.rect.centery = HEIGHT - self.rect.top
            self.trace_coord = [self.rect.center] * self.trace_length
        if self.rect.centerx < 0:
            self.rect.centerx = WIDTH
            #self.rect.centery = HEIGHT - self.rect.top
            self.trace_coord = [self.rect.center] * self.trace_length
        if self.rect.centery < 0:
            self.rect.centery = HEIGHT
           # self.rect.centerx = WIDTH - self.rect.left
            self.trace_coord = [self.rect.center] * self.trace_length
        if self.rect.centery > HEIGHT:
            self.rect.centery = 0
            #self.rect.centerx = WIDTH - self.rect.left
            self.trace_coord = [self.rect.center] * self.trace_length

# ПРАВИЛА СОЦИАЛЬНОГО ВЗАИМОДЕЙСТВИЯ
    def dont_crush(self):
        for neighbour in self.neighbours_list:
            if neighbour[0] < const.min_distance**2:
                if neighbour[1] > self.move_angle:
                    self.change_direction(self.rule_weights[0] * const.turn_angle)
                else:
                    self.change_direction(- self.rule_weights[0] * const.turn_angle)

    def average_neighbour_speed(self):
        average_speed = 0
        average_angle = 0
        if len(self.neighbours_list) < 1:
            return
        for neighbour in self.neighbours_list:
            average_speed += neighbour[2]
            average_angle += neighbour[3]
        average_speed = average_speed / len(self.neighbours_list)
        average_angle = average_angle / len(self.neighbours_list)
        self.speed += self.rule_weights[1] * (average_speed - self.speed)
        self.change_direction(self.rule_weights[1] * (average_angle - self.move_angle))

    def geometric_mass_center(self):
        average_x = 0
        average_y = 0
        if len(self.neighbours_list) < 1:
            return
        for neighbour in self.neighbours_list:
            average_x += neighbour[4][0]
            average_y += neighbour[4][1]
        average_x /= len(self.neighbours_list)
        average_y /= len(self.neighbours_list)
        dx = average_x - self.rect.centerx
        dy = average_y - self.rect.centery
        new_move_angle = math.atan2(dy, dx)
        self.change_direction(self.rule_weights[2] * (new_move_angle - self.move_angle))

# ЕЖЕКАДРОВОЕ ОБНОВЛЕНИЕ ЭКРАНА
    def update(self):


        self.cycle_world(WIDTH, HEIGHT)
        if const.second_rule:
            self.average_neighbour_speed()
        if const.third_rule:
            self.geometric_mass_center()
        if const.first_rule:
            self.dont_crush()
        #if self.i % 10 == 5:
        #    self.change_direction(2 * math.pi * random.random())
        self.rect.x += self.speed * math.cos(self.move_angle)
        self.rect.y += self.speed * math.sin(self.move_angle)
        self.i+=1

    def output(self):
        #вывод бактерии на экран
        self.screen.blit(self.image, self.rect)

