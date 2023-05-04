
import pygame
from pygame.sprite import Sprite

from game.utils.constants import RUNNING, JUMPING, DUCKING, FONT_STYLE, COLORS


DINO_RUNNING = "running"
DINO_JUMPING = "jumping"
DINO_DUCKING = "ducking"
class Dinosaur(Sprite):
    POSITION_X = 80
    POSITION_Y = 430 ##380
    JUMP_VELOCITY = 8.5
    POSITION_Y_DUCK = 460 ##410

    def __init__(self,name):
        self.image = RUNNING[0]
        self.rect = self.image.get_rect()
        self.rect.x = self.POSITION_X
        self.rect.y = self.POSITION_Y
        self.action = DINO_RUNNING  
        self.jump_velocity = self.JUMP_VELOCITY
        self.step = 0

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
            else:
                self.action = DINO_RUNNING
                self.state ="running"
        
        if self.step >= 10:
            self.step = 0

    def run(self):
        self.update_image(RUNNING[self.step // 5])
        self.step += 1

    def duck(self):
        self.update_image(DUCKING[self.step // 5], pos_y = self.POSITION_Y_DUCK)
        self.step += 1

    def jump(self):
        pos_y = self.rect.y - self.jump_velocity * 6 
        self.update_image(JUMPING, pos_y = pos_y)
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
        screen.blit(self.image,(self.rect.x, self.rect.y))

        if self.run or self.jump or self.duck:
           self.status_text = self.status_font.render(self.state, True, (0,0,0))
        screen.blit(self.status_text, self.status_rect)
        screen.blit(self.text, self.text_rect)