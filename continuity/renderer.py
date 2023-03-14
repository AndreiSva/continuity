import pygame

class Camera:
    ypos: float
    xpos: float
    scale: float
    def __init__(self, xpos=0.0, ypos=0.0, scale=1):
        self.xpos = ypos
        self.ypos = ypos
        self.scale = scale
    
class Renderer:
    def __init__(self, screen, terrain):
        self.camera = Camera()
        self.screen = screen
        self.screen.fill((0, 0, 255))
        self.terrain = pygame.Surface((500,500))
        self.terrain.fill((50, 100, 0))
        
    def render_screen(self):
        # clear the screen
        self.screen.fill((30,30,30))

        self.terrain = pygame.transform.scale(self.terrain, (500 * self.camera.scale, 500 * self.camera.scale))
        self.screen.blit(self.terrain, pygame.Rect((0 + self.camera.xpos) * self.camera.scale, (0 + self.camera.ypos) * self.camera.scale, 500 * self.camera.scale, 500 * self.camera.scale))

        pygame.draw.circle(self.screen, (255, 0, 0), ((250 + self.camera.xpos) * self.camera.scale, (250 + self.camera.ypos) * self.camera.scale), 10 * self.camera.scale)

        #self.other = pygame.transform.scale(self.other, (100 * self.camera.scale, 100 * self.camera.scale))
        #self.screen.blit(self.other, pygame.Rect((100 + self.camera.xpos) * self.camera.scale, (100 + self.camera.ypos) * self.camera.scale, 100 * self.camera.scale, 100 * self.camera.scale))
        
def read_heightmap(path):
    pass
