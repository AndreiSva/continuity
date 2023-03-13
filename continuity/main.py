import pygame
# import numpy

import continuity.renderer as renderer

def main():
    pygame.init()
    screen = pygame.display.set_mode([500, 500])

    main_renderer = renderer.Renderer(screen, 123)
    running = True
    
    while running:
        for event in pygame.event.get():
           if event.type == pygame.QUIT:
                running = False
           elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    main_renderer.camera.scale *= 1.5
                elif event.button == 5:
                    main_renderer.camera.scale /= 1.5
           elif event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[2]:
                mouse_dx, mouse_dy = event.rel
                main_renderer.camera.xpos += mouse_dx / main_renderer.camera.scale
                main_renderer.camera.ypos += mouse_dy / main_renderer.camera.scale
                
        main_renderer.render_screen()
        pygame.display.flip()
        
pygame.quit()
