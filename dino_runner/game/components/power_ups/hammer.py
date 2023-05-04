from game.utils.constants import HAMMER,HAMMER_TYPE
from game.components.power_ups.power_up import PowerUp

class Hammer(PowerUp):
    def __init__(self):
        super().__init__(HAMMER,HAMMER_TYPE)