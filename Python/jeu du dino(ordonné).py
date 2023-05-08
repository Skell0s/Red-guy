import pygame
import random


class Player:
    def __init__ (self, x, y): 
        self.player = pygame.image.load("Ballon de plage(resized).png").convert()
        self.rect = self.player.get_rect(x=x, y=y)
        self.speed = 1
        self.velocity = [0, 0]
        self.touch_floor = False
        self.double_jump = False
        self.in_air = False

    def move (self):
        self.rect.move_ip(self.velocity[0] * self.speed, self.velocity[1] * self.speed)
    
    def physic (self):
        #Frottement
        if self.velocity[0] > 0:
            self.velocity[0] += -1
        if self.velocity[0] < 0:
            self.velocity[0] += 1
        #Gravité
        self.velocity[1] += 1
        #Collision sol
        if self.rect[1] > 800:
            self.velocity[1] = 0
            self.rect[1] = 800
            self.touch_floor = True
            self.double_jump = True
        #Collision limites du terrain
        if self.rect[0] < 0:
            self.velocity[0] = 0
            self.rect[0] = 0
        if self.rect[0] > 1700:
            self.velocity[0] = 0
            self.rect[0] = 1700
        #Collision plafond
        if self.rect[1] < 0:
            self.velocity[1] = 0
            self.rect[1] = 0

    def draw (self, screen):
        screen.blit(self.player, self.rect)









class Wall_g:
    def __init__ (self, player, speed):
        self.player = player
        self.time = 0
        self.speed = speed
        self.color = (100, 100, 100)
        self.width = 100
        self.height = random.randint(100, 600)
        self.wall = [-101, 900 - self.height, self.width, self.height]
        self.rect = pygame.draw.rect(screen, self.color, self.wall)
        self.velocity = [-1, 0]
        self.spawn = False
    
    def move (self, speed):
        self.wall[0] += self.velocity[0] * self.speed
        self.wall[1] += self.velocity[1] * self.speed
        self.speed = speed
        speed = 0
        if self.rect[0] < -100 and self.spawn:
            self.height = random.randint(100, 600)
            self.wall = [1800, 900 - self.height, self.width, self.height]
            self.rect = pygame.draw.rect(screen, self.color, self.wall)
            speed = 1
            self.spawn = False
        return speed


    def physic (self):
        if self.player.rect[1] + 49 < self.rect[1] < self.player.rect[1] + 101 and self.player.rect[0] - 100 < self.rect[0] < self.player.rect[0] + 100:
            self.player.touch_floor = True
            self.player.double_jump = True
            self.player.in_air = False
            self.player.velocity[1] = 0
            self.player.rect[1] = self.rect[1] - 100
            self.player.rect[0] += self.velocity[0] * self.speed
            return True
        elif self.player.rect[0] - 100 < self.rect[0] < self.player.rect[0] and self.player.rect[1] > self.rect[1]:
            self.player.rect[0] = self.rect[0] + 100
            self.player.rect[0] += self.velocity[0]
            return False
        elif self.player.rect[0] < self.rect[0] < self.player.rect[0] + 100 and self.player.rect[1] > self.rect[1]:
            self.player.rect[0] = self.rect[0] - 101
            return False
        else:
            self.player.in_air = True
            return True
        
    def draw (self, screen):
        self.rect = pygame.draw.rect(screen, self.color, self.wall)











class Wall_c(Wall_g):
    def __init__(self):
        super().__init__()
        self.wall = [-101, self.height, self.width, self.height]











