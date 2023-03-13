import pygame

class Camera:
    ypos: float
    xpos: float
    scale: float
    def __init__(self, xpos=0.0, ypos=0.0, scale=30):
        self.xpos = ypos
        self.ypos = ypos
        self.scale = scale
    
class Renderer:
    def __init__(self, screen, terrain):
        self.camera = Camera()
        self.screen = screen
        self.screen.fill((0, 0, 255))
        self.terrain = pygame.Surface((50,50))
        self.terrain.fill((0, 255, 0))
        
    def render_screen(self):
        # clear the screen
        self.screen.fill((30,30,30))
        rect = self.terrain.get_rect()
        self.terrain = pygame.transform.scale(self.terrain, (self.camera.scale, self.camera.scale))
        self.screen.blit(self.terrain, pygame.Rect(self.camera.xpos + 250 - self.camera.scale / 2, self.camera.ypos + 250 - self.camera.scale / 2, self.camera.scale, self.camera.scale))

def read_heightmap(path):
    pass
