import pygame
import sys
import random
import pygame_menu
import os

pygame.init()
FRAME_COLOR = (140, 140, 140)
LIGHT_GREY = (170, 170, 170)
GREY = (200, 200, 200)
HEADER_COLOR = (50, 50, 50)
SNAKE_COLOR = (0, 100, 0)

image = pygame.image.load("picture_menu.png")
apple_image = pygame.image.load("apple.png")

count_of_blocks = 20
HEADER = 70
block_size = 20
MARGIN = 1

size = [560, 530]
screen = pygame.display.set_mode(size)

pygame.display.set_caption('Проект "Змейка"')
timer = pygame.time.Clock()
courier = pygame.font.SysFont('courier', 28)
dif_speed = 7
running = True
variant = 1


def load_image(name, papka):
    fullname = os.path.join(papka, name)
    image = pygame.image.load(fullname)
    return image


# Передвижение основной части
move_horizontal_image = load_image("h_body1.png", "skin1")
move_vertical_image = load_image("v_body1.png", "skin1")
# Голова
head_image = load_image("h_top1.png", "skin1")
up_down_image = load_image("v_top1.png", "skin1")
# Поворот
up_right_image = load_image("turn_1.png", "skin1")

back_vertical = load_image("v_back1.png", "skin1")
back_horizontal = load_image("h_back1.png", "skin1")
head_image = pygame.transform.scale(head_image, (20, 20))
up_down_image = pygame.transform.scale(up_down_image, (20, 20))
move_horizontal_image = pygame.transform.scale(move_horizontal_image, (20, 20))
move_vertical_image = pygame.transform.scale(move_vertical_image, (20, 20))
back_vertical = pygame.transform.scale(back_vertical, (20, 20))
back_horizontal = pygame.transform.scale(back_horizontal, (20, 20))
up_right_image = pygame.transform.scale(up_right_image, (20, 20))


def skin_select(value, skin):
    global move_horizontal_image, \
        move_vertical_image, head_image, up_down_image, up_right_image, back_vertical, back_horizontal
    if skin == 2:
        move_horizontal_image = load_image("h_body1.png", "skin2")
        move_vertical_image = load_image("v_body1.png", "skin2")
        head_image = load_image("h_top1.png", "skin2")
        up_down_image = load_image("v_top1.png", "skin2")
        up_right_image = load_image("turn_1.png", "skin2")
        back_vertical = load_image("v_back1.png", "skin2")
        back_horizontal = load_image("h_back1.png", "skin2")
    elif skin == 3:
        move_horizontal_image = load_image("h_body1.png", "skin3")
        move_vertical_image = load_image("v_body1.png", "skin3")
        head_image = load_image("h_top1.png", "skin3")
        up_down_image = load_image("v_top1.png", "skin3")
        up_right_image = load_image("turn_1.png", "skin3")
        back_vertical = load_image("v_back1.png", "skin3")
        back_horizontal = load_image("h_back1.png", "skin3")
    head_image = pygame.transform.scale(head_image, (20, 20))
    up_down_image = pygame.transform.scale(up_down_image, (20, 20))
    move_horizontal_image = pygame.transform.scale(move_horizontal_image, (20, 20))
    move_vertical_image = pygame.transform.scale(move_vertical_image, (20, 20))
    back_vertical = pygame.transform.scale(back_vertical, (20, 20))
    back_horizontal = pygame.transform.scale(back_horizontal, (20, 20))
    up_right_image = pygame.transform.scale(up_right_image, (20, 20))


class SnakeBlock:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_inside(self):
        return 0 <= self.x < count_of_blocks and 0 <= self.y < count_of_blocks

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y and isinstance(other, SnakeBlock):
            return True
        return False


# Получение координат
def snake_images(row, column):
    x_position = block_size + column * block_size + MARGIN * (column + 1)
    y_position = HEADER + block_size + row * block_size + MARGIN * (row + 1)
    return x_position, y_position


