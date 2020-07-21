from body import Body


class Atmosphere(Body):
    def __init__(self, spawn, img_path, size, press):
        super().__init__(spawn, img_path, size)

        # Atmospheric pressure which modifies how much drag will act upon the body that moves within it
        self.press = press

        # Drag variable changes based on how far into the atmosphere the ship is
        self.drag = 0.0

    def apply_drag(self, ship):
        accel_mag = self.press * self.drag
        ship.drag(accel_mag, ship.get_vel_dir())

    def update_drag(self, ship):
        distance = ship.get_r_mag(self)
        if distance > self.get_radius():
            self.drag = 0.0
        elif self.get_radius() >= distance > 0.9 * self.get_radius():
            self.drag = 0.1
        elif self.get_radius() * 0.9 >= distance > 0.8 * self.get_radius():
            self.drag = 0.2
        else:
            self.drag = 0.3

        self.apply_drag(ship)
