import pygame
import sys
import random
import pygame_menu

pygame.init()
FRAME_COLOR = (140, 140, 140)
LIGHT_GREY = (170, 170, 170)
GREY = (200, 200, 200)
HEADER_COLOR = (50, 50, 50)
SNAKE_COLOR = (0, 100, 0)

# Фон и яблоко
image = pygame.image.load("picture_menu.png")
apple_image = pygame.image.load("apple.png")
# Передвижение основной части
move_horizontal_image = pygame.image.load("move.png")
up_down_moves = pygame.image.load("up_down_moves.png")
# Голова
head_image = pygame.image.load("top.png")
up_down_image = pygame.image.load("up_down.png")
# Поворот
up_right_image = pygame.image.load("up_right.png")

back_vertical = pygame.image.load("back_vertical.png")
back_horizontal = pygame.image.load("back_horizontal.png")

head_image = pygame.transform.scale(head_image, (20, 20))
up_down_image = pygame.transform.scale(up_down_image, (20, 20))
move_horizontal_image = pygame.transform.scale(move_horizontal_image, (20, 20))
move_vertical_image = pygame.transform.scale(up_down_moves, (20, 20))
back_vertical = pygame.transform.scale(back_vertical, (20, 20))
back_horizontal = pygame.transform.scale(back_horizontal, (20, 20))
up_right_image = pygame.transform.scale(up_right_image, (20, 20))

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
    pre_switch = switch
    turns = False
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
                            head_pos.append((snake_blocks[-1].x, snake_blocks[-1].y))
                            pre_switch = switch
                        switch = 1
                    buf_row = -1
                    buf_col = 0
                elif event.key == pygame.K_a and d_row != 0:
                    if switch == 2:
                        flag = False
                    else:
                        flag = True
                        if len(snake_blocks) > 2:
                            head_pos.append((snake_blocks[-1].x, snake_blocks[-1].y))
                        pre_switch = switch
                        switch = 2
                    buf_row = 0
                    buf_col = -1
                elif event.key == pygame.K_d and d_row != 0:
                    if switch == 3:
                        flag = False
                    else:
                        flag = True
                        if len(snake_blocks) > 2:
                            head_pos.append((snake_blocks[-1].x, snake_blocks[-1].y))
                            pre_switch = switch
                        switch = 3
                    buf_row = 0
                    buf_col = 1
                elif event.key == pygame.K_s and d_col != 0:
                    if switch == 4:
                        flag = False
                    else:
                        flag = True
                        if len(snake_blocks) > 2:
                            head_pos.append((snake_blocks[-1].x, snake_blocks[-1].y))
                        pre_switch = switch
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
                if i != 0 and i != len(snake_blocks) - 1 and len(head_pos) > 0 \
                        and (snake_blocks[i].x, snake_blocks[i].y) == head_pos[0]:
                    block_pos = (snake_blocks[i].x, snake_blocks[i].y)
                    other_block_pos = (snake_blocks[i + 1].x, snake_blocks[i + 1].y)
                    print(other_block_pos)
                    if head_pos[0][0] - other_block_pos[0] > 0 and switch == 1:
                        new_up_right = pygame.transform.flip(up_right_image, True, False)
                        screen.blit(new_up_right, snake_images(snake_blocks[i].x, snake_blocks[i].y))
                        if i == 1:
                            head_pos.pop(0)
                    elif switch == 3 and pre_switch == 4:
                        new_up_right = pygame.transform.flip(up_right_image, False, True)
                        screen.blit(new_up_right, snake_images(snake_blocks[i].x, snake_blocks[i].y))
                        if i == 1:
                            head_pos.pop(0)

                    elif switch == 4 and pre_switch == 3:
                        new_up_right = pygame.transform.flip(up_right_image, True, False)
                        screen.blit(new_up_right, snake_images(snake_blocks[i].x, snake_blocks[i].y))
                        if i == 1:
                            head_pos.pop(0)
                    elif switch == 1 and pre_switch == 2:
                        new_up_right = pygame.transform.flip(up_right_image, False, True)
                        screen.blit(new_up_right, snake_images(snake_blocks[i].x, snake_blocks[i].y))
                        if i == 1:
                            head_pos.pop(0)

                    elif block_pos[0] - other_block_pos[0] > 0:
                        new_up_right = pygame.transform.flip(up_right_image, True, False)
                        screen.blit(new_up_right, snake_images(snake_blocks[i].x, snake_blocks[i].y))
                        screen.blit(up_right_image, snake_images(snake_blocks[i].x, snake_blocks[i].y))
                        if i == 1:
                            head_pos.pop(0)


                    elif head_pos[0][0] - other_block_pos[0] < 0 and switch == 2:
                        screen.blit(up_right_image, snake_images(snake_blocks[i].x, snake_blocks[i].y))
                    elif head_pos[0][0] - other_block_pos[0] > 0 and switch == 4:
                        screen.blit(up_right_image, snake_images(snake_blocks[i].x, snake_blocks[i].y))
                        if i == 1:
                            head_pos.pop(0)

                    elif block_pos == head_pos[0] and switch == 2 and pre_switch == 4:
                        new_up_right = pygame.transform.flip(up_right_image, True, True)
                        screen.blit(new_up_right, snake_images(snake_blocks[i].x, snake_blocks[i].y))
                        if i == 1:
                            head_pos.pop(0)
                    elif block_pos == head_pos[0] and switch == 1 and pre_switch == 3:
                        new_up_right = pygame.transform.flip(up_right_image, True, True)
                        screen.blit(new_up_right, snake_images(snake_blocks[i].x, snake_blocks[i].y))
                        if i == 1:
                            head_pos.pop(0)
                    # =========================================================================================
                    # Вертикальное и горизонтальное движение
                    # =========================================================================================
                    elif head_pos[0][0] - block_pos[0] == 0 and head_pos[0][1] - block_pos[1] != 0:
                        screen. \
                            blit(move_horizontal_image, snake_images(snake_blocks[i].x, snake_blocks[i].y))
                    elif head_pos[0][0] - block_pos[0] != 0 and head_pos[0][1] - block_pos[1] == 0:
                        screen. \
                            blit(move_vertical_image, snake_images(snake_blocks[i].x, snake_blocks[i].y))

                    elif i != 0 and i != len(snake_blocks) - 1:
                        print("hello")
                        if switch == 1 or switch == 4:
                            screen.blit(move_vertical_image, snake_images(snake_blocks[i].x, snake_blocks[i].y))
                        else:
                            screen.blit(move_horizontal_image, snake_images(snake_blocks[i].x, snake_blocks[i].y))
                # =========================================================================================
                # Задняя
                # =========================================================================================
                elif i == 0 and len(head_pos) > 0:
                    block_pos = (snake_blocks[i].x, snake_blocks[i].y)
                    if head_pos[0][0] - block_pos[0] >= 0 and head_pos[0][1] - block_pos[1] == 0:
                        new_back_vertical = pygame.transform.flip(back_vertical, False, False)
                        screen.blit(new_back_vertical, snake_images(snake_blocks[i].x, snake_blocks[i].y))
                    elif head_pos[0][0] - block_pos[0] <= 0 and head_pos[0][1] - block_pos[1] == 0:
                        new_back_vertical = pygame.transform.flip(back_vertical, False, True)
                        screen.blit(new_back_vertical, snake_images(snake_blocks[i].x, snake_blocks[i].y))
                    elif head_pos[0][0] - block_pos[0] == 0 and head_pos[0][1] - block_pos[1] >= 0:
                        new_back_horizontal = pygame.transform.flip(back_horizontal, True, False)
                        screen.blit(new_back_horizontal, snake_images(snake_blocks[i].x, snake_blocks[i].y))
                    elif head_pos[0][0] - block_pos[0] == 0 and head_pos[0][1] - block_pos[1] <= 0:
                        new_back_horizontal = pygame.transform.flip(back_horizontal, False, False)
                        screen.blit(new_back_horizontal, snake_images(snake_blocks[i].x, snake_blocks[i].y))
                    else:
                        head_pos.pop(0)

                elif i == 0:
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
                print(i)

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
menu = pygame_menu.Menu(300, 320, '',
                        theme=main_theme)
menu.add_text_input('Имя :', default='Игрок')
menu.add_selector('Сложность :', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)
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
