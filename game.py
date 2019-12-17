import sys
import pygame
from deck import Deck
class Game:
    """ Overall class to manage game assets and behavior."""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('Break brick')
        self.bg_color = (0,0,0)
        # ship
        self.deck = Deck(self)

    def run_game(self):
        """ Main loop for the game."""
        while True:
            self.check_event()
            # Change the ship's position by calling its 'update' method
            self.deck.update()
            self.update_game()

    def check_event(self):
        """ Watch for keyboard and mouse event."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # Check key pressed
            elif event.type == pygame.KEYDOWN:
                # Move the ship to the right by activating 'direction' flag
                if event.key == pygame.K_RIGHT:
                    self.deck.moving_right = True
                # Move the ship to the left by activating 'direction' flag
                elif event.key == pygame.K_LEFT:
                    self.deck.moving_left = True
            # Check key released
            elif event.type == pygame.KEYUP:
                # Stop the ship by activating 'direction' flag
                if event.key == pygame.K_RIGHT:
                    self.deck.moving_right = False
                # Stop the ship by activating 'direction' flag
                elif event.key == pygame.K_LEFT:
                    self.deck.moving_left = False
                   

    def update_game(self):
        # Redraw the screen
        self.screen.fill(self.bg_color)
        # Draw the ship
        self.deck.blitme()
        # Make the most recently drawn screen visible.
        pygame.display.flip()
    
if __name__ == '__main__':
    # Make a game instance, and run the game.
    game = Game()
    game.run_game()
