#!/usr/bin/env python3

"""Gun Tag by E1Z0

Gun Tag is like the game tag, but the chasing player
uses bullets to tag the runner player.

The runner player will get a point
for every half second they stay running.

Then winner is the player who gets 100 points first.

A tag will cause the players to switch roles,
which gives the other player an
opportunity to get points.
"""

import time
import random
import pygame

pygame.init()

class Sprite:
    """Class for sprites to be blitted to a surface."""

    def __init__(self, image):
        """Create the sprite."""
        self.image = image
        self.rect = image.get_rect()

    def blit_to(self, surface):
        """Blit the sprite to a surface."""
        surface.blit(self.image, self.rect)

class Player(Sprite):
    """Sprite subclass for the players."""

    size = (100, 100)
    run_speed = 30
    jump_power = -52
    dive_power = 100
    gravity = 2

    def __init__(self, display):
        """Create the player."""
        image = pygame.Surface(self.size)
        image.fill(self.colour)
        super().__init__(image)
        self.rect.topleft = (
            self.start_pos
            * display.get_width(),
            0
        )
        self.velocity = [0, 0]
        self.score = 0
        self.base_time = 0
        self.bullet = None
        self.direction = -2*self.start_pos + 1
        self.jump_hold = False
        self.dive_hold = False
        self.shoot_hold = False

    def update(self, other_player, display):
        """Update the player.

        The update will move the player according
        to what keys are being pressed.

        The update will create a bullet object if
        the player pressed their shoot button and
        the player is the chaser.

        The player will switch roles with the
        other player if the player has shot the
        other player.

        The player will blit their sprite to the
        display.
        """
        # Movement calculated and executed
        self.velocity[0] = self.run_speed * (
            pygame.key.get_pressed()[self.keys["right"]]
            - pygame.key.get_pressed()[self.keys["left"]]
        )

        if self.velocity[0]:
            self.direction = int(self.velocity[0] / self.run_speed)

        if self.rect.bottom == display.get_height():
            if pygame.key.get_pressed()[self.keys["up"]]:
                if not self.jump_hold:
                    self.jump_hold = True
                    self.velocity[1] = self.jump_power

            else:
               self.jump_hold = False

            self.dive_hold = False

        elif self.rect.bottom < display.get_height():
            if pygame.key.get_pressed()[self.keys["down"]]:
                if not self.dive_hold:
                    self.velocity[1] += self.dive_power
            self.velocity[1] += self.gravity

        self.rect.move_ip(self.velocity)

        # Move the player onscreen if offscreen
        if self.rect.top < 0:
            self.rect.top = 0

        elif self.rect.bottom > display.get_height():
            self.rect.bottom = display.get_height()

        if self.rect.left < 0:
            self.rect.left = 0

        elif self.rect.right > display.get_width():
            self.rect.right = display.get_width()

        # Create a bullet object if the player is the chaser
        # and has pressed the shoot button
        if self.state == "chaser":
            if pygame.key.get_pressed()[self.keys["shoot"]]:
                if not self.bullet:
                    if not self.shoot_hold:
                        self.bullet = Bullet(self)
                        self.shoot_hold = True
            else:
                self.shoot_hold = False

        if self.bullet:
            if self.bullet.update(other_player, display):
                self.base_time = time.perf_counter()
                switch_states(self, other_player)
                self.bullet = None
            # If the bullet goes offscreen, it is deleted
            elif (
                self.bullet.rect.right < 0
                or self.bullet.rect.left > display.get_width()
            ):
                self.bullet = None

        # A new score sprite object is made to display the player's score
        ScoreSprite(self, display)

        # The player's sprite is blitted to the display
        self.blit_to(display)

class PlayerOne(Player):
    """Player subclass for player one."""

    start_pos = 1
    colour = (255, 0, 0)
    keys = {
        "up": pygame.K_UP,
        "left": pygame.K_LEFT,
        "down": pygame.K_DOWN,
        "right": pygame.K_RIGHT,
        "shoot": pygame.K_RETURN,
    }

