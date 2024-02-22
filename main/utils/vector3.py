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

    def __add__(self, v):
        if isinstance(v, vec3):
            return vec3(self.x + v.x, self.y + v.y, self.z + v.z)
        elif isinstance(v, numbers.Number) or isinstance(v, np.ndarray):
            return vec3(self.x + v, self.y + v, self.z + v)
    def __radd__(self, v):
        if isinstance(v, vec3):
            return vec3(self.x + v.x, self.y + v.y, self.z + v.z)
        elif isinstance(v, numbers.Number) or isinstance(v, np.ndarray):
            return vec3(self.x + v, self.y + v, self.z + v)
        
    def __sub__(self, v):
        if isinstance(v, vec3):
            return vec3(self.x - v.x, self.y - v.y, self.z - v.z)
        elif isinstance(v, numbers.Number) or isinstance(v, np.ndarray):
            return vec3(self.x - v, self.y - v, self.z - v)
    def __rsub__(self, v):
        if isinstance(v, vec3):
            return vec3(v.x - self.x, v.y - self.y ,  v.z - self.z)
        elif isinstance(v, numbers.Number) or isinstance(v, np.ndarray):
            return vec3(v  - self.x, v  - self.y ,  v - self.z)

    def __mul__(self, v):
        if isinstance(v, vec3):
            return vec3(self.x * v.x , self.y *  v.y , self.z * v.z )
        elif isinstance(v, numbers.Number) or isinstance(v, np.ndarray):
            return vec3(self.x * v, self.y * v, self.z * v) 
    def __rmul__(self, v):
        if isinstance(v, vec3):
            return vec3(v.x *self.x  , v.y * self.y, v.z * self.z )
        elif isinstance(v, numbers.Number) or isinstance(v, np.ndarray):
            return vec3(v *self.x  , v * self.y, v * self.z ) 
    
    def __truediv__(self, v):
        if isinstance(v, vec3):
            return vec3(self.x / v.x , self.y /  v.y , self.z / v.z )
        elif isinstance(v, numbers.Number) or isinstance(v, np.ndarray):
            return vec3(self.x / v, self.y / v, self.z / v)
    def __rtruediv__(self, v):
        if isinstance(v, vec3):
            return vec3(v.x / self.x, v.y / self.y, v.z / self.z)
        elif isinstance(v, numbers.Number) or isinstance(v, np.ndarray):
            return vec3(v / self.x, v / self.y, v / self.z)

    def __abs__(self):
        return vec3(np.abs(self.x), np.abs(self.y), np.abs(self.z))

def array_to_vec3(array):
    return vec3(array[0],array[1],array[2])