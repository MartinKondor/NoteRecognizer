import pygame
from pygame import locals as keys

from src.display import Display
from src.config import IS_FULLSCREEN, WINDOW_WIDTH, WINDOW_HEIGHT, FPS


def check_events():
    """
    :returns bool: false if window must be exited
    """
    for event in pygame.event.get():
        if event.type == keys.QUIT:
            return False
    return True


if __name__ == '__main__':
    if not pygame.font:
        print('ERROR: fonts are disabled')
        exit(1)
    if not pygame.mixer:
        print('ERROR: sounds are disabled')
        exit(1)
    if WINDOW_HEIGHT < 600:
        print(f'Invalid window height ({WINDOW_HEIGHT}) it must be > 600')
        exit(1)
    if FPS < 30:
        FPS = 30
        
    # Initialize window
    pygame.init()
    screen_size = (WINDOW_WIDTH, WINDOW_HEIGHT,)
    if IS_FULLSCREEN:
        screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode(screen_size)
        
    pygame.display.set_caption('Note detector')
    pygame.mouse.set_visible(1)
    clock = pygame.time.Clock()
    display = Display()

    while check_events():
        display.display(screen)
        clock.tick(FPS)
        pygame.display.update()
        pygame.display.flip()
        
    pygame.quit()
