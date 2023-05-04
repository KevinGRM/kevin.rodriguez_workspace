import pygame

class Game():
    def __init__(self, caption = "My first game", screen_width=640, screen_heigth=480):
     print("Initializing game attributes")

     pygame.init()

     pygame.display.set_caption(caption)

     self.screen = pygame.display.set_mode((screen_width, screen_heigth)) 
     self.screen_width = screen_width
     self.screen_heigth = screen_heigth

     ##posicion inicial
     self.circle_x = self.screen_heigth // 2
     self.circle_y = self.screen_width // 2
     self.circle_radius = 20
     self.circle_x_factor = 5
     self.circle_y_factor = 5


     self.keep_screen_open = True


    def run(self):
      print("this is the game run method")
      while self.keep_screen_open:
        print("the game is running")
        self.capture_events()
        self.update()
        self.draw()
      else:
        print("Quit Game because self.keep_screen_open is ", self.keep_screen_open)
        pygame.quit()

    def capture_events(self):
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          print("received event.type", event.type, "that indicates close screen")
          self.keep_screen_open = False

    def update(self):
       pass

    def draw_circle(self):
      
      self.circle_x += self.circle_x_factor
      self.circle_y += self.circle_y_factor

      if self.circle_x - self.circle_radius < 0 or self.circle_x + self.circle_radius > self.screen_width:
        self.circle_x_factor = -self.circle_x_factor
    
      if self.circle_y - self.circle_radius < 0 or self.circle_y + self.circle_radius > self.screen_heigth:
        self.circle_y_factor = -self.circle_y_factor

      circle_color=(255, 0, 0)

      pygame.draw.circle(self.screen, circle_color, (self.circle_x,self.circle_y), self.circle_radius)

    def draw(self):
      self.screen.fill((255,255,255))

      self.draw_circle()

      pygame.display.flip()

      pygame.time.delay(20)


      ##if self.action != RESET:
           ##if user_input[pygame.K_SPACE]:
               ##self.action = RESET
           ##else:
               ##self.action = RUN

      ##def RESET(self):
         ##self.circle_x = self.screen_heigth // 2
         ##self.circle_y = self.screen_width // 2