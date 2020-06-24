# This class is identical to the Gravitative class but will remain so that it can be extended later
from gravitative import Gravitative


class Planet(Gravitative):
    def __init__(self, spawn, img_path, size, mass, influence_height):
        super().__init__(spawn, img_path, size, mass, influence_height)
