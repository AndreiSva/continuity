import pygame
from dataclasses import dataclass

class Camera:
    ypos: float
    xpos: float
    scale: float
    def __init__(self, xpos=0.0, ypos=0.0, scale=1):
        self.xpos = ypos
        self.ypos = ypos
        self.scale = scale

@dataclass
class RendererObject:
    surface: pygame.Surface
    scale: float
    
class Renderer:
    def __init__(self, screen, terrain):
        self.camera = Camera()

        self.screen = screen
        
        self.terrain = RendererObject(pygame.Surface((1000,1000)), 1.0)
        self.terrain.surface.fill((50, 100, 0))
        
    def render_screen(self):
        # clear the screen
        self.screen.fill((30,30,30))

        if self.terrain.scale != self.camera.scale:
            self.terrain.surface = pygame.transform.scale(self.terrain.surface, (1000 * self.camera.scale, 1000 * self.camera.scale))
            self.terrain.scale = self.camera.scale
        self.screen.blit(self.terrain.surface, pygame.Rect((0 + self.camera.xpos) * self.camera.scale, (0 + self.camera.ypos) * self.camera.scale, 1000 * self.camera.scale, 1000 * self.camera.scale))

        pygame.draw.circle(self.screen, (255, 0, 0), ((250 + self.camera.xpos) * self.camera.scale, (250 + self.camera.ypos) * self.camera.scale), 10 * self.camera.scale)


    def main_loop(self):
        running = True
    
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if event.button == 4:
                        self.camera.scale *= 1.5
                    elif event.button == 5:
                        self.camera.scale /= 1.5
                elif event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[2]:
                    mouse_dx, mouse_dy = event.rel
                    self.camera.xpos += mouse_dx / self.camera.scale
                    self.camera.ypos += mouse_dy / self.camera.scale
                
            self.render_screen()
            pygame.display.flip()

        pygame.quit()
        
def read_heightmap(path):
    pass
