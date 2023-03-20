import pygame
# import numpy

import continuity.renderer as renderer
import continuity.network as network

def main():
    pygame.init()
    screen = pygame.display.set_mode([1000, 1000])
    main_renderer = renderer.Renderer(screen)
    main_renderer.main_loop()
