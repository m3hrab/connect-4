import pygame 

class Settings():
    """A class to store all settings for Connect -4 ."""
    def __init__(self):

        # Screen settings
        self.screen_width = 800
        self.screen_height = 600
        self.background_img = pygame.image.load('assets/images/bg2.jpg')
        self.logo = pygame.image.load('assets/images/logo.png')
        self.logo_pos = (self.screen_width//2 - self.logo.get_width()//2, 50)

        # Font settings
        self.custom_font1 = pygame.font.Font('assets/fonts/arial.ttf', 32)
        self.custom_font2 = pygame.font.Font('assets/fonts/Stopbuck.ttf', 18)
        self.custom_font3 = pygame.font.Font('assets/fonts/arial.ttf', 24)


        # Game board settings
        self.rows = 6
        self.columns = 7
        self.cell_size = 85
        self.radius = 30
        #(222, 226, 230)


        # game Sound
        self.button_click_sound = pygame.mixer.Sound('assets/sounds/button_click.mp3')
        self.button_click_sound.set_volume(0.5)
        self.piece_drop_sound = pygame.mixer.Sound('assets/sounds/drop_sound.mp3')
        self.piece_drop_sound.set_volume(0.5)
        self.game_over_sound = pygame.mixer.Sound('assets/sounds/game_over.mp3')
        # self.piece_drop_sound = pygame.mixer.Sound('assets/sounds/piece_drop.wav')


class Button():

    def __init__(self, screen, text, x, y,width=400, height=60, font_size=32, color=None):
        self.screen = screen
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.is_hover = False
        self.button_font = pygame.font.Font('assets/fonts/Akira.otf', font_size)

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.text_pos = (self.x + width//2, self.y + self.height//2)

        self.color = color



    def draw(self):

        if self.color is not None:
            pygame.draw.rect(self.screen, (255, 255, 255), self.rect)
            pygame.draw.rect(self.screen, self.color, (self.x+5, self.y+5, self.width - 10 , self.height - 10))
        else:
            pygame.draw.rect(self.screen, (255,255,255), self.rect)
            pygame.draw.rect(self.screen, (255, 0, 0), (self.x+5, self.y+5, self.width - 10 , self.height - 10))

        if self.is_hover:
            text = self.button_font.render(self.text, True, 'white')
        else:
            text = self.button_font.render(self.text, True, 'yellow')
            
        text_rect = text.get_rect(center=self.text_pos)
        self.screen.blit(text, text_rect)