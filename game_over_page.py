import pygame 
from settings import Button

class GameOver():

    def __init__(self, screen, settings):
        # Initialize the main menu page attributes
        self.settings = settings
        self.screen = screen

        self.winner = None
        # font
        self.font = pygame.font.Font('assets/fonts/Akira.otf', 62)

        # buttons 
        self.back_button = Button(self.screen, 'Main Menu', 200, 370)



    def handle_events(self, event):
        
        # Handle the events for the main menu page
        if event.type == pygame.MOUSEMOTION:
            if self.back_button.rect.collidepoint(event.pos):
                self.back_button.is_hover = True
            else:
                self.back_button.is_hover = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_button.rect.collidepoint(event.pos):
                self.settings.button_click_sound.play()
                return "main_menu_page"
            
    def draw(self):
        # Draw the main menu page
        self.screen.blit(self.settings.background_img, (0, 0))
        
        if self.winner is not None:
            text = self.font.render(f'{self.winner} WON!', True, 'yellow')
        else:
            text = self.font.render('Draw', True, 'yellow')

        text_rect = text.get_rect(center=(self.settings.screen_width//2, self.settings.screen_height//2))
        self.screen.blit(text, text_rect)
        self.back_button.draw()