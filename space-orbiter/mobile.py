import math


class Mobile:
    def __init__(self, dx, dy):
        # Initialize velocity based on arguments, acceleration to zero
        self.dx = dx
        self.dy = dy
        self.ddx = 0
        self.ddy = 0

    # Add horizontal velocity
    def add_dx(self, ddx):
        self.dx += ddx

    # Add vertical velocity
    def add_dy(self, ddy):
        self.dy += ddy

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
        # self.dx += self.thrust_x
        # self.dy += self.thrust_y

    # Update position
    def update_position(self):
        pass
        # May have to make this class a child of Body, and instantiate x and y through this class to the Body class
        # self.x += self.dx
        # self.y += self.dy
        # Another option is to make this one an abstract method

    def get_vel_mag(self):
        return math.sqrt(self.dx ** 2 + self.dy ** 2)
