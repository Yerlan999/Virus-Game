from pygame.sprite import Sprite
import pygame


class Ship(Sprite):
    """ CLASS FOR STORING SHIP PARAMETRES """

    def __init__(self, screen, ai_settings):
        super().__init__()
        """ Initialize the ship and sets its starting position """

        self.screen = screen
        self.ai_settings = ai_settings

        # Load the ship image nad gets its rect(frame)
        self.image = pygame.image.load("game_images/starship.bmp")
        self.s_image = pygame.image.load("game_images/superior_starship.bmp")
        self.rect = self.image.get_rect()
        self.screen_rect = self.screen.get_rect()  # different

        # Starts each new  ship at the bottom centre of the screen

        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        #
        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)

        # Moving right Flag
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

        # Superior Ship Flag
        self.is_superior = False
        self.superior_mode_duration = 5

    def update(self):
        """ Updates the user`s ship """

        # NOTE! Ship`s center is being updated here, NOT rect centre
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.x -= self.ai_settings.ship_speed_factor

        if self.moving_up and self.rect.top > self.screen_rect.top:
            self.y -= self.ai_settings.ship_speed_factor
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.ai_settings.ship_speed_factor

        # Update the ship`s rect center by using ships`s center coordinates
        self.rect.centerx = self.x
        self.rect.centery = self.y

    def blitme(self):
        """ Draws the starship on its current location """

        if self.is_superior:
            self.screen.blit(self.s_image, self.rect)
        else:
            self.screen.blit(self.image, self.rect)

    def center_ship(self):

        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        self.x = 650
        self.y = 615


class Boss(Sprite):
    """ CLASS FOR INITIALIZING BOSS CHARACTER """

    def __init__(self, screen):
        super().__init__()
        """ Initializes the boss and sets for starting position """

        self.screen = screen
        self.image = pygame.image.load("game_images/alien.bmp")
        self.rect = self.image.get_rect()
        self.screen_rect = self.screen.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery

    def update(self):
        """ Updates the boss`s character """
        pass

    def blitme(self):
        """ Draws the boss on the screen """

        self.screen.blit(self.image, self.rect)
