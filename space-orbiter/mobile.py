import math

from gravitative import Gravitative


class Mobile(Gravitative):
    def __init__(self, spawn, img_path, size, mass, influence_height, vel_vector):
        super().__init__(spawn, img_path, size, mass, influence_height)

        # Initialize velocity based on arguments, acceleration to zero
        self.dx = vel_vector[0]
        self.dy = vel_vector[1]
        self.ddx = 0
        self.ddy = 0

    # Add horizontal velocity
    def add_dx(self, ddx):
        self.dx += ddx

    # Add vertical velocity
    def add_dy(self, ddy):
        self.dy += ddy

    # Stop horizontal velocity
    def stop_dx(self):
        self.dx = 0.0

    # Stop vertical velocity
    def stop_dy(self):
        self.dy = 0.0

    # Stop horizontal acceleration
    def stop_ddx(self):
        self.ddx = 0

    # Stop vertical acceleration
    def stop_ddy(self):
        self.ddy = 0

    # Update velocity
    def update_velocity(self):
        self.dx += self.ddx
        self.dy += self.ddy
        # Implement these in the subclass, extending this function
        # super().update_velocity()
        # self.dx += self.thrust_x
        # self.dy += self.thrust_y

    # Update position
    def update_position(self):
        self.x += self.dx
        self.y += self.dy

    # Return the speed (velocity magnitude)
    def get_vel_mag(self):
        return math.sqrt(self.dx ** 2 + self.dy ** 2)
