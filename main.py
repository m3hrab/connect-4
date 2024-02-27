import pygame 
from settings import Settings

# game pages
from main_menu_page import MainMenu


def run_game():
    pygame.init()
    settings = Settings()
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    pygame.display.set_caption("Connect-4")
    pygame.display.set_icon(settings.logo)


    # Instances of game pages
    mainmenu_page = MainMenu(screen, settings)


    # Set the current page
    current_page = mainmenu_page

    # Main game loop
    while True:

        # Event loop 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            flag = current_page.handle_events(event)

            if flag == "game_mode_page":
                pass
            elif flag == "mainmenu_page":
                current_page = mainmenu_page


        # Draw the current page elements
        current_page.draw()

        # Update the display
        pygame.display.update()

run_game()

        