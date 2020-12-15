#!/usr/bin/env python3

"""Projectile Simulator by E1Z0.

The user is asked for a initial velocity and an angle and a pygame window
is then opened to display the projectile's path using the attributes
given to it by the player.
"""

import pygame
import math
import time
import PygameTools

# Constants defined here:
GRAVITY = 10
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PLAYER_SIZE = (100, 100)
DISPLAY_SIZE = (1600, 800)

class Projectile(PygameTools.Sprite):
    """Subclass of PygameTools.Sprite for the player's sprite."""

    def __init__(self, velocity, angle, display):
        """Create the projectile."""
        image = PygameTools.rect_surface(PLAYER_SIZE, WHITE)
        super().__init__(image, (0, display.get_height()), "bottomleft")
        velocity_x = velocity * math.cos(math.radians(angle))
        velocity_y = -(velocity * math.sin(math.radians(angle)))
        self.velocity = [velocity_x, velocity_y]

    def update(self, display):
        """Update the projectile's position and velocity."""
        self.rect.move_ip(self.velocity)
        self.velocity[1] += GRAVITY
        self.blit_to(display)
        if self.rect.bottom >= display.get_height():
            return True

def main():
    """Start the simulation."""
    while True:
        try:
            velocity = float(input("Initial velocity: "))
            if velocity <= 0:
                raise ValueError
        except ValueError:
            print("Please use a number greater than 0.")
        else:
            break

    while True:
        try:
            angle = float(input("Initial angle: "))
            if angle < 5 or angle > 85:
                raise ValueError
        except ValueError:
            print("Please use a number between 5 and 85.")
        else:
            break

    pygame.init()
    display = pygame.display.set_mode(DISPLAY_SIZE)
    projectile = Projectile(velocity, angle, display)

    while True:
        display.fill(BLACK)
        if projectile.update(display):
            break
        pygame.display.flip()
        time.sleep(0.01)

    time.sleep(1)

if __name__ == "__main__":
    main()
