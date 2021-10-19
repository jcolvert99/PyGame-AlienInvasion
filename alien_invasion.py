import sys 

import pygame  #contains the functionality we need to make a game

from settings import Settings
from ship import Ship

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

        #create an instance of the Ship
        self.ship = Ship(self)

        #set the backgroun color. (color is a mix of RGB colors- 3 numbers)
        self.bg_color = (230,230,230)

    def run_game(self):
        '''Start the main loop for the game'''
        while True:
            self._check_events()
            self.ship.update()
            self._update_screen()
            
              

    def _check_events(self):
        '''Respond to keypresses and mouse events (called actions'''
        '''Each keypress is picked up by the pygame.event.get() method'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    #move the ship to the right. - calls the moving.right attribute of the ship class
                    self.ship.moving_right = True  #when player presses right arrow - true
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = False  #when player releases right arrow - false
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = False


    def _update_screen(self):
        '''redraw the screen during each pass through the loop'''
        self.screen.fill(self.settings.bg_color)
        #ship appears at top of background
        self.ship.blitme()

        #make the most recently drawn screen visible
        pygame.display.flip()


if __name__ == '__main__':
    '''make a game instance, and run the game'''
    ai = AlienInvasion()
    ai.run_game()