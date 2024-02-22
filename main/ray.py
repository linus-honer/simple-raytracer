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

class Hit:
    def __init__(self, distance, orientation, material, collider,surface):
        self.distance = distance
        self.orientation = orientation 
        self.material = material
        self.collider = collider
        self.surface = surface
        self.u = None
        self.v = None
        self.N = None
        self.point = None 

    def get_uv(self):
        if self.u is None:
            self.u, self.v = self.collider.assigned_primitive.get_uv(self)
        return self.u, self.v

    def get_normal(self):
        if self.N is None:
            self.N = self.collider.get_N(self)
        return self.N