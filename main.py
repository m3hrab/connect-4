import pygame 
import sys
from settings import Settings

# game pages
from main_menu_page import MainMenu
from how_to_play_page import HowToPlay
from game_mode_page import GameMode
from two_player_game import TwoPlayerGame
from game_over_page import GameOver
from ai_bot import AIBotGame

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
    two_player_game_page = TwoPlayerGame(screen, settings)
    game_over_page = GameOver(screen, settings)
    ai_bot_game_page = AIBotGame(screen, settings)

    # Set the current page
    current_page = mainmenu_page

    # temp
    previous_page = None    
    
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
            elif flag == "two_players_game_page":
                current_page = two_player_game_page
                previous_page ='two_players_game_page'
            elif flag == "ai_bot_game_page":
                current_page = ai_bot_game_page
                previous_page = 'ai_bot_game_page'
            elif flag == "game_over_page":
                if previous_page == 'two_players_game_page':
                    game_over_page.winner = two_player_game_page.winner # Update the winner 
                elif previous_page == 'ai_bot_game_page':
                    game_over_page.winner = ai_bot_game_page.winner # Update the winner
                current_page = game_over_page



        # Draw the current page elements
        current_page.draw()

        # Update the display
        pygame.display.update()

run_game()

        