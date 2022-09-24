import pygame


class Text(pygame.sprite.Sprite):
    def __init__(self, screen: object, pos: tuple, showMenu: str, fontName: str, size: int, bold: bool, italic: bool, color: tuple, text: str, isPopup=False):
        super().__init__()
        self.screen = screen
        self.font = pygame.font.SysFont(fontName, size, bold, italic)
        self.fontName = fontName
        self.seize = size
        self.bold = bold
        self.italic = italic
        self.color = color
        self.text = text
        self.image = self.font.render(text, True, color)
        self.showMenu = showMenu
        self.pos = pos
        self.isPopup = isPopup
        self.updatePos()

    def setText(self, text: str):
        self.text = text
        self.image = self.font.render(text, True, self.color)
        self.updatePos()

    def setColor(self, color: tuple):
        self.color = color
        self.image = self.font.render(self.text, True, color)

    def setSeize(self, size: int):
        self.seize = size
        self.font = pygame.font.SysFont(self.fontName, size, self.bold, self.italic)
        self.image = self.font.render(self.text, True, self.color)
        self.updatePos()

    def update(self):
        self.screen.blit(self.image, self.rect)

    def updatePos(self):
        self.rect = self.image.get_rect()

        if self.pos[0] == "center":
            self.rect.centerx = self.screen.get_width() / 2
        else:
            self.rect.centerx = self.pos[0]

        if self.pos[1] == "center":
            self.rect.centery = self.screen.get_height() / 2
        else:
            self.rect.centery = self.pos[1]
