import pygame


class Root:
    # creating a window
    def init(size: tuple[int], caption: str) -> pygame.display.set_mode:
        root = pygame.display.set_mode(size)
        pygame.display.set_caption(caption)
        # icon shown in the top left corner of the window
        pygame.display.set_icon(pygame.image.load("data/images/image_board.png"))
        return root
    
    # updating the screen
    def update(clock: pygame.time.Clock, fps: int):
        clock.tick(fps)
        pygame.display.update()