import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scoreboard:
    '''A class to report scoring information'''

    def __init__(self, ai_game):
        '''Initialize scorekeeping attributes'''
        self.ai_game = ai_game
        self.screen = ai_game.screen  #ai_game parameter allows it to access the values in settings, screen, and stats objects
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        #font settings for scoring information
        self.text_color = (30,30,30)
        self.font = pygame.font.SysFont(None, 48)  #none is default font

        #prepare the initial score images
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()


    def prep_score(self):
        '''Turn the score into a rendered image'''
        rounded_score = round(self.stats.score, -1)  #negative argument in round function will round to 10
        score_str = "{:,}".format(rounded_score)     #insert commas at 1,000's intervals
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)
        #^^^render creates the image

        #display the score at the top right of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20  #right edge of score_rect is always 20 pixels from the right edge of the screen
        self.score_rect.top = 20


    def show_score(self):
        '''Draw scores, level, and ships to the screen'''
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

    
    def prep_high_score(self):
        '''Turn the high score into a rendered image'''
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)
        #^^^render (generate) an image from the high score method

        #center the high score at the top of the screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    
    def check_high_score(self):  #checks the current game score against the high score
        '''Check to see if there's a new high score'''
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()


    def prep_level(self):
        '''Turn the level into a rendered image'''
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bg_color)

        #position the level below the score
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10  #sets the attribute 10 pixels beneath the bottom of the score image

    
    def prep_ships(self):
        '''Show how many ships are left'''
        self.ships = Group()   #creates an empty group to hold ship instances
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width  #ships appear next to each other with a 10 pixel margin
            ship.rect.y = 10
            self.ships.add(ship)