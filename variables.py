from functions import *
import pygame
import random

pygame.init()

# Определение размеров окна
window_width = 1500
window_height = 900

# Создание игрового окна
window = pygame.display.set_mode((window_width, window_height))

count = 0
counter = False
running = True

# Определение цветов
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

clock = pygame.time.Clock()

count_txt = pygame.font.SysFont('arial', 40)
timer_txt = pygame.font.SysFont('arial', 40)
game_over_txt = pygame.font.SysFont('arial', 100)
score_txt = pygame.font.SysFont('arial', 100)
restart_txt = pygame.font.SysFont('arial', 70)
menu_txt = pygame.font.SysFont('arial', 70)

# Определение размеров игрока и платформы
player_width = 50
player_height = 50
platform_width = 200
platform_height = 30
reward_width = 10
reward_height = 10

# Определение скорости игрока
player_speed = 5
FPS = 60

timer = 0

is_jump = False
FPS_count = 0
jump_count = 0

pygame.display.set_caption("Changing Level Game")

player_rect = None