import math

from body import Body

# Gravitational constant
G = 6.673e-11


class Gravitative(Body):
    def __init__(self, spawn, img_path, size, mass, influence_height):
        super().__init__(spawn, img_path, size)
        self.mass = mass
        self.inf = influence_height

    # Get R vector tuple, the distance vector between the planet and the body; using center coords
    def get_r_vector(self, body):
        body_center = body.get_center()
        return tuple([self.get_center()[0] - body_center[0], self.get_center()[1] - body_center[1]])

    # Get R vector magnitude, the scalar distance between the planet and the body
    def get_r_mag(self, body):
        r_vector = self.get_r_vector(body)
        return math.sqrt(r_vector[0] ** 2 + r_vector[1] ** 2)

    # Get the unit vector which gives vector direction
    def get_dir(self, body):
        r_vector = self.get_r_vector(body)
        r_vector_mag = self.get_r_mag(body)
        return tuple([r_vector[0] / r_vector_mag, r_vector[1] / r_vector_mag])

    # Get acceleration vector
    def get_accel_vector(self, body):
        r_vector_dir = self.get_dir(body)
        gravitation = (G * self.mass)
        return tuple([r_vector_dir[0] * gravitation / self.get_r_mag(body) ** 2,
                      r_vector_dir[1] * gravitation / self.get_r_mag(body) ** 2])

    # Find the distance of self from a point in space
    def get_distance_from_point(self, point):
        dist_vector = tuple([self.get_center()[0] - point[0], self.get_center()[1] - point[1]])
        return math.sqrt(dist_vector[0] ** 2 + dist_vector[1] ** 2)

    # Apply gravitational acceleration to body
    def attract_body(self, body):
        r_vector_mag = self.get_r_mag(body)
        accel_vector = self.get_accel_vector(body)

        # If body is within sphere of influence, add the acceleration to body object
        if r_vector_mag < self.inf:
            body.add_dx(accel_vector[0])
            body.add_dy(accel_vector[1])
