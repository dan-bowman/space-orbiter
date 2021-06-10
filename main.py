import pygame

from keybinds import get_keystrokes
from ship import Ship
from planet import Planet
from atmosphere import Atmosphere


def main():
    # Initial setup
    pygame.init()
    running = True
    clock = pygame.time.Clock()
    tick_time = 30

    # Screen size and screen object creation
    screen_size = (1920, 1080)
    # screen = pygame.display.set_mode(screen_size)
    screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)

    # Window title and icon
    pygame.display.set_caption("SPACE")
    pygame.display.set_icon(pygame.image.load("assets/img/ship.png"))

    # Background color
    bg = (0, 0, 0)

    # Set font for text
    font = pygame.font.SysFont('consolas', 16)

    # Initialize the actors
    # Ship initial conditions
    # Default spawn point is defined in ship class
    ship_img_path = "assets/img/ship.png"
    ship_spawn = (25, 75)
    ship_size = (20, 15)
    ship = Ship(ship_spawn, ship_img_path, ship_size)

    # Planet initial conditions
    planet_spawn = (500, 375)
    planet_img_path = "assets/img/moon1.png"
    planet_mass = 8e10
    planet_size = (50, 50)
    planet_influence_height = 250
    planet_radius_offset = 1.3  # used below for fine tuning planet collision detection
    planet = Planet(planet_spawn, planet_img_path, planet_size, planet_mass, planet_influence_height)

    # Atmosphere initial conditions
    atm_spawn = (planet_spawn[0] - planet_size[0] / 2, planet_spawn[1] - planet_size[1] / 2)
    atm_img_path = "assets/img/atm.png"
    atm_size = (100, 100)
    atm_press = .002
    atm = Atmosphere(atm_spawn, atm_img_path, atm_size, atm_press)

    min_orbit_radius = 180
    min_orbit = pygame.Rect(tuple([planet.get_center()[0] - min_orbit_radius, planet.get_center()[1] - min_orbit_radius]), tuple([min_orbit_radius * 2, min_orbit_radius * 2]))

    max_orbit_radius = 200
    max_orbit = pygame.Rect(tuple([planet.get_center()[0] - max_orbit_radius, planet.get_center()[1] - max_orbit_radius]), tuple([max_orbit_radius * 2, max_orbit_radius * 2]))

    success_orbit_padding = 4
    success_orbit_radius = max_orbit_radius - (success_orbit_padding // 2)
    success_orbit_thickness = max_orbit_radius - min_orbit_radius - success_orbit_padding
    success_orbit = pygame.Rect(tuple([planet.get_center()[0] - success_orbit_radius, planet.get_center()[1] - success_orbit_radius]), tuple([success_orbit_radius * 2, success_orbit_radius * 2]))

    while running:
        # Paint screen background
        screen.fill(bg)

        # Get events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            tick_time = get_keystrokes(event, ship)

        # Set collision boundaries with walls
        ship.set_wall_collision(screen_size)

        # Set collision boundaries with planet
        ship.set_body_collision(planet, planet_radius_offset)

        # Gravitational attraction
        planet.attract_body(ship)

        # Update atmospheric drag deceleration on ship
        atm.update_drag(ship)

        # Update ship velocity and position
        ship.update_velocity()
        ship.update_position()
        ship.check_fuel()

        # Text objects here:
        # Fuel display text object
        fuel_display_string = "Fuel:"
        fuel_display_loc = (10, 10)
        fuel_display = font.render(fuel_display_string, True, (0, 255, 0))

        score = 0
        if min_orbit_radius <= ship.get_apoapsis(planet) <= max_orbit_radius:
            score = int(50 / ship.get_eccentricity(planet))
            if min_orbit_radius <= ship.get_periapsis(planet) <= max_orbit_radius:
                pygame.draw.ellipse(screen, (0, 63, 0), success_orbit, success_orbit_thickness)

        # Debug Text
        debug_display_string = "Score: " + str(score) + " xAccel: " + str(ship.thrust_x) + " yAccel: " + str(ship.thrust_y)
        debug_display_loc = (10, 120)
        debug_display = font.render(debug_display_string, True, (0, 255, 0))

        # Update ship trail points
        if ship.get_distance_from_point(ship.trail_points[-1]) >= ship.trail_res:
            ship.trail_points.append(ship.get_center())
        # Trim the ship trail length if it gets too long
        if len(ship.trail_points) > ship.trail_len:
            ship.trail_points.pop(0)

        # Draw a trailing line from the ship
        if len(ship.trail_points) > 1 and ship.get_apoapsis(planet) <= planet_influence_height:
            pygame.draw.lines(screen, (0, 127, 0), False, ship.trail_points)

        pygame.draw.ellipse(screen, (127, 127, 0), min_orbit, width = 1)
        pygame.draw.ellipse(screen, (127, 127, 0), max_orbit, width = 1)

        # Blit sprites to screen
        ship.blit_sprite(screen)
        atm.blit_sprite(screen)
        planet.blit_sprite(screen)

        fuel_bar_width = 100
        fuel_bar_height = 15
        fuel_bar_dyn_width = fuel_bar_width * ship.fuel / 100.0
        # Avoiding left-side fuel_bar bleed when fuel value is less than 1.0
        if ship.fuel <= 1.0:
            fuel_bar_dyn_width = 1
        fuel_bar_container = pygame.Rect((10, 30), (fuel_bar_width, fuel_bar_height))
        fuel_bar = pygame.Rect((10, 30), (fuel_bar_dyn_width, fuel_bar_height))

        # Blit text
        screen.blit(fuel_display, fuel_display_loc)
        screen.blit(debug_display, debug_display_loc)

        # Dynamic fuel bar color (Default: Green; Half-fuel: Yellow; Low-Fuel: Red)
        fuel_bar_color = (0, 255, 0)
        if 50.0 > ship.fuel >= 10.0:
            fuel_bar_color = (255, 255, 0)
        elif ship.fuel < 10.0:
            fuel_bar_color = (255, 0, 0)

        # Draw fuel bars
        pygame.draw.rect(screen, (127, 127, 127), fuel_bar_container)
        # Fuel bar disappears if fuel is depleted
        if ship.fuel != 0.0:
            pygame.draw.rect(screen, fuel_bar_color, fuel_bar)

        clock.tick(tick_time)

        # Update screen at end of loop
        pygame.display.update()


main()
