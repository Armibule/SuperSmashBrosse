import pygame


class Attack(pygame.sprite.Sprite):
    def __init__(self, game, player, damage, maxTime, speed, vibration: tuple):
        super().__init__()
        self.game = game
        self.player = player
        self.createdTime = game.time
        self.rect = pygame.rect.Rect(player.x, player.y, 30, 30)
        self.x, self.y = self.rect.center

        self.damage = damage
        self.maxTime = maxTime
        self.speed = speed
        if self.player.axeX == 0:
            if player.speedX < 0:
                self.speed *= -1
        else:
            if self.player.axeX < 0:
                self.speed *= -1
        self.vibration = vibration

    def update(self, time):
        self.physics()
        self.checkDeath(time)
        self.checkTouch()
        self.display()

    def physics(self):
        self.x += self.speed
        self.rect.centerx = self.x

    def checkDeath(self, time):
        if self.createdTime+self.maxTime < time:
            self.kill()

    def checkTouch(self):
        for player in self.game.players:
            if player is not self.player and self.rect.colliderect(player.rect):
                vibration = self.vibration
                self.player.joystick.rumble(vibration[0]/1.4, vibration[1]/1.4, int(vibration[2]/1.3))
                player.joystick.rumble(*vibration)
                player.harm(self.damage, self.speed/abs(self.speed))
                self.kill()
                break

    def display(self):
        pygame.draw.rect(self.game.screen, (128, 128, 128), self.rect)


class CannonBall(Attack):
    def __init__(self, game, player):
        super().__init__(game, player, 5, 5, 10, (0.5, 0.15, 100))
