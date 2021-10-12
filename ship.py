import pygame #pygame lets you treat all game elements like rectanges (rects)

class Ship:
    '''A class to manage the ship.'''

    def __init__(self, ai_game):
        '''Initialize the ship and set its starting position'''
        self.screen = ai_game.screen   #ai_game references the current instance of AI class
        self.screen_rect = ai_game.screen.get_rect()

        #Load the ship image and get its rect.
        self.image = pygame.image.load('images/ship.bmg')
        self.rect = self.image.get_rect()
        #Start each new ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        #in pygame, origin (0,0) is at the top left of the screen
        
    def blitme(self):
        '''Draw the ship at its current location.'''
        self.screen.blit(self.image, self.rect)