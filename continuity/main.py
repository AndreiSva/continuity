import pygame
import argparse
# import numpy

from . import renderer
from . import network

def main():
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode([1000, 1000])
    main_renderer = renderer.Renderer(screen)
    main_renderer.main_loop()
