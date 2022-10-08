import pygame

class Render:
    def image(surface: pygame.Surface, position: tuple[int], file: str, transform_image = False, size = None):
        image = pygame.image.load(file)
        # changing the scale of the image in case there is a specification
        if transform_image:
            image = pygame.transform.scale(image, size)
        surface.blit(image, position)
    
    def text(surface: pygame.Surface, font: pygame.font.Font, text: str, position: tuple[int]):
        font_text = font.render(text, False, (255, 255, 255))
        text_width, text_height = font.size(text)
        surface.blit(font_text, (position[0] - text_width/2, position[1] - text_height/2))

    def background(surface: pygame.Surface):
        surface.fill(pygame.Color("#15BDAC"))