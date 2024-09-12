import pygame
import random
import time

# Инициализация Pygame
pygame.init()

# Константы
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
CELL_SIZE = 50
GRID_WIDTH = 10
GRID_HEIGHT = 10
N = 5

# Создание окна
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Игра")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Функция для рисования кнопки
def draw_button(text, x, y, width, height, color, hover_color):
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()

    if x < mouse_pos[0] < x + width and y < mouse_pos[1] < y + height:
        pygame.draw.rect(screen, hover_color, (x, y, width, height))
        if mouse_pressed[0]:
            return True
    else:
        pygame.draw.rect(screen, color, (x, y, width, height))

    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)

    return False

# Функция для открытия окна настроек
def open_settings_window():
    settings_window = pygame.display.set_mode((400, 300))
    pygame.display.set_caption("Настройки")

    # Создаем поля ввода текста
    grid_width_input_box = pygame.Rect(50, 50, 300, 50)
    grid_height_input_box = pygame.Rect(50, 150, 300, 50)
    n_input_box = pygame.Rect(50, 250, 300, 50)

    # Инициализируем значения
    grid_width_input = ""
    grid_height_input = ""
    n_input = ""

    active_input_box = None  # Текущий активный поле ввода

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    try:
                        global GRID_WIDTH, GRID_HEIGHT, N
                        GRID_WIDTH = int(grid_width_input)
                        GRID_HEIGHT = int(grid_height_input)
                        N = int(n_input)
                        running = False
                    except ValueError:
                        pass  # Обработать неверный ввод
                elif event.key == pygame.K_BACKSPACE:
                    if active_input_box == grid_width_input_box:
                        grid_width_input = grid_width_input[:-1]
                    elif active_input_box == grid_height_input_box:
                        grid_height_input = grid_height_input[:-1]
                    elif active_input_box == n_input_box:
                        n_input = n_input[:-1]
                elif event.unicode.isdigit():
                    if active_input_box == grid_width_input_box:
                        grid_width_input += event.unicode
                    elif active_input_box == grid_height_input_box:
                        grid_height_input += event.unicode
                    elif active_input_box == n_input_box:
                        n_input += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if grid_width_input_box.collidepoint(event.pos):
                    active_input_box = grid_width_input_box
                elif grid_height_input_box.collidepoint(event.pos):
                    active_input_box = grid_height_input_box
                elif n_input_box.collidepoint(event.pos):
                    active_input_box = n_input_box
                else:
                    active_input_box = None

        settings_window.fill(WHITE)

        # Рисуем поля ввода
        pygame.draw.rect(settings_window, GRAY, grid_width_input_box)
        font = pygame.font.Font(None, 36)
        text_surface = font.render(f"GRID_WIDTH: {grid_width_input}", True, BLACK)
        settings_window.blit(text_surface, (grid_width_input_box.x + 10, grid_width_input_box.y + 10))

        pygame.draw.rect(settings_window, GRAY, grid_height_input_box)
        text_surface = font.render(f"GRID_HEIGHT: {grid_height_input}", True, BLACK)
        settings_window.blit(text_surface, (grid_height_input_box.x + 10, grid_height_input_box.y + 10))

        pygame.draw.rect(settings_window, GRAY, n_input_box)
        text_surface = font.render(f"N: {n_input}", True, BLACK)
        settings_window.blit(text_surface, (n_input_box.x + 10, n_input_box.y + 10))

        pygame.display.flip()

    pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Функция для рисования сетки
def draw_grid():
    # Рисование сетки
    for x in range(0, WINDOW_WIDTH, CELL_SIZE):
        for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
            # Рисование горизонтальных и вертикальных линий
            pygame.draw.line(screen, BLACK, (x, 0), (x, WINDOW_HEIGHT), 1)
            pygame.draw.line(screen, BLACK, (0, y), (WINDOW_WIDTH, y), 1)

            # Рисование диагональных линий
            pygame.draw.line(screen, BLACK, (x, y), (x + CELL_SIZE, y + CELL_SIZE), 1)
            pygame.draw.line(screen, BLACK, (x + CELL_SIZE, y), (x, y + CELL_SIZE), 1)


