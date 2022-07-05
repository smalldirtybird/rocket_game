import asyncio
import time
import curses


def draw(canvas):
    row, column = (5, 20)
    curses.curs_set(False)
    canvas.border()
    canvas.refresh()
    while True:
        canvas.addstr(row, column, '*', curses.A_DIM)
        time.sleep(2)
        canvas.refresh()
        canvas.addstr(row, column, '*')
        time.sleep(0.3)
        canvas.refresh()
        canvas.addstr(row, column, '*', curses.A_BOLD)
        time.sleep(0.5)
        canvas.refresh()
        canvas.addstr(row, column, '*')
        time.sleep(0.3)
        canvas.refresh()


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


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
