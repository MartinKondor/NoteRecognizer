import pygame as pg
from pygame import locals as keys

from src.display import Display
from src.config import *


def check_events():
    """
    :returns bool: false if window must be exited
    """
    for event in pg.event.get():
        if event.type == keys.QUIT:
            return False
    return True


if __name__ == '__main__':
    if not pg.font:
        print('ERROR: fonts are disabled')
        exit(1)
    if not pg.mixer:
        print('ERROR: sounds are disabled')
        exit(1)

    pg.init()
    screen_size = (WINDOW_WIDTH, WINDOW_HEIGHT,)
    display = Display()

    if IS_FULLSCREEN:
        screen = pg.display.set_mode(screen_size, pg.FULLSCREEN)
    else:
        screen = pg.display.set_mode(screen_size)

    pg.display.set_caption('Note detector')
    pg.mouse.set_visible(1)
    clock = pg.time.Clock()

    while check_events():

        # Display and update
        display.display(screen)
        
        clock.tick(FPS)
        pg.display.update()
        pg.display.flip()

    display.close()
    pg.quit()
