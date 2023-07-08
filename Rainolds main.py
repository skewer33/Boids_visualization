import pygame
import sys
import turtle
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
    bg_color = const.BLACK #цвет фона
    running = True
    time = 0
    all_sprites = pygame.sprite.Group()
    birds = pygame.sprite.Group() # группа объектов типа бактерия

    add_birds(birds, all_sprites)
    birds.sprites()[0].image_orig = pygame.image.load('bird3.png')
    birds.sprites()[0].image_orig = pygame.transform.scale(birds.sprites()[0].image_orig, (const.size, const.size))
    birds.sprites()[0].image = birds.sprites()[0].image_orig


    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        time += 1
        time_render = const.font.render("Time: %d ticks" %(time), False, const.WHITE) # рендерим текст
        all_sprites.update() #
        neighbours(birds)
        screen.fill(bg_color) # прорисовка бэкграунда
        all_sprites.draw(screen) # прорисовка спрайтов
        screen.blit(time_render, (0, 0)) # прорисовка текста со временем симуляции
        # if time % 10 == 1:
        #     print(birds.sprites()[0].neighbours_list)
        #     print(birds.sprites()[1].neighbours_list)
        #     print(birds.sprites()[2].neighbours_list)

        if 1:
            for bird in birds:
                bird.trace()
        pygame.display.flip() #прорисовка последнего кадра

def add_birds(birds, all_sprites):

    for i in range(const.N_birds):
        x = random.uniform(0, 1) * WIDTH
        y = random.uniform(0, 1) * HEIGHT
        #x = 0.5 * WIDTH
        #y = 0.5 * HEIGHT
        speed = abs(random.gauss(const.speed, 1.5))
        bird = Birds(x, y, speed=speed)
        all_sprites.add(bird)
        birds.add(bird)

def neighbours(birds):
    if len(birds) < 2:
        return
    for bird in birds:
        bird.neighbours_list = []
    for i in range(len(birds)):
        for j in range(1 + i, len(birds)):
            dx = birds.sprites()[i].rect.centerx - birds.sprites()[j].rect.centerx
            dy = birds.sprites()[i].rect.centery - birds.sprites()[j].rect.centery
            square_dist = dx*dx + dy*dy
            if (square_dist < const.sense**2):
                angle_between = math.atan2(dy, dx) #угол между 2 птицами в радианах (мб надо будет сделать dy, а не -dy)
                birds.sprites()[i].neighbours_list.append([square_dist,
                                                           angle_between,
                                                           birds.sprites()[j].speed,
                                                           birds.sprites()[j].move_angle,
                                                           (birds.sprites()[j].rect.centerx, birds.sprites()[j].rect.centery)])
                birds.sprites()[j].neighbours_list.append([square_dist,
                                                           angle_between + math.pi/2,
                                                           birds.sprites()[i].speed,
                                                           birds.sprites()[i].move_angle,
                                                           (birds.sprites()[i].rect.centerx, birds.sprites()[i].rect.centery)])

def main():
    print('Hello! GUYS')
    run(const.N_birds)
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    running = True
    main()