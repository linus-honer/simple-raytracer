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
colorLight = numpy.ones(3)

scene = [addSphere([0, 0, 1], .5, [1, 0, 0]),
         addPlane([0, -.5, 0], [0, 1, 0]),
    ]

lightPos = numpy.array([5, 5, -10])

ambient = .05
diffuseC = 1
specularC = 1
specularK = 50

depthMax = 5  # maximum number of reflections
col = numpy.zeros(3)
camOrigin = numpy.array([0, 0.35, -1])
camDir = numpy.array([0, 0, 0])

ratio = float(width) / height
screenCoords = (-1, -1 / ratio + .25, 1, 1 / ratio + .25)

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

def intersect(RayOrigin, RayDirection, obj):
    if obj['type'] == 'plane':
        return intersectPlane(RayOrigin, RayDirection, obj['position'], obj['normal'])
    elif obj['type'] == 'sphere':
        return intersectSphere(RayOrigin, RayDirection, obj['position'], obj['radius'])
    
def traceRay(rayOrigin, rayDir):
    t = numpy.inf
    for i, obj in enumerate(scene):
        tObj = intersect(rayOrigin, rayDir, obj)
        if tObj < t:
            t, objIdk = tObj, i
    
    if t == numpy.inf:
        return
    
    obj = scene[objIdk]

    M = rayOrigin + rayDir * t

    N = getNormal(obj, M)
    color = getColor(obj, M)
    toL = normalize(lightPos - M)
    toO = normalize(camOrigin - M)

    l = [intersect(M + N * .0001, toL, objSh) 
            for k, objSh in enumerate(scene) if k != objIdk]
    if l and min(l) < numpy.inf:
        return
    
    colRay = ambient

    colRay += obj.get('diffuse_c', diffuseC) * max(numpy.dot(N, toL), 0) * color
    # blinn-phong shade
    colRay += obj.get('specular_c', specularC) * max(numpy.dot(N, normalize(toL + toO)), 0) ** specularK * colorLight
    return obj, M, N, colRay

img = numpy.zeros((height, width, 3))

for i, x in enumerate(numpy.linspace(screenCoords[0], screenCoords[2], width)):
    if i % 10 == 0:
        print(i / float(width) * 100, "%")
    for j, y in enumerate(numpy.linspace(screenCoords[1], screenCoords[3], height)):
        col[:] = 0
        camDir[:2] = (x, y)
        D = normalize(camDir - camOrigin)
        depth = 0
        rayOrigin, rayDir = camOrigin, D
        reflection = 1.
        # Loop through initial and secondary rays.
        while depth < depthMax:
            traced = traceRay(rayOrigin, rayDir)
            if not traced:
                break
            obj, M, N, col_ray = traced
            # Reflection: create a new ray.
            rayOrigin, rayDir = M + N * .0001, normalize(rayDir - 2 * numpy.dot(rayDir, N) * N)
            depth += 1
            col += reflection * col_ray
            reflection *= obj.get('reflection', 1.)
        img[height - j - 1, i, :] = numpy.clip(col, 0, 1)

im = Image.fromarray((255 * img).astype(numpy.uint8), "RGB")
im.save("output.png")