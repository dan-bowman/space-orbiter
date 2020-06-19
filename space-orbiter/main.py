import pygame

from keybinds import get_keystrokes
from ship import Ship
from planet import Planet


def main():
    # Initial setup
    pygame.init()
    running = True

    # Screen size and screen object creation
    screen_size = (1000, 750)
    screen = pygame.display.set_mode(screen_size)

    # Window title and icon
    pygame.display.set_caption("SPACE")
    pygame.display.set_icon(pygame.image.load("ship.png"))

    # Background color
    bg = (0, 0, 0)

    # Set font for text
    font = pygame.font.SysFont('consolas', 16)

    # Initialize the actors
    # Ship initial conditions
    # Default spawn point is defined in ship class
    ship_img_path = "ship.png"
    ship_width = 20
    ship_height = 15
    ship = Ship(ship_img_path, ship_width, ship_height)

    # Planet initial conditions
    planet_x = 500
    planet_y = 375
    planet_img_path = "moon1.png"
    planet_mass = 8e10
    planet_radius = 25
    planet_atm_height = 20
    planet_atm_press = 0
    planet_influence_height = 250
    planet_radius_offset = 1.3  # used below for fine tuning planet collision detection
    planet = Planet(planet_x, planet_y, planet_img_path, planet_mass, planet_radius,
                    planet_atm_height, planet_atm_press, planet_influence_height)

    # clock = pygame.time.Clock()

    while running:
        # Paint screen background
        screen.fill(bg)

        # Get events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            get_keystrokes(event, ship)

        # Set collision boundaries with walls
        ship.set_wall_collision(screen_size)

        # Set collision boundaries with planet
        ship.set_planet_collision(planet, planet_radius_offset)

        # Gravitational attraction
        planet.attract_body(ship)

        # Update ship velocity and position
        ship.update_velocity()
        ship.update_position()
        ship.check_fuel()

        # Text objects here:
        # Fuel display text object
        fuel_display_string = "Fuel:"
        fuel_display_loc = (10, 10)
        fuel_display = font.render(fuel_display_string, True, (0, 255, 0))

        print(ship.get_vel_mag())

        # Blit sprites to screen
        ship.blit_sprite(screen)
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

        # clock.tick(500)
        # Update screen at end of loop
        pygame.display.update()


main()
