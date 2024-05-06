import pygame
import random
import pygame.locals as pl
from sortedcontainers import SortedDict

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
big_font = pygame.font.SysFont('Comic Sans MS', 64)
small_font = pygame.font.SysFont('Comic Sans MS', 24)

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
target_img_1 = pygame.image.load("Img/pig.png").convert_alpha()
target_img_2 = pygame.image.load("Img/pig_2.png").convert_alpha()
target_img_3 = pygame.image.load("Img/pig_3.png").convert_alpha()
possible_targets = [(target_img_1, 80, 80), (target_img_2, 80, 110), (target_img_3, 80, 89)]

# Загружаем изображение для курсора
cursor_image = pygame.image.load('Img/cursor.png')
cursor_image = pygame.transform.scale(cursor_image, (64, 64))
cur_width, cur_height = cursor_image.get_size()

# Преобразование маски в строки для compile
cursor_strings = []
for y in range(cur_height):
    row = ''
    for x in range(cur_width):
        if cursor_image.get_at((x, y))[3] > 100:
            row += 'X'  # Белый пиксель
        else:
            row += ' '  # Прозрачный пиксель
    cursor_strings.append(row)

# Компилируем строки в данные для курсора
compiled_cursor = pygame.cursors.compile(cursor_strings, white='X', black='.')

# Установка курсора
pygame.mouse.set_cursor((cur_width, cur_height), (cur_width // 2, cur_height // 2), compiled_cursor[0], compiled_cursor[1])

# Выстрелы
bullet_hole = pygame.image.load("Img/bullethole.png")
bullet_width = 60
bullet_height = 60
bullet_hole = pygame.transform.scale(bullet_hole, (bullet_width, bullet_height))

class Target:
    def __init__(self):
        self.randomize()

    def randomize(self):
        self.shown = random.randint(0, 1)
        self.lifetime = random.randint(10, 20)
        self.selftime = 0
        if self.shown == 1:
            self.index = random.randint(0, 2)
            self.img, self.width, self.height = possible_targets[self.index]
            self.x = random.randint(10, SCREEN_WIDTH - self.width - 10)
            self.y = random.randint(time_bar_y + time_bar_height + 10, SCREEN_HEIGHT - self.height - 10)
            for target in targets:
                if target == self or target.shown == 0:
                    continue
                if (self.x < target.x + target.width + 10 and self.x + self.width > target.x - 10 and
                    self.y < target.y + target.height + 10 and self.y + self.height > target.y - 10):
                    self.shown = 0
    
    def show(self):
        if self.shown == 1:
            alpha = 255 * self.selftime / 5 if self.selftime < 5 else 255
            self.img.set_alpha(alpha)
            delta_x = random.randint(-5, 5)
            delta_y = random.randint(-5, 5)
            screen.blit(self.img, (self.x + delta_x, self.y + delta_y))
        self.selftime += 1
        if self.selftime >= self.lifetime:
            self.randomize()

targets = []
for _ in range(10):
    targets.append(Target())

# Начальные настройки таймера
total_time = 600  # 1 минута = 600 сантисекунд
start_ticks = pygame.time.get_ticks()  # стартовое время

def main_game():
    score = 0
    global running
    while running:
        # Отрисовка фона
        screen.fill(black)
        
        # Отрисовка целей
        for target in targets:
            target.show()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                screen.blit(bullet_hole, (event.pos[0]-bullet_width//2, event.pos[1] - bullet_height//2))
                for target in targets:
                    if target.shown == 1:
                        if target.x < event.pos[0] < target.x + target.width and target.y < event.pos[1] < target.y + target.height:
                            if target.index == 2:
                                score += 10
                            else:
                                score -= 20
                            target.randomize()
        
        # Текущее время
        ticks = pygame.time.get_ticks()
        s_seconds = (ticks - start_ticks) // 100  # количество прошедших сантисекунд

        if s_seconds > total_time:
            return

        # Расчет оставшегося времени
        remaining_s_seconds = total_time - s_seconds
        remaining_seconds = remaining_s_seconds // 10 + 1

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

def start_page():
    global running
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (screen.get_width() // 2 - text_start.get_width() // 2 <= event.pos[0] <= screen.get_width() // 2 + text_start.get_width() // 2 and
                    20 <= event.pos[1] <= 20 + text_start.get_height()):
                    return
        # Отрисовка фона
        screen.fill(black)

        # Отрисовка кнопки "START"
        phase = pygame.time.get_ticks() // 100 % 20
        if phase < 10:
            color = (255 * phase / 10, 255, 255 * (10 - phase) / 10)
        else:
            phase -= 10
            color = (255 * (10 - phase) / 10, 255, 255 * phase / 10)
        text_start = big_font.render("START", True, color)
        screen.blit(text_start, (screen.get_width() // 2 - text_start.get_width() // 2, 20))

        # Отрисовка таблицы рекордов
        y = 150
        for score, name in score_table.items():
            text = small_font.render(f"{name} - {score}", True, white)
            screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, y))
            y += 50

        pygame.display.flip()
        pygame.time.delay(100)

# Начальная таблица рекордов
score_table = SortedDict()
score_table[10] = "Kurt Cobain"
score_table[20] = "Michael Jackson"
score_table[30] = "Jessie J"
score_table[40] = "Elvis Presley"
score_table[50] = "Bob Marley"
score_table[60] = "Bob Dylan"
score_table[70] = "Queen"

# Основной цикл приложения
running = True
while running:
    start_page()
    main_game()

pygame.quit()