import keyboard
from variables import *
import pygame
import random

# Инициализация pygame
pygame.init()




#functions
def generate_level():
    current_platform = None
    platforms = []
    num_platforms = 13

    for platform in range(num_platforms):
        x = random.randint(50, window_width - platform_width - 50)
        y = random.randint(150, window_height - platform_height - 150)
        current_platform = pygame.Rect(x, y, platform_width, platform_height)
        if len(platforms) > 0:
            for platform in platforms:
                while True:
                    if not current_platform.colliderect(platform):
                        break
                    x = random.randint(50, window_width - platform_width - 50)
                    y = random.randint(150, window_height - platform_height - 150)
                    current_platform = pygame.Rect(x, y, platform_width, platform_height)
        platforms.append(pygame.Rect(x, y, platform_width, platform_height))

    return platforms

def spawn_player(platforms):
    min_y = 0
    min_left = 0
    min_right = 0
    for platform in platforms:
        if platform.y > min_y:
            min_y = platform.y
            min_left = platform.left
            min_right = platform.right
    player_rect = pygame.Rect(
        (min_left + min_right) // 2 - reward_width // 2,
        min_y,
        player_width,
        player_height
    )
    return player_rect
def update_game(player_rect, platforms):
    global count
    global counter
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player_rect.x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_rect.x += player_speed

    for platform in platforms:
        if player_rect.colliderect(platform):
            # Обработка столкновения игрока с платформой
            player_rect.y = platform.top - player_height

    if player_rect.left < 0:
        # Обработка выхода игрока за границы окна
        player_rect.left = 0
    if player_rect.right > window_width:
        player_rect.right = window_width
    if player_rect.top < 0:
        player_rect.top = 0


def is_on_platform():
    for platform in platforms:
        if player_rect.bottom == platform.top and player_rect.x in range(platform.left, platform.right):
            return True
    return False

def new_game():
    choosing = True
    while choosing:
        window.fill(BLACK)
        game_over_text = game_over_txt.render('GAME OVER', True, WHITE)
        score_text = score_txt.render('SCORE: ' + str(count), True, WHITE)
        restart_text = restart_txt.render('RESTART', True, WHITE)
        menu_text = menu_txt.render('MAIN MENU', True, WHITE)

        window.blit(game_over_text, (150, 50))
        window.blit(score_text, (190, (window_height // 2) - 100))
        window.blit(restart_text, (220, 350))
        window.blit(menu_text, (210, 450))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                choosing = False
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if x in range(210, 500) and y in range(350, 430):
                    choosing = False
                    return True


        pygame.display.update()


def spawn_reward(platforms):
    max_y = window_width
    max_left = 0
    max_right = 0
    for platform in platforms:
        if platform.y < max_y:
            max_y = platform.y
            max_left = platform.left
            max_right = platform.right
    reward_rect = pygame.Rect(
        (max_left + max_right) // 2 - reward_width // 2,
        max_y - reward_height - 5,
        reward_width,
        reward_height
    )
    return reward_rect

platforms = generate_level()
reward_rect = spawn_reward(platforms)
player_rect = spawn_player(platforms)


while running:
    clock.tick(FPS)

    if player_rect.colliderect(reward_rect):
        count += 1
        counter = True

    if player_rect.bottom > window_height or timer == FPS * 10:
        if new_game():
            player_rect = spawn_player(platforms)
            platforms = generate_level()
            reward_rect = spawn_reward(platforms)
            player_rect = spawn_player(platforms)
            is_jump = False
            timer = 0
            FPS_count = 0
            jump_count = 0
            count = 0
            counter = False
            continue
        else:
            running = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and is_on_platform():
                is_jump = True
                player_rect.y -= 5
                jump_count += 5

    if is_jump:
        player_rect.y -= 5
        jump_count += 5
        if jump_count >= 200:
            jump_count = 0
            is_jump = False

    if not is_on_platform() and not is_jump:
        player_rect.y += 5

    window.fill(BLACK)

    update_game(player_rect, platforms)

    pygame.draw.rect(window, WHITE, player_rect)
    pygame.draw.rect(window, RED, reward_rect)

    for platform in platforms:
        pygame.draw.rect(window, WHITE, platform)

    count_text = count_txt.render(str(count), False, WHITE)
    if (10 - timer / FPS) > 5:
        timer_text = timer_txt.render(str(round((10 - timer / FPS), 1)), False, WHITE)
    else:
        timer_text = timer_txt.render(str(round((10 - timer / FPS), 1)), False, RED)

    window.blit(count_text, (0, 0))
    window.blit(timer_text, (0, 50))

    if counter:
        platforms = generate_level()
        reward_rect = spawn_reward(platforms)
        player_rect = spawn_player(platforms)
        timer = 0
        counter = False

    pygame.display.update()

    timer += 1

pygame.quit()
