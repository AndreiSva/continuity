import numpy
import random
import math

class Entity:
    def __init__(self, position = [0, 0], color = (255, 255, 255), size = 1):
        self.energy = 100
        self.color = color
        self.size = size
        self.position = position
        self.velocity = [0.0, 0.0]
    def is_colliding(self, other):
        # Wall
        if type(other) == float:
            return not ((self.position[0] + self.size > other) or (self.position[1] + self.size > other))
        
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
    def live(self):
        pass

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
