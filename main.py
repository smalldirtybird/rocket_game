import asyncio
import time
import curses


def draw(canvas):
    row, column = (5, 20)
    curses.curs_set(False)
    canvas.border()
    while True:
        canvas.refresh()
        star_blink = blink(canvas, row, column)
        star_blink.send(None)
        time.sleep(1)
        canvas.refresh()
        star_blink.send(None)
        time.sleep(1)
        canvas.refresh()
        star_blink.send(None)
        time.sleep(1)
        canvas.refresh()
        star_blink.send(None)
        time.sleep(1)


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
