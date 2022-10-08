import pygame

class Button:
    def __init__(self, files: list[str], position, command) -> None:
        # stores 2 images:
        # first image is showed always
        # second image is showed when the user is hovering the button
        self.images = []
        self.current_image = 0
        for file in files:
            self.images.append(pygame.image.load(file))

        # button width, height
        self.width = self.images[0].get_width()
        self.height = self.images[0].get_height()
        self.position = (position[0] - self.width/2, position[1] - self.height/2)
        # command which is executed on click
        self.command = command

    # checking if mouse collides with the button
    def get_hover(self) -> bool:
        rect = pygame.Rect(self.position[0], self.position[1], self.width, self.height)
        if rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
            return True
        return False

    # updating button image
    def update(self) -> None:
        if self.get_hover():
            self.current_image = 1
        else:
            self.current_image = 0
    
    def render(self, surface: pygame.Surface):
        surface.blit(self.images[self.current_image], self.position)