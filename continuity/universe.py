import numpy
import random
import math
import copy
import numpy
from . import network

class Entity:
    def __init__(self, position = [0, 0], color = (255, 255, 255), size = 1, brain = None, epoch = 0):
        if brain == None:
            brain = network.Brain()
        self.energy = 100
        self.birth_epoch = epoch
        self.color = color
        self.size = size
        self.position = position
        self.last_position = self.position
        self.velocity = [0.0, 0.0]
        self.brain = brain
        self.genome = {"color": self.color, "size": self.size, "brain": self.brain, "smart-nose": random.choice([True, False])}
        self.target = None
        self.generation = 0
        self.breeding_timer = 0
    def reproduce(self, mutation_rate, epoch):
        child_genome = copy.copy(self.genome)
        child_brain = self.brain.__copy__()

        if mutation_rate > 0:
            for gene in child_genome.items():
                if random.randint(1, mutation_rate) == 1:
                    # print(gene)
                    if type(gene[1]) == tuple:
                        child_genome[gene[0]] = list(child_genome[gene[0]])
                        color_index = random.randint(0,2)
                        child_genome[gene[0]][color_index] += int(numpy.random.normal(loc=0, scale=15))
                        if child_genome[gene[0]][color_index] < 0:
                            child_genome[gene[0]][color_index] = 0
                        elif child_genome[gene[0]][color_index] > 255:
                            child_genome[gene[0]][color_index] = 255
                        child_genome[gene[0]] = tuple(child_genome[gene[0]])
                    elif type(gene[1]) == network.Brain:
                        child_brain.mutate()
                        pass
                    elif type(gene[1]) == bool:
                        if random.randint(1, 2) == 1:
                            child_genome[gene[0]] = not gene[1]
                    else:
                        child_genome[gene[0]] += int(numpy.random.normal(loc=0, scale=5))
                        if child_genome[gene[0]] < 0:
                            child_genome[gene[0]] = 0
        child_pos = copy.copy(self.position)

        if child_genome["size"] < 1:
            child_genome["size"] = 1
            
        child = Entity(child_pos, child_genome["color"], child_genome["size"], child_brain, epoch)
        child.energy = self.energy // 2 + 1
        child.generation = self.generation + 1
        return child
    def is_colliding(self, other):
        distance = math.sqrt((self.position[0] - other.position[0])**2 + (self.position[1] - other.position[1])**2)
        if distance < self.size + other.size:
            return True
        else:
            return False
    def live(self, epoch):
        age = epoch - self.birth_epoch
        self.energy -= (((self.size)**2) + 50) / ((40 * math.log((age + 1)/100) + 200))

class Pellet(Entity):
    def __init__(self, position):
        super().__init__(position, (255, 128, 0), 2)

def populate(e, n, distance, size):
    x = []
    for i in range(n):
        while True:
            valid = True
            position = [random.randint(distance, size - distance), random.randint(distance, size - distance)]
            scale = random.randint(4, 20)
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0,255))
            entity = Entity(position, color, scale)
            for other in x:
                if entity.is_colliding(other):
                    valid = False
                    break
            if valid:
                entity.velocity[0] = random.randint(-2, 2)
                entity.velocity[1] = random.randint(-2, 2)
                x.append(entity)
                break
    return x
