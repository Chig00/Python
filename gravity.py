#!/usr/bin/env python3

"""Gravity by Chigozie Agomo.

The aim of the game is to avoid touching the approaching missiles
and to avoid the edge of the screen by reversing gravity.

Gravity is reversed with the gravity switch key (spacebar).
Game is reset with the end key (escape).
Game is quit with the quit key and end key (q and escape).

Each missile dodged increases the score by 1 and increases the
game difficulty (the frequency of missile launches increases).
"""

import math
import time
import random
import pygame

# Game constants
# Universal constants
DISPLAY_SIZE = (500, 500)
ICON_SIZE = (32, 32) # Blank icon
CAPTION = "Gravity"
DELAY = 0.01 # Inbuilt lag to slow down the game
END_KEY = pygame.K_ESCAPE # Starts a new game
QUIT_KEY = pygame.K_q # Quits the game when pressed with the end key

# RGBA colour value constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLANK = (0, 0, 0, 0)

# Player constants
PLAYER_SIZE = (25, 25)
PLAYER_SPAWN = (250, 50) # The player's spawn position (player.rect.center)
PLAYER_MAX_SPEED = 7
GRAVITY = 1 # Acceleration that the player experiences from gravity
GRAVITY_SWITCH = pygame.K_SPACE # Key to change gravity

# Missile constants
MISSILE_SIZE = (90, 10)
MISSILE_BASE_SPEED = 1 # Missiles' starting speed
MISSILE_MAX_SPEED = 5
MISSILE_THRUST = 0.07 # Missiles' acceleration
COOLDOWN_BASE = 1 # Starting missile launch delay
COOLDOWN_DECAY = 0.1 # Missile launch delay formula constant

# Score constants
SCORE_POSITION = (500, 500)
SCORE_RECT_POINT = "bottomright" # Position is for the bottom right of the sprite
SCORE_SIZE = 25 # Score text font size

class Sprite:
    """Class for the sprites.

    All sprites have image and rect attributes that are used for
    blitting to surfaces easily.
    """

    def __init__(self, image, position=(0,0), rect_point="topleft"):
        """Initialise a sprite."""
        self.image = image
        self.rect = image.get_rect()
        self.reposition(position, rect_point)

    def reposition(self, position=(0,0), rect_point="topleft"):
        """Move the sprite to a new position (rect's point)."""
        exec("self.rect." + rect_point + " = " + str(position))

    def move(self, movement):
        """Move the sprite in place."""
        self.rect.move_ip(movement)

    def blit(self, surface):
        """Blit the sprite's image to a surface."""
        surface.blit(self.image, self.rect)

class Player(Sprite):
    """Class for the player's sprite."""

    def __init__(self):
        """Create the player."""
        image = rect_surface(PLAYER_SIZE, WHITE)
        super().__init__(image, PLAYER_SPAWN, "center")
        self.velocity = [0, 0]
        self.gravity = GRAVITY # Gravity accelerates downwards initially
        self.press = False # Prevents multiple key presses for a single press

    def update(self, missiles, display):
        """Update the player's status.

        Gravity is reversed if the gravity switch key was released.
        The player is accelerated according to gravity.
        If the player's velocity is too great the player is slowed down.
        The player is moved according to the velocity they have.
        The player's sprite is blitted to the display.
        If the player has collided with a missile, they return a True value.
        If the player has touched a boundary, they return a True value.
        """
        if pygame.key.get_pressed()[GRAVITY_SWITCH]:
            self.press = True
        elif self.press:
            self.gravity = -self.gravity
            self.press = False

        self.velocity[1] += self.gravity
        self.velocity_fix()
        self.move(self.velocity)
        self.blit(display)

        for missile in missiles:
            if missile.rect.colliderect(self.rect):
                return True

        return self.bound_check()

    def velocity_fix(self):
        """Ensure that the player is at or below terminal velocity."""
        if self.velocity[1] > PLAYER_MAX_SPEED:
            self.velocity[1] = PLAYER_MAX_SPEED
        elif self.velocity[1] < -PLAYER_MAX_SPEED:
            self.velocity[1] = -PLAYER_MAX_SPEED

    def bound_check(self):
        """Check if the player has touched the boundaries."""
        if self.rect.top <= 0:
            return True
        elif self.rect.bottom >= DISPLAY_SIZE[1]:
            return True

