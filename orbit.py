#!/usr/bin/env python3

import math
import time
import pygame

CAPTION = "Orbit"
ICON_SIZE = (1, 1)
DISPLAY_SIZE = (900, 900)
QUIT_KEY = pygame.K_ESCAPE
DELAY = 0
BG_COLOUR = (0, 0, 0)

STAR_RADIUS = 100
STAR_COLOUR = (255, 153, 0)
STAR_CENTRE = (int(DISPLAY_SIZE[0] / 2),
               int(DISPLAY_SIZE[1] / 2))

PLANET_RADIUS = int(STAR_RADIUS / 3)
PLANET_COLOUR = (0, 102, 255)
PLANET_CENTRE = (0, 0)
PLANET_INCR = math.pi / 180
PLANET_DIST = 400

class Sprite:

    def initialise(self, radius, colour, centre):
        self.surface = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA)
        pygame.draw.circle(self.surface, colour, (radius, radius), radius)
        self.rect = self.surface.get_rect()
        self.rect.center = centre

    def blit_to_surface(self, surface):
        surface.blit(self.surface, self.rect)

class Star(Sprite):

    def __init__(self):
        self.initialise(STAR_RADIUS, STAR_COLOUR, STAR_CENTRE)

class Planet(Sprite):

    def __init__(self):
        self.initialise(PLANET_RADIUS, PLANET_COLOUR, PLANET_CENTRE)
        self.angle = 0
        self.increment = PLANET_INCR

    def update(self, display):
        self.rect.center = (STAR_CENTRE[0] + PLANET_DIST * math.cos(self.angle),
                            STAR_CENTRE[1] + PLANET_DIST * math.sin(self.angle))
        self.blit_to_surface(display)
        self.angle += self.increment

def main():
    pygame.init()
    pygame.display.set_caption(CAPTION)
    pygame.display.set_icon(pygame.Surface(ICON_SIZE, pygame.SRCALPHA))
    display = pygame.display.set_mode(DISPLAY_SIZE)
    star = Star()
    planet = Planet()

    while not pygame.key.get_pressed()[QUIT_KEY]:
        star.blit_to_surface(display)
        planet.update(display)
        pygame.display.flip()
        pygame.event.pump()
        time.sleep(DELAY)
        display.fill(BG_COLOUR)

    pygame.quit()

if __name__ == "__main__":
    main()
