import pygame


class TextInput:
    def __init__(self, screen, showMenu: str, fontName: str, seize: int, bold: bool, italic: bool,
                 color: tuple, text: str, backColor: tuple, pos, height, maxCharacters: int, allowedCharacters: str, maxX, gvars, isPopup=False):
        self.gvars = gvars
        self.screen = screen
        self.font = pygame.font.SysFont(fontName, seize, bold, italic)
        self.color = color

        self.showMenu = showMenu
        self.backColor = backColor
        self.pos = pos
        self.height = height

        self.isPopup = isPopup
        self.active = False
        self.allowedCharacters = allowedCharacters
        self.maxX = maxX
        self.maxCharacters = maxCharacters

        self.setText(text)

        self.update()

    def setText(self, text: str):
        self.text = text
        if self.active:
            self.textImage = self.font.render(f"{text}|", True, self.color)
        else:
            self.textImage = self.font.render(text, True, self.color)
        self.update()

    def display(self):
        self.screen.blit(self.image, self.pos)

    def setActive(self, active: bool):
        if self.active != active:
            self.active = active
            self.setText(self.text)
            self.update()

    def update(self):
        self.imageRect = pygame.rect.Rect(0, 0, max(min(self.textImage.get_width()+20, self.maxX), 30), self.height)
        self.image = pygame.surface.Surface((self.imageRect.w, self.imageRect.h))

        self.image.fill(self.backColor)

        self.image.blit(self.textImage, self.textImage.get_rect(center=self.imageRect.center))

        if self.active:
            pygame.draw.rect(self.image, (236, 167, 59), self.imageRect, 4)

        self.imageRect.x, self.imageRect.y = self.pos

    def addChar(self, char: str):
        if self.validCharacter(char) and len(self.text) != self.maxCharacters:
            # ajoute le caractère
            self.setText(self.text + char)

    def paste(self, text: str):
        filtered = "".join([char if self.validCharacter(char) else "" for char in text])
        filtered = filtered[:self.maxCharacters-len(self.text)]
        self.setText(self.text + filtered)

    def backspace(self):
        self.setText(self.text[:-1])

    def validCharacter(self, char):
        return char in self.allowedCharacters
