import pygame as pg
import sys
from settings import Settings
from ship import Ship

class AlienInvasion:
    def __init__(self):
        pg.init()
        # Initialize game settings
        self.settings = Settings()
        # Set up the game window
        self.screen = pg.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        # Set the window title
        pg.display.set_caption("Alien Invasion")
        # Set up the clock for controlling fps
        self.clock = pg.time.Clock()
        # Black background
        self.bg_color = (self.settings.bg_color) 
        # self -> AlienInvasion instance
        self.ship = Ship(self)

# Main loop for the game
    def run_game(self):
        while True:
            self._check_events()
            self._update_screen()
            self.clock.tick(self.settings.fps)

# Check for events   
    def _check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()

# Update screen elements    
    def _update_screen(self):
        self.screen.fill(self.bg_color)
        self.ship.blitme()
        pg.display.flip()

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()