import sys
import pygame
from deck import Deck
import time
import random
class Game:
    """ Overall class to manage game assets and behavior."""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('Break brick')
        self.bg_color = (0,0,0)
                
        # deck
        self.deck = Deck(self)
        # brick
        self.create_brick()
        
        
    def create_brick(self):
        
        BRICK_WIDTH= 60
        BRICK_HEIGHT=30
        y_ofs = 70
        self.bricks = []
        for i in range(6):
            x_ofs = 70
            for j in range(10):      
                self.bricks.append(pygame.Rect(x_ofs,y_ofs,BRICK_WIDTH,BRICK_HEIGHT)) 
                x_ofs += BRICK_WIDTH + 3
            y_ofs += BRICK_HEIGHT + 3  
               
            
    def draw_bricks(self):
        img= pygame.image.load("images/yellow.bmp")
        for brick in self.bricks:
            self.screen.blit(img,brick)           
  
    def run_game(self):
        """ Main loop for the game."""
        while True:
            self.check_event()
            # Change the deck's position by calling its 'update' method
            
            self.deck.update()
            
            self.update_game()

    def check_event(self):
        """ Watch for keyboard and mouse event."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # Check key pressed
            elif event.type == pygame.KEYDOWN:
                # Move the deck to the right by activating 'direction' flag
                if event.key == pygame.K_RIGHT:
                    self.deck.moving_right = True
                # Move the deck to the left by activating 'direction' flag
                elif event.key == pygame.K_LEFT:
                    self.deck.moving_left = True
            # Check key released
            elif event.type == pygame.KEYUP:
                # Stop the deck by activating 'direction' flag
                if event.key == pygame.K_RIGHT:
                    self.deck.moving_right = False
                # Stop the deck by activating 'direction' flag
                elif event.key == pygame.K_LEFT:
                    self.deck.moving_left = False
                   

    def update_game(self):
        # Redraw the screen
        self.screen.fill(self.bg_color)
        self.draw_bricks()
        # Draw the deck
        self.deck.blitme()
        
        # Make the most recently drawn screen visible.
        pygame.display.flip()



        
if __name__ == '__main__':
    # Make a game instance, and run the game.
    game = Game()
    game.run_game()
