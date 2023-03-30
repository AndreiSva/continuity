import pygame
import argparse
# import numpy

from . import renderer
from . import network

def main():
    parser = argparse.ArgumentParser(description='An artificial life simulator')
    parser.add_argument("--mutation-chance", type=int, help="the denominator of the mutation probability. a higher number will result in a smaller mutation chance", default=10)
    parser.add_argument("--population", type=int, help="the initial population", default=50)
    parser.add_argument("--max-food", type=int, help="the maximum food allowed on the map", default=200)

    args = parser.parse_args()
    
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode([1000, 1000])
    main_renderer = renderer.Renderer(screen, args)
    main_renderer.main_loop()
