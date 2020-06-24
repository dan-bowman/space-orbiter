import pygame
import math


class Body:
    def __init__(self, spawn, img_path, size):
        # Initialize spawn location
        self.x = spawn[0]
        self.y = spawn[1]

        # Load image from img_path to create sprite
        self.sprite = pygame.image.load(img_path)

        # Width and Height for collision detection
        self.width = size[0]
        self.height = size[1]

        # Radius calculated through the size, used for circular Bodies
        self.radius = math.sqrt((self.width / 2)**2 + (self.height / 2)**2)

    # Return a tuple with actual coordinates (top-left corner)
    def get_coords(self):
        return tuple([self.x, self.y])

    # Return a tuple with coordinates of center
    def get_center(self):
        return tuple([self.x + (self.width / 2), self.y + (self.height / 2)])

    # Blit sprite to screen
    def blit_sprite(self, screen):
        screen.blit(self.sprite, self.get_coords())
