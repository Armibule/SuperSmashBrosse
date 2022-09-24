import pygame
from time import time
from os import chdir
from pathlib import Path
chdir(Path(__file__).parent)

pygame.init()
pygame.mixer.set_num_channels(4)
screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN | pygame.RESIZABLE | pygame.SCALED)

from buttons import Button
from textInputs import TextInput
from texts import Text
from choiceList import ChoiceList
from gVars import GVars
from save import Save
from mouseManager import MouseManager
from game import Game
import pyperclip


mouseManager = MouseManager(screen)
gvars = GVars(screen, mouseManager)

pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

save = Save(gvars)
game = Game(screen, gvars, joysticks)

bg = pygame.image.load("assets/textures/bg.png").convert()
title = pygame.image.load("assets/textures/title.png").convert_alpha()
titleRect = title.get_rect(center=(gvars.SCREEN_WIDTH/2, 200))
popupBack = pygame.image.load("assets/textures/popupBack.png").convert_alpha()
popupCanvas = pygame.image.load("assets/textures/popupCanvas.png").convert_alpha()
popupCanvasRect = popupCanvas.get_rect(center=gvars.SCREEN_CENTER)
popupCanvasScale = 0.3


buttons = [Button("yes", screen, gvars, ("center", "center"), "menu", lambda:gvars.setMenu("play"))]
texts = []
textInputs = []
choiceLists = []

FPS = 60
clock = pygame.time.Clock()

while gvars.running:
    mousePos = pygame.mouse.get_pos()
    currentTime = time()

    screen.blit(bg, (0, 0))

    # MENUS
    if gvars.menu == "menu":
        screen.blit(title, titleRect)

    elif gvars.menu == "play":
        game.update(currentTime)

    # ELEMENTS
    for button in buttons:
        if button.showMenu == gvars.menu and not button.isPopup:
            button.update(screen, mousePos)

    for text in texts:
        if text.showMenu == gvars.menu and not text.isPopup:
            text.update()

    for textInput in textInputs:
        if textInput.showMenu == gvars.menu and not textInput.isPopup:
            textInput.display()

    for choiceList in choiceLists:
        if choiceList.showMenu == gvars.menu:
            choiceList.display(mousePos)

    if gvars.popup:
        screen.blit(popupBack, (0, 0))

        if gvars.popupCanvasScale > 0.99:
            screen.blit(popupCanvas, popupCanvasRect)
        else:
            gvars.popupCanvasScale += (1-gvars.popupCanvasScale)/5
            transformed = pygame.transform.smoothscale(popupCanvas, (popupCanvasRect.w*gvars.popupCanvasScale, popupCanvasRect.h*gvars.popupCanvasScale))
            screen.blit(transformed, transformed.get_rect(center=gvars.SCREEN_CENTER))

        for button in buttons:
            if button.showMenu == gvars.popup and button.isPopup:
                button.update(screen, mousePos)

        for text in texts:
            if text.showMenu == gvars.popup and text.isPopup:
                text.update()

        for textInput in textInputs:
            if textInput.showMenu == gvars.popup and textInput.isPopup:
                textInput.display()

    mouseManager.update(currentTime)

    # EVENTS
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            gvars.keyPressed[event.key] = True

            if event.key == pygame.K_ESCAPE:
                pygame.display.toggle_fullscreen()

            shortcut = False
            if event.key == pygame.K_v:
                mods = pygame.key.get_mods()
                if mods & pygame.KMOD_CTRL:
                    shortcut = True
                    for textInput in textInputs:
                        if textInput.active:
                            textInput.paste(pyperclip.paste())
                            break

            if not shortcut:
                # ajouter le caractères aux inputs de texte qui sont actifs
                for textInput in textInputs:
                    if textInput.active:
                        if event.key == pygame.K_BACKSPACE:
                            textInput.backspace()
                        else:
                            textInput.addChar(event.unicode)
                        break

        elif event.type == pygame.KEYUP:
            gvars.keyPressed[event.key] = False

        elif event.type == pygame.JOYBUTTONDOWN:
            print(event.button)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                openPopup = bool(gvars.popup)

                clickFound = False
                for button in buttons:
                    if (button.showMenu == gvars.menu or button.showMenu == gvars.popup) and button.isPopup == openPopup and button.rect.collidepoint(mousePos):
                        if button.useCondition:
                            if button.useCondition():
                                button.onClick()
                                clickFound = True
                        else:
                            button.onClick()
                            clickFound = True
                        break

                for textInput in textInputs:
                    if (textInput.showMenu == gvars.menu or textInput.showMenu == gvars.popup) and textInput.imageRect.collidepoint(event.pos) and textInput.isPopup == openPopup and not clickFound:
                        if not textInput.active:
                            textInput.setActive(True)
                        clickFound = True
                        break
                    else:
                        textInput.setActive(False)

                if not clickFound:
                    for choiceList in choiceLists:
                        if choiceList.showMenu == gvars.menu and choiceList.choicesRect.collidepoint(event.pos):
                            choiceList.checkChoices(event.pos)
                            clickFound = True
                            break

                if not clickFound and not openPopup:
                    gvars.clickedPos = mousePos
            elif event.button == 4:
                for choiceList in choiceLists:
                    if choiceList.showMenu == gvars.menu and choiceList.choicesRect.collidepoint(mousePos):
                        choiceList.scrollSpeed -= 5
            elif event.button == 5:
                for choiceList in choiceLists:
                    if choiceList.showMenu == gvars.menu and choiceList.choicesRect.collidepoint(mousePos):
                        choiceList.scrollSpeed += 5

        elif event.type == pygame.QUIT:
            gvars.setPopup("askToQuit")
            gvars.running = False

    pygame.display.flip()

    if gvars.running:
        clock.tick(FPS)

pygame.quit()
save.save()
