#import numpy
from dataclasses import dataclass
import random
import copy

def activation(x):
    if x < 0:
        return 0
    else:
        return x

class Neuron:
    def __init__(self, connections, value=0):
        self.value = value
        self.connections = connections
    def propagate(self, bias):
        output_value = sum(map(lambda x : x["weight"] * x["neuron"].value, self.connections)) + (bias[0] * bias[1])
        output_value = activation(output_value)
        self.value = output_value

class Brain:
    def __init__(self):
        self.network = [
            # input layer
            [
                Neuron(None),
                Neuron(None)
            ],
        ]

        self.bias = [1, random.randint(1, 10)]
        layer = []
        #print(self.network)
        for i in range(5):
            connections = list(map(lambda x : {"weight": random.randint(-10, 10), "neuron": x}, self.network[0]))
            layer.append(Neuron(connections))

        self.network.append(layer)

        output_layer = []
        for i in range(4):
            connections = list(map(lambda x : {"weight": random.randint(-10, 10), "neuron": x}, self.network[-1]))
            output_layer.append(Neuron(connections))

        self.network.append(output_layer)
    def think(self, inputs):
        for i, neuron in enumerate(self.network[0]):
            neuron.value = inputs[i]
        for layer_index in range(1, len(self.network)):
            for neuron in self.network[layer_index]:
                neuron.propagate(self.bias)

        return tuple(self.network[-1])
    def mutate(self):
        for layer_index in range(1, len(self.network)):
            for neuron in self.network[layer_index]:
                for connection in neuron.connections:
                    if random.randint(1, 6) == 1:
                        connection["weight"] += random.randint(-5, 5)
        if random.randint(1, 10) == 1:
            self.bias[0] += random.randint(-1, 1)
        if random.randint(1, 10) == 1:
            self.bias[1] += random.randint(-1, 1)
    def __copy__(self):
        result = Brain()
        result.network = copy.deepcopy(self.network)
        result.bias = self.bias
        return result

if __name__ == "__main__":

    #i = [10, 20]
    while True:
        x = Brain()
        y = [int(x) for x in input("> ").split()]
        #y = [10, 20]
        result = x.think(y)
        #if result != (0, 0, 0, 0):
        #    print(result)
        print(list(map(lambda x : x.value, x.network[0])))
        print(list(map(lambda x : x.value, x.network[1])))
        print(list(map(lambda x : x.value, x.network[2])))
        print(result)
