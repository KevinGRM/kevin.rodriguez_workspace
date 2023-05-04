import random
from game.components.obstacles.obstacles import Obstacle
from game.utils.constants import BIRD

class Birds(Obstacle):
    def __init__(self):
        image = BIRD[0]
        super().__init__(image)
        positions = [390, 320, 260] ##100 250 150////170, 320, 220
        self.rect.y = random.choice(positions)
        self.step = 0

    def update(self, game_speed, obstacles):
        super().update(game_speed, obstacles)
        self.image = BIRD[self.step // 10]
        self.step += 1
        if self.step >= 20:
            self.step = 0