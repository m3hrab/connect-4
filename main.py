import pygame 
from settings import Settings

def run_game():
    pygame.init()
    settings = Settings()
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    pygame.display.set_caption("Connect-4")
    pygame.display.set_icon(settings.logo)

    # Main game loop
    while True:

        # Event loop 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Draw the background
        screen.blit(settings.background_img, (0, 0))
        screen.blit(settings.logo, settings.logo_pos)

        # Update the display
        pygame.display.update()

run_game()

        