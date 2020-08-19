from geometryObjects import Vec3, Ray
from random import random
from math import pi, tan

class Camera:

    # define an offset vector from look_from in order to simulate defocus blur, or depth of field
    @staticmethod
    def random_in_unit_disk():
        while True:
            p = Vec3(random(), random(), 0) * 2.0 -  Vec3(1,1,0)
            if Vec3.dot(p,p) >= 1.0:
                break
        return p

    # FOV is defined in degrees for intuitive use, but converted to radians for maths
    # Using a fixed vertical FOV allows the horizontal FOV to expand nicely depending on the width of the image
    def __init__(self, look_from: Vec3, look_at: Vec3, up: Vec3, \
                vert_FOV: float, aspect_ratio: float, \
                aperture: float, focal_dist: float):
        self.lens_radius = aperture/2
        theta = vert_FOV * pi / 180
        half_height = tan(theta/2)
        half_width = aspect_ratio * half_height

        self.w = (look_from - look_at).unit()
        self.u = Vec3.cross(up, self.w).unit()
        self.v = Vec3.cross(self.w, self.u)

        self.eye = look_from
        self.lower_left = self.eye - self.u * half_width * focal_dist - self.v * half_height * focal_dist - self.w * focal_dist
        self.horizontal = self.u * 2 * half_width * focal_dist
        self.vertical = self.v * 2 * half_height * focal_dist
        
    def get_ray(self, s, t):
        rd = self.random_in_unit_disk() * self.lens_radius
        offset = self.u * rd.x + self.v * rd.y
        # return Ray(self.eye + offset, self.lower_left + self.horizontal * s + self.vertical * t - self.eye - offset)
        return Ray(self.eye, self.lower_left + self.horizontal * s + self.vertical * t - self.eye)