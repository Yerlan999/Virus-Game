import pygame.font


class Button():
    """ """

    def __init__(self, screen, ai_settings, message):
        # Initializing the button attributes
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Setting dimensions and properties of the button
        self.width, self.height = 200, 50
        self.button_color = (10, 150, 40)
        self.text_color = (20, 20, 20)
        self.font = pygame.font.SysFont(None, 48, italic=True)

        # Building the buttons rect object and centering it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # The button message needs to be prep only once
        self.prep_message(message)

    def prep_message(self, message):
        # Turn message into image and render/center  it on the button
        self.message_image = self.font.render(message, True, self.text_color, self.button_color)
        self.message_image_rect = self.message_image.get_rect()
        self.message_image_rect.center = self.rect.center

    def draw_button(self):
        # Draws the blank button and then draws image on ot
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.message_image, self.message_image_rect)
