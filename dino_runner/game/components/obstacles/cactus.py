import random

from game.components.obstacles.obstacles import Obstacle
from game.utils.constants import SMALL_CACTUS, LARGE_CACTUS


class Cactus(Obstacle):
    def __init__(self):
        CACTUS_IMG = SMALL_CACTUS + LARGE_CACTUS
        cactus_type = random.randint(0, len(CACTUS_IMG)-1)
        image = CACTUS_IMG[cactus_type]
        super().__init__(image)
        if cactus_type > 2:
            self.rect.y = 425                     #**** ( ( - )--- ( - )*( - ) =  +   /   ( + )---- ( + )*( - ) =  - )**** AL PONER MAS ES HACIA LO NEGATIVO  SI PONEMOS MENOS ES HACIA ARRIBA (CUADRO DE CORDENADAS)
        else:
            self.rect.y = 445