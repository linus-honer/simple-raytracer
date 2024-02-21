from PIL import Image
import numpy

width = 1920
height = 1080

def addSphere(position, radius, color):
    return dict(type='sphere', position=numpy.array(position), 
        radius=numpy.array(radius), color=numpy.array(color), reflection=.5)
    
def addPlane(position, normal):
    return dict(type='plane', position=numpy.array(position), 
        normal=numpy.array(normal),
        color=lambda M: (checkerColor1 
            if (int(M[0] * 2) % 2) == (int(M[2] * 2) % 2) else checkerColor2),
        diffuse_c=.75, specular_c=.5, reflection=.25)

checkerColor1 = numpy.ones(3)
checkerColor2 = 0
color_light = numpy.ones(3)

scene = [addSphere([0, 0, 1], .5, [1, 0, 0]),
         addPlane([0, -.5, 0], [0, 1, 0]),
    ]

lightPos = numpy.array([5., 5., -10.])

ambient = .05
diffuseC = 1.
specularC = 1.
specularK = 50

depth_max = 5  # maximum number of reflections
col = numpy.zeros(3)
camOrigin = numpy.array([0., 0.35, -1.])
camDir = numpy.array([0., 0., 0.])
img = numpy.zeros((h, w, 3))

ratio = float(width) / height
screenCoords = (-1, -1 / r + .25, 1, 1 / r + .25)