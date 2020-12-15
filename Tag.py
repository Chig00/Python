#!/usr/bin/env python3

"""Tag by E1Z0"""

import pygame, time, random

class Player:
    """Class for the players' common attributes."""
    
    def __init__(self):
        """Create the player's image and rect."""
        
        self.image = pygame.Surface((100, 100))
        self.image.fill(pygame.Color(self.colour))
        self.rect = self.image.get_rect()
        self.velocity = [0, 0]
        self.hold = False
        self.score = 0
    
            
    def update(self, other_player, display):
        """Move the player according to the current situation."""
        
        self.velocity[0] = 40 * (pygame.key.get_pressed()[self.right]
                                 - pygame.key.get_pressed()[self.left])
            
        self.rect.move_ip(self.velocity)
        
        if self.rect.left < 0:
            self.rect.left = 0
            
        elif self.rect.right > display.get_width():
            self.rect.right = display.get_width()
            
        if self.rect.top < 0:
            self.rect.top = 0
            
        elif self.rect.bottom > display.get_height():
            self.rect.bottom = display.get_height()
            
        if self.rect.bottom < display.get_height():
            self.velocity[1] += 2
            if pygame.key.get_pressed()[self.down]:
                self.velocity[1] = 100
            
        elif self.rect.bottom == display.get_height():
            self.velocity[1] = 0
            
            if pygame.key.get_pressed()[self.up] and not self.hold:
                self.velocity[1] = -55
                
        if pygame.key.get_pressed()[self.up]:
            self.hold = True
            
        else:
            self.hold = False
            
        display.blit(self.image, self.rect)
        display.blit(other_player.image, other_player.rect)
        
class ScoreText:
    """Class for the game's score display."""
    
    def __init__(self):
        """Initialise the instance."""
        
        self.font = pygame.font.Font(None, 100)
        
    def update(self, player_one, player_two, display):
        """Update the text to display the scores."""
        
        self.image_one = self.font.render(str(int(player_one.score)),
                                          True,
                                          pygame.Color("Red"))
                         
        self.rect_one = self.image_one.get_rect()
        self.rect_one.center = (int(display.get_width() * 2 / 3), 100)
        
        self.image_two = self.font.render(str(int(player_two.score)),
                                          True,
                                          pygame.Color("Blue"))
                         
        self.rect_two = self.image_two.get_rect()
        self.rect_two.center = (int(display.get_width() / 3), 100)
        
        display.blit(self.image_one, self.rect_one)
        display.blit(self.image_two, self.rect_two)
        
class PlayerOne(Player):
    """Player subclass for player one's control scheme."""
    
    up = pygame.K_UP
    down = pygame.K_DOWN
    left = pygame.K_LEFT
    right = pygame.K_RIGHT
    colour = "Red"
    
class PlayerTwo(Player):
    """Player subclass for player two's control scheme."""
    
    up = pygame.K_w
    down = pygame.K_s
    left = pygame.K_a
    right = pygame.K_d
    colour = "Blue"

def main():
    """Start the game."""
    
    pygame.init()
    display = pygame.display.set_mode((1760, 880))
    player_one = PlayerOne()
    player_two = PlayerTwo()
    score_text = ScoreText()
    winner = random.randint(1, 2)
    if winner == 1:
        colour = (50, 50, 255)
    else:
        colour = (255, 50, 50)
    touch = False
    
    while not pygame.key.get_pressed()[pygame.K_ESCAPE]:
        display.fill(colour)
        
        score_text.update(player_one, player_two, display)
        
        player_one.update(player_two, display)
        player_two.update(player_one, display)
        
        if player_one.rect.colliderect(player_two.rect):
            if not touch:
                if winner == 1:
                    winner = 2
                    colour = (50, 50, 255)
                
                else:
                    winner = 1
                    colour = (255, 50, 50)
                    
                touch = True
                
        else:
            touch = False
        
        if winner == 1:
            player_one.score += 0.1
            
        else:
            player_two.score += 0.1
            
        pygame.display.flip()
        pygame.event.pump()
        
        time.sleep(0.01)
    
if __name__ == "__main__":
    main()