#!/usr/bin/env python3

"""Plot a sine wave in pygame. Made by E1Z0."""

import math
import time
import pygame
import PygameTools

def main():
    """Plot the graph"""
    pygame.init()
    display = pygame.display.set_mode((615, 200))
    blitter = PygameTools.Sprite(
        PygameTools.rect_surface((1, 1), (255, 255, 255))
    )

    for i in range(1, 615):
        blitter.rect.midleft = (
            i,
            int(display.get_height()/2)
            -int(display.get_height()/2 * math.sin(i/100))
        )
        blitter.blit_to(display)
        pygame.display.flip()

    time.sleep(1)

if __name__ == "__main__":
    main()
