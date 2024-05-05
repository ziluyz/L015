import pygame
import random
import sys

pygame.init()

# Параметры экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Игра Тир")
icon = pygame.image.load("Img/icon.png")
pygame.display.set_icon(icon)

# Параметры цели
target_img = pygame.image.load("Img/pig.png")
target_width = 80
target_height = 80
target_x = random.randint(0, SCREEN_WIDTH - target_width)
target_y = random.randint(0, SCREEN_HEIGHT - target_height)

# Цвета
red = (255, 0, 0)
black = (0, 0, 0)
white = (255, 255, 255)

# Шрифт и размер текста
font = pygame.font.Font(None, 36)

# Начальные настройки таймера
total_time = 600  # 1 минута = 600 сантисекунд
start_ticks = pygame.time.get_ticks()  # стартовое время

# Основной цикл приложения
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if target_x < event.pos[0] < target_x + target_width and target_y < event.pos[1] < target_y + target_height:
                target_x = random.randint(0, SCREEN_WIDTH - target_width)
                target_y = random.randint(0, SCREEN_HEIGHT - target_height)
    
     # Текущее время
    ticks = pygame.time.get_ticks()
    seconds = (ticks - start_ticks) // 100  # количество прошедших сантисекунд

    if seconds > total_time:
        running = False

    # Расчет оставшегося времени
    remaining_s_seconds = total_time - seconds
    remaining_seconds = remaining_s_seconds // 10 + 1

    # Отрисовка фона
    screen.fill(black)
    
    # Отрисовка цели
    screen.blit(target_img, (target_x, target_y))

    # Отрисовка шкалы времени
    time_bar_length = (remaining_s_seconds / total_time) * (SCREEN_WIDTH - 70)
    time_bar = pygame.Rect(10, 10, time_bar_length, 20)
    pygame.draw.rect(screen, red, time_bar)

    # Отрисовка текста с оставшимся временем
    text = font.render(f"{remaining_seconds}", True, white)
    screen.blit(text, (SCREEN_WIDTH - 50, 5))

    # Обновление экрана
    pygame.display.flip()

    # Задержка для снижения загрузки процессора
    pygame.time.delay(100)

pygame.quit()