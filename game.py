import pygame
from random import randint, choice
from player import Player
from platform import Platform
from item import Item


allItems = ["canon"]


class Game:
    def __init__(self, screen, gvars, joysticks):
        self.screen = screen
        self.gvars = gvars
        self.time = 0
        self.platforms = pygame.sprite.Group([Platform(self, pygame.rect.Rect(100, 800, 1200, 50), False), Platform(self, pygame.rect.Rect(100, 300, 50, 500), False), Platform(self, pygame.rect.Rect(100, 600, 100, 50), False)])
        self.players = pygame.sprite.Group([Player(self, joystick) for joystick in joysticks])
        self.items = pygame.sprite.Group([Item(self, "canon")])

    def update(self, time):
        self.time = time
        if len(self.items) < 5 and randint(0, 100) == 0:
            self.spawnItem()

        self.platforms.update()
        self.players.update(time)
        self.items.update()

    def spawnItem(self):
        self.items.add(Item(self, choice(allItems)))
