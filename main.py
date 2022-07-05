import asyncio
import time
import curses


async def blink(canvas, row, column, symbol='*'):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        await asyncio.sleep(0)


def draw(canvas):
    row = 5
    animation_steps_number = 4
    stars_count = 5
    coroutines = []
    zero_column_intent = 20
    column_step = 10
    for number in range(stars_count):
        column = zero_column_intent + column_step * number
        coroutines.append(blink(canvas, row, column))
    curses.curs_set(False)
    canvas.border()
    while True:
        canvas.refresh()
        for num in range(animation_steps_number + 1):
            for coroutine in coroutines.copy():
                coroutine.send(None)
                canvas.refresh()
            time.sleep(1)


def main():
    curses.update_lines_cols()
    curses.wrapper(draw)


if __name__ == '__main__':
    main()
