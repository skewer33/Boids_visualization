import pygame
import sys
#import turtle
import constants as const
import random
from birds import *


#constants, если хотите их изменить, меняйте в файле "constants"
WIDTH = const.WIDTH  # ширина игрового окна
HEIGHT = const.HEIGHT  # высота игрового окна
FPS = const.FPS  # частота кадров в секунду
screen = const.screen
pygame.display.set_caption("Rainolds`s Model")
clock = pygame.time.Clock()


def run(N_birds):

    pygame.init()
    pygame.font.init()  # вызов шрифтов, чтобы использовать текст
    bg_color = const.bg_color #цвет фона
    running = True
    time = 0
    scene_bias = [0, 0]

    global all_sprites
    global birds
    all_sprites = pygame.sprite.Group()
    birds = pygame.sprite.Group() # группа объектов типа бактерия

    add_birds()
    birds.sprites()[0].image_orig = pygame.image.load('bird6.png')
    birds.sprites()[0].image_orig = pygame.transform.scale(birds.sprites()[0].image_orig, (const.bird_size, const.bird_size))
    birds.sprites()[0].image = birds.sprites()[0].image_orig
    predator = False

    while running:
        clock.tick(FPS)
        # Event processing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                eagle = Predator(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                all_sprites.add(eagle)
                predator = True
            elif event.type == pygame.MOUSEBUTTONUP:
                eagle.kill()
                predator = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    scene_bias = move_scene(const.DirectMove['UP'], scene_bias)
                elif event.key == pygame.K_DOWN:
                    scene_bias = move_scene(const.DirectMove['DOWN'], scene_bias)
                elif event.key == pygame.K_LEFT:
                    scene_bias = move_scene(const.DirectMove['LEFT'], scene_bias)
                elif event.key == pygame.K_RIGHT:
                    scene_bias = move_scene(const.DirectMove['RIGHT'], scene_bias)

        # Update simulation
        time += 1
        time_render = const.font.render("Time: %d ticks" %(time), False, const.WHITE) # рендерим текст
        bias_render = const.font.render(f'Bias: OX={scene_bias[0]} OY={scene_bias[1]} ', False, const.WHITE)
        check_world(scene_bias)
        all_sprites.update() #
        if predator:
            hunt(eagle, birds)
        neighbours(all_sprites)

        # Draw objects
        screen.fill(bg_color) # draw background
        all_sprites.draw(screen) # draw sprites
        screen.blit(time_render, (0, 0)) # draw simulation time
        screen.blit(bias_render, (0, 20)) # draw bias (how long current scene from start scene
        pygame.draw.rect(screen, (100, 100, 100),
                         (scene_bias[0], scene_bias[1], const.WORLD_WIDTH, const.WORLD_HEIGHT), 2)
        if const.trace_length: # draw birds traces
            for bird in all_sprites:
                bird.trace()

        # Viewing last rendered frame
        pygame.display.flip()


def check_world(bias):
    """
    function for replacing birds which moved out of the world
    :param bias:
    :return:
    """
    for bird in birds.sprites():
        bird.cycle_world(bias[0], const.WORLD_WIDTH + bias[0],  # x_min, x_max
                         bias[1], const.WORLD_HEIGHT + bias[1])  # y_min, y_max

def biass_compensation_trace(bird_trace, bias):
    """
    function for compensation bias of bird`s trace during scene moving
    :param bird: current bird
    :param bias: tuple values of bias (bias_x, bias_y)
    :return:
    """
    bird_trace = [(coord[0]+bias[0], coord[1]+bias[1]) for coord in bird_trace]
    return bird_trace

def move_scene(direct, bias):
    """
    function for moving scene
    :param direct: (x, y) - value of moving scene
    :return:
    """
    bias[0] += direct[0]
    bias[1] += direct[1]
    for sprite in all_sprites.sprites():
        sprite.rect.centerx += direct[0]
        sprite.rect.centery += direct[1]
        sprite.trace_coord = biass_compensation_trace(sprite.trace_coord, direct)
    return bias

def hunt(eagle, birds):
    for bird in birds:
        if eagle.is_collided_with(bird):
            print('Съел!')
            bird.kill()


def add_birds():

    for i in range(const.N_birds):
        x = random.uniform(0, 1) * const.WORLD_WIDTH
        y = random.uniform(0, 1) * const.WORLD_HEIGHT
        #x = 0.5 * WIDTH
        #y = 0.5 * HEIGHT
        speed = abs(random.gauss(const.speed, const.speed/3))
        bird = Birds(x, y, speed=speed)
        all_sprites.add(bird)
        birds.add(bird)

def min_dist_toroid(r1:float, r2:float, width = WIDTH, heigth = HEIGHT) -> float:
    """
    function return square of distance between 2 points in toroidal 2D surface
    :param r1: coordinate of point1  (x1 or y1)
    :param r2: coordinate of point2  (x2 or y2)
    :return: square distance between p1, p2
    """
    min_r = min(r1, r2)
    max_r = max(r1, r2)
    d1 = max_r - min_r
    d2 = width - max_r + min_r
    return min(d1, d2)

def neighbours(birds):
    if len(birds) < 2:
        return
    for bird in birds:
        bird.neighbours_list = []
    for i in range(len(birds)):
        for j in range(1 + i, len(birds)):
            dx = min_dist_toroid(birds.sprites()[i].rect.centerx, birds.sprites()[j].rect.centerx)
            dy = min_dist_toroid(birds.sprites()[i].rect.centery, birds.sprites()[j].rect.centery)
            square_dist = dx*dx + dy*dy
            if (square_dist < const.sense**2):
                angle_between = math.atan2(dy, dx) #угол между 2 птицами в радианах (мб надо будет сделать dy, а не -dy)
                birds.sprites()[i].neighbours_list.append({'square_dist': square_dist,
                                                            'angle_between': angle_between,
                                                            'speed'    : birds.sprites()[j].speed,
                                                            'direction': birds.sprites()[j].move_angle,
                                                            'coord'    : (birds.sprites()[j].rect.centerx, birds.sprites()[j].rect.centery),
                                                            'class'    : birds.sprites()[j].identify})

                birds.sprites()[j].neighbours_list.append({'square_dist': square_dist,
                                                            'angle_between': angle_between,
                                                            'speed'    : birds.sprites()[i].speed,
                                                            'direction': birds.sprites()[i].move_angle,
                                                            'coord'    : (birds.sprites()[i].rect.centerx, birds.sprites()[i].rect.centery),
                                                            'class'    : birds.sprites()[i].identify})


def main():
    print('Hello! GUYS')
    run(const.N_birds)
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    running = True
    main()