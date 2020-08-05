from pygame.sprite import Sprite
from random import randint
import pygame
from time import time


class Gift(Sprite):

    def __init__(self, screen, settings, stats):
        super().__init__()

        self.screen = screen
        self.settings = settings
        self.stats = stats
        self.speed = [1.1, 1.1]

        self.screen_rect = screen.get_rect()

        self.image = pygame.image.load("game_images/gold_star.bmp")
        self.rect = self.image.get_rect()

        self.rect.x = randint(0, self.screen_rect.width - self.rect.width)
        self.rect.y = randint(0, self.screen_rect.height - self.rect.height)

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):

        if (self.rect.x < 0) or (self.rect.right > self.screen_rect.right):
            self.speed[0] *= -1
        if (self.rect.bottom > self.screen_rect.height) or (self.rect.y < 0):
            self.speed[1] *= -1

        self.x += self.speed[0]
        self.y += self.speed[1]

        self.rect.x = self.x
        self.rect.y = self.y

    def edge_hit_check(self):

        if (self.rect.x < 0) or (self.rect.right > self.screen_rect.right):
            self.speed[0] *= -1
        if (self.rect.bottom > self.screen_rect.height) or (self.rect.y < 0):
            self.speed[1] *= -1

    def star_time_checker(self, time_1, time_2):

        if int(time_2 - time_1) == 3:
            self.settings.star_is_active = False

    def draw_star(self):

        self.screen.blit(self.image, self.rect)
