import numpy
import random
import math

class Entity:
    def __init__(self, position = [0, 0], color = (255, 255, 255), size = 1):
        self.energy = 100
        self.color = color
        self.size = size
        self.genome = {"color": self.color, "size": self.size}
        self.position = position
        self.velocity = [0.0, 0.0]
    def reproduce(self, mutation_rate):
        child_genome = self.genome.copy()
        if mutation_rate > 0:
            for gene in child_genome.values():
                if random.randint(1, mutation_rate) == 1:
                    if type(gene) == tuple:
                        for color in gene:
                            color += random.randint(-15, 15)
                    else:
                        gene += random.randint(-5, 5)
        child = Entity(self.position.copy(), child_genome["color"], child_genome["size"])
        child.energy = self.energy // 2 + 1
        self.energy //= 2 
        return child
    def is_colliding(self, other):
        distance = math.sqrt((self.position[0] - other.position[0])**2 + (self.position[1] - other.position[1])**2)
        if distance < self.size + other.size:
            return True
        else:
            return False
    def live(self):
        self.energy -= 1

class Pellet(Entity):
    def __init__(self, position):
        super().__init__(position, (0, 255, 0), 2)

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
