import pygame
import math

# Spawn location
spawn = tuple([25, 175])

# Wall bounce coefficient
bounce = -0.5

# Fuel efficiency (lower uses less fuel)
fuel_eff = 0.0012


class Ship:
    def __init__(self, img_path, width, height):
        # Initialize position and set velocity and acceleration to zero
        self.x = spawn[0]
        self.y = spawn[1]
        self.dx = 0
        self.dy = 0
        self.ddx = 0
        self.ddy = 0

        # Load image from img_path to create sprite
        self.sprite = pygame.image.load(img_path)

        # Width and Height for collision detection
        self.width = width
        self.height = height

        # Set initial fuel quantity and change in fuel (dfuel)
        self.fuel = 100.0
        self.dfuel = 0.0

        # Thrust vector used for differentiating between thrust acceleration and gravity acceleration
        self.thrust_x = 0.0
        self.thrust_y = 0.0

    # Return a tuple with actual coordinates (top-left corner)
    def get_coord_tuple(self):
        return tuple([self.x, self.y])

    # Return a tuple with coordinates of center
    def get_center_tuple(self):
        return tuple([self.x + self.width // 2, self.y + self.height // 2])

    # Blit sprite to screen
    def blit_sprite(self, screen):
        screen.blit(self.sprite, self.get_coord_tuple())

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
        self.dx += self.thrust_x
        self.dy += self.thrust_y

    # Update position
    def update_position(self):
        self.x += self.dx
        self.y += self.dy

    def get_vel_mag(self):
        return math.sqrt(self.dx**2 + self.dy**2)

    # Prograde acceleration
    def prograde(self, accel_mag, vel_dir):
        self.thrust_x = accel_mag * vel_dir[0]
        self.thrust_y = accel_mag * vel_dir[1]
        self.use_fuel(fuel_eff)

    # Retrograde acceleration
    def retrograde(self, accel_mag, vel_dir):
        self.thrust_x = accel_mag * vel_dir[0] * -1
        self.thrust_y = accel_mag * vel_dir[1] * -1
        self.use_fuel(fuel_eff)

    # Add thrust to x
    def add_thrust_x(self, accel_mag):
        self.thrust_x = accel_mag
        self.use_fuel(fuel_eff)

    # Add thrust to y
    def add_thrust_y(self, accel_mag):
        self.thrust_y = accel_mag
        self.use_fuel(fuel_eff)

    # Start depleting fuel
    def use_fuel(self, eff):
        self.dfuel = eff

    # Update fuel value, set dfuel to zero if there is zero thrust
    def update_fuel(self):
        if self.thrust_x == 0.0 and self.thrust_y == 0.0:
            self.dfuel = 0.0
        self.fuel -= self.dfuel

    # Check to see if there is fuel to use
    def check_fuel(self):
        if self.fuel <= 0.0:
            self.fuel = 0.0
            self.add_thrust_x(0.0)
            self.add_thrust_x(0.0)
        else:
            self.update_fuel()

    # Set collision with planet, reset ship position and velocity if collides
    def set_planet_collision(self, planet, offset):
        if planet.get_r_mag(self) <= offset * planet.radius:
            self.x = spawn[0]
            self.y = spawn[1]
            self.dx = 0
            self.dy = 0
            self.ddx = 0
            self.ddy = 0

    # Set bounce off screen boundaries using bounce coefficient
    def set_wall_collision(self, screen_size):
        if (self.x <= 0 and self.dx < 0) or (self.x >= (screen_size[0] - self.width) and self.dx > 0):
            self.dx = self.dx * bounce
        if (self.y <= 0 and self.dy < 0) or (self.y >= (screen_size[1] - self.height) and self.dy > 0):
            self.dy = self.dy * bounce
