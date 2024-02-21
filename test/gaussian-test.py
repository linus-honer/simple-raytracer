import Image
import numpy
import time
import numbers

class vec3():
    def __init__(self, x, y, z):
        (self.x, self.y, self.z) = (x, y, z)
    def __mul__(self, other):
        return vec3(self.x * other, self.y * other, self.z * other)
    def __add__(self, other):
        return vec3(self.x + other.x, self.y + other.y, self.z + other.z)
    def __sub__(self, other):
        return vec3(self.x - other.x, self.y - other.y, self.z - other.z)
    def dot(self, other):
        return (self.x * other.x) + (self.y * other.y) + (self.z * other.z)
    def __abs__(self):
        return self.dot(self)
    def norm(self):
        mag = numpy.sqrt(abs(self))
        return self * (1.0 / numpy.where(mag == 0, 1, mag))
    def components(self):
        return (self.x, self.y, self.z)
rgb = vec3

(width, height) = (512, 512)
x = numpy.tile(numpy.linspace(-1, 1, width), height)
y = numpy.repeat(numpy.linspace(-1, 1, height), width)

if 0:
    c = numpy.sqrt(.5)
    print 'c', c
    def norm(v):
        # v -= min(v)
        v /= max(v)
        return v
    gx = norm(numpy.exp(-(x*x) / (2 * c ** 2)))
    gy = norm(numpy.exp(-(y*y) / (2 * c ** 2)))
    g = gx * gy
else:
    g = ((x*x) + (y*y))
    if 1:
        g = g / 2
    else:
        g = numpy.sqrt(g) / 1.4
    g = 1 - g
print min(g), max(g)
print g[256]