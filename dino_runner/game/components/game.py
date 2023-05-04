import pygame
import time
from game.components.dinosaur import Dinosaur
from game.components.obstacles.cloud import Clouds
from game.components.obstacles.obstacle_manager import Obstacle_manager

from game.components.power_ups.power_up_manager import PowerUpManager
from game.components.score import Score


from game.utils.constants import BG, CLOUD, DINO_START, FONT_STYLE, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, SHIELD_TYPE, TITLE, FPS, GAMES_SPEED,DINO_FALL

BG_2 = pygame.image.load("dino_runner/assets/Track_3.png")

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False  
        self.executing = False  
        self.game_speed = GAMES_SPEED
        self.x_pos_bg = 0
        self.y_pos_bg = 0
        self.cloud = Clouds()
        self.player = Dinosaur("Yoshi")      
        self.obstacle_manager = Obstacle_manager()
        self.score = Score()
        self.death_count = 0
        self.power_up_manger = PowerUpManager()
        self.power_up_manger.reset()
        

        pygame.mixer.init()
        self.YoshiIslandSound =  pygame.mixer.music.load("dino_runner/game/assets/Themes/Yoshi_Island.mp3") 
        self.YoshiIslandSound = pygame.mixer.music.play(1)
        
        self.GameOverSound =  pygame.mixer.music.load("dino_runner/game/assets/Themes/GAMEOVER.mp3")

    def run(self):
        self.executing = True
        while self.executing:
            if not self.playing:
                self.show_menu()
            
        pygame.quit()

    def start_game(self):
        # Game loop: events - update - draw
        self.playing = True
        self.obstacle_manager.reset()
        self.player.lifes.reset_heart(3)
        self.score.score = 0
        self.player.extra_point = 0
        self.game_speed = 20 #VELOCIDAD DEL JUEGO
        #self.score.reset()
        while self.playing:
            self.capture_events()
            self.update()
            self.draw()

    def capture_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self.game_speed, self.player, self.on_death,self.screen)
        self.score.update(self,self.player.extra_point)
        self.power_up_manger.update(self.game_speed, self.score.score,self.player)

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.player.draw(self.screen)
        self.cloud.draw(self.screen)
        self.cloud.update()
        self.obstacle_manager.draw(self.screen)
        self.score.draw(self.screen)
        self.power_up_manger.draw(self.screen)
        self.player.check_power_up(self.screen,self.score.score)
        # pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def on_death(self):
        is_invincible = self.player.type == SHIELD_TYPE
        if not is_invincible:
            self.playing = False
            self.death_count += 1
            ##self.hit_sound.play()
            self.GameOverSound = pygame.mixer.music.play(1) 
            
    def show_menu(self):
        self.screen.blit(BG_2, (0, 0))


        # self.screen.fill((255, 255, 255))
        # Mensaje de bienvenida
        half_screen_width = SCREEN_WIDTH // 2
        half_screen_height = SCREEN_HEIGHT // 2
        if not self.death_count:
            self.screen.blit(BG_2, (0, 0))
            #self.screen.fill((255,255,255))
            font = pygame.font.Font(FONT_STYLE, 42)
            text = font.render("Loading....", True, (0, 0, 255))
            text_rect = text.get_rect()
            text_rect.center = (half_screen_width, half_screen_height)
            self.screen.blit(text, text_rect)
            time.sleep(1)

        else:
            self.screen.blit(BG_2, (0, 0))
            #self.screen.fill((255,255,255))

            self.screen.blit(DINO_FALL, (780, 100))

            self.message("GAME OVER", half_screen_width, half_screen_height)
            self.message(f"Death: {self.death_count}", half_screen_width, half_screen_height + 50)
            self.message(f"Score: {self.score.score}", half_screen_width, half_screen_height + 100)
            self.message(f"Press a key to play again", half_screen_width, half_screen_height + 150)

        # Imagen a modo de inicio en el centro
        self.screen.blit(DINO_START, (half_screen_width - 40, half_screen_height - 140))
        pygame.display.update()
        # Manejar eventos
        self.handle_menu_events()

    def message(self, message, width_position, height_position):
        font = pygame.font.Font(FONT_STYLE, 42)
        text = font.render(message, True, (0, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (width_position, height_position)
        self.screen.blit(text, text_rect)

    def handle_menu_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.executing = False

            if event.type == pygame.KEYDOWN:
                self.start_game()