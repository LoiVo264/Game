import pygame
class Deck:
    """ A class to manage the deck """
    def __init__(self, game):
        """ Initiliazing the deck and set its starting position"""
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()

        # load the deck image and get it rect
        self.image = pygame.image.load('images/deck.bmp')
        self.rect = self.image.get_rect()
        # Set its location at middle bottom of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        # Direction
        self.moving_right = False
        self.moving_left = False

    def blitme(self):
        """ Draw the deck at its current location """
        self.screen.blit(self.image, self.rect)

    def update(self):
        """ Update the deck's position based on direction."""
        if self.moving_right and (self.rect.right<800):
            self.rect.x +=1
        if self.moving_left and (self.rect.x>0):
            self.rect.x -=1
        
