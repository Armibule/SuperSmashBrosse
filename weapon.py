import pygame
from attack import *


class Weapon(pygame.sprite.Sprite):
    def __init__(self, game, player, time, cooldown, maxUses, product, maxTime, vibration: tuple):
        super().__init__()
        self.game = game
        self.player = player
        self.lastUsed = 0
        self.uses = 0
        self.createdTime = time

        self.cooldown = cooldown
        self.maxUses = maxUses
        self.product = product
        self.maxTime = maxTime
        self.vibration = vibration

    def use(self, time):
        if self.lastUsed+self.cooldown < time:
            self.uses += 1
            self.lastUsed = time
            self.player.attacks.add(self.product(self.game, self.player))
            self.player.joystick.rumble(*self.vibration)
            if self.uses >= self.maxUses:
                self.delete()

    def delete(self):
        self.player.joystick.rumble(1, 0, 80)
        self.player.weapon = None
        self.kill()

    def display(self):
        pygame.draw.rect(self.game.screen, (0, 0, 0), self.player.rect.inflate(-5, -40))

    def checkDeath(self, time):
        if time-self.createdTime > self.maxTime:
            self.delete()

    def update(self, time):
        self.checkDeath(time)
        self.display()


class Canon(Weapon):
    def __init__(self, game, player, time):
        super().__init__(game, player, time, 1, 5, CannonBall, 10, (0.2, 0.1, 80))
