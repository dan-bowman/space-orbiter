# This class is identical to the Mobile class but will remain so that it can be extended later
from mobile import Mobile


class Satellite(Mobile):
    def __init__(self, spawn, img_path, size, mass, influence_height, vel_vector):
        super().__init__(spawn, img_path, size, mass, influence_height, vel_vector)