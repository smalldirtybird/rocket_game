import asyncio
import time
import curses
import random

TIC_TIMEOUT = 0.1


async def blink(canvas, row, column, symbol='*'):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        for _ in range(20):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(3):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        for _ in range(5):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(3):
            await asyncio.sleep(0)


def generate_starry_sky(canvas):
    max_rows, max_columns = curses.window.getmaxyx(canvas)
    stars_count = max_columns
    coords_seen = []
    stars = []
    for number in range(stars_count):
        row = random.randint(1, max_rows - 1)
        column = random.randint(1, max_columns - 1)
        if [row, column] not in coords_seen:
            stars.append(blink(canvas, row, column, symbol=random.choice('+*.:')))
            coords_seen.append([row, column])
    return stars


def draw(canvas):
    stars = generate_starry_sky(canvas)
    curses.curs_set(False)
    canvas.border()
    while True:
        try:
            for star in stars.copy():
                star.send(None)
                canvas.refresh()
            time.sleep(TIC_TIMEOUT)
        except StopIteration:
            break


def main():
    curses.update_lines_cols()
    curses.wrapper(draw)


if __name__ == '__main__':
    main()
