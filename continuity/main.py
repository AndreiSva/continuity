import pygame
import numpy

import renderer

def main():
    pygame.init()
    screen = pygame.display.set_mode([500, 500])

    main_renderer = renderer.Renderer(screen, 123)
    
    running = True
    while running:
        main_render.render()

pygame.quit()

