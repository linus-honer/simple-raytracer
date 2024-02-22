from PIL import Image
import numpy as np
import time

from .utils import colourTransform as cf
from .camera import Camera
from .utils.vector3 import vec3

class Scene():
     def __init__(self, ambient_color = rgb(0.01, 0.01, 0.01), n = vec3(1.0,1.0,1.0)) :
        self.scene_primitives = []
        self.collider_list = []
        self.shadowed_collider_list = []
        self.Light_list = []
        self.importance_sampled_list = []
        self.ambient_color = ambient_color
        self.n = n
        self.importance_sampled_list = []