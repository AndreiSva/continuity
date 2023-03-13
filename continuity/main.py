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
            match event.type:
                case pygame.QUIT:
                    running = False
                case pygame.MOUSEWHEEL:
                    if event.y > 0:
                        main_renderer.camera.scale *= 1.5
                    else:
                        main_renderer.camera.scale /= 1.5
                    x, y = pygame.mouse.get_pos()
                    main_renderer.camera.xpos += x
                    main_renderer.camera.ypos += y 
                    print(main_renderer.camera.scale)
                    
        if pygame.mouse.get_pressed()[0]:
            mouse_dx, mouse_dy = pygame.mouse.get_rel()
            main_renderer.camera.xpos += mouse_dx
            main_renderer.camera.ypos += mouse_dy

        pygame.mouse.get_rel()
                
        main_renderer.render_screen()
        pygame.display.flip()
        
pygame.quit()
