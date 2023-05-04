from game.components.life.heart import Heart
import pygame
from pygame.sprite import Sprite
from game.utils.constants import DEFAULT_TYPE, DUCKING, DUCKING_SHIELD, JUMPING, JUMPING_SHIELD, RUNNING, RUNNING_SHIELD, SHIELD_TYPE,FONT_STYLE,HAMMER_TYPE,DUCKING_HAMMER,JUMPING_HAMMER,RUNNING_HAMMER, FONT_STYLE, COLORS
from game.components.score import Score


DINO_RUNNING = "running"
DINO_JUMPING = "jumping"
DINO_DUCKING = "ducking"

DUCK_IMG = {DEFAULT_TYPE: DUCKING, SHIELD_TYPE: DUCKING_SHIELD , HAMMER_TYPE:DUCKING_HAMMER }
JUMP_IMG = {DEFAULT_TYPE: JUMPING, SHIELD_TYPE: JUMPING_SHIELD, HAMMER_TYPE: JUMPING_HAMMER}
RUN_IMG = {DEFAULT_TYPE: RUNNING, SHIELD_TYPE: RUNNING_SHIELD, HAMMER_TYPE: RUNNING_HAMMER}

class Dinosaur(Sprite):
    POSITION_X = 80
    POSITION_Y = 430 ##380
    JUMP_VELOCITY = 8.5
    POSITION_Y_DUCK = 460 ##410

    def __init__(self,name):
        self.type = DEFAULT_TYPE
        self.power_up_time_up = 0
        self.update_image(RUN_IMG[self.type][0])
        self.action = DINO_RUNNING
        self.jump_velocity = self.JUMP_VELOCITY
        self.step = 0
        self.lifes = Heart(3) #TRES CORAZONDES DE VIDA
        self.shield_status = False
        self.hammer_status = False
        self.extra_point = 0

        self.name = name
        self.state = ''

        self.font = pygame.font.Font(FONT_STYLE, 20)
        self.text = self.font.render(f'{self.name}: {self.state}', True, COLORS["black"])
        self.text_rect = self.text.get_rect()
        self.text_rect.bottomleft = (20,580)

        self.status_font = pygame.font.Font(FONT_STYLE, 20)
        self.status_text = self.status_font.render('', True, COLORS["black"])
        self.status_rect = self.status_text.get_rect()
        self.status_rect.bottomleft = (self.text_rect.right,580)

        pygame.mixer.init()
        self.jumpSound = pygame.mixer.Sound("dino_runner/game/assets/Themes/Jump.mp3")
        self.duckSound = pygame.mixer.Sound("dino_runner/game/assets/Themes/Mlem.mp3")

    def update(self, user_input):
        if self.action == DINO_RUNNING:
            self.run()
        elif self.action == DINO_DUCKING:
            self.duck()
        elif self.action == DINO_JUMPING:
            self.jump()

        if user_input[pygame.K_DOWN] or user_input[pygame.K_z]:
            if self.action == DINO_JUMPING:
                self.jump()
            else:
                self.action = DINO_DUCKING
                self.state ="down"
                
        elif self.action != DINO_JUMPING:
            if user_input[pygame.K_UP]or user_input[pygame.K_a]:
                self.action = DINO_JUMPING
                self.state ="jump"
                self.duckSound.play()
            else:
                self.action = DINO_RUNNING
                self.state ="running"
        
        if self.step >= 10:
            self.step = 0

    def run(self):
        self.update_image(RUN_IMG[self.type][self.step // 5])
        self.step += 1

    def duck(self):
        self.update_image(DUCK_IMG[self.type][self.step // 5], pos_y = self.POSITION_Y_DUCK)
        self.step += 1

    def jump(self):
        pos_y = self.rect.y - self.jump_velocity * 6 
        self.update_image(JUMP_IMG[self.type], pos_y = pos_y)
        self.jump_velocity -= 0.8
        if self.jump_velocity < -self.JUMP_VELOCITY:
            self.jump_velocity = self.JUMP_VELOCITY
            self.action = DINO_RUNNING
            self.rect.y = self.POSITION_Y

    def update_image(self, image:pygame.Surface, pos_x = None, pos_y=None):
        self.image = image
        self.rect = image.get_rect()
        self.rect.x = pos_x or self.POSITION_X
        self.rect.y = pos_y or self.POSITION_Y

    def draw(self, screen):
        self.lifes.draw(screen)
        screen.blit(self.image,(self.rect.x, self.rect.y))

        if self.run or self.jump or self.duck:
           self.status_text = self.status_font.render(self.state, True, (0,0,0))
        screen.blit(self.status_text, self.status_rect)
        screen.blit(self.text, self.text_rect)


    def one_pick_power_up(self, power_up):
        self.type = power_up.type
        self.power_up_time_up = power_up.start_time + (power_up.duration * 1000) 

    def print_message(self, message,screen, width_position, height_position):
        font = pygame.font.Font(FONT_STYLE, 32)
        text = font.render(message, True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (width_position, height_position)
        screen.blit(text, text_rect)

    def check_power_up(self, screen,score):
        #TIPO ESCUDO
        if self.type == SHIELD_TYPE:
            time_to_show = round((self.power_up_time_up - pygame.time.get_ticks()) / 1000, 2)
            if time_to_show >= 0:
                self.print_message(f"{self.type.capitalize()} anable for {time_to_show} seconds",screen, 580, 100)
                if(time_to_show <= 0.5):
                    self.shield_status = False#DESACTIVANDO EL ESCUDO
            else:
                self.type = DEFAULT_TYPE
                self.power_up_time_up = 0
        #TIPO MARTILLO
        elif self.type == HAMMER_TYPE:
            time_to_show = round((self.power_up_time_up - pygame.time.get_ticks()) / 1000, 2)
            if time_to_show >= 0:
                self.print_message(f"{self.type.capitalize()} anable for {time_to_show} seconds",screen, 580, 100)
                self.print_message(f"EXTRA:{self.extra_point}",screen,580,400)
            else:
                self.type = DEFAULT_TYPE
                self.power_up_time_up = 0 
                self.hammer_status = False#DESACTIVANDO EL ESCUDO
                print("AUMENTANDO PUNTOS EXTRA")
                print(score)
                print(self.extra_point)
                score += self.extra_point
                self.extra_point = 0
                 # RESETEAMOS los puntos extra       
    def addPoints(self,score):
        score += self.extra_point
