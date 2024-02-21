import numpy as np
import numbers

def extract(cond, x):
    if isinstance(x, numbers.Number):
        return x
    else:
        return np.extract(cond, x)

class vec3():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

def array_to_vec3(array):
    return vec3(array[0],array[1],array[2])