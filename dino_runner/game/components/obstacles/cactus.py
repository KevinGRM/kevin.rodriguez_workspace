import random

from game.components.obstacles.obstacles import Obstacle
from game.utils.constants import SMALL_CACTUS, LARGE_CACTUS


class Cactus(Obstacle):
    def __init__(self):
        cactus = [SMALL_CACTUS, LARGE_CACTUS]
        cactus_var = random.randint(0, 4)
        cactus_type = random.choice(cactus)
        image = cactus_type[cactus_var]
        super().__init__(image)
        if cactus_type == SMALL_CACTUS:
            self.rect.y = 445  ##405 ##325
        else:
            self.rect.y = 425 ##385 ##300