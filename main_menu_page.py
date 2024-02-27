import pygame 
from settings import Button

class MainMenu():

    def __init__(self, screen, settings):
        # Initialize the main menu page attributes
        self.settings = settings
        self.screen = screen


        # buttons 
        self.start_button = Button(self.screen, 'START', 200, 300)
        self.how_to_play_button = Button(self.screen, 'How to play', 200, 385)
        self.quit_button = Button(self.screen, 'Quit', 200, 470)


    def handle_events(self, event):
        
        # Handle the events for the main menu page
        if event.type == pygame.MOUSEMOTION:
            if self.start_button.rect.collidepoint(event.pos):
                self.start_button.is_hover = True
            else:
                self.start_button.is_hover = False

            if self.how_to_play_button.rect.collidepoint(event.pos):
                self.how_to_play_button.is_hover = True
            else:
                self.how_to_play_button.is_hover = False

            if self.quit_button.rect.collidepoint(event.pos):
                self.quit_button.is_hover = True
            else:
                self.quit_button.is_hover = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_button.rect.collidepoint(event.pos):
                return "game_mode_page"
            if self.how_to_play_button.rect.collidepoint(event.pos):
                return "how_to_play_page"
            if self.quit_button.rect.collidepoint(event.pos):
                pygame.quit()
                quit()
    
    def draw(self):
        # Draw the main menu page
        self.screen.blit(self.settings.background_img, (0, 0))
        self.screen.blit(self.settings.logo, self.settings.logo_pos)
        self.start_button.draw()
        self.how_to_play_button.draw()
        self.quit_button.draw()