class Missile(Sprite):
    """Class for the sprites of the missiles that the player must avoid."""

    def __init__(self):
        """Initialise a missile."""
        image = rect_surface(MISSILE_SIZE, RED)
        position, rect_point = self.position_missile()
        super().__init__(image, position, rect_point)
        self.velocity = [self.velocity_calc(), 0]
        self.thrust = self.thrust_calc()

    def position_missile(self):
        """Assign a random position for the missile."""
        side = random.randint(0, 1)
        height = random.randint(0, DISPLAY_SIZE[1] - MISSILE_SIZE[1])
        position = (DISPLAY_SIZE[0] * side, height)
        if position[0]:
            rect_point = "topleft"
        else:
            rect_point = "topright"

        return position, rect_point

    def velocity_calc(self):
        """Caculcate the signing of the missile's initial velocity."""
        return math.copysign(MISSILE_BASE_SPEED, -self.rect.left)

    def thrust_calc(self):
        """Calculate the signing of the missile's acceleration."""
        return math.copysign(MISSILE_THRUST, -self.rect.left)

    def update(self, display):
        """Update the missile.

        The missile is accelerated.
        The missile's velocity is kept at or below maximum speed.
        The missile is moved.
        The missile's sprite is blitted onto the display.
        The missile returns True if it is offscreen.
        """
        self.velocity[0] += self.thrust
        self.velocity_fix()
        self.move(self.velocity)
        self.blit(display)
        return self.offscreen()

    def offscreen(self):
        """Return True if the missile is offscreen."""
        return (self.rect.right <= 0 or self.rect.left >= DISPLAY_SIZE[1])

    def velocity_fix(self):
        """Keep the missile below maximum speed."""
        if self.velocity[1] > MISSILE_MAX_SPEED:
            self.velocity[1] = MISSILE_MAX_SPEED
        elif self.velocity[1] < -MISSILE_MAX_SPEED:
            self.velocity[1] = -MISSILE_MAX_SPEED

class ScoreCounter(Sprite):
    """Class for the one-time use score counter."""

    def __init__(self, score, display):
        """Initialise the score couter and blit it to the display."""
        font = pygame.font.Font(None, SCORE_SIZE)
        image = font.render(str(score), True, WHITE)
        super().__init__(image, SCORE_POSITION, SCORE_RECT_POINT)
        self.blit(display)

def rect_surface(size, colour):
    """Return a rectangular surface."""
    surface = pygame.Surface(size, pygame.SRCALPHA)
    surface.fill(colour)

    return surface

def cooldown_calc(score):
    """Calculate the new missile launch cooldown."""
    return COOLDOWN_BASE / (score * COOLDOWN_DECAY + 1) # y = a/(bx + 1)

def main():
    pygame.init()

    while True:
        # The icon is removed and the caption is set
        pygame.display.set_icon(rect_surface(ICON_SIZE, BLANK))
        pygame.display.set_caption(CAPTION)
        display = pygame.display.set_mode(DISPLAY_SIZE)

        # Objects used for the game are initialised
        player = Player()
        score = 0
        end = False
        missiles = [] # No missiles are created initially
        time_base = time.perf_counter() # The last missile launch

        while not end and not pygame.key.get_pressed()[END_KEY]:
            display.fill(BLACK) # Display is cleared every game loop
            current_time = time.perf_counter() # Used to reduce discrepancy between two perf_counter() calls
            # If there has been enough time, a new missile will be launched
            if current_time >= time_base + cooldown_calc(score):
                missiles.append(Missile())
                time_base = current_time

            for missile in missiles:
                # If the update returns True, the missile is offscreen and the player gets a point
                if missile.update(display):
                    score += 1
                    missiles.remove(missile) # Offscreen missiles are destroyed
            end = player.update(missiles, display) # A True return will end the game
            ScoreCounter(score, display) # Each object is only initialised, but never re-referenced

            pygame.display.flip() # Display is updated
            pygame.event.pump() # Key input is synchornised with events
            time.sleep(DELAY) # Game is lagged to ease gameplay

        while not pygame.key.get_pressed()[END_KEY]:
            pygame.event.pump() # Synchronisation required for input

        if pygame.key.get_pressed()[QUIT_KEY]: # If the quit key is also pressed, the game ends
            break

    pygame.quit() # Closes the window if this module is imported

if __name__ == "__main__":
    main()
