class Settings():
    """ A CLASS TO STORE ALL SETTINGS FOR ALIEN INVASION """

    def __init__(self):
        """ Initalizes the game settings """

        self.screen_width = 1300
        self.screen_height = 650
        self.background_color = (230, 250, 120)

        # Bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # Virus settings
        self.fleet_drop_speed = 25

        self.ship_limit = 3

        # How fast game levels up
        self.level_speedup_scale = 1.02

        # How quickly virus hit points goes up as level increases
        self.score_scale = 1.5

        self.init_dynamic_settings()

        self.star_is_active = False
        self.star_activator_points = [1000, 5000, 10000, 30000, 50000, 100000,
                                      200000, 500000, 1000000, 5000000]

    def init_dynamic_settings(self):
        # Changing settings during the game
        self.ship_speed_factor = 1.5
        self.bullet_speed = 2
        self.virus_speed_factor = 0.3

        # Scoring settings
        self.virus_hit_score = 10

        # '1' stands for rightward movement and  '-1' for leftward
        self.fleet_direction = 1

    def increase_speed(self):
        # Leveling up the key attributes behavior
        self.ship_speed_factor *= self.level_speedup_scale
        self.bullet_speed *= self.level_speedup_scale
        self.virus_speed_factor *= self.level_speedup_scale

        self.virus_hit_score = int(self.virus_hit_score * self.score_scale)
