from PIL import Image
from geometryObjects import Vec3, Ray
from hitable import HitRecord, Hitable, HitableList, Sphere
from materials import Lambertian, Specular, Dielectric
from camera import Camera
from random import seed, random
from functools import reduce
from time import time, gmtime, strftime
from math import cos, pi
import numpy as np

MAX_RAY_LENGTH = 1_000_000.0
RES_WIDTH = 200
RES_HEIGHT = 100
LERP_SAMPLE_DENSITY = 100

# called to determine color of pixel hit by lerp
def color(r: Ray, world: Hitable, depth: int) -> Vec3:
    rec = HitRecord(0,Vec3(0,0,0),Vec3(0,0,1))

    if world.hit(r, 0.001, MAX_RAY_LENGTH, rec):
        attenuation = Vec3(0,0,0)
        scattered = Ray(Vec3(0,0,0), Vec3(1,0,0))
        if depth < 50 and \
            rec.material.scatter(r, rec.hitPoint, rec.normal, attenuation, scattered):
            return attenuation * color(scattered, world, depth + 1)
        else:
            return Vec3(0,0,0)
        
    else:
        unit_direction = r.direction.unit()
        t = 0.5 * (unit_direction.y + 1)
        return Vec3(1.0,1.0,1.0) * (1.0 - t) + Vec3(0.5,0.7,1.0) * t

# linear interpolation
def lerp(pixels, cam, world):

    for x in range(RES_WIDTH):
        for y in range(RES_HEIGHT):
            col = Vec3(0.0, 0.0, 0.0)

            for _ in range(LERP_SAMPLE_DENSITY):
                u = float(x + random())/RES_WIDTH
                v = float(y + random())/RES_HEIGHT

                r = cam.get_ray(u,v)
                # p = r.point_at_param(2.0)
                col = col + color(r, world, 0)
            
            col = col / LERP_SAMPLE_DENSITY
            col = Vec3(col.x**0.5, col.y**0.5, col.z**0.5)
            ir = min(255,int(255.99*col.x))
            ig = min(255,int(255.99*col.y))
            ib = min(255,int(255.99*col.z))
            pixels[x,99-y] = (ir,ig,ib)

if __name__ == '__main__':

    cam = Camera(Vec3(-2,2,1), Vec3(0,0,-1), Vec3(0,1,0), 90, RES_WIDTH/RES_HEIGHT)
    hit_list = []
    hit_list.append(Sphere(Vec3(0,0,-1), 0.5, Lambertian(Vec3(0.1, 0.2, 0.5))))
    hit_list.append(Sphere(Vec3(0,-100.5,-1), 100, Lambertian(Vec3(0.8, 0.8, 0))))
    hit_list.append(Sphere(Vec3(1,0,-1), 0.5, Specular(Vec3(0.8, 0.6, 0.2))))
    hit_list.append(Sphere(Vec3(-1,0,-1), 0.5, Dielectric(1.5)))
    hit_list.append(Sphere(Vec3(-1,0,-1), -0.45, Dielectric(1.5)))
    world = HitableList(hit_list)

    seed()

    # S is the screen coordinates (x0, y0, x1, y1)
    # np.linspace(start, stop, num) produces num evenly spaced samples over [start, stop]
    # np.tile(A, reps) constructs an array by repeating A, reps amount of times
    # np.repeat(a, repeats) repeats a, repeats amount of times

    # S = (-1, RES_HEIGHT/RES_WIDTH + .25, 1, -RES_HEIGHT/RES_WIDTH + .25)
    # x = np.tile(np.linspace(S[0], S[2], RES_WIDTH), RES_HEIGHT)
    # y = np.repeat(np.linspace(S[1], S[3], RES_HEIGHT), RES_WIDTH)
    
    start = time()

    # r = Ray(Vec3(0,0,0), cam.lower_left + cam.width.data * x + cam.height.data * y)

    # col = color(r, world, 0)
    # col = col / LERP_SAMPLE_DENSITY
    # reduce(lambda a : a**0.5, col.data)

    # rgb = [Image.fromarray(255 * np.clip(c, 0, 1).reshape((RES_HEIGHT, RES_WIDTH)).astype(np.uint8), "L") for c in col.data]
    # Image.merge("RGB", rgb).save("testOut.jpg")

    im = Image.new('RGB', (RES_WIDTH, RES_HEIGHT))
    pixels = im.load()

    lerp(pixels, cam, world)

    end = time()

    timeSpent = end-start
    print(strftime("%H:%M:%S", gmtime(timeSpent)))

    im.save("testOut.jpg")