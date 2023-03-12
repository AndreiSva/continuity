import pygame

class Camera:
    ypos: float
    xpos: float
    scale: float
    def __init__(self, xpos=None, ypos=None, scale=None):
        self.xpos = 0
        self.ypos = 0
        self.scale = 1
    
class Renderer:
    def __init__(self, screen, terrain):
        self.screen = screen
        self.screen.fill((0, 0, 256))
        self.terrain = pygame.Surface((50,50))
        self.terrain.fill((0, 0, 0))
    def render():
        rect = self.terrain.get_rect()
        self.screen.blit(self.terrain, rect)

def read_heightmap(path):
    pass
