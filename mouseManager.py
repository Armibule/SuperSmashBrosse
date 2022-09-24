import pygame
from math import sin


class MouseManager:
    def __init__(self, screen):
        self.screen = screen
        self.image = pygame.image.load("assets/textures/waitCursor.png")
        self.imageWidth = self.image.get_width()
        self.imageHeight = self.image.get_height()
        self.waiting = False

    def setWaiting(self, value: bool):
        self.waiting = value

        pygame.mouse.set_visible(not value)

    def update(self, time):
        if self.waiting:
            transformed = pygame.transform.smoothscale(self.image, (self.imageWidth*abs(sin(time*5)), self.imageWidth))
            self.screen.blit(transformed, transformed.get_rect(center=pygame.mouse.get_pos()))
