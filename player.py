import pygame
from weapon import Canon


class Player(pygame.sprite.Sprite):
    def __init__(self, game, joystick):
        super().__init__()
        self.game = game
        self.joystick: pygame.joystick.Joystick = joystick
        self.rect = pygame.rect.Rect(self.game.gvars.SCREEN_WIDTH/2, 0, 100, 100)
        self.x, self.y = self.rect.center
        self.collideXRect = self.rect.inflate(0, -51)
        self.collideYRect = self.rect.inflate(0, 0)
        self.axeX = 0
        self.axeY = 0
        self.speedX = 0
        self.speedY = 0
        self.upPressed = False
        self.leftPressed = False
        self.lastJump = 0
        self.onGround = False
        self.hp = 3
        self.percent = 0
        self.weapon = None
        self.item = None
        self.attacks = pygame.sprite.Group()
        self.permeable = False

    def update(self, time):
        self.getInputs()
        self.controls(time)
        self.physics()
        self.checkDeath()
        self.collectItems(time)
        self.display()
        self.updateWeapon(time)
        self.attacks.update(time)

    def updateWeapon(self, time):
        if self.weapon:
            self.weapon.update(time)

    def respawn(self):
        self.rect = pygame.rect.Rect(self.game.gvars.SCREEN_WIDTH / 2, 0, 100, 100)
        self.x, self.y = self.rect.center
        self.collideXRect = self.rect.inflate(0, -51)
        self.collideYRect = self.rect.inflate(0, 0)
        self.speedX = 0
        self.speedY = 0
        self.lastJump = 0
        self.percent = 0
        self.onGround = False
        self.weapon = None
        self.item = None

    def controls(self, time):
        if self.onGround:
            self.speedX += self.axeX * 2
            if (self.axeY < -0.4 or self.upPressed) and self.lastJump+0.4 < time:
                self.speedY = -30
                self.lastJump = time
        else:
            self.speedX += self.axeX/3
        if self.leftPressed and self.weapon:
            self.weapon.use(time)

    def getInputs(self):
        self.axeX = self.joystick.get_axis(0)
        self.axeY = self.joystick.get_axis(1)
        # no joycon drift
        if round(self.axeX * 30) == 0:
            self.axeX = 0
        if round(self.axeY * 30) == 0:
            self.axeY = 0
        self.upPressed = self.joystick.get_button(3)
        self.leftPressed = self.joystick.get_button(2)

    def harm(self, amount, direction: int):
        self.percent += amount
        self.speedX += (self.percent+amount)*direction

    def checkDeath(self):
        if self.y > 1300:
            if self.hp > 1:
                self.hp -= 1
                self.respawn()
            else:
                self.kill()

    def collectItems(self, time):
        for item in self.game.items:
            if self.rect.colliderect(item.rect):
                item.kill()
                self.joystick.rumble(0.1, 0.5, 150)
                name = item.name
                if name == "canon":
                    self.weapon = Canon(self.game, self, time)

    def collisions(self):
        self.onGround = False
        for platform in self.game.platforms:
            if self.rect.colliderect(platform.rect):
                # clip left
                if self.collideXRect.colliderect(platform.rect) and not platform.permeable:
                    if self.rect.left < platform.rect.right < self.rect.right:
                        self.speedX = 0
                        self.rect.left = platform.rect.right
                        self.x = self.rect.centerx
                    # clip right
                    elif self.rect.left < platform.rect.left < self.rect.right:
                        self.speedX = 0
                        self.rect.right = platform.rect.left
                        self.x = self.rect.centerx
                elif self.collideYRect.colliderect(platform.rect):
                    # clip down
                    if platform.rect.bottom > self.rect.bottom > platform.rect.top:
                        self.speedY = 0
                        self.rect.bottom = platform.rect.top + 1
                        self.onGround = True
                        self.y = self.rect.centery
                    # clip up
                    elif platform.rect.bottom > self.rect.top > platform.rect.top and not platform.permeable:
                        self.speedY *= -0.2
                        self.rect.top = platform.rect.bottom + 1
                        self.y = self.rect.centery

    def physics(self):
        # apply forces
        self.x += self.speedX
        self.y += self.speedY
        self.rect.center = self.collideXRect.center = self.collideYRect.center = self.x, self.y

        # friction
        if self.onGround:
            self.speedX *= 0.85
        else:
            self.speedX *= 0.955
        self.speedY *= 0.955
        # gravity
        self.speedY += 0.9

        self.collisions()

    def display(self):
        pygame.draw.rect(self.game.screen, (255, 255, 255), self.rect)
