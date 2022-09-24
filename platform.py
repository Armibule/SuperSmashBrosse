import pygame


class Platform(pygame.sprite.Sprite):
    def __init__(self, game, rect: pygame.rect.Rect, permeable: bool):
        super().__init__()
        self.game = game
        self.rect = rect
        self.permeable = permeable

    def update(self):
        pygame.draw.rect(self.game.screen, (0, 0, 0), self.rect)
