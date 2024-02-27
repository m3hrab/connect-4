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


class Button():

    def __init__(self, screen, text, x, y, color=(255, 255, 255), hover_color=(255, 0, 0)):
        self.screen = screen
        self.text = text
        self.x = x
        self.y = y
        self.is_hover = False
        self.button_font = pygame.font.Font('assets/fonts/Akira.otf', 32)

        self.rect = pygame.Rect(self.x, self.y, 400, 60)
        
        self.text_pos = (self.x + 200, self.y + 30)

    def draw(self):
        pygame.draw.rect(self.screen, (255,255,255), self.rect)
        pygame.draw.rect(self.screen, (255, 0, 0), (self.x+5, self.y+5, 390, 50))

        if self.is_hover:
            text = self.button_font.render(self.text, True, (228, 208, 10))
        else:
            text = self.button_font.render(self.text, True, 'yellow')
            
        text_rect = text.get_rect(center=self.text_pos)
        self.screen.blit(text, text_rect)