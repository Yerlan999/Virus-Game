from scoreboard import ScoreBoard
from game_stats import GameStats
from pygame.sprite import Group
from pygame.mixer import Sound
from settings import Settings
import game_functions as gf
from button import Button
from ship import Ship
import pygame.mixer
import pygame


def run_game():
    """ Initializes the game objects and starts the game screen """

    pygame.mixer.init()
    missile = Sound("sounds/missile.wav")
    explosion = Sound("sounds/explosion.wav")
    warning = Sound("sounds/warning.wav")
    pygame.init()  # starts the game or initializes
    ai_settings = Settings()  # sets up an object with settings of the game
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")  # defines the title name of the game
    ship = Ship(screen, ai_settings)  # creates the object 'ship' passing an arg 'screen'
    bullets = Group()
    viruses = Group()
    star_gr = Group()
    stats = GameStats(ai_settings)
    score_board = ScoreBoard(ai_settings, screen, stats)
    gf.create_fleet(ai_settings, screen, viruses, ship)

    play_button = Button(screen, ai_settings, "Play!")
    clock = pygame.time.Clock()

    # Stanrting the main loop for the game
    while True:

        # checks if any events happening in the game
        gf.check_events(ai_settings, screen, ship, bullets, stats, play_button, viruses, score_board, missile)
        star_group = gf.star_initializer(stats, ai_settings, screen, star_gr)
        gf.update_screen(ai_settings, screen, ship, bullets, viruses, play_button, stats, score_board, warning,
                         star_group)

        if stats.game_active:
            ship.update()
            gf.update_bullets(bullets, viruses, ai_settings, screen, ship, stats, score_board, explosion)
            gf.update_viruses(ai_settings, viruses, ship, stats, bullets, screen, ai_settings, score_board, explosion)
            # Update images on the screen and flip to the new screen
            # gf.update_screen(ai_settings, screen, ship, bullets, viruses, play_button, stats)


run_game()
