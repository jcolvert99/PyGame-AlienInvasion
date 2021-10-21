import sys 

import pygame  #contains the functionality we need to make a game

from settings import Settings
from ship import Ship
from bullet import Bullet

class AlienInvasion:
    '''Overall class to manage game assets and behavior'''

    def __init__(self):
        '''Initialize the game, and create game resources'''
        pygame.init()
        self.settings = Settings() #creating an instance of the class settings
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        #surface- part of the screen where a game element can be displayed
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width,self.settings.screen_height)) 
        pygame.display.set_caption("Alien Invasion")

        #create an instance of the Ship and a group of bullets
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()


        #set the backgroun color. (color is a mix of RGB colors- 3 numbers)
        self.bg_color = (230,230,230)

    def run_game(self):
        '''Start the main loop for the game'''
        while True:
            self._check_events()
            self.ship.update()
            self._update_screen()
            self.bullets.update()
            
              

    def _check_events(self):
        '''Respond to mouse events (called actions)'''
        '''Each keypress is picked up by the pygame.event.get() method'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

                
    
    def _check_keydown_events(self, event):
        '''Respond to keypresses'''
        if event.key == pygame.K_RIGHT:
            #move the ship to the right. - calls the moving.right attribute of the ship class
            self.ship.moving_right = True  #when player presses right arrow - true
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:  #press q to close the game
            sys.exit()
        elif event.key == pygame.K_SPACE:  #fire bullet doesn't need to be in keyup because nothing happens when spacebar released
            self._fire_bullet()

    def _check_keyup_events(self, event):
        '''Respond to key releases'''  
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False  #when player releases right arrow - false
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        '''Create a new bullet and add it to the bullets group.'''
        new_bullet = Bullet(self)   #make an instance of bullet and call it new_bullet
        self.bullets.add(new_bullet)


    def _update_screen(self):
        '''redraw the screen during each pass through the loop'''
        self.screen.fill(self.settings.bg_color)
        #ship appears at top of background
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        #make the most recently drawn screen visible
        pygame.display.flip()


if __name__ == '__main__':
    '''make a game instance, and run the game'''
    ai = AlienInvasion()
    ai.run_game()