import math
import time
import random
import pygame

DISP_WIDTH = 400
DISP_HEIGHT = 400

class Button:

    def __init__(self, buttons):
        width = int(DISP_WIDTH / 8)
        height = int(DISP_HEIGHT / 8)
        size = (width, height)
        self.surface = pygame.Surface(size)
        self.rect = self.surface.get_rect()
        x = int(DISP_WIDTH / 2) + 150 * int(math.cos(len(buttons) * math.pi / 2))
        y = int(DISP_WIDTH / 2) + 150 * int(math.sin(len(buttons) * math.pi / 2))
        self.rect.center = (x, y)

    def light(self, display, colour=(255, 255, 255)):
        self.surface.fill(colour)
        display.blit(self.surface, self.rect)
        pygame.display.update(self.rect)

    def delight(self, display):
        self.surface.fill((0, 0, 0))
        display.blit(self.surface, self.rect)
        pygame.display.update(self.rect)

def display_pattern(pattern, buttons, display):
    for i in pattern:
        buttons[i].light(display, (127, 127, 127))
        time.sleep(0.5)
        buttons[i].delight(display)
        time.sleep(0.1)

def accept_pattern(pattern, buttons, display):
    player_pattern = []
    while len(player_pattern) < len(pattern):
        while any(pygame.key.get_pressed()):
            pygame.event.pump()
        while True:
            if pygame.key.get_pressed()[pygame.K_UP]:
                player_pattern.append(3)
                buttons[3].light(display)
                time.sleep(0.1)
                buttons[3].delight(display)
                break
            elif pygame.key.get_pressed()[pygame.K_LEFT]:
                player_pattern.append(2)
                buttons[2].light(display)
                time.sleep(0.1)
                buttons[2].delight(display)
                break
            elif pygame.key.get_pressed()[pygame.K_DOWN]:
                player_pattern.append(1)
                buttons[1].light(display)
                time.sleep(0.1)
                buttons[1].delight(display)
                break
            elif pygame.key.get_pressed()[pygame.K_RIGHT]:
                player_pattern.append(0)
                buttons[0].light(display)
                time.sleep(0.1)
                buttons[0].delight(display)
                break
            elif pygame.key.get_pressed()[pygame.K_ESCAPE]:
                return
            pygame.event.pump()
    time.sleep(0.5)
    return pattern == player_pattern

def display_score(score, display):
    surface = pygame.font.Font(None, 100).render("Score: " + str(score), True, (255, 255, 255))
    rect = surface.get_rect()
    x = int(DISP_WIDTH / 2)
    y = int(DISP_HEIGHT / 2)
    rect.center = (x, y)
    display.blit(surface, rect)
    pygame.display.update()
    while any(pygame.key.get_pressed()):
        pygame.event.pump()
    while not pygame.key.get_pressed()[pygame.K_ESCAPE]:
        pygame.event.pump()

def main():
    pygame.init()
    pygame.display.set_caption("Repimem - Memory Game by Chigozie Agomo")
    pygame.display.set_icon(pygame.Surface((1, 1), pygame.SRCALPHA))
    display = pygame.display.set_mode((DISP_WIDTH, DISP_HEIGHT))
    buttons = []
    for i in range(4):
        buttons.append(Button(buttons))
    score = 0
    pattern = []
    time.sleep(1)
    while True:
        pattern.append(random.randint(0, 3))
        display_pattern(pattern, buttons, display)
        if not accept_pattern(pattern, buttons, display):
            break
        score += 1
    display_score(score, display)
    pygame.quit()

if __name__ == "__main__":
    main()