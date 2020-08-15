import numpy as np
import numbers

def extract(cond, x):
    if isinstance(x, numbers.Number):
        return x
    else:
        return np.extract(cond, x)


class Vec3:
    def __init__(self, x, y, z):
        (self.x, self.y, self.z) = (x,y,z)

    def r(self):
        return self.x
    def g(self):
        return self.y
    def b(self):
        return self.z

    def __add__(self, other):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        if isinstance(other, Vec3):
            return Vec3(self.x * other.x, self.y * other.y, self.z * other.z)
        elif isinstance(other, float) or isinstance(other, int):
            return Vec3(self.x * other, self.y * other, self.z * other)
        else:
            raise TypeError

    def __truediv__(self, other):
        if isinstance(other, Vec3):
            return Vec3(self.x / other.x, self.y / other.y, self.z / other.z)
        elif isinstance(other, float) or isinstance(other, int):
            return Vec3(self.x / other, self.y / other, self.z / other)
        else:
            raise TypeError

    @staticmethod
    def dot(a, b):
        return (a.x * b.x) + (a.y * b.y) + (a.z * b.z)

    @staticmethod
    def cross(a, b):
        aData = np.array([a.x, a.y, a.z])
        bData = np.array([b.x, b.y, b.z])
        x,y,z = np.cross(aData, bData)
        return Vec3(x,y,z)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        self.z += other.z

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z

    def __imul__(self, other):
        if isinstance(other, Vec3):
            self.x *= other.x
            self.y *= other.y
            self.z *= other.z
        elif isinstance(other, float) or isinstance(other, int):
            self.x *= other
            self.y *= other
            self.z *= other
        else:
            raise TypeError

    def __itruediv__(self, other):
        if isinstance(other, Vec3):
            self.x /= other.x
            self.y /= other.y
            self.z /= other.z
        elif isinstance(other, float) or isinstance(other, int):
            self.x /= other
            self.y /= other
            self.z /= other
        else:
            raise TypeError

    def length(self):
        return np.sqrt(self.dot(self, self))

    def normalize(self):
        if self.length() == 0:
            return
        else:
            self /= float(self.length())

    def unit(self):
        mag = self.length()
        if mag == 0:
            return self
        else:
            return self / mag

    def set(self, other):
        self.x, self.y, self.z = other.x, other.y, other.z

    def extract(self, cond):
        return Vec3(extract(cond, self.x), extract(cond, self.y), extract(cond, self.z))

    def place(self, cond):
        r = Vec3(np.zeros(cond.shape), np.zeros(cond.shape), np.zeros(cond.shape))
        np.place(r.x, cond, self.x)
        np.place(r.y, cond, self.y)
        np.place(r.z, cond, self.z)
        return r

    def __repr__(self):
        return f"Vec3({self.x()}, {self.y()}, {self.z()}"

    def __str__(self):
        return f"<{self.x()}, {self.y()}, {self.z()}>"

class Ray:
    def __init__(self, origin: Vec3, direction: Vec3):
        self.origin = origin
        self.direction = direction
        self.direction.normalize()

    def point_at_param(self, t: [float, int]):
        return self.origin + self.direction * t

    def set(self, other):
        self.origin.set(other.origin)
        self.direction.set(other.direction)

    def __repr__(self):
        return f"Ray({self.origin},{self.direction})"

    def __str__(self):
        return f"Origin: {self.origin}\nDirection: {self.direction}"