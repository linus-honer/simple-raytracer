from .utils.vector3 import vec3, extract, rgb
import numpy as np
from functools import reduce as reduce

class Ray:
    def __init__(self, origin, dir, depth, n, reflections, transmissions, diffuse_reflections):

        self.origin  = origin
        self.dir = dir
        self.depth = depth
        self.n = n

        self.reflections = reflections
        self.transmissions = transmissions
        self.diffuse_reflections = diffuse_reflections
    
    def extract(self,hit_check):
        return Ray(self.origin.extract(hit_check), self.dir.extract(hit_check), self.depth,  self.n.extract(hit_check), self.reflections, self.transmissions,self.diffuse_reflections)