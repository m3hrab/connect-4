import pygame 
from settings import Button

class HowToPlay():

    def __init__(self, screen, settings):
        # Initialize the main menu page attributes
        self.settings = settings
        self.screen = screen


        # buttons 
        self.back_button = Button(self.screen, 'Back', 20, 20, 100, 60, 20)


    def handle_events(self, event):
        
        # Handle the events for the main menu page
        if event.type == pygame.MOUSEMOTION:
            if self.back_button.rect.collidepoint(event.pos):
                self.back_button.is_hover = True
            else:
                self.back_button.is_hover = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_button.rect.collidepoint(event.pos):
                return "main_menu_page"
            
    def draw(self):
        # Draw the main menu page
        self.screen.blit(self.settings.background_img, (0, 0))
        self.back_button.draw()