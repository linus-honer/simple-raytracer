import numpy as np
from functools import reduce as reduce

from .utils.constants import *
from .utils.vector3 import vec3, extract, rgb

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
    
def get_raycolor(ray, scene):
    inters = [s.intersect(ray.origin, ray.dir) for s in scene.collider_list]
    distances, hit_orientation = zip(*inters)

    nearest = reduce(np.minimum, distances)
    color = rgb(0., 0., 0.)
    
    for (coll, dis , orient) in zip(scene.collider_list, distances, hit_orientation):
        hit_check = (nearest != FARAWAY) & (dis == nearest)

        if np.any(hit_check):
            material = coll.assigned_primitive.material
            hit_info = Hit(extract(hit_check,dis) , extract(hit_check,orient), material, coll, coll.assigned_primitive)
            
            cc = material.get_color(scene,  ray.extract(hit_check), hit_info)
            color += cc.place(hit_check)

    return color

def get_distances(ray, scene):
    inters = [s.intersect(ray.origin, ray.dir) for s in scene.collider_list]
    distances, hit_orientation = zip(*inters)

    nearest = reduce(np.minimum, distances)
    
    max_r_distance = 10
    r_distance = np.where(nearest <= max_r_distance, nearest, max_r_distance)
    norm_r_distance = r_distance/max_r_distance
    return rgb(norm_r_distance, norm_r_distance, norm_r_distance)