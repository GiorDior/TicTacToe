import pygame

class Sound:
    def play(file: str):
        sound = pygame.mixer.Sound(file)
        sound.play()