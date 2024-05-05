import pygame
import random
import sys

pygame.init()

# Параметры экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Оформление приложения

pygame.display.set_caption("Игра Тир")
icon = pygame.image.load("Img/icon.png")
pygame.display.set_icon(icon)

# Цвета
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
black = (0, 0, 0)
white = (255, 255, 255)

# Шрифт и размер текста
font = pygame.font.SysFont('Comic Sans MS', 32)

# Параметры шкалы времени
text_time = font.render(f"Time:", True, white)
time_text_x = 10
time_bar_x = time_text_x + text_time.get_width() + 10
time_bar_y = 10
time_bar_width = SCREEN_WIDTH - 280 - text_time.get_width() - 10
time_bar_height = 40
time_x = time_bar_x + time_bar_width + 20

# Параметры табло подсчёта очков
score_text_x = SCREEN_WIDTH - 190
text_score = font.render(f"Score:", True, white)
score_x = score_text_x + text_score.get_width() + 10

# Параметры целей
target_img_1 = pygame.image.load("Img/pig.png")
target_img_2 = pygame.image.load("Img/pig_2.png")
target_img_3 = pygame.image.load("Img/pig_3.png")
targets = [(target_img_1, 80, 80), (target_img_2, 80, 110), (target_img_3, 80, 89)]

def random_target():
    global target_index,target_img, target_width, target_height, target_x, target_y, target_delay
    target_index = random.randint(0, 2)
    target_img, target_width, target_height = targets[target_index]
    target_x = random.randint(0, SCREEN_WIDTH - target_width)
    target_y = random.randint(time_bar_y + time_bar_height, SCREEN_HEIGHT - target_height)
    target_delay = random.randint(10, 20)

random_target()

# Начальные настройки таймера
total_time = 600  # 1 минута = 600 сантисекунд
start_ticks = pygame.time.get_ticks()  # стартовое время

# Основной цикл приложения
running = True
score = 0
while running:
    target_delay -= 1
    if target_delay <= 0:
        random_target()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if target_x < event.pos[0] < target_x + target_width and target_y < event.pos[1] < target_y + target_height:
                if target_index == 2:
                    score += 10
                else:
                    score -= 20
                random_target()
    
     # Текущее время
    ticks = pygame.time.get_ticks()
    s_seconds = (ticks - start_ticks) // 100  # количество прошедших сантисекунд

    if s_seconds > total_time:
        running = False

    # Расчет оставшегося времени
    remaining_s_seconds = total_time - s_seconds
    remaining_seconds = remaining_s_seconds // 10 + 1

    # Отрисовка фона
    screen.fill(black)
    
    # Отрисовка цели
    screen.blit(target_img, (target_x, target_y))

    # Отрисовка шкалы времени
    screen.blit(text_time, (time_text_x, 5))
    time_bar_length = (remaining_s_seconds / total_time) * time_bar_width
    if time_bar_length < 10:
        time_bar_length = 10
    time_bar = pygame.Rect(time_bar_x, time_bar_y, time_bar_width, time_bar_height)
    pygame.draw.rect(screen, red, time_bar)
    time_bar = pygame.Rect(time_bar_x + 3, time_bar_y + 3, time_bar_width - 6, time_bar_height - 6)
    pygame.draw.rect(screen, black, time_bar)
    time_bar = pygame.Rect(time_bar_x + 5, time_bar_y + 5, time_bar_length - 10, time_bar_height - 10)
    pygame.draw.rect(screen, red, time_bar)

    # Отрисовка текста с оставшимся временем
    text = font.render(f"{remaining_seconds}", True, red)
    screen.blit(text, (time_x, 5))

     # Отрисовка текста с очками
    text = font.render(f"{score}", True, green if score >= 0 else blue)
    screen.blit(text_score, (score_text_x, 5))
    screen.blit(text, (score_x, 5))

    # Обновление экрана
    pygame.display.flip()

    # Задержка для снижения загрузки процессора
    pygame.time.delay(100)

pygame.quit()