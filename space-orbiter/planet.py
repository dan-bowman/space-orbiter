import pygame
import math

# Gravitational constant
G = 6.673e-11


class Planet:
    def __init__(self, x, y, img_path, mass, radius,  atm_height, atm_press, influence_height):
        # Planet coordinates
        self.x = x
        self.y = y

        # Mass used for gravity equation
        self.mass = mass

        # Radius used for collision detection
        self.radius = radius

        # Atmosphere attributes to calculate drag
        self.atm_height = atm_height
        self.atm_press = atm_press

        # Height of sphere of influence
        self.inf = influence_height

        # String image path for sprite
        self.sprite = pygame.image.load(img_path)

    # Return a tuple with actual coordinates (top-left corner)
    def get_coord_tuple(self):
        return tuple([self.x, self.y])

    # Return a tuple with coordinates of center
    def get_center_tuple(self):
        # Radius is the hypotenuse: r**2 = x**2 + y**2; where x = y; --> r**2 = 2*x**2 --> x = sqrt((r**2) / 2)
        offset = int(math.sqrt((self.radius**2)))
        return tuple([self.x + offset, self.y + offset])

    # Blit sprite to screen
    def blit_sprite(self, screen):
        screen.blit(self.sprite, self.get_coord_tuple())

    # Get R vector tuple, the distance vector between the planet and the body; using center coords
    def get_r_vector(self, body):
        body_center = body.get_center_tuple()
        return tuple([self.get_center_tuple()[0] - body_center[0], self.get_center_tuple()[1] - body_center[1]])

    # Get R vector magnitude, the scalar distance between the planet and the body
    def get_r_mag(self, body):
        r_vector = self.get_r_vector(body)
        return math.sqrt(r_vector[0]**2 + r_vector[1]**2)

    # Get the unit vector which gives vector direction
    def get_dir(self, body):
        r_vector = self.get_r_vector(body)
        r_vector_mag = self.get_r_mag(body)
        return tuple([r_vector[0] / r_vector_mag, r_vector[1] / r_vector_mag])

    # Get acceleration vector
    def get_accel_vector(self, body):
        r_vector_mag = self.get_r_mag(body)
        r_vector_dir = self.get_dir(body)
        gravitation = (G * self.mass)
        return tuple([r_vector_dir[0] * gravitation / r_vector_mag**2, r_vector_dir[1] * gravitation / r_vector_mag**2])

    # Apply gravitational acceleration to body
    def attract_body(self, body):
        r_vector_mag = self.get_r_mag(body)
        accel_vector = self.get_accel_vector(body)

        # If body is within sphere of influence, add acceleration to body object
        if r_vector_mag < self.inf:
            body.add_dx(accel_vector[0])
            body.add_dy(accel_vector[1])

    # TODO: Implement atmospheric drag
