from geometryObjects import Vec3, Ray
from math import pi, tan

class Camera:
    # FOV is defined in degrees for intuitive use, but converted to radians for maths
    # Using a fixed vertical FOV allows the horizontal FOV to expand nicely depending on the width of the image
    def __init__(self, look_from: Vec3, look_at: Vec3, up: Vec3, vert_FOV: float, aspect_ratio: float):
        theta = vert_FOV * pi / 180
        half_height = tan(theta/2)
        half_width = aspect_ratio * half_height

        w = (look_from - look_at).unit()
        u = Vec3.cross(up, w).unit()
        v = Vec3.cross(w,u)

        self.eye = look_from
        self.lower_left = self.eye - u * half_width - v * half_height - w
        self.horizontal = u * 2 * half_width
        self.vertical = v * 2 * half_height
        
    def get_ray(self, a, t):
        return Ray(self.eye, self.lower_left + self.horizontal * a + self.vertical * t - self.eye)