import pygame 
from settings import Button

class GameMode():

    def __init__(self, screen, settings):
        # Initialize the main menu page attributes
        self.settings = settings
        self.screen = screen

        # font
        self.title_font = pygame.font.Font('assets/fonts/Akira.otf', 62)
        self.title = self.title_font.render('GAME MODE', True, 'yellow')
        self.title_pos = (self.settings.screen_width//2 - self.title.get_width()//2, 60)

        # buttons 
        self.two_players_button = Button(self.screen, 'Two Players', 200, 200)
        self.ai_bot_button = Button(self.screen, 'AI Bot', 200, 285)
        self.back_button = Button(self.screen, 'Back', 200, 370)



    def handle_events(self, event):
        
        # Handle the events for the main menu page
        if event.type == pygame.MOUSEMOTION:
            if self.two_players_button.rect.collidepoint(event.pos):
                self.two_players_button.is_hover = True
            else:
                self.two_players_button.is_hover = False

            if self.ai_bot_button.rect.collidepoint(event.pos):
                self.ai_bot_button.is_hover = True
            else:
                self.ai_bot_button.is_hover = False

            if self.back_button.rect.collidepoint(event.pos):
                self.back_button.is_hover = True
            else:
                self.back_button.is_hover = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.two_players_button.rect.collidepoint(event.pos):
                return "two_players_game_page"
            if self.ai_bot_button.rect.collidepoint(event.pos):
                return "ai_bot_game_page"
            if self.back_button.rect.collidepoint(event.pos):
                return "main_menu_page"
            
    def draw(self):
        # Draw the main menu page
        self.screen.blit(self.settings.background_img, (0, 0))
        self.screen.blit(self.title, self.title_pos)
        self.back_button.draw()
        self.two_players_button.draw()
        self.ai_bot_button.draw()