
import pygame
import random
from game.components.obstacles.birds import Birds
from game.components.obstacles.cactus import Cactus
from game.utils.constants import FONT_STYLE


class Obstacle_manager:
    def __init__(self):
        self.obstacles = []
        self.collisions = 0 
        self.collision_bird=0
        self.collision_cactus=0    
        self.extra_point = 0

    def update(self, game_speed, player, on_death,screen):
        if random.randint(0, 7) >= 5:
         if not self.obstacles:
             self.obstacles.append(Cactus())
        elif not self.obstacles:
            self.obstacles.append(Birds())


        for obstacle in self.obstacles:
                obstacle.update(game_speed, self.obstacles)
                if player.rect.colliderect(obstacle.rect):
               
                    if player.hammer_status == True:
                        if(obstacle == Birds()):
                            print("bird")
                            self.obstacles.remove(obstacle)
                            player.lifes.heart_list.pop()
                        else:
                            player.extra_point += 100                            
                            self.obstacles.remove(obstacle)
                    if player.shield_status == False and player.hammer_status == False:
                        self.obstacles.remove(obstacle)
                        player.lifes.heart_list.pop()#LISTA DE VIDAS LE QUITAS UNA VIDA EL POP ELIMINA DE LA LISTA UNA VALOR LA ULTIMA
                        #QUE PASA SI TIENES LONGITUD 0
                        #   not        0 = false = true
                        if(not len(player.lifes.heart_list)):
                            on_death()


    def draw(self, screen):
        
        for obstacle in self.obstacles:
            obstacle.draw(screen)
            

    def reset(self):
        self.obstacles = []



        
















            ## def update(self, game_speed, player, on_death,screen):
                ## if random.randint(0, 7) >= 5:
                     ##if not self.obstacles:
                         ##self.obstacles.append(Cactus())
                 ##elif not self.obstacles:
                    ## self.obstacles.append(Birds())

            ##for obstacle in self.obstacles:
            ##obstacle.update(game_speed, self.obstacles)
            ##if player.rect.colliderect(obstacle.rect):
                ##if type(obstacle) is Cactus:
                   ## self.collision_cactus += 1
               ## elif type(obstacle) is Birds:
                   ## self.collision_bird += 1
               ## self.obstacles = []


 ## font = pygame.font.Font(FONT_STYLE, 20)
     ##         text = font.render(f"colisiones con el cactus:{self.collision_cactus} colisiones con pajaros: {self.collision_bird}", True, (0,0,0))
         ##     text_rect = text.get_rect()
             ## text_rect.bottomleft = (220,580)
             ## screen.blit(text, text_rect)





        