"""Useful classes and functions for pygame by E1Z0.

The Sprite class is a class for image-rect pairs to be
blitted to a surface. The function of sprites in this module
is identical to pygame's sprites, but these aer much more simple
and intuitive to use.

The TextSprite class is a subclass of Sprite for text based
image sprites.

The CircleSprite class is a subclass of Sprite that supports
calculation for circular hitboxes.

The rect_surface() function returns a surface that is
completely filled in a with a chosen colour. This is
useful for minimalistic representation.

The circle_surface() function returns a coloured circle
on a surface with alpha 0.

The lighten_colour() function returns a lightened version
of the colour given as an argument.

The darken_colour() function returns a darkened version
of the colour given as an argument.
"""

import pygame

class Sprite:
    """Class for image-rect pairs to be blitted to a surface.

    A sprite will have an image attribute, which is the surface
    that is blitted to another surface.

    The sprite has a rect attribute that is used to blit the
    image in the correct position. Subclasses can also use
    the rect attribute for hitboxes and the like.

    Upon creation, the sprite will have an image, rect,
    and will be in a certain position given in the __init__()
    method.

    The blit_to() method is used to blit the sprite's image
    to the surface given in the arguments in the position
    determined by the rect.
    """

    def __init__(self, image, pos=(0,0), point="topleft"):
        """Create a sprite object.

        The sprite's image, and position are determined by the
        arguments, and the rect will be determined by those
        arguments.
        """
        self.image = image
        self.rect = image.get_rect()
        exec("self.rect." + point + " = " + str(pos))

    def blit_to(self, surface):
        """Blit the sprite's image to the surface.

        The location is determined by the sprite's rect attribute.
        """
        surface.blit(self.image, self.rect)

class TextSprite(Sprite):
    """Subclass of Sprite for sprites with text-based images.

    As this class relies on pygame's font module, objects cannot
    be created from this class unless the font module is initialised
    with either pygame.init() or pygame.font.init().
    """

    def __init__(self, font_size, text, colour,
                 pos=(0,0), point = "topleft"):
        """Create the font sprite as defined by the arguments."""
        image = pygame.font.Font(None, font_size).render(
            text, True, colour
        )
        super().__init__(image, pos, point)

class CircleSprite(Sprite):
    """Subclass of Sprite for sprites with circular hitboxes.

    This class has methods to help with calculating hit registration
    with circles by using the circle's radius and Pythagoras' Theorem
    to calculate.
    """

    def point_collision(self, point):
        """Return true if the point is in the circle."""
        distance_x = self.rect.centerx - point[0]
        distance_y = self.rect.centery - point[1]
        distance = (distance_x**2 + distance_y**2)**0.5
        if distance <= self.rect.width/2:
            return True

    def circle_collision(self, other):
        """Return true if the two circles overlap."""
        distance_x = self.rect.centerx - other.rect.centerx
        distance_y = self.rect.centery - other.rect.centery
        distance = (distance_x**2 + distance_y**2)**0.5
        if distance <= self.rect.width/2 + other.rect.width/2:
            return True

def rect_surface(size, colour):
    """Return a rectangular surface.

    The size and colour of the surface are determined by the arguments.
    """
    surface = pygame.Surface(size)
    surface.fill(colour)
    return surface

def circle_surface(radius, colour):
    """Return a circular surface (alpha=0 for background).

    The radius of the circle and the colour are determined by
    the arguments given.
    """
    surface = pygame.Surface((2*radius, 2*radius), pygame.SRCALPHA)
    pygame.draw.circle(surface, colour, (radius, radius), radius)
    return surface

def lighten_colour(colour):
    """Return a lighter colour than the one given.

    The colour will be 64 units lighter in r, g, and b,
    that is to say that a colour (r, g, b) will become
    (r+64, g+64, b+64).

    A colour that has r, g, or b exceed 255 will make
    it r, g, or b equal 255.

    Alpha values are ignored.
    """
    if type(colour) != tuple or type(colour) != list:
        raise TypeError("Tuple or List only.")

    elif len(colour) > 4 or len(colour) < 3:
        raise TypeError("Colours must be of format rgb or rbga.")

    for c in colour:
        if type(c) != int:
            raise TypeError("All colour values must be integers.")
        elif c < 0:
            raise ValueError("All colour values must be positive.")
        elif c > 255:
            raise ValueError("All colour values must not exceed 255.")

    new_colour = []
    for c in colour:
        if len(new_colour) == 3:
            break
        elif c + 64 > 255:
            new_colour.append(255)
        else:
            new_colour.append(c + 64)

    return tuple(new_colour)

def darken_colour(colour):
    """Return a darker colour than the one given.

    The colour will be 64 units darker than the one given.
    If a colour (r, g, b) is given, (r-64, g-64, b-64)
    is returned.

    Alpha values are ignored and values less than 0 will
    instead eqaul 0.
    """
    if type(colour) != tuple or type(colour) != list:
        raise TypeError("Use a list or a tuple.")

    elif len(colour) < 3 or len(colour) > 4:
        raise TypeError("Use rgb or rgba.")

    for c in colour:
        if type(c) != int:
            raise TypeError("Use colours with interger values.")
        elif c < 0:
            raise TypeError("Colours may not be negative.")
        elif c > 255:
            raise TypeError("Colours may not exceed 255.")

    new_colour = []
    for c in colour:
        if len(new_colour) == 3:
            break
        elif c - 64 < 0:
            new_colour.append(0)
        else:
            new_colour.append(c - 64)

    return tuple(new_colour)
