from geometryObjects import Ray
from geometryObjects import Vec3
from abc import ABC, abstractmethod
from materials import Material

class HitRecord:
    def __init__(self, t: float, p: Vec3, normal: Vec3):
        self.t = t
        self.hitPoint = p
        self.normal = normal

    def set(self, other):
        self.t = other.t
        self.hitPoint = other.hitPoint
        self.normal = other.normal
        self.material = other.material

    def __repr__(self):
        pass

    def __str__(self):
        return f"t = {self.t}, p = {self.hitPoint}, normal = {self.normal}"

class Hitable(ABC):
    @abstractmethod
    def hit(self, r: Ray, t_min: float, t_max: float, rec: HitRecord) -> bool:
        pass

class Sphere(Hitable):
    def __init__(self, center: Vec3, radius: float, material: Material):
        self.center = center
        self.radius = radius
        self.material = material
    
    def hit(self, r: Ray, t_min: float, t_max: float, rec: HitRecord):
        oc = r.origin - self.center
        a = Vec3.dot(r.direction, r.direction)
        b = Vec3.dot(oc, r.direction)
        c = Vec3.dot(oc, oc) - (self.radius)*(self.radius)
        discriminant = b*b - a*c
        if discriminant > 0:
            temp = (-b - discriminant**(0.5))/a
            if temp < t_max and temp > t_min:
                rec.t = temp
                rec.hitPoint.set(r.point_at_param(rec.t))
                rec.normal.set((rec.hitPoint - self.center) / self.radius)
                rec.material = self.material
                return True
            
            temp = (-b + discriminant**(0.5))/a 
            if temp < t_max and temp > t_min:
                rec.t = temp
                rec.hitPoint.set(r.point_at_param(rec.t))
                rec.normal.set((rec.hitPoint - self.center) / self.radius)
                rec.material = self.material
                return True
                
        else:
            return False

class HitableList(Hitable):
    def __init__(self, l: [Hitable]):
        self.hit_list = l

    def hit(self, r: Ray, t_min: float, t_max: float, rec: HitRecord):
        hit_anything = False
        closest_so_far = t_max

        temp_rec = HitRecord(0,Vec3(0,0,0),Vec3(0,0,1))

        for item in self.hit_list:
            if item.hit(r, t_min, closest_so_far, temp_rec):
                hit_anything = True
                closest_so_far = temp_rec.t
                rec.set(temp_rec)
        return hit_anything