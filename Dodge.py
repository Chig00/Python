#!/usr/bin/env python3

"""
Dodge - 'One-tap' dodger.

This a 'one-tap' game where the player controls a ball and must avoid the walls
approaching by pressing the space bar.

Each wall successfully dodged gives the player a point.

Over time, the game will become harder by increasing the speed of the walls.

"""

import pygame
from pygame.locals import *
from time import perf_counter as counter, sleep
from random import randint

#Constants set.
screen_width = 200
screen_height = 600
screen_size = (screen_width, screen_height)
black = (0, 0, 0)
white = (255, 255, 255)

class FakeSprite:
    """
    Class for image, rectangle pairs, which would act like sprites.

    These objects will have their source image with the desired transformation,
    the rectangle for hitboxes and the like, and methods for movement.

    """

    def __init__(self, image_name, position = (0, 0),
                 size = None, rotation = None):
        """
        Make a fake sprite using the inputted arguments.

        The only required argument is the image file's file name/directory.

        The position of the fake sprite (which is determined by the top-left
        corner) defaults to (0, 0), which is the top-left corner of the display
        surface.

        The size is an optional argument, that will make the image (and thus
        the rectangle) equal in size to the argument. Using no size argument
        will cause the size to be equal to the picture's actual size.

        Rotation is like size - it's optional and not inputting it will use the
        image file's natural rotation. Rotation will cause the image to be
        rotated by the argument's value (in degrees).

        """

        self.image = pygame.image.load(image_name)
        
        if size:
            self.image = pygame.transform.scale(self.image, size)
            
        if rotation:
            self.image = pygame.transform.rotate(self.image, rotation)
            
        self.rectangle = self.image.get_rect()
        self.rectangle.topleft = position

    def reposition(self, position):
        """
        Move the fake sprite to the position given.

        The position must be a tuple or list of the co-ordinates of the new
        position for the fake sprite.

        """

        self.rectangle.topleft = position

    def move(self, movement):
        """
        Move the fake sprite by the amount given (movement argument).

        The movement must be a tuple or list and the fake sprite will be moved
        in place.

        """

        self.rectangle.move_ip(movement)

    def blit_on(self, surface):
        """
        Blit the fake sprite's image onto the surface given.

        Note that this blit_on() method is different from other blit methods,
        as the image of this fake sprite is being blitted onto a surface,
        rather than having an surface being blitted onto the image.

        """

        surface.blit(self.image, self.rectangle)

def new_wall():
    """
    Create and return a new wall obstacle for the game.

    The wall is placed in one of the two wall spawns at the top of the screen.

    The wall's spawning spot is determined randomly and the wall is retuned as
    a fake sprite object.

    """

    if randint(0, 1):
        wall = FakeSprite("White Rectangle.jpg",
                          position = (0, 0),
                          size = (int(screen_width * 0.45),
                                  int(screen_height / 30)))
    else:
        wall = FakeSprite("White Rectangle.jpg",
                          position = (int(screen_width * 0.55), 0),
                          size = (int(screen_width * 0.45),
                                  int(screen_height / 30)))

    return wall

def game_over(screen, score):
    """End the game and display the player's score."""

    #A game over image is used.
    game_over = FakeSprite("Game Over.jpg",
                           position = (0, int(screen_height / 6)),
                           size = (screen_width, int(screen_height / 3)))

    #The text for the score display is created.
    score_text = pygame.font.Font(None, 60).render("Score: " + str(score),
                                                   True, white)

    #The screen is erased and "GAME OVER" and the score are displayed.
    screen.fill(black)
    game_over.blit_on(screen)
    screen.blit(score_text, (0 , int(screen_height * 2/3)))
    pygame.display.flip()

def main():
    """Start Dodge."""

    pygame.init()

    #Display created with the screen size constants set priorly.
    screen = pygame.display.set_mode(screen_size)

    #The line that separates the lanes is set using the size of the screen.
    lane_line = FakeSprite("White Rectangle.jpg",
                           position = (int(screen_width * 0.45), 0),
                           size = (screen_height, int(screen_width / 10)),
                           rotation = 90)

    player_ball = FakeSprite("White Ball.jpg",
                             position = (int(screen_width * 0.025),
                                         int(screen_height * 13/15)),
                             size = (int(screen_width * 0.4),
                                     int(screen_height * 2/15)))

    first_wall = FakeSprite("White Rectangle.jpg",
                            position = (0, 0),
                            size = (int(screen_width * 0.45),
                                    int(screen_height / 30)))

    lane_line.blit_on(screen)
    player_ball.blit_on(screen)
    first_wall.blit_on(screen)
    pygame.display.flip()
    
    walls = [first_wall]
    wall_speed = [0, 5]
    wall_space = player_ball.rectangle.height * 5
    base_time = counter()
    press = False
    over = False
    score = 0

    #Main Game Loop
    while True:
        #If a wall makes contact with the ball, the player loses.
        for wall in walls:
            if wall.rectangle.colliderect(player_ball.rectangle):
                game_over(screen, score)
                over = True

        #If the game is over, the game no longer loops.
        if over:
            sleep(3)
            break

        #The game gets progressively harder.
        if counter() - base_time >= 1:
            base_time = counter()
            wall_speed[1] += 1

        #When the previous wall has gone far enough, the next wall comes down.
        if walls[-1].rectangle.top >= wall_space:
            walls.append(new_wall())
            
        #Every time a rectangle comes offscreen, it is no longer animated
        #to keep process speeds high. The player also gets a point.
        for wall in walls:
            if wall.rectangle.top >= screen_height:
                del walls[walls.index(wall)]
                score += 1

        #All the walls currently onscreen move down with their curent speed.
        for wall in walls:
            wall.move(wall_speed)

        #The player's ball is moved to the other side
        #if the space bar is pressed.
        if pygame.key.get_pressed()[K_SPACE]:
            press = True

        elif not pygame.key.get_pressed()[K_SPACE] and press:
            press = False
            if player_ball.rectangle.left == 5:
                player_ball.rectangle.left = 115
            elif player_ball.rectangle.left == 115:
                player_ball.rectangle.left = 5

        #Image update phase.
        #The screen is filled black to erase the previous frame.
        screen.fill(black)

        #All of the (fake) sprites are blitted back onto the display.
        lane_line.blit_on(screen)
        player_ball.blit_on(screen)

        for wall in walls:
            wall.blit_on(screen)

        #The display is updated.
        pygame.display.flip()

        #The pump() function is called to keep input working.
        pygame.event.pump()

        sleep(0.01)

    #3 seconds after game over, pygame quits.
    pygame.quit()

if __name__ == "__main__":
    main()
