import sys 

import pygame  #contains the functionality we need to make a game

from settings import Settings

class AlienInvasion:
    '''Overall class to manage game assets and behavior'''

    def __init__(self):
        '''Initialize the game, and create game resources'''
        pygame.init()
        self.settings = Settings() #creating an instance of the class settings

        #surface- part of the screen where a game element can be displayed
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width,self.settings.screen_height)) 
        pygame.display.set_caption("Alien Invasion")

        #set the backgroun color. (color is a mix of RGB colors- 3 numbers)
        self.bg_color = (230,230,230)

    def run_game(self):
        '''Start the main loop for the game'''
        while True:
            #watch for keyboard and mouse events. (called actions)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit

            #redraw the screen during each pass through the loop
            self.screen.fill(self.settings.bg_color)

            #make the most recently drawn screen visible
            pygame.display.flip()

if __name__ == '__main__':
    '''make a game instance, and run the game'''
    ai = AlienInvasion()
    ai.run_game()