#!/usr/bin/env python3

"""Plotter by E1Z0

This plotter is different from the first as the upper limit
on the number of plots is changed from 4 to 215 (6**3 - 1).

The new mechanism is based on the creation of a function object
that has a list of all of the colours use for the plots as
a class variable. Therefore, an original colour can always be
gotten.

The colours are of form rbg with rgb taking a value that is a
multiple of 51 (the only only colour barred is (0, 0, 0)).

As in the original plotter, the user enters in up to 215 functions
to plot on the graph. However, this version of the plotter also
includes a grid from (-10, -10) to (10, 10) (bigger than the old
plotter that went from (-8, -8) to (8, 8). The gridlines are also
displayed.
"""

import pygame
import time
import random
import PygameTools
from math import (
    e, exp, log, expm1, log1p,
    pi, sin, cos, tan, asin, acos, atan,
    sinh, cosh, tanh, asinh, acosh, atanh,
)

DISPLAY_SIZE = (500, 500)
WEAK_WHITE = (255, 255, 255, 51)
BLACK = (0, 0, 0)

class FunctionOfX:
    """Class for the functions to be plotted.

    A function will be of x and any other symbols
    must have been predefined (like e or pi).

    Each function will have a plotter that is a uniquely
    coloured sprite (from PygameTools.Sprite).

    The unique colours are maintained by having a class
    variable (a list) that will update as colours are taken.

    There are 215 different colours available (6**3 - 1) for
    a plotter, so there are 215 different functions of x that
    can be plotted simultaneously.
    """

    # The used colours list starts with only one - black.
    # This is to prevent a black plot, because one wouldn't
    # show up on the black background.
    used_colours = [BLACK]

    def __init__(self, function):
        """Create the function object with an original plotter."""
        # f(x) is set
        try:
            self.f = lambda x: eval(function)
        except:
            print("Function was not understood.")
            self.f = lambda x: 0

        while True:
            colour = (
                random.randint(0, 5) * 51,
                random.randint(0, 5) * 51,
                random.randint(0, 5) * 51
            )

            if self.colour_check(colour):
                self.plotter = PygameTools.Sprite(
                    PygameTools.rect_surface((1, 1), colour)
                )
                break

    def plot(self, surface):
        """Plots the function to the surface."""
        for x in range(
            int(-surface.get_width()/2),
            int(surface.get_width()/2)
        ):
            # If the point can't be plotted, it is skipped.
            try:
                self.plotter.rect.topleft = (
                    # The plots are determined by the origin
                    # The origin is in the middle (half width and height).
                    int(surface.get_width()/2 + x),
                    # Division by 25 to set x between -10 and 10.
                    # Multiplication by 25 to get the graph back to
                    # the correct size.
                    int(surface.get_height()/2 - 25*self.f(x/25))
                )
            # 'Wildcard except' for exceptions of any kind.
            except:
                pass
            else:
                self.plotter.blit_to(surface)
                # Assumption that the surface is the display.
                # Makes a nice visual of the graph being drawn.
                pygame.display.flip()

    @classmethod
    def colour_check(cls, colour):
        """Return True and save the colour if the colour is original."""
        if colour not in cls.used_colours:
            cls.used_colours.append(colour)
            print("Colour:", colour)
            return True

def ln(x):
    """Return the natural logarithm of x.

    This function is identical to math.log() except
    that it only accepts a single argument (hence the
    separate definition instead of equation).
    """
    return log(x)

def draw_gridlines(surface, vert_line, hori_line):
    """Draw 38 gridlines onto the surface.

    The gridlines are drawn from -9 to 9 on both axis
    in white and the spacing is determined by the surface's size.
    Therefore, the surface size can be changed without any
    compatability worries.
    """
    # The sizes of the spaces between lines are calculated.
    space = (
        int(surface.get_width()/20),
        int(surface.get_height()/20)
    )

    for i in range(1, 20):
        # Two lines are drawn for each iteration.
        surface.blit(vert_line, (i*space[0], 0))
        surface.blit(hori_line, (0, i*space[1]))

        # Creates a nice visual with blitting one by one
        # (actually two by two).
        time.sleep(0.01)
        pygame.display.flip()

def main():
    """Start plotting."""
    functions = []

    while len(functions) < 215:
        function = input("f(x) = ")
        if not function:
            break
        functions.append(FunctionOfX(function))

    pygame.init()
    display = pygame.display.set_mode(DISPLAY_SIZE)

    # Transluscent line images are created for the gridlines.
    vert_line = pygame.Surface((1, display.get_height()), pygame.SRCALPHA)
    vert_line.fill(WEAK_WHITE)
    hori_line = pygame.Surface((display.get_width(), 1), pygame.SRCALPHA)
    hori_line.fill(WEAK_WHITE)

    # Gridlines from -10 to 10 are drawn onto the display.
    draw_gridlines(display, vert_line, hori_line)

    for f in functions:
        f.plot(display)

    # The plot ceases to display when the escape key is pressed.
    while not pygame.key.get_pressed()[pygame.K_ESCAPE]:
        pygame.event.pump()
    pygame.quit()

if __name__ == "__main__":
    main()
