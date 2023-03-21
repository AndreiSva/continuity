import pygame
import random
from dataclasses import dataclass
import continuity.universe as universe
import numpy

class SimEvent:
    SIMTICK = pygame.USEREVENT + 1
    PHYSICSTICK = pygame.USEREVENT + 2

class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.screen_size = 1000
        self.population = 0
        self.entities = []
        self.meta = {}
        
        self.terrain = pygame.Surface((1000,1000))
        self.terrain.fill((50, 100, 0))

    def spawn_food(self, n):
        x = []
        for i in range(n):
            while True:
                valid = True
                position = (random.randint(0, self.screen_size), random.randint(0, self.screen_size))
                entity = universe.Pellet(position)
                for other in self.entities:
                    if entity.is_colliding(other):
                        valid = False
                        break
                if valid:
                    x.append(entity)
                    break
        self.entities += x
        
    def render_screen(self):
        # clear the screen
        self.terrain.fill((50, 150, 0))
        for entity in self.entities:
            pygame.draw.circle(self.terrain, entity.color, entity.position, entity.size)
        self.screen.blit(self.terrain, pygame.Rect((0, 0), (1000, 1000)))

        for item in enumerate(self.meta.items()):
            text_surface = self.font.render(f"{item[1][0]}: {item[1][1]}", False, (0, 0, 0))
            self.screen.blit(text_surface, (0,0 + (item[0] * 20)))
        
    def main_loop(self):
        self.font = pygame.font.SysFont("Monospace", 13)
        
        running = True
        clock = pygame.time.Clock()
    
        epoch = 0
        pygame.time.set_timer(SimEvent.SIMTICK, 1000)
        pygame.time.set_timer(SimEvent.PHYSICSTICK, 10)

        self.entities = universe.populate(universe.Entity, 50, 20, self.screen_size)
        self.population = len(self.entities)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    self.meta["mousepos"] = f"({x}, {y})"
                elif event.type == SimEvent.SIMTICK:
                    epoch += 1
                    for entity in self.entities:
                        entity.live()
                        if entity.energy <= 0:
                            self.entities.append(universe.Pellet(entity.position))
                            self.entities.remove(entity)
                    self.spawn_food(10)
                elif event.type == SimEvent.PHYSICSTICK:
                    for entity in self.entities:
                        if not isinstance(entity, universe.Pellet):
                            entity.position[0] += (entity.velocity[0] * clock.get_time())
                            entity.position[1] += (entity.velocity[1] * clock.get_time())

                        if abs(entity.velocity[0]) < 0.3:
                            entity.velocity[0] = 0
                        if abs(entity.velocity[1]) < 0.3:
                            entity.velocity[1] = 0
                        entity.velocity[0] -= ((entity.size * 9.8) * 0.001) / entity.size
                        entity.velocity[1] -= ((entity.size * 9.8) * 0.001) / entity.size

                for entity in self.entities:
                    if not isinstance(entity, universe.Pellet):
                        for food in self.entities:
                            if isinstance(food, universe.Pellet):
                                if entity.is_colliding(food):
                                    entity.energy += 1
                                    self.entities.remove(food)
                    
                self.meta["epoch"] = epoch
                self.meta["population"] = self.population
                self.meta["fps"] = clock.get_fps()
                    
            self.render_screen()
            pygame.display.flip()
            clock.tick()

        pygame.quit()
        return True
        
def read_heightmap(path):
    pass
