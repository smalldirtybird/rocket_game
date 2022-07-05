import asyncio
import time
import curses

TIC_TIMEOUT = 1


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
    stars_count = 5
    zero_column_intent = 20
    column_step = 10
    coroutines = []
    for number in range(stars_count):
        column = zero_column_intent + column_step * number
        coroutines.append(blink(canvas, row, column))
    curses.curs_set(False)
    canvas.border()
    while True:
        try:
            for coroutine in coroutines.copy():
                coroutine.send(None)
                canvas.refresh()
            time.sleep(TIC_TIMEOUT)
        except StopIteration:
            break
            

def main():
    curses.update_lines_cols()
    curses.wrapper(draw)


if __name__ == '__main__':
    main()
