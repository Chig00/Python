import math
import time
import random
import pygame

CAPTION = "Target Smash"
DISPLAY_SIZE = (400, 400)
QUIT_KEY = pygame.K_ESCAPE
RADIUS = int(DISPLAY_SIZE[0] / 16)
START_COLOUR = (255, 255, 255)
INITIAL_LIFE = 5
LIFE_CONSTANT = 3
END_COLOUR = (255, 0, 0)
SCORE_SIZE = 100
SCORE_COLOUR = (255, 255, 255)
BACKGROUND_COLOUR = (0, 0, 0)

class Target:

    def __init__(self, score):
        self.surface = pygame.Surface((2 * RADIUS, 2 * RADIUS), pygame.SRCALPHA)
        pygame.draw.circle(self.surface, START_COLOUR, (RADIUS, RADIUS), RADIUS)
        self.rect = self.surface.get_rect()
        self.rect.center = (random.randint(RADIUS, DISPLAY_SIZE[0] - RADIUS),
                            random.randint(RADIUS, DISPLAY_SIZE[1] - RADIUS))
        self.life = INITIAL_LIFE * LIFE_CONSTANT / (score + LIFE_CONSTANT)
        self.birth = time.perf_counter()

    def update(self, display):
        age = time.perf_counter() - self.birth
        if age >= self.life:
            return True
        colour = (int((END_COLOUR[0] * age + START_COLOUR[0] * (self.life - age)) / self.life),
                  int((END_COLOUR[1] * age + START_COLOUR[1] * (self.life - age)) / self.life),
                  int((END_COLOUR[2] * age + START_COLOUR[2] * (self.life - age)) / self.life))
        pygame.draw.circle(self.surface, colour, (RADIUS, RADIUS), RADIUS)
        display.blit(self.surface, self.rect)

    def hit(self):
        x = self.rect.centerx - pygame.mouse.get_pos()[0]
        y = self.rect.centery - pygame.mouse.get_pos()[1]
        distance = (x ** 2 + y ** 2) ** 0.5
        return distance < RADIUS

def display_score(score, display):
    display.fill(BACKGROUND_COLOUR)
    surface = pygame.font.Font(None, SCORE_SIZE).render("Score: " + str(score), True, SCORE_COLOUR)
    rect = surface.get_rect()
    rect.center = (int(DISPLAY_SIZE[0] / 2),
                   int(DISPLAY_SIZE[1] / 2))
    display.blit(surface, rect)
    pygame.display.flip()
    while not pygame.key.get_pressed()[QUIT_KEY]:
        pygame.event.pump()

def main():
    pygame.init()
    pygame.display.set_caption(CAPTION)
    pygame.display.set_icon(pygame.Surface((1, 1), pygame.SRCALPHA))
    display = pygame.display.set_mode(DISPLAY_SIZE)
    score = 0
    target = None
    click = False
    while not pygame.key.get_pressed()[QUIT_KEY]:
        if target == None:
            target = Target(score)
        if target.update(display):
            break
        if pygame.mouse.get_pressed()[0]:
            if not click:
                if target.hit():
                    target = None
                    score += 1
                    display.fill(BACKGROUND_COLOUR)
                else:
                    break
            click = True
        else:
            click = False
        pygame.display.flip()
        pygame.event.pump()
    display_score(score, display)
    pygame.quit()

if __name__ == "__main__":
    main()
