#import numpy
from dataclasses import dataclass
import random
import copy
import math
import pdb
import numpy

#random.seed(0)

def activation(x):
    return max(0, x)

class Neuron:
    def __init__(self, connections, value=0):
        self.value = value
        self.connections = connections
    def propagate(self, bias):
        output_value = sum(map(lambda x : x["weight"] * x["neuron"].value, self.connections)) + (bias[0] * bias[1])
        output_value = activation(output_value)
        self.value = output_value
    def __copy__(self):
        return Neuron(copy.deepcopy(self.connections), 0)

class Brain:
    def __init__(self, network=None):
        #print(network)
        if network == None:
            #print("no network, creating new")
            #pdb.set_trace()
            self.network = [
                # input layer
                [
                    Neuron(None),
                    Neuron(None),
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
        else:
            self.network = network
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
                    if random.randint(1, 20) == 1:
                        connection["weight"] += float(numpy.random.normal(loc=0, scale=3.5))
        if random.randint(1, 20) == 1:
            self.bias[0] += float(numpy.random.normal(loc=0, scale=1))
        if random.randint(1, 20) == 1:
            self.bias[1] += float(numpy.random.normal(loc=0, scale=1))
    def __copy__(self):
        #print("copying brain")
        network = [
            # input layer
            [
                Neuron(None),
                Neuron(None),
            ],
        ]

        self.bias = [1, random.randint(1, 10)]
        layer = []
        #print(self.network)
        for i in range(5):
            connections = []
            for j in range(len(self.network[1][i].connections)):
                connections.append({"weight": self.network[1][i].connections[j]["weight"], "neuron": network[0][j]})
            layer.append(Neuron(connections))
        network.append(layer)

        output_layer = []
        for i in range(4):
            connections = []
            for j in range(len(self.network[-1][i].connections)):
                connections.append({"weight": self.network[-1][i].connections[j]["weight"], "neuron": network[1][j]})
            output_layer.append(Neuron(connections))
        network.append(output_layer)

        result = Brain(network)
        result.bias = copy.copy(self.bias)
        return result

if __name__ == "__main__":

    #i = [10, 20]
    while True:
        x = Brain()
        z = copy.deepcopy(x)
        for i in range(100):
            z.mutate()
        y = [int(x) for x in input("> ").split()]
        #y = [10, 20]
        result = x.think(y)

        #if result != (0, 0, 0, 0):
        #    print(result)
        print(list(map(lambda x : x.value, x.network[0])))
        print(list(map(lambda x : x.value, x.network[1])))
        print(list(map(lambda x : x.value, x.network[2])))
        print()
        result2 = z.think(y)
        
        print(list(map(lambda x : x.value, z.network[0])))
        print(list(map(lambda x : x.value, z.network[1])))
        print(list(map(lambda x : x.value, z.network[2])))
