import pygame

from mobile import Mobile
from keybinds import ACCEL_FINE

# Wall bounce coefficient
bounce = -0.5

# Fuel efficiency (lower uses less fuel)
fuel_eff = 0.0012

# Thrust sprites
reg_thrust_plume = pygame.image.load("assets/img/plume.png")
hot_thrust_plume = pygame.image.load("assets/img/hot_plume.png")
rcs_thrust_plume = pygame.image.load("assets/img/rcs.png")


class Ship(Mobile):
    def __init__(self, spawn, img_path, size):
        # Ship gravity interactions are negligible, initialize them to an arbitrary non-zero negligible number
        mass = 1
        influence_height = 1
        # Initial velocity of ship is zero
        vel_vector = (0.0, 0.0)
        super().__init__(spawn, img_path, size, mass, influence_height, vel_vector)

        # Save initial spawn location for respawning
        self.respawn_coords = spawn

        # Set initial fuel quantity and change in fuel (dfuel)
        self.fuel = 100.0
        self.dfuel = 0.0

        # Thrust vector used for differentiating between thrust acceleration and gravity acceleration
        self.thrust_x = 0.0
        self.thrust_y = 0.0

        # Drag vector used for atmospheric drag
        self.drag_x = 0.0
        self.drag_y = 0.0

        # Initialize dynamic-size list of points that draw the trailing line behind the ship
        self.trail_points = [spawn]
        # Ship trail resolution units (pixels)
        self.trail_res = 15
        # Ship trail length (number of vertices)
        self.trail_len = 75

        # Initialize ship orientation, for animation
        self.orientation = 'right'

    # Respawn the ship to the original spawn position
    def respawn(self):
        self.x = self.respawn_coords[0]
        self.y = self.respawn_coords[1]
        self.trail_points = [self.respawn_coords]
        self.orbit_point_radii = []

    # Update velocity override to add thrust
    def update_velocity(self):
        super().update_velocity()
        self.dx += self.thrust_x
        self.dy += self.thrust_y
        self.dx += self.drag_x
        self.dy += self.drag_y

    def get_orbit_radii(self, body):
        return [body.get_distance_from_point(point) for point in self.trail_points]

    def get_periapsis(self, body):
        return min(self.get_orbit_radii(body))

    def get_apoapsis(self, body):
        return max(self.get_orbit_radii(body))

    def get_eccentricity(self, body):
        return 1 - (2 / ((self.get_apoapsis(body) / self.get_periapsis(body)) + 1))

    def drag(self, accel_mag, vel_dir):
        self.drag_x = accel_mag * vel_dir[0] * -1
        self.drag_y = accel_mag * vel_dir[1] * -1

    # Prograde thrust acceleration (accelerate in direction of velocity, using fuel)
    def prograde(self, accel_mag, vel_dir):
        self.thrust_x = accel_mag * vel_dir[0]
        self.thrust_y = accel_mag * vel_dir[1]
        self.use_fuel(fuel_eff)

    # Retrograde thrust acceleration (accelerate in opposite direction of velocity, using fuel)
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
    def set_body_collision(self, body, offset):
        if body.get_r_mag(self) <= offset * body.get_radius():
            self.respawn()
            self.stop_dx()
            self.stop_dy()
            self.stop_ddx()
            self.stop_ddy()

    # Set bounce off screen boundaries using bounce coefficient
    def set_wall_collision(self, screen_size):
        if (self.x <= 0 and self.dx < 0) or (self.x >= (screen_size[0] - self.width) and self.dx > 0):
            self.dx = self.dx * bounce
        if (self.y <= 0 and self.dy < 0) or (self.y >= (screen_size[1] - self.height) and self.dy > 0):
            self.dy = self.dy * bounce

    # Override the blit_sprite function from body parent class to allow animation
    def blit_sprite(self, screen):
        if self.thrust_y > 0:
            screen.blit(rcs_thrust_plume, (self.get_coords()[0] + 12, self.get_coords()[1] - 5))
            screen.blit(rcs_thrust_plume, (self.get_coords()[0] + 3, self.get_coords()[1] - 5))
        elif self.thrust_y < 0:
            screen.blit(pygame.transform.flip(rcs_thrust_plume, False, True), (self.get_coords()[0] + 12, self.get_coords()[1] + 15))
            screen.blit(pygame.transform.flip(rcs_thrust_plume, False, True), (self.get_coords()[0] + 3, self.get_coords()[1] + 15))
        if self.orientation == 'left':
            if 0 < abs(self.thrust_x) <= ACCEL_FINE:
                screen.blit(pygame.transform.flip(reg_thrust_plume, True, False), (self.get_coords()[0] + 19, self.get_coords()[1] + 3))
            elif abs(self.thrust_x) > ACCEL_FINE:
                screen.blit(pygame.transform.flip(hot_thrust_plume, True, False), (self.get_coords()[0] + 19, self.get_coords()[1] + 3))
            screen.blit(pygame.transform.flip(self.sprite, True, False), self.get_coords())
        else:
            if 0 < abs(self.thrust_x) <= ACCEL_FINE:
                screen.blit(reg_thrust_plume, (self.get_coords()[0] - 9, self.get_coords()[1] + 3))
            elif abs(self.thrust_x) > ACCEL_FINE:
                screen.blit(hot_thrust_plume, (self.get_coords()[0] - 9, self.get_coords()[1] + 3))
            screen.blit(self.sprite, self.get_coords())
