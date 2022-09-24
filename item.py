import pygame
from random import randint


class Item(pygame.sprite.Sprite):
    def __init__(self, game, name):
        super().__init__()
        self.game = game
        self.rect = pygame.rect.Rect(randint(100, self.game.gvars.SCREEN_WIDTH-100), -10, 50, 50)
        self.groundRect = self.rect.move(0, 25)
        self.x, self.y = self.rect.center
        self.speedX = 0
        self.speedY = 0
        self.name = name

    def update(self):
        self.physics()
        self.checkDeath()
        self.display()

    def physics(self):
        # apply forces
        self.x += self.speedX
        self.y += self.speedY
        self.rect.center = self.x, self.y
        self.groundRect = self.rect.move(0, 25)

        # friction
        self.speedX *= 0.95
        self.speedY *= 0.95

        # gravity
        self.speedY += 0.8
        self.collisions()

    def checkDeath(self):
        if self.y > 1300:
            self.kill()

    def collisions(self):
        for platform in self.game.platforms:
            if self.groundRect.colliderect(platform.rect):
                # clip down
                if platform.rect.bottom > self.groundRect.bottom > platform.rect.top:
                    self.speedY = 0
                    self.groundRect.bottom = platform.rect.top + 1
                    self.rect = self.groundRect.move(0, -25)
                    self.y = self.rect.centery

    def display(self):
        pygame.draw.rect(self.game.screen, (255, 255, 255), self.rect)
