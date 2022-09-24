import pygame
from os import listdir


images = {name: pygame.image.load(f"assets/textures/buttons/{name}").convert_alpha() for name in
          listdir("assets/textures/buttons")}


class Button(pygame.sprite.Sprite):
    def __init__(self, image: str, screen, gvars, pos: tuple, showMenu: str, onClick, useCondition=None, whenHover=None, whenNoHover=None, isPopup=False):
        super().__init__()

        self.image = images[f"{image}.png"]
        self.rect = self.image.get_rect()
        self.onClick = onClick
        self.showMenu = showMenu
        self.useCondition = useCondition
        self.whenHover = whenHover
        self.whenNoHover = whenNoHover
        self.isPopup = isPopup
        self.gvars = gvars

        if useCondition:
            self.mask = pygame.mask.from_surface(self.image)
            self.grised = self.image.copy()
            self.grised.blit(self.mask.to_surface(setcolor=(20, 25, 20, 150), unsetcolor=(0, 0, 0, 0)), (0, 0))

        self.scale = 1

        if pos[0] == "center":
            self.rect.centerx = screen.get_width() / 2
        else:
            self.rect.centerx = pos[0]

        if pos[1] == "center":
            self.rect.centery = screen.get_height() / 2
        else:
            self.rect.centery = pos[1]

    def update(self, screen, mousePos):
        if self.isPopup == bool(self.gvars.popup) and self.rect.collidepoint(mousePos):
            if self.whenHover is None:
                self.scale += (1.15-self.scale)/5
            else:
                self.whenHover()
        else:
            if self.whenNoHover is None:
                self.scale += (1 - self.scale) / 5
            else:
                self.whenNoHover()

        if self.scale < 1.0005:
            image = self.image
        else:
            image = pygame.transform.smoothscale(self.image, (self.rect.w * self.scale, self.rect.h * self.scale))

        if self.useCondition:
            if self.useCondition():
                screen.blit(image, image.get_rect(center=self.rect.center))
            else:
                screen.blit(self.grised, self.rect)
        else:
            screen.blit(image, image.get_rect(center=self.rect.center))
