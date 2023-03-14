import pygame
# import numpy

import continuity.renderer as renderer

def main():
    pygame.init()
    screen = pygame.display.set_mode([500, 500])
    main_renderer = renderer.Renderer(screen, 123)
    main_renderer.main_loop()
