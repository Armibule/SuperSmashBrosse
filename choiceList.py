import pygame


class ChoiceList:
    def __init__(self, screen, gvars, showMenu: str, pos: tuple, width: int, height: int, maxOpen: int, textSize: int, textColor: tuple, textFont: str, bgColor: tuple, choices: list, choicesColors: tuple, question: str, maxSelected=-1, bold=False, italic=False):
        self.screen: pygame.Surface = screen
        self.gvars = gvars

        self.showMenu = showMenu

        self.rect = pygame.rect.Rect(*pos, width, height)
        self.maxOpen = maxOpen  # maximum de choix affichés quand déroulé
        self.choicesRect = pygame.rect.Rect(self.rect.left, self.rect.bottom, width, height*maxOpen)
        self.choicesSurf = pygame.Surface((width, height*len(choices)))

        self.font = pygame.font.SysFont(textFont, textSize, bold, italic)
        self.choicesFont = pygame.font.SysFont(textFont, textSize-20, bold, italic)
        self.textColor = textColor
        self.bgColor = bgColor

        self.choicesColors = choicesColors
        self.textImage = None
        self.textRect = None

        self.yScroll = 0
        self.scrollSpeed = 0

        if len(choices) > maxOpen:
            self.scrollBarRect = pygame.rect.Rect(0, 0, 5, height*(maxOpen/len(choices)))
        else:
            self.scrollBarRect = pygame.rect.Rect(0, 0, 5, 0)

        self.question = question
        self.renderText()
        self.choices = choices
        self.selected = []
        self.maxSelected = maxSelected

    def display(self, mousePos):
        self.screen.fill(self.bgColor, self.rect)
        self.screen.blit(self.textImage, self.textRect)

        mousePos = mousePos[0]-self.choicesRect.x, mousePos[1]-self.choicesRect.y+self.yScroll
        for choice in self.choices:
            choice.display(mousePos)
        self.screen.blit(self.choicesSurf, self.choicesRect, (0, self.yScroll, self.choicesRect.w, self.choicesRect.h))

        if len(self.choices) > self.maxOpen:
            self.updateScrollBar()

        self.scroll(self.scrollSpeed)
        self.scrollSpeed *= 0.85

    def scroll(self, amount):
        self.yScroll += amount
        self.yScroll = min(self.rect.height*max(0, len(self.choices)-self.maxOpen), max(0, self.yScroll))

    def getSelected(self):
        return [choice.value for choice in self.choices if choice.selected]

    def updateScrollBar(self):
        self.scrollBarRect.topright = (self.choicesRect.right-3, self.choicesRect.top+(self.choicesRect.h-self.scrollBarRect.h-8)*self.yScroll/(self.rect.height*(len(self.choices)-self.maxOpen))+4) # (self.rect.h * (self.maxOpen / len(self.choices)))
        self.screen.fill(self.textColor, self.scrollBarRect)

    def checkChoices(self, mousePos):
        transformedPos = mousePos[0]-self.choicesRect.x, mousePos[1]-self.choicesRect.y+self.yScroll

        for choice in self.choices:
            if choice.rect.collidepoint(transformedPos):
                choice.toggleSelect()

    def renderText(self):
        self.textImage = self.font.render(self.question, True, self.textColor)
        self.textRect = self.textImage.get_rect(left=self.rect.left+10, centery=self.rect.centery)

    @property
    def choices(self):
        return self._choices

    @choices.setter
    def choices(self, value):
        self.choicesSurf = pygame.Surface((self.rect.width, self.rect.height * len(value)))
        self._choices = [Choice(self, index, value) for index, value in enumerate(value)]
        if len(value) > self.maxOpen:
            self.scrollBarRect.h = self.rect.h * (self.maxOpen / len(value))
        self.scroll(0)


class Choice:
    def __init__(self, parent: ChoiceList, index: int, value: str):
        self.parent = parent
        self.index = index
        self.value = value
        self.selected = False

        self.rect = pygame.rect.Rect(0, self.parent.rect.height*self.index, self.parent.rect.w, self.parent.rect.h)

        self.renderText()

    def display(self, mousePos):
        self.parent.choicesSurf.fill(self.parent.choicesColors[self.index % 2], self.rect)
        self.parent.choicesSurf.blit(self.textImage, self.textRect)

        if self.selected:
            pygame.draw.rect(self.parent.choicesSurf, self.parent.gvars.WHITE, self.rect, 2)

        if self.rect.collidepoint(mousePos):
            self.parent.choicesSurf.fill((50, 50, 50), self.rect, pygame.BLEND_ADD)

    def renderText(self):
        self.textImage = self.parent.choicesFont.render(self.value, True, self.parent.textColor)
        self.textRect = self.textImage.get_rect(left=self.rect.left+10, centery=self.rect.centery)

    def toggleSelect(self):
        print(self.parent.maxSelected)
        if self.selected:
            self.selected = False
            if self.parent.maxSelected > 0:
                self.parent.selected.pop(self.parent.selected.index(self))
        else:
            if self.parent.maxSelected == -1:
                self.selected = True
                print("wtf2")
            elif self.parent.maxSelected == 0:
                pass
                print("wtf")
            else:
                print("hoi")
                self.selected = True

                self.parent.selected.append(self)
                if self.parent.maxSelected < len(self.parent.selected):
                    self.parent.selected.pop(0).turnOff()

        print(self.selected)

    def turnOff(self):
        self.selected = False
