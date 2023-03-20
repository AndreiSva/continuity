import pygame
from dataclasses import dataclass

class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.screen_size = 1000
        self.objects = []
        
        self.objects.append(pygame.Surface((1000,1000)))
        self.terrain = self.objects[0]
        self.terrain.fill((50, 100, 0))
        
    def render_screen(self):
        # clear the screen
        self.terrain.fill((50, 100, 0))

        pygame.draw.circle(self.terrain, (255, 0, 0), (100, 100), 10)

        self.screen.blit(self.terrain, pygame.Rect((0, 0), (1000, 1000)))
        
    def main_loop(self):
        running = True
    
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                
            self.render_screen()
            pygame.display.flip()

        pygame.quit()
        return True
        
def read_heightmap(path):
    pass
