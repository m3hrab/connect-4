import pygame 
import sys
from settings import Settings

# game pages
from main_menu_page import MainMenu
from how_to_play_page import HowToPlay
from game_mode_page import GameMode

def run_game():
    pygame.init()
    settings = Settings()
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    pygame.display.set_caption("Connect-4")
    pygame.display.set_icon(settings.logo)


    # Instances of game pages
    mainmenu_page = MainMenu(screen, settings)
    how_to_play_page = HowToPlay(screen, settings)
    game_mode_page = GameMode(screen, settings)

    # Set the current page
    current_page = mainmenu_page

    # Main game loop
    while True:

        # Event loop 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            flag = current_page.handle_events(event)

            if flag == "quit":
                sys.exit()
            elif flag == "game_mode_page":
                current_page = game_mode_page
            elif flag == "main_menu_page":
                current_page = mainmenu_page
            elif flag == "how_to_play_page":
                current_page = how_to_play_page



        # Draw the current page elements
        current_page.draw()

        # Update the display
        pygame.display.update()

run_game()

        