from pygame.sprite import Sprite
import pygame


class Virus(Sprite):
    """ """

    def __init__(self, settings, screen):
        super().__init__()

        self.settings = settings
        self.screen = screen

        self.image = pygame.image.load("game_images/virus.bmp")
        self.rect = self.image.get_rect()

        self.rect.x = 50  # self.rect.width
        self.rect.y = 50  # self.rect.height

        self.x = float(self.rect.x)

    def blitme(self):
        """ """
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        """ """
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """ Moving the virus right """

        self.x += (self.settings.virus_speed_factor *
                   self.settings.fleet_direction)
        self.rect.x = self.x
