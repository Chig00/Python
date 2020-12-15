#!/usr/bin/env python3

"""4 function plotter by E1Z0."""

import pygame
import math
import time
import PygameTools

from math import (
    sin, cos, tan, asin, acos, atan,
    sinh, cosh, tanh, asinh, acosh, atanh,
    exp, log, ceil, floor, e, pi,
    inf, nan, expm1, log1p
)

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DISPLAY_SIZE = (800, 800)

def main():
    """Get input and plot the functions."""
    # Up to 4 functions displayed at once.
    functions = []
    while len(functions) < 4:
        function = input("f(x) = ")
        if not function:
            break
        functions.append(function)

    pygame.init()
    display = pygame.display.set_mode(DISPLAY_SIZE)

    # The origin is at the centre of the graph.
    origin = (
        int(display.get_width()/2),
        int(display.get_height()/2)
    )

    # 4 sprite objects are used to plot the 4 graphs
    plotters = (
        PygameTools.Sprite(PygameTools.rect_surface((1, 1), WHITE)),
        PygameTools.Sprite(PygameTools.rect_surface((1, 1), RED)),
        PygameTools.Sprite(PygameTools.rect_surface((1, 1), GREEN)),
        PygameTools.Sprite(PygameTools.rect_surface((1, 1), BLUE))
    )

    # for i in range() form used for reference to both tuples.
    for i in range(len(functions)):
        # Functions are evaluated, so they should NOT contain
        # dangerous bytecode.
        try:
            f = lambda x: eval(functions[i])
        except:
            # Functions that don't work will produce a line of f(x) = 0.
            f = lambda x: 0
        # Calculation in the range 10 <= x < 10
        # with 0.02 increments (1000 numbers to calculate).
        for x in range(-1000, 1000, 2):
            try:
                plotters[i].rect.midleft = (
                    # x is divided by 2 to fit onscreen,
                    # but x values < -8 and > 8 are still missed.
                    origin[0] + int(x/2),
                    # Graph shape is fixed.
                    origin[1] - int(50*f(x/100))
                )
            except (TypeError, ValueError, ZeroDivisionError):
                pass
            # Each plot is blitted to the display every time a value
            # of x has f(x) applied.
            plotters[i].blit_to(display)

    # Update the display at the end
    pygame.display.flip()
    # Display the graphs until escape is pressed.
    while not pygame.key.get_pressed()[pygame.K_ESCAPE]:
        pygame.event.pump()
    pygame.quit()

if __name__ == "__main__":
    main()