class PlayerTwo(Player):
    """Player subclass for player two."""

    start_pos = 0
    colour = (0, 0, 255)
    keys = {
        "up": pygame.K_w,
        "left": pygame.K_a,
        "down": pygame.K_s,
        "right": pygame.K_d,
        "shoot": pygame.K_SPACE,
    }

class Bullet(Sprite):
    """Sprite subclass for the player's bullet."""

    size = (
        int(Player.size[0] / 5),
        int(Player.size[1] / 5)
    )
    speed = 2 * Player.run_speed

    def __init__(self, chaser):
        """Create the bullet."""
        image = pygame.Surface(self.size)
        image.fill(chaser.colour)
        super().__init__(image)
        self.velocity = (
            int(chaser.direction * self.speed),
            0
        )
        self.rect.center = chaser.rect.center

    def update(self, other_player, display):
        """Update the bullet.

        The update involves moveing the bullet, blitting it to the
        display, and checking if the bullet has hit the opponent.
        """
        self.rect.move_ip(self.velocity)
        self.blit_to(display)
        if self.rect.colliderect(other_player.rect):
            return True

class ScoreSprite(Sprite):
    """Sprite subclass for the player's score display."""

    font = pygame.font.Font(None, 100)

    def __init__(self, owner, display):
        """Create the score sprite and blit it to the display."""
        if owner.colour == (255, 0, 0):
            position = 2
        else:
            position = 1

        image = self.font.render(
            str(owner.score),
            True,
            owner.colour
        )
        super().__init__(image)

        self.rect.center = (
            int(position * display.get_width() / 3),
            150
        )

        self.blit_to(display)

class WinnerSprite(Sprite):
    """Sprite subclass to show the winner."""

    font = pygame.font.Font(None, 200)

    def __init__(self, winner, display):
        """Create the winner text."""

        image = self.font.render(
            "WINNER!",
            True,
            winner.colour
        )
        super().__init__(image)

        self.rect.center = (
            int(display.get_width() / 2),
            300
        )

        self.blit_to(display)

def switch_states(player_one, player_two):
    """Switch the players' states."""
    temp = player_one.state
    player_one.state = player_two.state
    player_two.state = temp

def lighten_colour(colour):
    """Lighten a colour by 64.

    A colour of (r, g, b) will be lightened
    to a colour of (r+64, g+64, b+64).

    Colour values above 255 are returned to 255.
    """
    new_colour = []
    for c in list(colour):
        c += 64
        if c > 255:
            c = 255
        new_colour.append(c)

    return tuple(new_colour)

def main():
    """Start the game."""
    display = pygame.display.set_mode((1600, 800))
    players = (
        PlayerOne(display),
        PlayerTwo(display)
    )

    # The starting states of the players is determined by chance
    if random.randint(0, 1):
        players[0].state = "runner"
        players[1].state = "chaser"

    else:
        players[0].state = "chaser"
        players[1].state = "runner"

    end = False
    winner = None

    while not end:
        # The runner player determines the background and will
        # get a point for every half second they stay running
        for player in players:
            if player.state == "runner":
                display.fill(
                    lighten_colour(player.colour)
                )
                if time.perf_counter() >= player.base_time + 0.5:
                    player.base_time = time.perf_counter()
                    player.score += 1

        # The escape key can end the game at any time
        # and will produce no winner
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            break

        # The players are updated along with their attribute
        # objects every game loop
        for player in players:
            other_player = players[1 - players.index(player)]
            player.update(other_player, display)
            if player.score >= 100:
                winner = player
                end = True
                break

        # Display is updated and events are synced once per loop
        pygame.display.flip()
        pygame.event.pump()
        time.sleep(0.005)

    for player in players:
        if player == winner:
            display.fill(lighten_colour(player.colour))
            WinnerSprite(player, display)
            player.rect.center = (
                int(display.get_width() / 2),
                display.get_height() - int(player.size[1] / 2)
            )
            player.blit_to(display)

    pygame.display.flip()

    while not pygame.key.get_pressed()[pygame.K_ESCAPE]:
        pygame.event.pump()

if __name__ == "__main__":
    main()
