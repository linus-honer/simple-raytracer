from PIL import Image
import numpy

width = 1920
height = 1080

def normalize(x):
    x /= numpy.linalg.norm(x)
    return x

def getNormal(obj, M):
    if obj['type'] == 'sphere':
        N = normalize(M - obj['position'])
    elif obj['type'] == 'plane':
        N = obj['normal']
    return N
    
def getColor(obj, M):
    color = obj['color']
    if not hasattr(color, '__len__'):
        color = color(M)
    return color

def intersectPlane(RayOrigin, RayDir, PlanePos, PlaneNorm):
    denom = numpy.dot(RayDir, PlaneNorm)
    if numpy.abs(denom) < 1e-6:
        return numpy.inf
    d = numpy.dot(PlanePos - RayOrigin, PlaneNorm) / denom
    if d < 0:
        return numpy.inf
    return d

def intersectSphere(RayOrigin, RayDir, SpherePos, SphereRadius):
    a = numpy.dot(RayDir, RayDir)
    dist = RayOrigin - SpherePos
    b = 2 * numpy.dot(RayDir, dist)
    c = numpy.dot(dist, dist) - SphereRadius * SphereRadius
    disc = b * b - 4 * a * c
    if disc > 0:
        distSqrt = numpy.sqrt(disc)
        q = (-b - distSqrt) / 2.0 if b < 0 else (-b + distSqrt) / 2.0
        t0 = q / a
        t1 = c / q
        t0, t1 = min(t0, t1), max(t0, t1)
        if t1 >= 0:
            return t1 if t0 < 0 else t0
    return numpy.inf

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
img = numpy.zeros((height, width, 3))

ratio = float(width) / height
screenCoords = (-1, -1 / ratio + .25, 1, 1 / ratio + .25)