# Функция для рисования игрока
def draw_player(player_pos, PLAYER_COLOR):
    # Определяем координаты точки на линии сетки
    x = player_pos[0] * CELL_SIZE + CELL_SIZE // 2
    y = player_pos[1] * CELL_SIZE + CELL_SIZE // 2

    # Рисуем точку на линии сетки
    pygame.draw.circle(screen, PLAYER_COLOR, (x, y), 5)

# Функция для вычисления расстояния между игроком и целью
def get_distance(player_pos, target_pos):
    dx = abs(player_pos[0] - target_pos[0])
    dy = abs(player_pos[1] - target_pos[1])
    return dx + dy

# Основной цикл игры
def main_game_loop():
    # Начальные позиции игрока и цели
    global distance
    player_pos = [0, 0]
    target_pos = [random.randint(1, GRID_WIDTH - 1), random.randint(1, GRID_HEIGHT - 1)]
    last_move_time = 0
    move_delay = 0.1  # Задержка между перемещениями (в секундах)

    n = 0

    # Счетчик ходов
    running = True

    while running:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Обновление позиции игрока
        keys = pygame.key.get_pressed()
        current_time = time.time()

        if current_time - last_move_time >= move_delay:
            dx = 0
            dy = 0

            if keys[pygame.K_LEFT]:
                dx = -0.5
            elif keys[pygame.K_RIGHT]:
                dx = 0.5
            elif keys[pygame.K_UP]:
                dy = -0.5
            elif keys[pygame.K_DOWN]:
                dy = 0.5

            new_x = player_pos[0] + dx
            new_y = player_pos[1] + dy

            # Проверяем, чтобы новая позиция игрока была в пределах игрового поля
            if new_x >= 0 and new_x < GRID_WIDTH and new_y >= 0 and new_y < GRID_HEIGHT:
                player_pos = [new_x, new_y]
                last_move_time = current_time
                n += 1

        # Обновление позиции цели
        if n == N:
            dx = 0
            dy = 0

            if player_pos[0] > target_pos[0]:
                dx = -0.5
            elif player_pos[0] < target_pos[0]:
                dx = 0.5

            if player_pos[1] > target_pos[1]:
                dy = -0.5
            elif player_pos[1] < target_pos[1]:
                dy = 0.5

            new_x = target_pos[0] + dx
            new_y = target_pos[1] + dy

            # Проверяем, чтобы новая позиция цели была в пределах игрового поля
            if new_x < 0:
                new_x = 0.5
            elif new_x >= GRID_WIDTH:
                new_x = GRID_WIDTH - 1

            if new_y < 0:
                new_y = 0.5
            elif new_y >= GRID_HEIGHT:
                new_y = GRID_HEIGHT - 1

            # Если цель находится в углу, двигаем ее в сторону от угла
            if (new_x == 0 and new_y == 0) or (new_x == GRID_WIDTH - 1 and new_y == 0) or (
                    new_x == 0 and new_y == GRID_HEIGHT - 1) or (new_x == GRID_WIDTH - 1 and new_y == GRID_HEIGHT - 1):
                if dx < 0:
                    new_x = 0.5
                elif dx > 0:
                    new_x = GRID_WIDTH - 1
                if dy < 0:
                    new_y = 0.5
                elif dy > 0:
                    new_y = GRID_HEIGHT - 1

            target_pos = [new_x, new_y]
            print(f"Расстояние до цели: {distance}")
            n = 0

        # Проверка, достиг ли игрок цели
        distance = get_distance(player_pos, target_pos)
        if distance == 0:
            print("Вы поймали цель!")
            running = False
            continue

        # Отображение игрового поля и игрока
        screen.fill(WHITE)
        draw_grid()
        draw_player(player_pos, BLUE)
        draw_player(target_pos, RED)

        # Отрисовка цели
        pygame.display.flip()

    pygame.quit()

# Главный цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)

    if draw_button("Начать игру", 50, 50, 200, 50, GRAY, (160, 160, 160)):
        # Запускаем игру
        main_game_loop()
        pygame.quit()  # Закрываем окно Pygame
        exit()

    if draw_button("Настройки", 50, 150, 200, 50, GRAY, (160, 160, 160)):
        open_settings_window()

    pygame.display.flip()

pygame.quit()
