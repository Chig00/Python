#!/usr/bin/env python3

"""Detector and Live Plotter by Chigozie Agomo.

readadc() function by Lady Ada.

This script relies on the correct wiring of the RPi's GPIO
pins to the MCP3008 ADC and the resistors.
Incorrect wiring will give erroneous readings.

This scripts detects the output of the MCP3008
and plots the data live using pygame."""

import time
import pygame
import RPi.GPIO as GPIO

CHANNEL = 0
SPICLK = 11
SPIMISO = 9
SPIMOSI = 10
SPICS = 8

DISPLAY_SIZE = (1000, 500)
ICON_SIZE = (20, 20)
ICON_COLOUR = (0, 0, 0, 0)
CAPTION = "Plotter"
PLOTTER_SIZE = (5, 5)
PLOTTER_COLOUR = (255, 255, 255)
POSITION_NULL = 0
ERASER = (0, 0, 0)
DELAY = 0.001
QUIT_KEY = pygame.K_ESCAPE

class Plotter:
    """Sprite for plotting the results live on the display."""

    def __init__(self):
        """Initialise the plotter."""
        self.surface = pygame.Surface(PLOTTER_SIZE)
        self.surface.fill(PLOTTER_COLOUR)
        self.rect = self.surface.get_rect()

    def plot(self, position, display):
        """Plot the plotter on the display for the given position."""
        display.blit(self.surface, position)

def readadc(adcnum, clockpin, mosipin, misopin, cspin):
    """Read and return the ADC's value."""
    if ((adcnum > 7) or (adcnum < 0)):
        return -1
    GPIO.output(cspin, True)

    GPIO.output(clockpin, False)  # start clock low
    GPIO.output(cspin, False)     # bring CS low

    commandout = adcnum
    commandout |= 0x18  # start bit + single-ended bit
    commandout <<= 3    # we only need to send 5 bits here
    for i in range(5):
        if (commandout & 0x80):
            GPIO.output(mosipin, True)
        else:
            GPIO.output(mosipin, False)
        commandout <<= 1
        GPIO.output(clockpin, True)
        GPIO.output(clockpin, False)

    adcout = 0
    # read in one empty bit, one null bit and 10 ADC bits
    for i in range(12):
        GPIO.output(clockpin, True)
        GPIO.output(clockpin, False)
        adcout <<= 1
        if (GPIO.input(misopin)):
            adcout |= 0x1

    GPIO.output(cspin, True)

    adcout >>= 1       # first bit is 'null' so drop it
    return adcout

def create_icon():
    """Create the blank icon."""
    icon = pygame.Surface(ICON_SIZE, pygame.SRCALPHA)
    icon.fill(ICON_COLOUR)
    return icon

def main():
    """Start the script."""
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    GPIO.setup(SPIMOSI, GPIO.OUT)
    GPIO.setup(SPIMISO, GPIO.IN)
    GPIO.setup(SPICLK, GPIO.OUT)
    GPIO.setup(SPICS, GPIO.OUT)

    pygame.init()
    pygame.display.set_icon(create_icon())
    pygame.display.set_caption(CAPTION)
    display = pygame.display.set_mode(DISPLAY_SIZE)
    plotter = Plotter()

    results = []
    for i in range(DISPLAY_SIZE[0]):
        results.append(POSITION_NULL)

    while not pygame.key.get_pressed()[QUIT_KEY]:
        display.fill(ERASER)
        results.append(readadc(CHANNEL, SPICLK, SPIMOSI, SPIMISO, SPICS))
        del results[0]
        for i in range(len(results)):
            plotter.plot((i, DISPLAY_SIZE[1] - results[i]/2), display)
        pygame.display.flip()
        pygame.event.pump()
        time.sleep(DELAY)

    pygame.quit()

if __name__ == "__main__":
    main()
