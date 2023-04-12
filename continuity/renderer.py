import pygame
import random
from dataclasses import dataclass
from . import universe
import numpy
import math
from . import network
import copy
import pickle

pygame.font.init()
font = pygame.font.SysFont("Monospace", 13)

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
                position = (random.randint(50, self.screen_size - 50), random.randint(50, self.screen_size - 50))
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
            text_surface = font.render(f"{item[1][0]}: {item[1][1]}", False, (0, 0, 0))
            self.screen.blit(text_surface, (0,0 + (item[0] * 20)))
        if self.selected_entity not in self.entities:
            self.selected_entity = None
        if self.selected_entity != None:
            properties = list(self.selected_entity.genome.items())
            properties = [("name", ("".join([str(hex(i))[1:3] for i in self.selected_entity.color]) + str(hex(self.selected_entity.size))))] + properties
            properties = [("energy", self.selected_entity.energy)] + properties
            properties = [("generation", self.selected_entity.generation)] + properties
            for i, item in enumerate(properties):
                entity_property = item[0]
                value = item[1]
                text_surface = font.render(f"{entity_property}: {str(value)[0:5] if type(value) == float else value}", False, (0, 0, 0))
                text_surface_rect = text_surface.get_rect()
                text_surface_rect.right = self.screen_size
                self.screen.blit(text_surface, (text_surface_rect.x, text_surface_rect.y + i * 20))

            brain_surface = self.gen_network_surface(self.selected_entity.brain)
            brain_surface_rect = brain_surface.get_rect()
            brain_surface_rect.center = (self.screen_size / 2, 100)
            self.screen.blit(brain_surface, brain_surface_rect)

    def gen_network_surface(self, brain):
        brain_surface = pygame.Surface((250, 150))
        brain_surface.fill("grey")

        neurons = {}

        for i, layer in enumerate(brain.network):
            for j, neuron in enumerate(layer):
                color = (255 if neuron.value > 0 else 0, 0, (255 if neuron.value < 1 else 0))
                pygame.draw.circle(brain_surface, color, (i * 80 + 40, j * 20 + 30), 10)
                neurons[neuron] = (i * 80 + 40, j * 20 + 30)
                if neuron.connections != None:
                    for connection in neuron.connections:
                        color = (255 if connection["neuron"].value > 0 else 0,0, (255 if connection["neuron"].value < 1 else 0))
                        pygame.draw.line(brain_surface, color, (i * 80 + 40, j * 20 + 30), neurons[connection["neuron"]], width=connection["weight"])

        return brain_surface

        #pygame.draw.line()

    def target_closest_pellet(self, entity):
        best = []
        if len(self.pellets) == 0:
            self.spawn_food(40)
        for pellet in self.pellets:
            #distance = 10
            distance = math.sqrt((pellet.position[0]-entity.position[0])**2 + (pellet.position[1]-entity.position[1])**2)
            if best == [] or distance < best[0]:
                best = [distance, pellet]
            entity.target = best[1]

    def main_loop(self):
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
        self.spawn_food(300)
        self.population = len(self.entities)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    found = False
                    for entity in self.entities:
                        distance = math.sqrt((entity.position[0] - x)**2 + (entity.position[1] - y)**2)
                        if distance < entity.size:
                            self.selected_entity = entity
                            found = True
                    if not found:
                        self.selected_entity = None
                elif event.type == pygame.KEYDOWN:
                    print(event)
                    if event.key == pygame.K_p:
                        if not paused:
                            paused = True
                        else:
                            paused = False
                            physics_clock.tick()
                            physics_clock.tick()
                    elif event.key == pygame.K_s:
                        objects = {"entities": self.entities, "pellets": self.pellets, "meta": self.meta, "epoch": self.epoch}
                        pickle.dump(objects, open("checkpoint.pkl", "wb"))
                    elif event.key == pygame.K_l:
                        objects = pickle.load(open("checkpoint.pkl", "rb"))
                        self.entities = objects["entities"]
                        self.pellets = objects["pellets"]
                        self.meta = objects["meta"]
                        self.epoch = objects["epoch"]
                elif event.type == SimEvent.SIMTICK and not paused:
                    self.epoch += 1
                    for entity in self.entities:
                        self.target_closest_pellet(entity)
                        entity.live()
                        if entity.energy <= 0:
                            self.pellets.append(universe.Pellet(entity.position))
                            self.entities.remove(entity)
                        elif entity.energy >= 50:
                            entity.breeding_timer += 1
                            self.population = len(self.entities)
                            pos_diffx = abs(entity.position[0] - entity.last_position[0])
                            pos_diffy = abs(entity.position[1] - entity.last_position[1])
                            if (self.population < 200 and entity.breeding_timer >= 3 and
                                (pos_diffx > 0 or pos_diffy > 0)):
                                self.entities.append(entity.reproduce(self.settings.mutation_chance))
                                entity.breeding_timer = 0
                            entity.energy *= 0.9
                        else:
                            entity.breeding_timer = 0
                            # entity.energy += 100
                    if len(self.pellets) <= self.settings.max_food:
                        self.spawn_food(10)
                elif event.type == SimEvent.PHYSICSTICK and not paused:
                    for entity in self.entities:
                        entity.position[0] += (entity.velocity[0] * physics_clock.get_time())
                        entity.position[1] += (entity.velocity[1] * physics_clock.get_time())

                        # find the closest pellet
                        if entity.target not in self.pellets:
                            self.target_closest_pellet(entity)

                        jitter = random.randint(-100, 100) / 100
                        options = entity.brain.think((entity.target.position[0] - entity.position[0] + jitter, entity.target.position[1] - entity.position[1] + jitter))
                        #options = entity.brain.think((0, 0))
                        entity.last_position = copy.copy(entity.position)
                        entity.position[0] += options[0].value / 5000
                        entity.position[1] += options[1].value / 5000
                        entity.position[0] -= options[2].value / 5000
                        entity.position[1] -= options[3].value / 5000


                        entity.energy -= (options[0].value / 500000) + (options[2].value / 500000) + (options[1].value / 500000) + (options[3].value / 500000)

                        if entity.position[0] + entity.size >= self.screen_size:
                            #entity.velocity[0] -= 5
                            self.entities.remove(entity)
                            continue
                        elif entity.position[0] - entity.size <= 0:
                            #entity.velocity[0] =+ 5
                            entity.energy -= 18
                            self.entities.remove(entity)
                            continue

                        if entity.position[1] + entity.size >= self.screen_size:
                            #entity.velocity[1] -= 5
                            entity.energy -= 18
                            self.entities.remove(entity)
                            continue
                        elif entity.position[1] - entity.size <= 0:
                            #entity.velocity[1] += 5
                            entity.energy -= 18
                            self.entities.remove(entity)
                            continue
                        
                        entity.velocity[0] *= 0.80
                        entity.velocity[1] *= 0.80

                        
                        for entity2 in self.pellets:
                            if entity.is_colliding(entity2):
                                #entity.energy += 20
                                entity.energy += -2**(entity.size - 18) + 20
                                #entity.energy += 150 / (entity.size if entity.size > 3 else 3) + (10 if entity.size < 30 else 0)
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
