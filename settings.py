import pygame 

class Settings():
    """A class to store all settings for Connect -4 ."""
    def __init__(self):

        # Screen settings
        self.screen_width = 800
        self.screen_height = 600
        self.background_img = pygame.image.load('assets/images/bg2.jpg')
        self.logo = pygame.image.load('assets/images/logo.png')
        self.logo_pos = (self.screen_width//2 - self.logo.get_width()//2, self.screen_height//2 - self.logo.get_height()//2)