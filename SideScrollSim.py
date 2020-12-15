#!/usr/bin/env python3

"""Pygame Side-Scroller Physics Simulator"""

import pygame, time

class Player:
    """Class for the player's attributes."""
    
    velocity = [0, 0]
    hold = False
    
    def __init__(self):
        """Initialise the player object."""
        
        self.image = pygame.Surface((100, 100))
        self.image.fill(pygame.Color("White"))
        self.rect = self.image.get_rect()
        
    def update(self, display):
        """Check the current situation and update the player to match."""
        
        self.velocity[0] = 10 * (pygame.key.get_pressed()[pygame.K_RIGHT]
                                 - pygame.key.get_pressed()[pygame.K_LEFT])
                
        if not pygame.key.get_pressed()[pygame.K_UP]:
            self.hold = False
                         
        if self.rect.bottom == 400:
            self.velocity[1] = 0
            if pygame.key.get_pressed()[pygame.K_UP] and not self.hold:
                self.velocity[1] = -25
                self.hold = True
                
        elif self.rect.bottom < 400:
            self.velocity[1] += 1
        
        else:
            self.rect.bottom = 400
            
        self.rect.move_ip(self.velocity)
            
        if self.rect.top < 0:
            self.rect.top = 0
            
        if self.rect.left < 0:
            self.rect.left = 0
            
        elif self.rect.right > 400:
            self.rect.right = 400
        
        display.fill(pygame.Color("Black"))
        display.blit(self.image, self.rect)
        pygame.display.flip()
        pygame.event.pump()

def main():
    """Start the simulation."""
    
    pygame.init()
    display = pygame.display.set_mode((400, 400))
    player = Player()
    
    while not pygame.key.get_pressed()[pygame.K_ESCAPE]:
        player.update(display)
        time.sleep(0.02)
    
if __name__ == "__main__":
    main()