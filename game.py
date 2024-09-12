import pygame
import random
import time

# Инициализация Pygame
pygame.init()

# Константы
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
CELL_SIZE = 50
GRID_WIDTH = 12
GRID_HEIGHT = 12
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
    WINDOW_WIDTH = CELL_SIZE * GRID_WIDTH
    WINDOW_HEIGHT = CELL_SIZE * GRID_HEIGHT
    for x in range(0, WINDOW_WIDTH, CELL_SIZE):
        for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
            # Рисование горизонтальных и вертикальных линий
            pygame.draw.line(screen, BLACK, (x, 0), (x, WINDOW_HEIGHT), 1)
            pygame.draw.line(screen, BLACK, (0, y), (WINDOW_WIDTH, y), 1)

            # Рисование диагональных линий
            pygame.draw.line(screen, BLACK, (x, y), (x + CELL_SIZE, y + CELL_SIZE), 1)
            pygame.draw.line(screen, BLACK, (x + CELL_SIZE, y), (x, y + CELL_SIZE), 1)

            # Рисование вертикальной линии, разделяющей квадрат пополам
            pygame.draw.line(screen, BLACK, (x + CELL_SIZE // 2, y), (x + CELL_SIZE // 2, y + CELL_SIZE), 1)

            # Рисование горизонтальной линии, разделяющей квадрат пополам
            pygame.draw.line(screen, BLACK, (x, y + CELL_SIZE // 2), (x + CELL_SIZE, y + CELL_SIZE // 2), 1)


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
    global distance
    player_pos = [0, 0]
    target_pos = [random.randint(1, GRID_WIDTH - 1), random.randint(1, GRID_HEIGHT - 1)]
    last_move_time = 0
    move_delay = 0.1

    n = 0
    running = True

    # Вывод расстояния до цели в начале игры
    distance = get_distance(player_pos, target_pos)
    print(f"Расстояние до цели: {distance}")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        current_time = time.time()

        def update_position(pos, dx, dy):
            # Проверяем, чтобы новая позиция была в пределах игрового поля
            new_x = pos[0] + dx
            new_y = pos[1] + dy

            # Проверка на наличие ромба между квадратами
            if dx != 0 and dy != 0:
                # Проверяем препятствие
                if is_blocked(pos[0], pos[1], dx, dy):
                    return pos  # Если движение по диагонали заблокировано, возвращаем текущую позицию

            # Проверка границ игрового поля
            if 0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT:
                pos[0] = new_x
                pos[1] = new_y

            # Округляем до целого числа, если игрок на линии
            pos[0] = round(pos[0] * 2) / 2
            pos[1] = round(pos[1] * 2) / 2

            return pos

        def is_blocked(x, y, dx, dy):
            # Проверяем, есть ли ромб между квадратами в направлении движения (dx, dy)
            # Это примерная функция, которую нужно адаптировать под ваше игровое поле
            # Возвращаем True, если движение заблокировано, и False в противном случае
            if (dx == 0.5 and dy == 0.5) or (dx == -0.5 and dy == 0.5):
                # Проверка наличия ромба по диагонали вправо-вниз или влево-вниз
                if is_diamond_present(x, y):
                    return True
            elif (dx == 0.5 and dy == -0.5) or (dx == -0.5 and dy == -0.5):
                # Проверка наличия ромба по диагонали вправо-вверх или влево-вверх
                if is_diamond_present(x, y):
                    return True

            return False

        def is_diamond_present(x, y):
            # Примерная функция для проверки наличия ромба между квадратами
            # В данной реализации мы проверяем существование ромба в верхнем левом углу
            # и в правом нижнем углу квадрата, который задается координатами (x, y)
            # Это примерная логика, которую нужно адаптировать под вашу конкретную сетку

            # Проверка ромба в верхнем левом углу квадрата
            if x > 0 and y > 0:
                if (x % (CELL_SIZE // 2) == 0) and (y % (CELL_SIZE // 2) == 0):
                    return True

            # Проверка ромба в правом нижнем углу квадрата
            if (x + CELL_SIZE < WINDOW_WIDTH) and (y + CELL_SIZE < WINDOW_HEIGHT):
                if ((x + CELL_SIZE) % (CELL_SIZE // 2) == 0) and ((y + CELL_SIZE) % (CELL_SIZE // 2) == 0):
                    return True

            return False


        # В основной цикл добавьте проверку на движение по диагонали
        if current_time - last_move_time >= move_delay:
            dx = 0
            dy = 0

            if keys[pygame.K_LEFT]:
                dx = -1
                n += 1
            elif keys[pygame.K_RIGHT]:
                dx = 1
                n += 1
            elif keys[pygame.K_UP]:
                dy = -1
                n += 1
            elif keys[pygame.K_DOWN]:
                dy = 1
                n += 1

            # Поддержка диагонального движения
            if keys[pygame.K_LEFT] and keys[pygame.K_UP]:
                dx = -0.5
                dy = -0.5
                n += 1
            elif keys[pygame.K_LEFT] and keys[pygame.K_DOWN]:
                dx = -0.5
                dy = 0.5
                n += 1
            elif keys[pygame.K_RIGHT] and keys[pygame.K_UP]:
                dx = 0.5
                dy = -0.5
                n += 1
            elif keys[pygame.K_RIGHT] and keys[pygame.K_DOWN]:
                dx = 0.5
                dy = 0.5
                n += 1

            player_pos = update_position(player_pos, dx, dy)
            last_move_time = current_time

        if n > N:
            dx = 0
            dy = 0

            # Вычисляем направление движения к цели
            if player_pos[0] > target_pos[0]:
                dx = -1  # Движение влево
                print("Расстояние до цели:" + str(distance))
            elif player_pos[0] < target_pos[0]:
                dx = 1  # Движение вправо
                print("Расстояние до цели:" + str(distance))
            if player_pos[1] > target_pos[1]:
                dy = -1  # Движение вверх
                print("Расстояние до цели:" + str(distance))
            elif player_pos[1] < target_pos[1]:
                dy = 1  # Движение вниз
                print("Расстояние до цели:" + str(distance))

            # Диагональное движение
            if abs(player_pos[0] - target_pos[0]) == abs(player_pos[1] - target_pos[1]):
                if dx != 0 and dy != 0:
                    dx *= 0.5
                    dy *= 0.5
                print("Расстояние до цели:" + str(distance))

            # Поворот в углу для цели
            if (player_pos[0] == target_pos[0] and player_pos[1] < target_pos[1]) or \
                    (player_pos[0] < target_pos[0] and player_pos[1] == target_pos[1]):
                dx = 0.5
                dy = 0.5
            elif (player_pos[0] == target_pos[0] and player_pos[1] > target_pos[1]) or \
                    (player_pos[0] > target_pos[0] and player_pos[1] == target_pos[1]):
                dx = -0.5
                dy = -0.5

            target_pos = update_position(target_pos, dx, dy)
            n = 0

        distance = get_distance(player_pos, target_pos)
        if distance == 0:
            print("Вы поймали цель!")
            running = False
            continue

        screen.fill(WHITE)
        draw_grid()
        draw_player(player_pos, BLUE)
        #draw_player(target_pos, RED)

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
