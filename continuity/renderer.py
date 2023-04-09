import pygame
import random
from dataclasses import dataclass
from . import universe
import numpy
import math
from . import network
import copy

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
        self.epoch = 0
        self.selected_entity = None
        
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

        if self.selected_entity != None:
            properties = list(self.selected_entity.genome.items())
            properties = [("name", ("".join([str(hex(i))[1:3] for i in self.selected_entity.color]) + str(hex(self.selected_entity.size))))] + properties
            properties = [("energy", self.selected_entity.energy)] + properties
            properties = [("generation", self.selected_entity.generation)] + properties
            for i, item in enumerate(properties):
                entity_property = item[0]
                value = item[1]
                text_surface = self.font.render(f"{entity_property}: {str(value)[0:5] if type(value) == float else value}", False, (0, 0, 0))
                text_surface_rect = text_surface.get_rect()
                text_surface_rect.right = self.screen_size
                self.screen.blit(text_surface, (text_surface_rect.x, text_surface_rect.y + i * 20))

    def main_loop(self):
        self.font = pygame.font.SysFont("Monospace", 13)
        
        running = True
        paused = False
        clock = pygame.time.Clock()
        physics_clock = pygame.time.Clock()
    
        self.epoch = 0
        #pygame.time.set_timer(SimEvent.SIMTICK, 1000)
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
                    for entity in self.entities:
                        distance = math.sqrt((entity.position[0] - x)**2 + (entity.position[1] - y)**2)
                        if distance < entity.size:
                            self.selected_entity = entity
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
                    self.epoch += 1
                    for entity in self.entities:
                        entity.live()
                        if entity.energy <= 0:
                            self.pellets.append(universe.Pellet(entity.position))
                            self.entities.remove(entity)
                        elif entity.energy >= 30:
                            if self.population < 300:
                                self.entities.append(entity.reproduce(self.settings.mutation_chance))
                            # entity.energy += 100
                    if len(self.pellets) <= self.settings.max_food:
                        self.spawn_food(30)
                elif event.type == SimEvent.PHYSICSTICK and not paused:
                    for entity in self.entities:
                        entity.position[0] += (entity.velocity[0] * physics_clock.get_time())
                        entity.position[1] += (entity.velocity[1] * physics_clock.get_time())

                        # find the closest pellet
                        if entity.target not in self.pellets:
                            best = []
                            if len(self.pellets) == 0:
                                self.spawn_food(40)
                            for pellet in self.pellets:
                                #distance = 10
                                distance = math.sqrt((pellet.position[0]-entity.position[0])**2 + (pellet.position[1]-entity.position[1])**2)
                                if best == [] or distance < best[0]:
                                    best = [distance, pellet]
                                entity.target = best[1]

                        jitter = random.randint(-100, 100) / 100
                        options = entity.brain.think((entity.target.position[0] - entity.position[0] + jitter, entity.target.position[1] - entity.position[1] + jitter))
                        #options = entity.brain.think((0, 0))
                        entity.position[0] += options[0].value / 3000
                        entity.position[1] += options[1].value / 3000
                        entity.position[0] -= options[2].value / 3000
                        entity.position[1] -= options[3].value / 3000


                        entity.energy -= (options[0].value / 200000) + (options[2].value / 100000) + (options[1].value / 100000) + (options[3].value / 100000)

                        if entity.position[0] + entity.size >= self.screen_size:
                            entity.velocity[0] -= 5
                            entity.energy -= 18
                            continue
                        elif entity.position[0] - entity.size <= 0:
                            entity.velocity[0] =+ 5
                            entity.energy -= 18
                            continue

                        if entity.position[1] + entity.size >= self.screen_size:
                            entity.velocity[1] -= 5
                            entity.energy -= 18
                            continue
                        elif entity.position[1] - entity.size <= 0:
                            entity.velocity[1] += 5
                            entity.energy -= 18
                            continue
                        
                        entity.velocity[0] *= 0.80
                        entity.velocity[1] *= 0.80

                        
                        for entity2 in self.pellets:
                            if entity.is_colliding(entity2):
                                entity.energy += 15
                                self.pellets.remove(entity2)
                    physics_clock.tick()


                    
                self.meta["epoch"] = self.epoch
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
