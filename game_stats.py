class GameStats():
    """ FOR TRACKING THE GAME STATISTIC """

    def __init__(self, ai_settings):
        """ Initialize the statistics """

        self.ai_settings = ai_settings
        self.high_score = 0
        self.reset_stats()

        self.game_active = False

    def reset_stats(self):
        """ Changable during the game """

        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 0
