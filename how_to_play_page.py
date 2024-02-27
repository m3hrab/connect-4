import pygame 
from settings import Button

class HowToPlay():

    def __init__(self, screen, settings):
        # Initialize the main menu page attributes
        self.settings = settings
        self.screen = screen

        # buttons 
        self.back_button = Button(self.screen, 'Back', 40, 53, 100, 40, 16)

        # Define Fonts
        self.heading_font = pygame.font.Font('assets/fonts/Akira.otf', 48)
        self.title_font = pygame.font.Font('assets/fonts/Akira.otf', 32)
        self.text_font = pygame.font.Font('assets/fonts/arial.ttf', 24)

        # How to play text
        self.htp_text1 = """
        Two player mode allows two players to compete each other
        to get 4 discs in a row. The players each take turns to place
        their coloured disc in one of the rows and the first player to
        get 4 of them in a row vertically, horizontally or diagonally
        will win scoring themselves one point.
        """

        self.htp_text2 = """
        AI Bot mode allows one player to play against a
        computerised player also known as a bot. The rules of the
        game are exactly the same as the two-player mode where
        the first player to get 4 of their coloured discs in a row
        vertically, horizontally or diagonally will win scoring
        themselves one point.
        """

        self.heading = self.heading_font.render('HOW TO PLAY', True, 'yellow')
        self.title1 = self.title_font.render('Two Player', True, 'white')
        self.title2 = self.title_font.render('AI Bot', True, 'white')

    def draw_htp_textes(self):
        """Draw the how to play textes with center alignment."""

        # text background 
        pygame.draw.rect(self.screen, 'black', (40, 130, 720, 440))

        self.screen.blit(self.title1, (60, 150))
        for i, line in enumerate(self.htp_text1.split('\n')):
            text = self.text_font.render(line, True, (255,255,255))
            self.screen.blit(text, (10, 170 + i*25))

        self.screen.blit(self.title2, (60, 350))
        for i, line in enumerate(self.htp_text2.split('\n')):
            text = self.text_font.render(line, True, (255,255,255))
            self.screen.blit(text, (10, 370 + i*25))


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

        self.screen.blit(self.heading, (200, 50))
        self.draw_htp_textes()

