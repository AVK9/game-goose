import random
import os
import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()

FPS = pygame.time.Clock()
HEIGHT = 700
WIDTH = 1200
START = (50, HEIGHT // 2)
BONUS_ENTER1 = WIDTH * 0.2
BONUS_ENTER2 = WIDTH * 0.8
ENEMY_ENTER1 = HEIGHT * 0.1
ENEMY_ENTER2 = HEIGHT * 0.9
FONT = pygame.font.SysFont('Verdana', 20)
GAME_OVER_FONT = pygame.font.SysFont("Arial", 70)
GAME_OVER_TEXT = "GAME OVER"

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_GOLD = (244, 202, 22)

main_display = pygame.display.set_mode((WIDTH, HEIGHT))
bgr = pygame.transform.scale(pygame.image.load('images/background.png'), (WIDTH, HEIGHT))
bgr_X1 = 0
bgr_X2 = bgr.get_width()
bg_move = 3

IMAGE_PATH = 'images/player'
PLAYER_IMAGES = os.listdir(IMAGE_PATH)

player_size = (20, 20)
player = pygame.image.load('images/player.png').convert_alpha() #pygame.Surface(player_size)
# player = pygame.transform.scale(pygame.image.load('images/player.png').convert_alpha(), player_size) 
# player.fill(COLOR_BLACK)
player_rect = player.get_rect(midleft=START)
# player_speed = [1, 1]

player_move_down = [0, 4]
player_move_up = [0, -4]
player_move_left = [-4, 0]
player_move_right = [4, 0]

def create_enemy():
    enemy_size = (20, 20)
    enemy = pygame.transform.scale(pygame.image.load('images/enemy.png').convert_alpha(), (100, 30)) #pygame.Surface(enemy_size)
    # enemy.fill(COLOR_BLUE)
    enemy_rect = pygame.Rect(WIDTH, random.randint(ENEMY_ENTER1, ENEMY_ENTER2), *enemy_size)
    enemy_move = [random.randint(-8, -4), 0]
    return [enemy, enemy_rect, enemy_move]

def create_bonus():
    bonus_size = (100, 140)
    bonus = pygame.transform.scale(pygame.image.load('images/bonus.png').convert_alpha(), bonus_size) #pygame.Surface(bonus_size)
    # bonus.fill(COLOR_GOLD)
    bonus_rect = pygame.Rect(random.randint(BONUS_ENTER1, BONUS_ENTER2), 0, *bonus_size)
    bonus_move = [0, random.randint(4, 8)]
    return [bonus, bonus_rect, bonus_move]

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)
CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 1000)
CHANGE_IMAGE = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMAGE, 200)

enemies = []
bonuses = []
score = 0

image_index = 0

plain = True
game_active = True

while plain:
    FPS.tick(120)
    for event in pygame.event.get():
        if event.type == QUIT:
            plain = False
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())
        if event.type == CHANGE_IMAGE:
            player = pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[image_index]))
            image_index += 1
            if image_index >= len(PLAYER_IMAGES):
                image_index = 0
    if game_active:

        bgr_X1 -= bg_move
        bgr_X2 -= bg_move

        if bgr_X1 < -bgr.get_width():
            bgr_X1 = bgr.get_width()

        if bgr_X2 < -bgr.get_width():
            bgr_X2 = bgr.get_width()

        main_display.blit(bgr, (bgr_X1, 0))
        main_display.blit(bgr, (bgr_X2, 0))
        # main_display.fill(COLOR_BLACK)

        keys = pygame.key.get_pressed()
        if keys[K_DOWN] and player_rect.bottom < HEIGHT:
            player_rect = player_rect.move(player_move_down)
        if keys[K_UP] and player_rect.top > 0:
            player_rect = player_rect.move(player_move_up)
        if keys[K_RIGHT] and player_rect.right < WIDTH:
            player_rect = player_rect.move(player_move_right)
        if keys[K_LEFT] and player_rect.left > 0:
            player_rect = player_rect.move(player_move_left)

        for bonus in bonuses:
            bonus[1] = bonus[1].move(bonus[2])
            main_display.blit(bonus[0], bonus[1])

            if player_rect.colliderect(bonus[1]):
                bonuses.pop(bonuses.index(bonus))
                score += 1

        for enemy in enemies:
            enemy[1] = enemy[1].move(enemy[2])
            main_display.blit(enemy[0], enemy[1])

            if player_rect.colliderect(enemy[1]):
                main_display.blit(GAME_OVER_FONT.render(str(GAME_OVER_TEXT), True, COLOR_GOLD), (WIDTH // 3, HEIGHT // 2))
                game_active = False

        main_display.blit(FONT.render(str(score), True, COLOR_BLACK), (WIDTH-50, 20))
    


        main_display.blit(player, player_rect)
        pygame.display.flip()

        for enemy in enemies:
            if enemy[1].left < 0:
                enemies.pop(enemies.index(enemy))

        for bonus in bonuses:
            if bonus[1].bottom > HEIGHT:
                bonuses.pop(bonuses.index(bonus))