class Game:
    def __init__ (self, screen):
        self.screen = screen
        self.running = True
        self.clock = pygame.time.Clock()
        self.player = Player(0, 0)
        self.wall_timer = 0
        self.wall_counter = 1
        self.wall_speed = 3
        self.wall_speedlevel = 1
        self.wall_g = Wall_g(self.player, self.wall_speed)
        self.wall_g2 = Wall_g(self.player, self.wall_speed)
        self.wall_g3 = Wall_g(self.player, self.wall_speed)
        self.wall_g4 = Wall_g(self.player, self.wall_speed)
        self.wall_g5 = Wall_g(self.player, self.wall_speed)
        pygame.font.init()
        self.my_font = pygame.font.SysFont('Comic Sans MS', 30)
        self.score = 0
        self.score_past = 1
        self.time = 0
        self.tick = 0
        self.text_surface = self.my_font.render(f'Score : {self.score}', False, (255, 255, 255))
        self.text_surface2 = self.my_font.render(f'Speed of the walls : {self.wall_speedlevel}', False, (255, 255, 255))
        self.text_surface3 = self.my_font.render(f'Time : {self.time}', False, (255, 255, 255))
        self.text_surface4 = self.my_font.render(f'Your speed : {self.player.velocity}', False, (255, 255, 255))

    def handling_events (self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            #Saut
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.player.touch_floor:
                    self.player.velocity[1] += -20
                    self.player.touch_floor = False
                elif event.key == pygame.K_SPACE and self.player.double_jump:
                    self.player.velocity[1] += -25
                    self.player.double_jump = False
                if event.key == pygame.K_s and self.player.in_air:
                    self.player.velocity[1] += 50

        
        #Mouvements droite/guauche
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            if self.player.velocity[0] > -10:
                self.player.velocity[0] += -2
        if keys[pygame.K_d]:
            if self.player.velocity[0] < 10:
                self.player.velocity[0] += 2
     
    def update(self):
        self.player.move()
        self.player.physic()
        self.score += self.wall_g.move(self.wall_speed) + self.wall_g2.move(self.wall_speed) + self.wall_g3.move(self.wall_speed) + self.wall_g4.move(self.wall_speed) + self.wall_g5.move(self.wall_speed)
        self.running = self.wall_g.physic() and self.wall_g2.physic() and self.wall_g3.physic() and self.wall_g4.physic() and self.wall_g5.physic()
        if self.time == 30 * self.wall_speedlevel:
            self.wall_speed += 1
            self.wall_speedlevel += 1


    
    def display(self):
        self.screen.fill((0, 0, 0))
        self.player.draw(self.screen)
        self.wall_g.draw(self.screen)
        self.wall_g2.draw(self.screen)
        self.wall_g3.draw(self.screen)
        self.wall_g4.draw(self.screen)
        self.wall_g5.draw(self.screen)
        self.text_surface = self.my_font.render(f'Score : {self.score}', False, (255, 255, 255))
        self.text_surface2 = self.my_font.render(f'Speed : {self.wall_speedlevel}', False, (255, 255, 255))
        self.text_surface3 = self.my_font.render(f'Time : {self.time}', False, (255, 255, 255))
        self.text_surface4 = self.my_font.render(f'Your speed : {self.player.velocity}', False, (255, 255, 255))
        self.screen.blit(self.text_surface, (0,0))
        self.screen.blit(self.text_surface2, (0,30))
        self.screen.blit(self.text_surface3, (0,60))
        self.screen.blit(self.text_surface4, (0,90))
        pygame.display.flip()
    
    def run(self):
        while True:
            self.handling_events()
            if not self.running:
                break
            self.update()
            if not self.running:
                break
            self.display()
            #Gestion du temps
            self.clock.tick(60)
            self.tick += 1
            if self.tick == 60:
                self.time += 1
                self.tick = 0
                print(random.randint(0,2))
                #Spawn des murs
                if random.randint(0,1) == 1 and self.wall_timer == 2:
                    self.wall_timer = 0
                    if self.wall_counter == 1:
                        self.wall_g.spawn = True
                        self.wall_counter = 2
                    elif self.wall_counter == 2:
                        self.wall_g2.spawn = True
                        self.wall_counter = 3
                    elif self.wall_counter == 3:
                        self.wall_g3.spawn = True
                        self.wall_counter = 4
                    elif self.wall_counter == 4:
                        self.wall_g4.spawn = True
                        self.wall_counter = 5
                    elif self.wall_counter == 5:
                        self.wall_g5.spawn = True
                        self.wall_counter = 1
                elif self.wall_timer == 2:
                    self.wall_timer = self.wall_timer
                else:
                    self.wall_timer += 1






pygame.init()
screen = pygame.display.set_mode((1800, 900))
game = Game(screen)
game.run()

pygame.quit()