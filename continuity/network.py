import numpy
from dataclasses import dataclass
import random

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
        output_value = sum(map(lambda x : x["weight"] * x["neuron"].value)) + (bias[0] * bias[1])
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

        for i in range(5):
            connections = list(map(self.network[0], lambda x : {"weight": random.randint(1, 10), "neuron": x}))
            layer.append(Neuron(connections))

        self.network.append(layer)

        output_layer = []
        for i in range(4):
            connections = list(map(self.network[-1], lambda x : {"weight": random.randint(1, 10), "neuron": x}))
            output_layer.append(Neuron(connections))

        self.network.append(output_layer)
    def think(self, inputs):
        for i, neuron in enumerate(self.network[0]):
            neuron.value = inputs[i]
        for layer_index in range(1, len(self.network) - 1):
            for neuron in self.network[layer_index]:
                neuron.propagate(self.bias)

        return tuple(map(self.network[-1], lambda x : x.value))
