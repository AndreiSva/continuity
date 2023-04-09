import pygame
import random
from dataclasses import dataclass
from . import universe
import numpy
import math

class SimEvent:
    SIMTICK = pygame.USEREVENT + 1
    PHYSICSTICK = pygame.USEREVENT + 2

class Renderer:
    def __init__(self, screen, settings):
        self.screen = screen
        self.screen_size = 1000
        self.settings = settings
        self.population = 0
        self.pellets = []
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
        self.pellets += x
        
    def render_screen(self):
        # clear the screen
        self.terrain.fill((50, 150, 0))
        for entity in self.entities + self.pellets:
            pygame.draw.circle(self.terrain, entity.color, entity.position, entity.size)
        self.screen.blit(self.terrain, pygame.Rect((0, 0), (1000, 1000)))

        for item in enumerate(self.meta.items()):
            text_surface = self.font.render(f"{item[1][0]}: {item[1][1]}", False, (0, 0, 0))
            self.screen.blit(text_surface, (0,0 + (item[0] * 20)))
        
    def main_loop(self):
        self.font = pygame.font.SysFont("Monospace", 13)
        
        running = True
        paused = False
        clock = pygame.time.Clock()
        physics_clock = pygame.time.Clock()
    
        epoch = 0
        pygame.time.set_timer(SimEvent.SIMTICK, 1000)
        pygame.time.set_timer(SimEvent.PHYSICSTICK, 10)

        self.entities = universe.populate(universe.Entity, self.settings.population, 20, self.screen_size)
        #self.entities = universe.populate(universe.Entity, 1, 20, self.screen_size)
        self.spawn_food(50)
        self.population = len(self.entities)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    self.meta["mousepos"] = f"({x}, {y})"
                elif event.type == pygame.KEYDOWN:
                    print(event)
                    if event.key == pygame.K_p:
                        if not paused:
                            paused = True
                            #pygame.time.set_timer(SimEvent.SIMTICK, 0)
                            #pygame.time.set_timer(SimEvent.PHYSICSTICK, 0)
                        else:
                            paused = False
                            #pygame.time.set_timer(SimEvent.SIMTICK, 1000)
                            #pygame.time.set_timer(SimEvent.PHYSICSTICK, 10)
                            physics_clock.tick()
                            physics_clock.tick()
                elif event.type == SimEvent.SIMTICK and not paused:
                    epoch += 1
                    for entity in self.entities:
                        entity.live()
                        if entity.energy <= 0:
                            self.pellets.append(universe.Pellet(entity.position))
                            self.entities.remove(entity)
                        elif entity.energy >= 50:
                            self.entities.append(entity.reproduce(self.settings.mutation_chance))
                            # entity.energy += 100
                    if len(self.pellets) <= self.settings.max_food:
                        self.spawn_food(40)
                elif event.type == SimEvent.PHYSICSTICK and not paused:
                    for entity in self.entities:
                        entity.position[0] += (entity.velocity[0] * physics_clock.get_time())
                        entity.position[1] += (entity.velocity[1] * physics_clock.get_time())

                        # find the closest pellet
                        best = []
                        for pellet in self.pellets:
                            distance = math.sqrt((pellet.position[0]-entity.position[0])**2 + (pellet.position[1]-entity.position[1])**2)
                            if best == [] or distance < best[0]:
                                best = [distance, pellet]      
                        
                        options = entity.brain.think(best[1].position)
                        #print(options)
                        if options[0] == 1:
                            entity.velocity[0] += 0.2
                        if options[1] == 1:
                            entity.velocity[0] -= 0.2
                        if options[2] == 1:
                            entity.velocity[1] += 0.2
                        if options[3] == 1:
                            entity.velocity[1] -= 0.2
                        

                        if entity.position[0] + entity.size >= self.screen_size:
                            entity.velocity[0] = -abs(entity.velocity[0])
                            continue
                        elif entity.position[0] - entity.size <= 0:
                            entity.velocity[0] = abs(entity.velocity[0])
                            continue

                        if entity.position[1] + entity.size >= self.screen_size:
                            entity.velocity[1] = -abs(entity.velocity[0])
                            continue
                        elif entity.position[1] - entity.size <= 0:
                            entity.velocity[1] = abs(entity.velocity[0])
                            continue
                        
                        if abs(entity.velocity[0]) <= 0.1:
                            entity.velocity[0] = 0
                        if abs(entity.velocity[1]) <= 0.1:
                            entity.velocity[1] = 0

                        if entity.velocity[0] == 0 and entity.velocity[1] == 0:
                            continue

                        mulx = -1 if entity.velocity[0] > 0 else 1
                        muly = -1 if entity.velocity[1] > 0 else 1

                        #entity.velocity[0] += (-1 if entity.velocity[0] > 0 else 1) * entity.size * entity.velocity[0]
                        #entity.velocity[1] += (-1 if entity.velocity[1] > 0 else 1) * entity.size * entity.velocity[1]
                        entity.velocity[0] += (entity.size * (9.8 * 0.0001)) * mulx
                        entity.velocity[1] += (entity.size * (9.8 * 0.0001)) * muly
                    physics_clock.tick()


                for entity in self.entities:
                    for entity2 in self.pellets:
                        if entity.is_colliding(entity2):
                            entity.energy += 1
                            self.pellets.remove(entity2)
                    
                self.meta["epoch"] = epoch
                self.meta["population"] = len(self.entities)
                self.meta["food"] = len(self.pellets)
                self.meta["fps"] = clock.get_fps()
                    
            self.render_screen()
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
        return True
        
def read_heightmap(path):
    pass