# Отрисовка поля
def draw_block(color, row, column):
    pygame.draw.rect(screen, color,
                     (block_size + column * block_size + MARGIN * (column + 1),
                      HEADER + block_size + row * block_size + MARGIN * (row + 1), block_size, block_size))


# Установка сложности
def set_difficulty(value, difficulty):
    global dif_speed
    if difficulty == 1:
        dif_speed = 7
    else:
        dif_speed = 3
    return dif_speed


# Начало игры (кнопка из меню)
def start_the_game():
    switch = 3
    snake_blockss = list()
    total = 0
    running = True
    global dif_speed
    speed = dif_speed
    flag = True
    head_pos = list()
    head_pos.append((9, 8))

    # Новое место яблоку
    def get_random_empty_block():
        x = random.randint(0, count_of_blocks - 1)
        y = random.randint(0, count_of_blocks - 1)
        empty_block = SnakeBlock(x, y)
        while empty_block in snake_blocks:
            x = random.randint(0, count_of_blocks - 1)
            y = random.randint(0, count_of_blocks - 1)
        empty_block = SnakeBlock(x, y)
        return empty_block

    snake_blocks = [SnakeBlock(9, 7), SnakeBlock(9, 8)]
    snake_blockss.append((9, 7))
    snake_blockss.append((9, 8))

    apple = get_random_empty_block()
    d_row = buf_row = 0
    d_col = buf_col = 1

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Выход")
                sys.exit()

            # Проверка нажатий
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and d_col != 0:
                    if switch == 1:
                        flag = False
                    else:
                        flag = True
                        if len(snake_blocks) > 2:
                            head_pos.append((snake_blocks[-1].x, snake_blocks[-1].y, switch))
                        switch = 1
                    buf_row = -1
                    buf_col = 0
                elif event.key == pygame.K_a and d_row != 0:
                    if switch == 2:
                        flag = False
                    else:
                        flag = True
                        if len(snake_blocks) > 2:
                            head_pos.append((snake_blocks[-1].x, snake_blocks[-1].y, switch))
                        switch = 2
                    buf_row = 0
                    buf_col = -1
                elif event.key == pygame.K_d and d_row != 0:
                    if switch == 3:
                        flag = False
                    else:
                        flag = True
                        if len(snake_blocks) > 2:
                            head_pos.append((snake_blocks[-1].x, snake_blocks[-1].y, switch))
                        switch = 3
                    buf_row = 0
                    buf_col = 1
                elif event.key == pygame.K_s and d_col != 0:
                    if switch == 4:
                        flag = False
                    else:
                        flag = True
                        if len(snake_blocks) > 2:
                            head_pos.append((snake_blocks[-1].x, snake_blocks[-1].y, switch))
                        switch = 4
                    buf_row = 1
                    buf_col = 0

        screen.fill(FRAME_COLOR)
        pygame.draw.rect(screen, HEADER_COLOR, [0, 0, size[0], HEADER])

        text_total = courier.render(f"Собрано яблок: {total}", False, LIGHT_GREY)
        text_speed = courier.render(f"Скорость: {speed}", False, LIGHT_GREY)
        screen.blit(text_total, (block_size, block_size))
        screen.blit(text_speed, (block_size + 320, block_size))

        for row in range(count_of_blocks):
            for column in range(count_of_blocks):
                if (row + column) % 2 == 0:
                    color = GREY
                else:
                    color = LIGHT_GREY

                draw_block(color, row, column)

        head = snake_blocks[-1]

        # Проигрыш при выходе за поле
        if not head.is_inside():
            print("Вы вышли за поле!")
            break

        # Проверка стороны, в которую движется змейка и отрисовка головы с хвостом
        if switch == 4:
            screen.blit(up_down_image, snake_images(snake_blocks[-1].x, snake_blocks[-1].y))
        elif switch == 2:
            new_head_image = pygame.transform.flip(head_image, True, False)
            screen.blit(new_head_image, snake_images(snake_blocks[-1].x, snake_blocks[-1].y))
        elif switch == 3:
            screen.blit(head_image, snake_images(snake_blocks[-1].x, snake_blocks[-1].y))
        elif switch == 1:
            new_up_down_image = pygame.transform.flip(up_down_image, False, True)
            screen.blit(new_up_down_image, snake_images(snake_blocks[-1].x, snake_blocks[-1].y))

        # Отрисовка тела
        for i in range(len(snake_blocks)):
            if len(snake_blocks) > 2:
                if i != 0 and i != len(snake_blocks) - 1:
                    block_pos = (snake_blocks[i].y, snake_blocks[i].x)
                    prev_block_pos = (snake_blocks[i + 1].y, snake_blocks[i + 1].x)
                    next_block_pos = (snake_blocks[i - 1].y, snake_blocks[i - 1].x)
                    a = block_pos[0] - next_block_pos[0]
                    b = block_pos[1] - next_block_pos[1]
                    if block_pos[0] - prev_block_pos[0] > 0 and b > 0:
                        new_up_right = pygame.transform.flip(up_right_image, True, True)
                        screen.blit(new_up_right, snake_images(snake_blocks[i].x, snake_blocks[i].y))
                    elif block_pos[0] - prev_block_pos[0] > 0 and b < 0:
                        new_up_right = pygame.transform.flip(up_right_image, True, False)
                        screen.blit(new_up_right, snake_images(snake_blocks[i].x, snake_blocks[i].y))

                    elif block_pos[0] - prev_block_pos[0] < 0 and b < 0:
                        new_up_right = pygame.transform.flip(up_right_image, False, False)
                        screen.blit(new_up_right, snake_images(snake_blocks[i].x, snake_blocks[i].y))
                    elif block_pos[0] - prev_block_pos[0] < 0 and b > 0:
                        new_up_right = pygame.transform.flip(up_right_image, False, True)
                        screen.blit(new_up_right, snake_images(snake_blocks[i].x, snake_blocks[i].y))

                    elif block_pos[1] - prev_block_pos[1] > 0 and a > 0:
                        new_up_right = pygame.transform.flip(up_right_image, True, True)
                        screen.blit(new_up_right, snake_images(snake_blocks[i].x, snake_blocks[i].y))
                    elif block_pos[1] - prev_block_pos[1] > 0 and a < 0:
                        new_up_right = pygame.transform.flip(up_right_image, False, True)
                        screen.blit(new_up_right, snake_images(snake_blocks[i].x, snake_blocks[i].y))

                    elif block_pos[1] - prev_block_pos[1] < 0 and a < 0:
                        new_up_right = pygame.transform.flip(up_right_image, False, False)
                        screen.blit(new_up_right, snake_images(snake_blocks[i].x, snake_blocks[i].y))
                    elif block_pos[1] - prev_block_pos[1] < 0 and a > 0:
                        new_up_right = pygame.transform.flip(up_right_image, True, False)
                        screen.blit(new_up_right, snake_images(snake_blocks[i].x, snake_blocks[i].y))

                    elif block_pos[0] - next_block_pos[0] == 0 and block_pos[1] - next_block_pos[1] != 0:
                        screen.blit(move_vertical_image, snake_images(snake_blocks[i].x, snake_blocks[i].y))
                    elif block_pos[1] - next_block_pos[1] == 0 and block_pos[0] - next_block_pos[0] != 0:
                        screen.blit(move_horizontal_image, snake_images(snake_blocks[i].x, snake_blocks[i].y))

                # =========================================================================================
                # Хвост змеи
                # =========================================================================================
                elif i == 0:
                    block_pos = (snake_blocks[i].y, snake_blocks[i].x)
                    prev_block_pos = (snake_blocks[i + 1].y, snake_blocks[i + 1].x)
                    if block_pos[0] - prev_block_pos[0] == 0 and block_pos[1] - prev_block_pos[1] < 0:
                        screen.blit(back_vertical, snake_images(snake_blocks[i].x, snake_blocks[i].y))
                    elif block_pos[0] - prev_block_pos[0] == 0 and block_pos[1] - prev_block_pos[1] > 0:
                        new_back_vertical = pygame.transform.flip(back_vertical, False, True)
                        screen.blit(new_back_vertical, snake_images(snake_blocks[i].x, snake_blocks[i].y))
                    elif block_pos[0] - prev_block_pos[0] > 0 and block_pos[1] - prev_block_pos[1] == 0:
                        screen.blit(back_horizontal, snake_images(snake_blocks[i].x, snake_blocks[i].y))
                    else:
                        new_back_horizontal = pygame.transform.flip(back_horizontal, True, False)
                        screen.blit(new_back_horizontal, snake_images(snake_blocks[i].x, snake_blocks[i].y))

                elif i == 0:
                    block_pos = (snake_blocks[i].y, snake_blocks[i].x)
                    prev_block_pos = (snake_blocks[i + 1].y, snake_blocks[i + 1].x)
                    if block_pos[0] - prev_block_pos[0] == 0 and block_pos[1] - prev_block_pos[1] < 0:
                        screen.blit(back_vertical, snake_images(snake_blocks[i].x, snake_blocks[i].y))
                    elif block_pos[0] - prev_block_pos[0] == 0 and block_pos[1] - prev_block_pos[1] > 0:
                        new_back_vertical = pygame.transform.flip(back_vertical, False, True)
                        screen.blit(new_back_vertical, snake_images(snake_blocks[i].x, snake_blocks[i].y))
                    elif block_pos[0] - prev_block_pos[0] > 0 and block_pos[1] - prev_block_pos[1] == 0:
                        screen.blit(back_horizontal, snake_images(snake_blocks[i].x, snake_blocks[i].y))
                    else:
                        new_back_horizontal = pygame.transform.flip(back_horizontal, True, False)
                        screen.blit(new_back_horizontal, snake_images(snake_blocks[i].x, snake_blocks[i].y))

            elif len(snake_blocks) == 2 and i == 0:
                if switch == 4:
                    screen.blit(back_vertical, snake_images(snake_blocks[i].x, snake_blocks[i].y))
                elif switch == 1:
                    new_back_vertical = pygame.transform.flip(back_vertical, False, True)
                    screen.blit(new_back_vertical, snake_images(snake_blocks[i].x, snake_blocks[i].y))
                elif switch == 2:
                    screen.blit(back_horizontal, snake_images(snake_blocks[i].x, snake_blocks[i].y))
                else:
                    new_back_horizontal = pygame.transform.flip(back_horizontal, True, False)
                    screen.blit(new_back_horizontal, snake_images(snake_blocks[i].x, snake_blocks[i].y))

        screen.blit(apple_image, snake_images(apple.x, apple.y))
        pygame.display.flip()

        if apple == head:
            total += 1
            speed = total // 5 + dif_speed
            flag = False
            apple = get_random_empty_block()
        d_row = buf_row
        d_col = buf_col
        new_head = SnakeBlock(head.x + d_row, head.y + d_col)

        if new_head in snake_blocks:
            print("Вы попытались съесть самого себя")
            break

        snake_blocks.append(new_head)
        if flag:
            snake_blocks.pop(0)
        else:
            flag = True

        timer.tick(speed)


main_theme = pygame_menu.themes.THEME_BLUE.copy()
main_theme.set_background_color_opacity(0.5)
menu = pygame_menu.Menu(350, 320, '',
                        theme=main_theme)
menu.add_text_input('Имя :', default='Игрок')
menu.add_selector('Сложность :', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)
menu.add_selector('Скин :', [("Обычный", 1), ("Сердечки", 2), ("Радуга", 3)], onchange=skin_select)
menu.add_button('Играть', start_the_game)
menu.add_button('Выход', pygame_menu.events.EXIT)

while True:
    screen.blit(image, (0, 0))
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit()

    if menu.is_enabled():
        menu.update(events)
        menu.draw(screen)

    pygame.display.update()
