from geometryObjects import Ray, Vec3
from random import random
from abc import ABC, abstractmethod

class Material(ABC): 
    def __init__(self, albedo: Vec3):
        self.albedo = albedo
        super().__init__()

    @staticmethod
    def random_in_unit_sphere() -> Vec3:
        p = Vec3(random(), random(), random()) * 2.0 - Vec3(1,1,1)

        while p.length()**2 >= 1:
            p = Vec3(random(), random(), random()) * 2.0 - Vec3(1,1,1)
        
        return p

        
    @staticmethod
    def reflect(v: Vec3, n: Vec3):
        return v - n * 2 * Vec3.dot(v,n)

    @abstractmethod
    def scatter(self, r_in: Ray, hitPoint: Vec3, hitNormal: Vec3, \
                attenuation: Vec3, scattered: Ray) -> bool:
        pass

class Lambertian(Material):
    def __init__(self, albedo: Vec3):
        super().__init__(albedo)

    def scatter(self, r_in: Ray, hitPoint: Vec3, hitNormal: Vec3, \
        attenuation: Vec3, scattered: Ray):
        target = hitPoint + hitNormal + super().random_in_unit_sphere()
        scattered.set(Ray(hitPoint, target - hitPoint))
        attenuation.set(self.albedo)
        return True

class Specular(Material):
    def __init__(self, albedo: Vec3, fuzz: float = 0.0):
        super().__init__(albedo)
        self.fuzz = fuzz if fuzz in range(0,1) else 1.0

    def scatter(self, r_in: Ray, hitPoint: Vec3, hitNormal: Vec3, \
        attenuation: Vec3, scattered: Ray):
        reflected = super().reflect(r_in.direction.unit(), hitNormal)
        scattered.set(Ray(hitPoint, reflected + super().random_in_unit_sphere() * self.fuzz))
        attenuation.set(self.albedo)
        return Vec3.dot(scattered.direction, hitNormal) > 0

class Dielectric(Material):
    def __init__(self, reflective_index: float):
        self.reflective_index = reflective_index

    # calculate refracted ray using Snell's law
    @staticmethod
    def refract(v: Vec3, n: Vec3, ni_over_nt: float, refracted: Vec3) -> bool:
        uv = v.unit()
        dt = Vec3.dot(uv, n)
        discriminant = 1 - ni_over_nt * ni_over_nt * (1 - dt * dt)
        if discriminant > 0:
            refracted.set((uv - n * dt) * ni_over_nt - n * (discriminant**0.5))
            return True
        else:
            return False

    # Schlick's approximation for Fresnel factor
    @staticmethod
    def schlick(cosine: float, reflective_index: float) -> float:
        r0 = (1 - reflective_index) / (1 + reflective_index)
        r0 *= r0
        return r0 + (1-r0) * (1-cosine)**5

    def scatter(self, r_in: Ray, hitPoint: Vec3, hitNormal: Vec3, \
                attenuation: Vec3, scattered: Ray):
        reflected = super().reflect(r_in.direction, hitNormal)
        attenuation.set(Vec3(1,1,1))
        if Vec3.dot(r_in.direction, hitNormal) > 0:
            outward_normal = hitNormal * -1
            ni_over_nt = self.reflective_index
            cosine = self.reflective_index * Vec3.dot(r_in.direction, hitNormal) / r_in.direction.length()
        else:
            outward_normal = hitNormal
            ni_over_nt = 1 / self.reflective_index
            cosine = -1 * Vec3.dot(r_in.direction, hitNormal) / r_in.direction.length()
        
        refracted = Vec3(0,0,0)
        if self.refract(r_in.direction, outward_normal, ni_over_nt, refracted):
            reflect_prob = self.schlick(cosine, self.reflective_index)
        else:
            reflect_prob = 1.0
        
        if random() < reflect_prob:
            scattered.set(Ray(hitPoint, reflected))
        else:
            scattered.set(Ray(hitPoint, refracted))
        
        return True