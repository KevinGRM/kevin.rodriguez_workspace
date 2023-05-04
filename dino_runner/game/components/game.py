import pygame

from game.components.dinosaur import Dinosaur
from game.components.obstacles.cloud import Clouds
from game.components.obstacles.obstacle_manager import Obstacle_manager

from game.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, GAMES_SPEED


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False    
        self.game_speed = GAMES_SPEED
        self.x_pos_bg = 0
        self.y_pos_bg = 0

        self.cloud = Clouds()
        self.player = Dinosaur("Yoshi")      
        self.obstacle_manager = Obstacle_manager()

    def run(self):
        # This is Game Loop: events - update - draw
        print("starting the game loop")
        self.playing = True
        while self.playing:
            self.capture_events()
            self.update()
            self.draw()
        else:
            print("quit the game")
            pygame.quit()

    def capture_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("received event.type", event.type, "that indicates `quit` game")
                self.playing = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self.game_speed, self.player, self)

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.player.draw(self.screen)
        self.cloud.draw(self.screen)
        self.cloud.update()
        self.obstacle_manager.draw(self.screen)
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed