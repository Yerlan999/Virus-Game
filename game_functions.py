from super_gift import Gift
from bullet import Bullet
from pygame import time
from virus import Virus
from time import sleep
from time import time
import pygame
import sys


def get_number_rows(settings, ship_height, virus_height):
    """ """

    availabe_space_y = settings.screen_height - (2 * virus_height) - ship_height
    number_rows = int(availabe_space_y / (2 * virus_height))
    return number_rows


def get_number_viruses_x(settings, virus_width):
    """ """
    available_space = settings.screen_width - 2 * virus_width
    number_viruses_fit = int(available_space / (virus_width * 2))
    return number_viruses_fit


def create_virus(settings, screen, viruses, virus_number, row_number):
    """ """

    virus = Virus(settings, screen)
    virus_width = 100
    virus_height = 50
    virus.x = virus_width + 2 * virus_width * virus_number
    virus.rect.x = virus.x
    virus.rect.y = virus_height + 1.5 * virus_height * row_number
    viruses.add(virus)


def create_fleet(settings, screen, viruses, ship):
    """" Creates the fleet of viruses on the screen """

    virus_width = 100
    virus_height = 70
    number_viruses_x = get_number_viruses_x(settings, virus_width)
    number_rows = get_number_rows(settings, ship.rect.height, virus_height)

    for row_number in range(number_rows):
        for virus_number in range(number_viruses_x):
            create_virus(settings, screen, viruses, virus_number, row_number)


def fire_bullets(settings, screen, ship, bullets, missile):
    """ """

    if len(bullets) < settings.bullets_allowed:
        bullet = Bullet(settings, screen, ship)
        bullets.add(bullet)
        missile.play()
        missile.fadeout(1000)


def check_for_high_score(stats, score_board):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        score_board.prep_high_score()


def start_new_level(viruses, bullets, stats, score_board, settings, screen, ship):
    if len(viruses) == 0:
        bullets.empty()
        stats.level += 1
        score_board.prep_level()
        settings.increase_speed()
        create_fleet(settings, screen, viruses, ship)


# BULLETS WITH VIRUSES COLLISION FUNCTION
def check_bullets_virues_collision(bullets, viruses, settings, screen, ship, stats, score_board, explosion):
    collisions = pygame.sprite.groupcollide(bullets, viruses, True, True)
    if collisions:
        explosion.play()
        explosion.fadeout(600)
        for virus in collisions.values():
            stats.score += settings.virus_hit_score * len(virus)
            score_board.prep_score()
        check_for_high_score(stats, score_board)

    start_new_level(viruses, bullets, stats, score_board, settings, screen, ship)


# BULLETS WITH STAR COLLISION FUNCTION
def check_bullets_star_collision(star_group, bullets, settings, ship, warning):
    if star_group != None:
        hit_star = pygame.sprite.groupcollide(bullets, star_group, True, True)
    else:
        hit_star = {}

    if hit_star != {}:
        global time_star_hitted
        time_star_hitted = time()
        settings.star_is_active = False
        ship.is_superior = True
    time_current = time()

    try:
        if int(time_current - time_star_hitted) == 4:
            warning.play()
            warning.fadeout(2000)
        if int(time_current - time_star_hitted) == ship.superior_mode_duration:
            ship.is_superior = False
    except NameError:
        pass

    try:
        print(time() - time_star_created)
        if (hit_star != None) and (int(time() - time_star_created) == 5):
            star_group.empty()
            settings.star_is_active = False
    except NameError:
        pass


def update_bullets(bullets, viruses, settings, screen, ship, stats, score_board, explosion):
    """ Update the bullet`s position and get rid of old bullets """
    bullets.update()

    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullets_virues_collision(bullets, viruses, settings, screen, ship, stats, score_board, explosion)


def check_keydown_events(event, settings, screen, ship, bullets, stats, play_button, viruses, missile, score_board):
    """ """

    if event.key == pygame.K_q:
        # !!!
        with open("high_score_DB/high_score.txt", "w") as hs:
            hs.write(str(stats.high_score))
        sys.exit()
    elif event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    elif event.key == pygame.K_SPACE:
        fire_bullets(settings, screen, ship, bullets, missile)
    elif event.key == pygame.K_p:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        check_play_button(stats, play_button, mouse_x, mouse_y, screen, settings, ship, viruses, bullets, score_board)


def check_keyup_events(event, ship):
    """ """

    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False


def check_play_button(stats, play_button, mouse_x, mouse_y, screen, ai_settings, ship, viruses, bullets, score_board):
    # Start a new game when a user click the Play button

    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        ai_settings.init_dynamic_settings()
        # Hiding the mouse cursor
        pygame.mouse.set_visible(False)

        # Reseting the gate statistics
        stats.reset_stats()
        stats.game_active = True

        # Reseting all stats
        score_board.prep_high_score()
        score_board.prep_score()
        score_board.prep_level()
        score_board.prep_ships()

        # Emptying the groups
        bullets.empty()
        viruses.empty()

        # Create a new fleet and centering the ship
        create_fleet(ai_settings, screen, viruses, ship)
        ship.center_ship()


def check_events(settings, screen, ship, bullets, stats, play_button, viruses, score_board, missile):
    # Watch for keyboard and mouse events

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # !!!
            with open("high_score_DB/high_score.txt", "w") as hs:
                hs.write(str(stats.high_score))
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, settings, screen, ship, bullets, stats, play_button, viruses, missile,
                                 score_board)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(stats, play_button, mouse_x, mouse_y, screen, settings, ship, viruses, bullets,
                              score_board)


def star_initializer(stats, ai_settings, screen, star_gr):
    if ai_settings.star_is_active == False:
        if stats.score > ai_settings.star_activator_points[0]:
            star = Gift(screen, ai_settings, stats)
            star_gr.add(star)

            global time_star_created
            time_star_created = time()

            ai_settings.star_is_active = True
            del ai_settings.star_activator_points[0]
            return star_gr
        else:
            star_gr = None
            return star_gr
    else:
        return star_gr


def draw_gift_star(ai_settings, bullets, ship, warning, star_group, screen):
    try:
        check_bullets_star_collision(star_group, bullets, ai_settings, ship, warning)
        star_group.update()
        star_group.draw(screen)
    except AttributeError:
        pass


def update_screen(ai_settings, screen, ship, bullets, viruses, play_button, stats, score_board, warning, star_group):
    # Update images on the screen and flip to the new screen

    screen.fill(ai_settings.background_color)  # fill the screen with the given color
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()  # draws a ship on the screen
    viruses.draw(screen)
    draw_gift_star(ai_settings, bullets, ship, warning, star_group, screen)
    # boss.blitme() # draws the boss of the game
    score_board.show_score()
    if not stats.game_active:
        play_button.draw_button()

    pygame.display.flip()  # updates the screen


def change_fleet_direction(settings, viruses):
    """ """

    for virus in viruses.sprites():
        virus.rect.y += settings.fleet_drop_speed
    settings.fleet_direction *= -1


def check_fleet_edges(settings, viruses):
    """ """

    for virus in viruses.sprites():
        if virus.check_edges():
            change_fleet_direction(settings, viruses)
            break


def ship_hit(ai_settings, stats, screen, ship, viruses, bullets, score_board):
    """ Respond to ship being hit by visrus """

    if stats.ships_left > 0:
        # Decrement ships left
        stats.ships_left -= 1
        score_board.prep_ships()

        # Empying the groups of viruses and bullets
        viruses.empty()
        bullets.empty()

        # Creating the new virus fleet and centering the ship
        create_fleet(ai_settings, screen, viruses, ship)
        ship.center_ship()

        # Pause
        sleep(1)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
        ship.center_ship()


def visrues_bottom(screen, viruses, ai_settings, stats, ship, bullets, score_board):
    """ """

    screen_rect = screen.get_rect()
    for virus in viruses:
        if virus.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, screen, ship, viruses, bullets, score_board)
            break


# VIRUSES WITH SHIP COLLISION FUNCTION
def viruses_with_ship_collision(ship, ai_settings, stats, screen, viruses, bullets, score_board, explosion):
    virus_hit_with_ship = pygame.sprite.spritecollideany(ship, viruses)
    if virus_hit_with_ship:
        if ship.is_superior == False:
            ship_hit(ai_settings, stats, screen, ship, viruses, bullets, score_board)
        else:
            explosion.play()
            explosion.fadeout(600)
            stats.score += ai_settings.virus_hit_score
            score_board.prep_score()
            viruses.remove(virus_hit_with_ship)


def update_viruses(settings, viruses, ship, stats, bullets, screen, ai_settings, score_board, explosion):
    """ UPDATES THE VIRUSES` IMAGE """

    check_fleet_edges(settings, viruses)
    viruses.update()
    viruses_with_ship_collision(ship, ai_settings, stats, screen, viruses, bullets, score_board, explosion)
    visrues_bottom(screen, viruses, ai_settings, stats, ship, bullets, score_board)
