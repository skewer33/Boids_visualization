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
                 identify = 0,
                 img = pygame.image.load('bird1.png'), size = const.bird_size,
                 screen = const.screen):
        #инициализация бактерии
        pygame.sprite.Sprite.__init__(self) #инициализатор встроенных классов Sprite
        # движение
        self.speed = speed
        self.move_angle = random.uniform(-math.pi,0)
        print(f'start angle {self.move_angle}')
        # object features and it`s localization on the simulation`s field
        self.image_orig = img # храним исходное изображение, это нужно для rotate()
        self.image_orig = pygame.transform.scale(self.image_orig, (size, size))
        self.image = self.image_orig
        self.rect = self.image.get_rect()
        self.rotate()
        self.screen = screen
        self.rect.centerx = x
        self.rect.centery = y
        self.identify = identify

        # moving trace
        self.trace_length = trace_length
        self.trace_coord = [(self.rect.centerx, self.rect.centery)] * self.trace_length
        self.trace_color = random.choice([const.WHITE, const.BLUE, const.GREEN, const.YELLOW, const.GRAY])

        # Соседи
        self.neighbours_list = [] # contain the dicts of neighbours` features:
                                    # {'square_dist': distance from bird to neighbor,
                                    # 'angle_between': angle between birds and OX
                                    # 'speed': neighbor's speed
                                    # 'direction': neighbor's moving direction
                                    # 'coord': coordinate of neighbour (x, y)
                                    # 'class': class of neighbour: {0: friend, 1: enemy}
                                    # }

        # весовые коэффициенты для правил
        self.rule_weights = const.rule_weights
        # minimal distance dict for changing direction
        self.min_dist = {0: const.min_distance_friend, 1: const.min_distance_enemy}
        
    def __del__(self):
        print('umer')

# ДВИЖЕНИЕ
    def rotate(self):
        self.image = pygame.transform.rotate(self.image_orig, - self.move_angle * 180/math.pi - 90)
        self.rect = self.image.get_rect(center = self.rect.center)

    def change_direction(self, angle): # изменение направления
        self.move_angle += angle
        if self.move_angle > 2*math.pi:
            self.move_angle -= 2*math.pi
        elif self.move_angle < 0:
            self.move_angle = 2 * math.pi - self.move_angle
        self.rotate()

    def trace(self):
        """
        draw a line of the bird's movement path
        :return: None
        """
        self.trace_coord = self.trace_coord[1:] + [(self.rect.centerx, self.rect.centery)]
        for i in range(self.trace_length-1):
            pygame.draw.line(self.screen, self.trace_color, self.trace_coord[i], self.trace_coord[i+1])

    def null_trajectory(self):
        """
        function resets the trajectory line
        :return: None
        """
        self.trace_coord = [self.rect.center] * self.trace_length

    def limited_world(self, WIDTH, HEIGHT): # зацикленный мир
        if self.rect.centerx >= WIDTH:
            #self.move_angle = math.pi - self.move_angle
            self.move_angle = random.uniform(math.pi/2, 3*math.pi/2)
        if self.rect.centerx <= 0:
            #self.move_angle = math.pi - self.move_angle
            self.move_angle = random.choice([random.uniform(0, math.pi/2), random.uniform(3*math.pi/2, 2*math.pi)])
        if self.rect.centery <= 0:
            #self.move_angle = 2*math.pi - self.move_angle
            self.move_angle = random.uniform(0, math.pi)
        if self.rect.centery >= HEIGHT:
            #self.move_angle = 2*math.pi - self.move_angle
            self.move_angle = random.uniform(math.pi, 2 * math.pi)

    def cycle_world(self, WIDTH, HEIGHT):
        if self.rect.centerx > WIDTH:
            self.rect.centerx = 0
            self.null_trajectory()
        if self.rect.centerx < 0:
            self.rect.centerx = WIDTH
            self.null_trajectory()
        if self.rect.centery < 0:
            self.rect.centery = HEIGHT
            self.null_trajectory()
        if self.rect.centery > HEIGHT:
            self.rect.centery = 0
            self.null_trajectory()

