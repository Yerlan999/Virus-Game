from pygame.sprite import Group
from ship import Boss
import pygame.font


class ScoreBoard():
    """ SCORE CLASS FOR DISPLAYING THE SCORE OF THE PLAYER """

    def __init__(self, settings, screen, stats):
        # Initializing the main attributes
        self.settigns = settings
        self.screen = screen
        self.stats = stats

        # Getting the screen rect object
        self.screen_rect = screen.get_rect()

        # Font settings for scoring information
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # Preparing the initial score image
        self.prep_all_scores()

        try:
            with open("high_score_DB/high_score.txt", "r") as hs:
                self.stats.high_score = int(hs.read())
        except FileNotFoundError:
            print("File Not Found!")
            self.stats.high_score = 0

    def prep_all_scores(self):

        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_ships(self):
        self.bosses = Group()

        for number_boss in range(self.stats.ships_left):
            boss = Boss(self.screen)
            boss.rect.x = 50 * number_boss
            boss.rect.y = 15
            self.bosses.add(boss)

    def prep_score(self):
        # Turns the score into the rendered image

        rounded_score = int(round(self.stats.score, -1))
        score_str = f"{rounded_score:,}"
        self.image = self.font.render(score_str, True, self.text_color, self.settigns.background_color)
        self.image_rect = self.image.get_rect()

        # Displaying/placing the score image on the screen
        self.image_rect.right = self.screen_rect.right - 20
        self.image_rect.top = 20

    def prep_high_score(self):

        high_score = "{:,}".format(int(round(self.stats.high_score, -1)))
        self.high_score_image = self.font.render(high_score, True, self.text_color, self.settigns.background_color)

        #
        self.high_score_image_rect = self.high_score_image.get_rect()
        self.high_score_image_rect.top = 20
        self.high_score_image_rect.centerx = self.screen_rect.centerx

    def prep_level(self):
        self.level_image = self.font.render(str(self.stats.level), True, self.text_color,
                                            self.settigns.background_color)
        self.level_image_rect = self.level_image.get_rect()

        # Displaying/placing the score image on the screen
        self.level_image_rect.right = self.screen_rect.right - 20
        self.level_image_rect.top = 60

    def show_score(self):
        # Showing the screen on the screen
        self.screen.blit(self.image, self.image_rect)
        self.screen.blit(self.high_score_image, self.high_score_image_rect)
        self.screen.blit(self.level_image, self.level_image_rect)

        self.bosses.draw(self.screen)
