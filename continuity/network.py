import numpy
from dataclasses import dataclass

def activation(x):
    if x < 0:
        return 0
    else:
        return x

@dataclass
class Neuron:
    value: float
    connections: list

def propagate(network):
    pass
