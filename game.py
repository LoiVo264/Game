import sys
import pygame
import random
from deck import Deck

SCREEN_SIZE   = 800,600
BRICK_WIDTH= 60
BRICK_HEIGHT=30
       
DECK_WIDTH  = 100
DECK_HEIGHT = 15

BALL_DIAMETER = 10
BALL_RADIUS   = BALL_DIAMETER / 2

MAX_BALL_X   = SCREEN_SIZE[0] - BALL_DIAMETER
MAX_BALL_Y   = SCREEN_SIZE[1] - BALL_DIAMETER

white=(255,255,255)
black=(0,0,0)
#State constants
STATE_BALL_IN_DECK = 0
STATE_PLAYING = 1
STATE_WON = 2
STATE_GAME_OVER = 3
STATE_NEXT_LEVEL = 4
STATE_PAUSE = 5
class Game:
    """ Overall class to manage game assets and behavior."""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption('Break brick')
        #self.bg_color = (0,0,0)
        self.background= pygame.image.load('images/bg1.png')
        self.background_rect=self.background.get_rect()
        
        
        self.clock = pygame.time.Clock()
        if pygame.font:
            self.font = pygame.font.Font(None,30)
        else:
            self.font = None
        # deck
        self.deck = Deck(self)
        
        
        self.lives = 3
        self.level = 1
        self.score = 0
        self.init_game()
        
        
    def init_game(self):
        self.state= STATE_BALL_IN_DECK
        self.ball= pygame.Rect(0,SCREEN_SIZE[1]-DECK_HEIGHT-BALL_DIAMETER,BALL_DIAMETER,BALL_DIAMETER)
        
        if self.level == 1:
            self.ball_vel =[4,-4]
        elif self.level == 2:
            self.ball_vel = [6,-6]
        else:
            self.ball_vel = [9,-9]
        
        self.create_brick()
  
    def create_brick(self):      
        y_ofs = 70
        self.bricks = []
        for i in range(5):
            x_ofs = 70
            for j in range(10):     
                self.bricks.append(pygame.Rect(x_ofs,y_ofs,BRICK_WIDTH,BRICK_HEIGHT)) 
                x_ofs += BRICK_WIDTH +1
            y_ofs += BRICK_HEIGHT +1
               
    def draw_bricks(self):       
        #ListImg=[pygame.image.load("images/yellow.bmp"), pygame.image.load("images/red.bmp"), 
            #pygame.image.load("images/darkred.bmp"), pygame.image.load("images/green.bmp"),
            #pygame.image.load("images/darkgreen.bmp"), pygame.image.load("images/purple.bmp")]
        img= pygame.image.load("images/red.bmp")       
        for brick in self.bricks:   
            #img=random.choice(ListImg)
            self.screen.blit(img,brick)
    def draw_ball(self):             
        pygame.draw.circle(self.screen, white, (int(self.ball.left + BALL_RADIUS)
                            ,int(self.ball.top + BALL_RADIUS)),int(BALL_RADIUS))
   
    def run_game(self):
        """ Main loop for the game."""
        while True:
            self.clock.tick(50)
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
                    self.deck.moving_right= True
                # Move the deck to the left by activating 'direction' flag
                elif event.key == pygame.K_LEFT:
                    self.deck.moving_left =True
                elif event.key==pygame.K_SPACE and self.state == STATE_BALL_IN_DECK:
                    self.ball_vel = self.ball_vel
                    self.state = STATE_PLAYING 
                elif event.key==pygame.K_SPACE and self.state == STATE_NEXT_LEVEL:
                    self.level += 1
                    self.init_game()
                elif event.key==pygame.K_RETURN and (self.state == STATE_GAME_OVER or self.state == STATE_WON):
                    self.init_game()
                    self.lives = 3
                    self.score = 0
                    self.level = 1
            
                    self.ball_vel = [4,-4]   
            # Check key released
            elif event.type == pygame.KEYUP:
                # Stop the deck by activating 'direction' flag
                if event.key == pygame.K_RIGHT:
                    self.deck.moving_right = False
                # Stop the deck by activating 'direction' flag
                elif event.key == pygame.K_LEFT:
                    self.deck.moving_left = False     
                    
                     
        if len(self.bricks)==0:
            self.state= STATE_NEXT_LEVEL
             

    def state_game(self):
        if self.state == STATE_PLAYING:
            self.move_ball()       
            self.handle_collisions()
            
        elif self.state == STATE_BALL_IN_DECK:
            self.ball.left = self.deck.rect.left + self.deck.rect.width / 2
            self.ball.top  = self.deck.rect.top - self.deck.rect.height
            self.show_message("PRESS SPACE TO LAUNCH THE BALL") 
        elif self.state == STATE_GAME_OVER:
            self.show_message("GAME OVER. PRESS ENTER TO PLAY AGAIN")
        elif self.state == STATE_WON:
            self.show_message("YOU WON! PRESS ENTER TO PLAY AGAIN")
        elif self.state == STATE_NEXT_LEVEL:
            self.show_message("YOU WON THIS LEVEL! PRESS TO CONTINUE") 
    def move_ball(self):
        self.ball.left += self.ball_vel[0]
        self.ball.top  += self.ball_vel[1]

        if self.ball.left <= 0:
            self.ball.left = 0
            self.ball_vel[0] = -self.ball_vel[0]
        elif self.ball.left >= MAX_BALL_X:
            self.ball.left = MAX_BALL_X
            self.ball_vel[0] = -self.ball_vel[0]
        
        if self.ball.top < 0:
            self.ball.top = 0
            self.ball_vel[1] = -self.ball_vel[1]
        elif self.ball.top >= MAX_BALL_Y:            
            self.ball.top = MAX_BALL_Y
            self.ball_vel[1] = -self.ball_vel[1]
            
    def handle_collisions(self):
        for brick in self.bricks:
            if self.ball.colliderect(brick):
                if self.level==1:
                    self.score+=3
                    
                if self.level==2:
                    self.score+=5   
                    
                if self.level==3:
                    self.score+=9
                self.ball_vel[1] = -self.ball_vel[1]
                self.bricks.remove(brick)
                break
                
        if self.ball.colliderect(self.deck):
            self.ball.top=SCREEN_SIZE[1]-DECK_HEIGHT-BALL_DIAMETER
            self.ball_vel[1]= -self.ball_vel[1]
            
        elif self.ball.top > self.deck.rect.top:
            self.lives -= 1
            if self.lives > 0:
                self.state = STATE_BALL_IN_DECK
            #The Code below shows when the user could win the game.
            elif self.lives == 0 and self.score >= 1500:
                self.state = STATE_WON
            elif self.lives == 0 and self.score < 1500:
                self.state = STATE_GAME_OVER    
    def show_stats(self):
        if self.font:       
            font_surface = self.font.render("SCORE: " + str(self.score) + " LIVES: " + str(self.lives) + " LEVEL: " + str(self.level), False, white)
            self.screen.blit(font_surface, (205,5))   
            
    def show_message(self,message):
        if self.font:
            size = self.font.size(message)
            font_surface = self.font.render(message,False, white)
            x = (SCREEN_SIZE[0] -size[0]) / 2
            y = (SCREEN_SIZE[1] -size[1]) / 2
            self.screen.blit(font_surface, (x,y))
    def update_game(self):
        # Redraw the screen
        #self.screen.fill(self.bg_color)
       
        self.screen.blit(self.background,self.background_rect)
   
        self.deck.blitme()
        
        self.draw_bricks()   
        
        self.draw_ball()
        self.state_game()
        
        self.show_stats()
        
        # Make the most recently drawn screen visible.
        pygame.display.flip()
    
if __name__ == '__main__':
    # Make a game instance, and run the game.
    game = Game()
    game.run_game()
