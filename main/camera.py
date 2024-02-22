import numpy as np
from .ray import Ray

from .utils.vector3 import vec3, rgb
from .utils.random import random_in_unit_disk

class Camera():
    def __init__(self, look_from, look_at, screen_width = 400 ,screen_height = 300,  field_of_view = 90., aperture = 0., focal_distance = 1.):
        self.screenWidth = screen_width
        self.screenHeight = screen_height
        self.aspectRatio = float(screen_width) / screen_height

        self.lookFrom = look_from
        self.lookAt = look_at
        self.cameraWidth = np.tan(field_of_view * np.pi/180   /2.)*2.
        self.cameraHeight = self.camera_width/self.aspect_ratio

        self.cameraFwd = (look_at - look_from).normalize()
        self.cameraRight = (self.cameraFwd.cross(vec3(0.,1.,0.))).normalize()
        self.cameraUp = self.cameraRight.cross(self.cameraFwd)

        self.lensRadius =  aperture / 2.
        self.focalDistance = focal_distance

        self.x = np.linspace(-self.camera_width/2., self.camera_width/2., self.screen_width)
        self.y = np.linspace(self.camera_height/2., -self.camera_height/2., self.screen_height)

        xx,yy = np.meshgrid(self.x,self.y)
        self.x = xx.flatten()
        self.y = yy.flatten()
    
    def getRay(self,n):

        x = self.x + (np.random.rand(len(self.x )) - 0.5)*self.camera_width  /(self.screen_width)
        y = self.y + (np.random.rand(len(self.y )) - 0.5)*self.camera_height /(self.screen_height)

        rx, ry = randomInUnitDisk(x.shape[0])
        ray_origin = self.look_from  +   self.cameraRight *rx* self.lens_radius   +   self.cameraUp *ry* self.lens_radius
        ray_dir = (self.look_from  +   self.cameraUp*y*self.focal_distance  +  self.cameraRight*x*self.focal_distance  + self.cameraFwd*self.focal_distance - ray_origin  ).normalize()
        return Ray(origin=ray_origin, dir=ray_dir, depth=0,  n=n, reflections = 0, transmissions = 0, diffuse_reflections = 0)
