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
    def __init__ (self, player):
        self.player = player
        self.speed = 3
        self.velocity = [-1, 0]
        self.height = random.randint(100, 600)
        self.color = (100, 100, 100)
        self.wall = [-101, 900 - self.height, 100, self.height]
        self.rect = pygame.draw.rect(screen, self.color, self.wall)
        self.spawn = False
    
    def move (self):
        self.wall[0] += self.velocity[0] * self.speed
        self.wall[1] += self.velocity[1] * self.speed
        speed = 0
        if self.rect[0] < -100 and self.spawn:
            self.height = random.randint(100, 600)
            self.wall = [1800, 900 - self.height, 100, self.height]
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








class Wall_spawner:
    def __init__(self, walls_g, time):
        self.walls_g = walls_g
        self.time = time
        self.timer = 0
        self.spawn_recurrence = 180
        self.counter = 1
        self.speedlevel = 1
        self.sec = False

    def update(self):
        #Augmentation de la vitesse
        if self.time.time == 30 * self.speedlevel:
            for wall in self.walls_g:
                wall.speed += 1
            self.speedlevel += 1
            if self.spawn_recurrence > 30:
                self.spawn_recurrence += -10
                self.timer += -10
        
        if random.randint(0,self.spawn_recurrence) == 1 and self.timer == self.spawn_recurrence:
            self.timer = 0
            if self.counter == 1:
                self.walls_g[0].spawn = True
                self.counter = 2
            elif self.counter == 2:
                self.walls_g[1].spawn = True
                self.counter = 3
            elif self.counter == 3:
                self.walls_g[2].spawn = True
                self.counter = 4
            elif self.counter == 4:
                self.walls_g[3].spawn = True
                self.counter = 5
            elif self.counter == 5:
                self.walls_g[4].spawn = True
                self.counter = 1
        elif self.timer == self.spawn_recurrence:
            self.timer = self.timer
        else:
            self.timer += 1








class HUD:
    def __init__(self, wall_spawner, player, time):
        self.score = 0
        self.wall_spawner = wall_spawner
        self.time = time
        self.player = player
        pygame.font.init()
        self.my_font = pygame.font.SysFont('Comic Sans MS', 30)
    
    def draw (self, screen):
        text_score = self.my_font.render(f'Score : {self.score}', False, (255, 255, 255))
        text_walls_speed = self.my_font.render(f'Speed of the walls : {self.wall_spawner.speedlevel}', False, (255, 255, 255))
        text_time = self.my_font.render(f'Time : {self.time.time}', False, (255, 255, 255))
        text_self_speed = self.my_font.render(f'Your speed : {self.player.velocity}', False, (255, 255, 255))
        screen.blit(text_score, (0,0))
        screen.blit(text_walls_speed, (0,30))
        screen.blit(text_time, (0,60))
        screen.blit(text_self_speed, (0,90))





class Time:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.tick = 0
        self.time = 0

    def fps(self, fps, wall_spawner):
        self.wall_spawner = wall_spawner
        self.clock.tick(fps)
        self.tick += 1
        if self.tick == 60:
            self.time += 1
            self.tick = 0
            self.wall_spawner.sec = True







class Game:
    def __init__ (self, screen):
        self.screen = screen
        self.running = True
        self.player = Player(0, 0)
        self.time = Time()
        self.walls_g = [Wall_g(self.player) for i in range(0,5)]
        self.wall_spawner = Wall_spawner(self.walls_g, self.time)
        self.hud = HUD(self.wall_spawner, self.player, self.time)

    def handling_events (self):
        #Quitter le jeu
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
        self.wall_spawner.update()
        for wall in self.walls_g:
            self.hud.score += wall.move()
        #Mort
        self.running = self.walls_g[0].physic() and self.walls_g[1].physic() and self.walls_g[2].physic() and self.walls_g[3].physic() and self.walls_g[4].physic()
        
    def display(self):
        self.screen.fill((0, 0, 0))
        self.player.draw(self.screen)
        for wall in self.walls_g:
            wall.draw(self.screen)
        self.hud.draw(self.screen)
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
            self.time.fps(60, self.wall_spawner)





pygame.init()
screen = pygame.display.set_mode((1800, 900))
game = Game(screen)
game.run()

pygame.quit()