# ПРАВИЛА СОЦИАЛЬНОГО ВЗАИМОДЕЙСТВИЯ
    def dont_crush(self):
        """

        :param min_dist: in which distance the bird will change it`s direction
        In this code it uses for different behavior of bird when it`s meet objects of different classes:
        other bird: min_dist = const.min_distance
        predator  : min_dist = const.min_distance
        :return:
        """
        for neighbour in self.neighbours_list:
            nbr_class = neighbour['class']
            min_dist = self.min_dist[nbr_class]
            if neighbour['square_dist'] < min_dist**2:
                angle = random.choice([- self.rule_weights[nbr_class][0] * const.turn_angle,
                                       self.rule_weights[nbr_class][0] * const.turn_angle])
                self.change_direction(angle)
                #if neighbour['angle_between'] > self.move_angle: # интересно, что есть включить эту опцию, то птицы всегда летят на юго-восток
                #    self.change_direction(self.rule_weights[nbr_class][0] * const.turn_angle)
                #else:
                #    self.change_direction(- self.rule_weights[nbr_class][0] * const.turn_angle)

    @staticmethod
    def circular_mean(angles):
        """
        function for calculate mean angle, because common mean take wrong answers
        for example: mean(0, 2*pi) = pi
                     circular_mean(0, 2*pi) = 0
        :param angles: list of angles
        :return: mean angle (in radians)
        """
        # Calculate the sum of sin and cos values
        sin_sum = sum([math.sin(angle) for angle in angles])
        cos_sum = sum([math.cos(angle) for angle in angles])

        # Calculate the circular mean using arctan2
        # formula: theta = atan
        mean_rad = math.atan2(sin_sum, cos_sum)
        if mean_rad < 0:
            return 2 * math.pi - mean_rad
        return mean_rad

    def average_neighbour_speed(self):
        if len(self.neighbours_list) < 1:
            return
        # calculate delta speed: d_speed = mean((speed`s neighbours - self speed)*weights)
        d_speed = sum([(n['speed']-self.speed)*self.rule_weights[n['class']][1] for n in self.neighbours_list])/len(self.neighbours_list)
        average_angle = self.circular_mean([n['direction'] for n in self.neighbours_list if n['class'] == 0])
        self.speed += d_speed
        self.change_direction((average_angle - self.move_angle)*self.rule_weights[0][1])

    def geometric_mass_center(self):
        average_x = 0
        average_y = 0
        if len(self.neighbours_list) < 1:
            return
        for neighbour in self.neighbours_list:
            average_x += neighbour['coord'][0]
            average_y += neighbour['coord'][1]
        average_x /= len(self.neighbours_list)
        average_y /= len(self.neighbours_list)
        dx = average_x - self.rect.centerx
        dy = average_y - self.rect.centery
        new_move_angle = math.atan2(dy, dx)
        self.change_direction(self.rule_weights[0][2] * (new_move_angle - self.move_angle))

    def movement(self, speed, angle):
        self.rect.x += speed * math.cos(angle)
        self.rect.y += speed * math.sin(angle)

# ЕЖЕКАДРОВОЕ ОБНОВЛЕНИЕ ЭКРАНА
    def update(self):

        if const.second_rule:
            self.average_neighbour_speed()
        if const.third_rule:
            self.geometric_mass_center()
        if const.first_rule:
            self.dont_crush()
        #if self.i % 10 == 5:
        #    self.change_direction(2 * math.pi * random.random())
        self.cycle_world(WIDTH, HEIGHT)

        self.movement(self.speed, self.move_angle)

        self.i+=1

    def output(self):
        #вывод бактерии на экран
        self.screen.blit(self.image, self.rect)



class Predator(Birds):
    
    def __init__(self, x, y):
        print(x, y)
        super().__init__(x, y,
                         identify = 1,
                         img = pygame.image.load('bird3.png'),
                         size = const.eagle_size)
        self.trace_color = const.RED

    def __del__(self):
        print('Xishnik vmer')

    def take_position(self, x, y):
        self.rect.centerx, self.rect.centery = x, y

    def angle_between_2_points(self, ax, ay, bx, by):
        if ax-bx+ay-by == 0:
            return self.move_angle
        dx = ax - bx
        dy = ay - by
        rads = math.atan2(dy, dx)
        rads %= 2 * math.pi
        return rads

    def is_collided_with(self, sprite):
        return self.rect.colliderect(sprite.rect)

    def update(self):
        self.prev_pos = [self.rect.centerx, self.rect.centery]
        self.take_position(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        if pow((self.prev_pos[0] - self.rect.centerx), 2) + pow((self.prev_pos[1] - self.rect.centery), 2) > 0:
            self.move_angle = self.angle_between_2_points(self.rect.centerx, self.rect.centery,
                                                          self.prev_pos[0], self.prev_pos[1])
            self.rotate()

    def output(self):
        # вывод на экран
        self.screen.blit(self.image, self.rect)