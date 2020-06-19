import pygame

# Magnitude of acceleration applied from keystrokes
accel_mag = 0.0002


# Hardcoded keystroke event handlers for moving the ship
def get_keystrokes(event, ship):
    # KEYDOWN events
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_a:
            if ship.fuel > 0.0:
                ship.add_thrust_x(accel_mag * -1)
        if event.key == pygame.K_d:
            if ship.fuel > 0.0:
                ship.add_thrust_x(accel_mag)
        if event.key == pygame.K_w:
            if ship.fuel > 0.0:
                ship.add_thrust_y(accel_mag * -1)
        if event.key == pygame.K_s:
            if ship.fuel > 0.0:
                ship.add_thrust_y(accel_mag)
        if event.key == pygame.K_t:
            if ship.get_vel_mag() <= 0.01 and ship.fuel > 0.0:
                ship.thrust_x = 0.0
                ship.thrust_y = 0.0
                ship.dx = 0.0
                ship.dy = 0.0
                ship.ddx = 0.0
                ship.ddy = 0.0

        # Velocity information
        vel_mag = ship.get_vel_mag()
        if vel_mag != 0.0:
            vel_dir = tuple([ship.dx / vel_mag, ship.dy / vel_mag])
            # Prograde keybind
            if event.key == pygame.K_e and ship.fuel > 0.0:
                ship.prograde(accel_mag, vel_dir)
            # Retrograde keybind
            if event.key == pygame.K_r and ship.fuel > 0.0:
                ship.retrograde(accel_mag, vel_dir)
    # KEYUP events
    if event.type == pygame.KEYUP:
        if event.key in (pygame.K_a, pygame.K_d, pygame.K_r, pygame.K_e, pygame.K_t):
            ship.add_thrust_x(0.0)
        if event.key in (pygame.K_w, pygame.K_s, pygame.K_r, pygame.K_e, pygame.K_t):
            ship.add_thrust_y(0.0)
