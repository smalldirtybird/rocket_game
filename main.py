import asyncio
import curses
import os
import random
import time
from itertools import cycle

TIC_TIMEOUT = 0.1
SPACE_KEY_CODE = 32
LEFT_KEY_CODE = 260
RIGHT_KEY_CODE = 261
UP_KEY_CODE = 259
DOWN_KEY_CODE = 258


async def blink(canvas, row, column, symbol='*'):
    time_delay = random.randint(0, 25)
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        for _ in range(time_delay + 20):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(time_delay + 3):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        for _ in range(time_delay + 5):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(time_delay + 3):
            await asyncio.sleep(0)


def generate_starry_sky(canvas, window_height, window_width):
    stars_count = max_columns = window_width - 1
    max_rows = window_height - 1
    coords_seen = []
    stars = []
    for number in range(stars_count):
        row = random.randint(1, max_rows)
        column = random.randint(1, max_columns)
        if [row, column] not in coords_seen:
            stars.append(blink(
                canvas, row, column, symbol=random.choice('+*.:')))
            coords_seen.append([row, column])
    return stars


def draw_frame(canvas, start_row, start_column, text, negative=False):
    rows_number, columns_number = canvas.getmaxyx()
    for row, line in enumerate(text.splitlines(), round(start_row)):
        if row < 0:
            continue
        if row >= rows_number:
            break
        for column, symbol in enumerate(line, round(start_column)):
            if column < 0:
                continue
            if column >= columns_number:
                break
            if symbol == ' ':
                continue
            if row == rows_number - 1 and column == columns_number - 1:
                continue
            symbol = symbol if not negative else ' '
            canvas.addch(row, column, symbol)


def read_controls(canvas):
    rows_direction = columns_direction = 0
    space_pressed = False
    while True:
        pressed_key_code = canvas.getch()
        if pressed_key_code == -1:
            break
        if pressed_key_code == UP_KEY_CODE:
            rows_direction = -1
        if pressed_key_code == DOWN_KEY_CODE:
            rows_direction = 1
        if pressed_key_code == RIGHT_KEY_CODE:
            columns_direction = 1
        if pressed_key_code == LEFT_KEY_CODE:
            columns_direction = -1
        if pressed_key_code == SPACE_KEY_CODE:
            space_pressed = True
    return rows_direction, columns_direction, space_pressed


async def animate_spaceship(
        canvas, window_height, window_width, animation_frames):
    canvas.nodelay(True)
    spaceship_height = 9
    spaceship_width = 5
    vertical_center_position = (window_height - spaceship_height) / 2
    horizontal_center_position = (window_width - spaceship_width) / 2
    row = vertical_center_position
    column = horizontal_center_position
    vertical_borders = [0, window_height - spaceship_height]
    horizontal_borders = [0, window_width - spaceship_width]
    for frame in cycle(animation_frames):
        rows_direction, columns_direction, space_pressed = read_controls(
            canvas)
        row += rows_direction
        column += columns_direction
        if row < min(vertical_borders):
            row = min(vertical_borders)
        if row > max(vertical_borders):
            row = max(vertical_borders)
        if column < min(horizontal_borders):
            column = min(horizontal_borders)
        if column > max(horizontal_borders):
            column = max(horizontal_borders)
        draw_frame(canvas, row, column, frame)
        canvas.refresh()
        await asyncio.sleep(0)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, frame, negative=True)


def draw(canvas, animation_frames):
    window_height, window_width = curses.window.getmaxyx(canvas)
    coroutines = generate_starry_sky(
        canvas, window_height, window_width)
    spaceship = animate_spaceship(
        canvas, window_height, window_width, animation_frames)
    coroutines.append(spaceship)
    curses.curs_set(False)
    while True:
        try:
            canvas.refresh()
            for coroutine in coroutines.copy():
                coroutine.send(None)
            time.sleep(TIC_TIMEOUT)
        except StopIteration:
            coroutines.remove(coroutine)


def main():
    spaceship_frames_folder_path = os.path.normpath(r'./animations/spaceship/')
    spaceship_frames_filepaths = os.listdir(spaceship_frames_folder_path)
    spaceship_frames = []
    for filename in spaceship_frames_filepaths:
        filepath = os.path.join(spaceship_frames_folder_path, filename)
        with open(filepath) as frame_file:
            spaceship_frames.append(frame_file.read())
    curses.wrapper(draw, spaceship_frames)


if __name__ == '__main__':
    main()
