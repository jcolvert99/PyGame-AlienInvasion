import sys 
from time import sleep

import pygame  #contains the functionality we need to make a game

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien

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

        #create an instance to store game statistics and create a scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        #create an instance of the Ship, a group of bullets, and a group of aliens
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        #set the backgroun color. (color is a mix of RGB colors- 3 numbers)
        self.bg_color = (230,230,230)

        #make the play button
        self.play_button = Button(self, "Play")  #creates an instance of button but doesn't draw it to the screen


    def run_game(self):
        '''Start the main loop for the game'''
        while True:
            self._check_events()       #always need to respond to keystrokes even if game isn't active
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()  


    def _check_events(self):
        '''Respond to mouse events (called actions)'''
        '''Each keypress is picked up by the pygame.event.get() method'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)  #send the mouse coordinates to the check_play method (only want to click on button)


    def _check_play_button(self, mouse_pos):
        '''Start a new game when the player clicks Play'''
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:  #if keydown stroke position is on play button, start game
            #reset the game settings
            self.settings.initialize_dynamic_settings()
            
            #reset the game statistics
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()  #preps the scoreboard with a 0 score for a new game
            self.sb.prep_level()
            self.sb.prep_ships()  #shows player how many ships they have to start with

            #get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            #create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            #hide the mouse cursor
            pygame.mouse.set_visible(False)
                
    
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
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)   #make an instance of bullet and call it new_bullet
            self.bullets.add(new_bullet)


    def _update_bullets(self):
        '''update position of bullets and get rid of old bullets'''
        #update bullet positions
        self.bullets.update()
            
        #get rid of bullets that have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        
        self._check_bullet_alien_collisions()


    def _check_bullet_alien_collisions(self):
        '''Remove bullets and alients that have collied'''
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        #^^^sprite.groupcollide function compares the rects of multiple elements and returns a dictionary- key is bullet, 
        # corresponding value is the alien hit. when the rects of a bullet and alien overlap, the two True arguments tell pygame
        # to delete the bullets and the aliens

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)  #if collision dictionary, alien's value is added to the score
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            #detroy existing bullets and create new fleet when all aliens have been destroyed
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            #increase level
            self.stats.level += 1
            self.sb.prep_level()


    def _update_aliens(self):
        '''Update the positions of all aliens in the fleet'''
        #check if the fleet is at an edge, then update the positions of all aliens in the fleet
        self._check_fleet_edges()
        self.aliens.update()
        
        #look for alien_ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):  #takes a sprite and a group and looks for any members that have collieded
            self._ship_hit()

        #look for aliens hitting the bottom of the screen
        self._check_aliens_bottom()
        

    def _create_fleet(self):
        '''Create the fleet of aliens'''
        #create an alien and find the number of aliens in a row
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)  #total screen space divided by alien and non-alien space
        
        #determine the number of rows of aliens that fit on the screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        #^^find vertical space by subtracting alien height from top, ship height from bottom, and two alien heights
        #from bottom of the screen so the player has time to shoot aliens
        number_rows = available_space_y // (2 * alien_height)

        #create the full fleet of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x): #two nested loops, every row then every alien
                self._create_alien(alien_number, row_number)
            

    def _create_alien(self, alien_number, row_number):
        '''Create an alien and place it in a row'''
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        #^^^changing the aliens x-coordinate value- each alien is pushed to the right one alien width from the left margin
        alien.rect.x = alien.x
        alien.rect.y = alien_height + 2 * alien.rect.height * row_number
        #^^^changing the aliens y-coordinate value- each row starts two alien heights below the previous row
        self.aliens.add(alien)


    def _check_fleet_edges(self):
        '''Respond appropriately if any aliens have reached an edge (if check_edges is True)'''
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()  #calls the change direction to move the fleet if it's at the edge
                break


    def _change_fleet_direction(self):
        '''Drop the entire fleet and change the fleet's direction'''
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed  #loop through all aliens and drop each one
        self.settings.fleet_direction *= -1  #multiply current value by -1 to change the direction


    def _ship_hit(self):
        '''Respond to the ship being hit by an alient''' 
        if self.stats.ships_left > 0:
            #decrement ships_left, and update scoreboard
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            #get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            #create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            #pause
            sleep(0.5)
        else:
            self.stats.game_active = False  #ends the game
            pygame.mouse.set_visible(True)  #make the mouse visible again


    def _check_aliens_bottom(self):
        '''Check if any aliens have reaches the bottom of the screen'''
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                #treat this the same as if the ship got his
                self._ship_hit()
                break


    def _update_screen(self):
        '''redraw the screen during each pass through the loop'''
        self.screen.fill(self.settings.bg_color)
        #ship appears at top of background
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen) #draw method- draws each element at the position defined by its rect attribute

        #draw the score information
        self.sb.show_score()

        #draw the play button if the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()  #draw after other elements but before flipping to new screen

        #make the most recently drawn screen visible
        pygame.display.flip()


if __name__ == '__main__':
    '''make a game instance, and run the game'''
    ai = AlienInvasion()
    ai.run_game()