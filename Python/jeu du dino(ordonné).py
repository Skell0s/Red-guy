import pygame
import random
import math 


class Player:
    def __init__ (self, x, y): 
        self.life = 3
        self.player = pygame.image.load("Idle(resized).png").convert_alpha()
        self.display_x = x
        self.display_y = y
        self.rect = self.player.get_rect(x=0, y=self.display_y - 100)
        self.speed = 1
        self.velocity = [0, 0]
        self.touch_floor = False
        self.double_jump = False
        self.walk = True
        self.timer_walk = 0
        self.idle = False
        self.recovery_time = False
        self.recovery_timer = 0

    def move (self):
        self.rect.move_ip(self.velocity[0] * self.speed, self.velocity[1] * self.speed)
    
    def physic (self):
        #Frottement
        if self.velocity[0] > 7:
            self.velocity[0] += -10
        elif self.velocity[0] > 0:
            self.velocity[0] += -1
        if self.velocity[0] < -7:
            self.velocity[0] += 10
        elif self.velocity[0] < 0:
            self.velocity[0] += 1
        #Gravité
        self.velocity[1] += 1
        #Collision sol
        if self.rect[1] >= self.display_y - 100:
            self.velocity[1] = 0
            self.rect[1] = self.display_y - 100
            self.touch_floor = True
            self.double_jump = True
            self.idle = False
            self.walk = True
        #Collision limites du terrain
        if self.rect[0] < -20:
            self.velocity[0] = 0
            self.rect[0] = -20
        if self.rect[0] > self.display_x - 80:
            self.velocity[0] = 0
            self.rect[0] = self.display_x - 80
        #Collision plafond
        if self.rect[1] < 0:
            self.velocity[1] = 0
            self.rect[1] = 0

    def draw (self, screen):
        if self.recovery_time:
            if self.recovery_timer <= 10:
                self.show = False
            elif self.recovery_timer <= 20:
                self.show = True
            elif self.recovery_timer <= 30:
                self.show = False
            elif self.recovery_timer <= 40:
                self.show = True
            elif self.recovery_timer <= 50:
                self.show = False
            elif self.recovery_timer <= 60:
                self.show = True
            else:
                self.recovery_timer = 0
                self.recovery_time = False
            self.recovery_timer += 1
        else:
            self.show = True
        if self.idle:
            self.player = pygame.image.load("Idle(resized).png").convert_alpha()
            self.idle = False
        elif self.walk:
            if self.timer_walk <= 10:
                self.player = pygame.image.load("Walk1(resized).png").convert_alpha()
            elif self.timer_walk <= 20:
                self.player = pygame.image.load("Walk2(resized).png").convert_alpha()
            else:
                self.timer_walk = 0
            self.timer_walk += 1
            self.walk = False
        else:
            self.player = pygame.image.load("Walk1(resized).png").convert_alpha()
        if self.show:
            screen.blit(self.player, self.rect)









class Wall_g:
    def __init__ (self, player, time, display_x, display_y):
        self.player = player
        self.time = time
        self.display_x = display_x
        self.display_y = display_y
        self.speed = 5
        self.velocity = [-1, 0]
        self.height = random.randint(100, self.display_y - 200)
        self.color = (100, 100, 100)
        self.wall = [-101, self.display_y - self.height, 100, self.height]
        self.rect = pygame.draw.rect(screen, self.color, self.wall)
        self.spawn = False
        self.height_move = random.randint(100, self.display_y - 200)
        self.spawn_active = False
        if random.randint(0,6) == 1:
            self.spawn_active = True
        else:           
            self.spawn_active = False
    
    def move (self):
        self.wall[0] += self.velocity[0] * self.speed
        self.wall[1] += self.velocity[1] * self.speed
        speed = 0
        if self.rect[0] < -100 and self.spawn:
            self.height_move = random.randint(100, self.display_y - 200)
            self.height = random.randint(100, self.display_y - 200)
            self.wall = [self.display_x, self.display_y - self.height, 100, self.height]
            self.rect = pygame.draw.rect(screen, self.color, self.wall)
            speed = 1
            self.spawn = False
            if random.randint(0,6) == 1:
                self.spawn_active = True
            else:
                self.spawn_active = False
        if self.spawn_active:
            self.height = 100 + self.height_move * math.sin(((2*math.pi)/120)*(self.time.tick))
            self.wall[1] = self.display_y - self.height
        return speed

    def physic (self):
        if self.player.rect[1] + 49 <= self.rect[1] <= self.player.rect[1] + 101 and self.player.rect[0] - 80 < self.rect[0] < self.player.rect[0] + 80:
            self.player.touch_floor = True
            self.player.double_jump = True
            keys = pygame.key.get_pressed()
            if keys[pygame.K_q] or keys[pygame.K_d]:
                self.player.walk = True
            else:
                self.player.idle = True
            self.player.velocity[1] = 0
            self.player.rect[1] = self.rect[1] - 100
            if not keys[pygame.K_d]:
                self.player.rect[0] += self.velocity[0] * self.speed
            return True
        elif not self.player.recovery_time and self.player.rect[0] - 80 < self.rect[0] < self.player.rect[0] and self.player.rect[1] > self.rect[1]:
            self.player.rect[0] = self.rect[0] + 80
            self.player.rect[0] += self.velocity[0]
            return False
        elif not self.player.recovery_time and self.player.rect[0] < self.rect[0] < self.player.rect[0] + 80 and self.player.rect[1] > self.rect[1]:
            self.player.rect[0] = self.rect[0] - 81
            return False
        else:
            return True
        
    def draw (self, screen):
        self.wall[3] = self.height
        self.rect = pygame.draw.rect(screen, self.color, self.wall)











class Wall_c:
    def __init__ (self, player, time, display_x, display_y):
        self.player = player
        self.time = time
        self.display_x = display_x
        self.display_y = display_y
        self.speed = 5
        self.velocity = [-1, 0]
        self.height = random.randint(int(self.display_y * 0.25), display_y - 200)
        self.wall = [-101, 0, 100, self.height]
        self.rect = pygame.draw.rect(screen, (100, 100, 100), self.wall)
        self.spawn = False
        self.height_move = random.randint(int(self.display_y * 0.25), self.display_y - 200)
        self.spawn_active = False
        if random.randint(0,6) == 1:
            self.spawn_active = True
        else:
            self.spawn_active = False
    
    def move (self):
        self.wall[0] += self.velocity[0] * self.speed
        self.wall[1] += self.velocity[1] * self.speed
        speed = 0
        if self.rect[0] < -100 and self.spawn:
            self.height = random.randint(200, self.display_y - 200 )
            self.wall = [self.display_x, 0, 100, self.height]
            self.rect = pygame.draw.rect(screen, (100, 100, 100), self.wall)
            self.height_move = random.randint(0, self.display_y - 200)
            speed = 1
            self.spawn = False
            if random.randint(0,6) == 1:
                self.spawn_active = True
            else:
                self.spawn_active = False
        if self.spawn_active:
            self.height = 100 + self.height_move * math.sin(((2*math.pi)/120)*(self.time.tick))
        return speed

    def physic (self):
        if self.height > self.player.rect[1] > self.height - 30 and self.player.rect[0] - 80 < self.rect[0] < self.player.rect[0] + 80:
            self.player.velocity[1] = 0
            self.player.rect[1] = self.height + 1
            return True
        elif not self.player.recovery_time and self.player.rect[0] - 80 < self.rect[0] < self.player.rect[0] and self.height > self.player.rect[1]:
            self.player.rect[0] = self.rect[0] + 80
            self.player.rect[0] += self.velocity[0]
            return False
        elif not self.player.recovery_time and self.player.rect[0] < self.rect[0] < self.player.rect[0] + 80 and self.height > self.player.rect[1]:
            self.player.rect[0] = self.rect[0] - 81
            return False
        else:
            return True
        
    def draw (self, screen):
        self.wall[3] = self.height
        self.rect = pygame.draw.rect(screen, (100, 100, 100), self.wall)








class Wall_spawner:
    def __init__(self, walls_g, walls_c, time):
        self.walls_g = walls_g
        self.walls_c = walls_c
        self.time = time
        self.timer = 0
        self.spawn_recurrence = 60
        self.random_spawn_recurrence = 60
        self.counter = 1
        self.speedlevel = 1

    def update(self):
        #Augmentation de la vitesse
        if self.time.time == 15 * self.speedlevel:
            for wall in self.walls_g:
                wall.speed += 1
            for wall in self.walls_c:
                wall.speed += 1
            self.speedlevel += 1

            if self.random_spawn_recurrence > 1:
                self.random_spawn_recurrence += -int(self.walls_g[0].speed/2)
            if self.spawn_recurrence > 1:
                self.timer += -int(self.walls_g[0].speed/2)
                self.spawn_recurrence += -int(self.walls_g[0].speed/2)
        #Walls
        if random.randint(0, self.random_spawn_recurrence) == 0 and self.timer == self.spawn_recurrence:
            self.timer = 0
            if self.counter == 1:
                self.walls_g[0].spawn = True
                self.counter = 2
            elif self.counter == 2:
                self.walls_c[0].spawn = True
                self.counter = 3
            elif self.counter == 3:
                self.walls_g[1].spawn = True
                self.counter = 4
            elif self.counter == 4:
                self.walls_c[1].spawn = True
                self.counter = 5
            elif self.counter == 5:
                self.walls_g[2].spawn = True
                self.counter = 6
            elif self.counter == 6:
                self.walls_c[2].spawn = True
                self.counter = 7
            elif self.counter == 7:
                self.walls_g[3].spawn = True
                self.counter = 8
            elif self.counter == 8:
                self.walls_c[3].spawn = True
                self.counter = 9
            elif self.counter == 9:
                self.walls_g[4].spawn = True
                self.counter = 10
            elif self.counter == 10:
                self.walls_c[4].spawn = True
                self.counter = 1
        #Timer
        elif self.timer == self.spawn_recurrence:
            self.timer = self.timer
        else:
            self.timer += 1








class HUD:
    def __init__(self, player, wall_g, time):
        self.player = player
        self.score = 0
        self.wall_g = wall_g
        self.time = time
        pygame.font.init()
        self.my_font = pygame.font.SysFont('Comic Sans MS', 40)
    
    def draw (self, screen):
        if self.player.life > 1:
            text_life = self.my_font.render(f'Lifes :', False, (0, 0, 0))
        else:
            text_life = self.my_font.render(f'Life :', False, (0, 0, 0))
        text_score = self.my_font.render(f'Score : {self.score}', False, (0, 0, 0))
        text_walls_speed = self.my_font.render(f'Speed of the walls : {self.wall_g[1].speed - 4}', False, (0, 0, 0))
        text_time = self.my_font.render(f'Time : {self.time.time}', False, (0, 0, 0))
        for i in range(self.player.life):
            self.heart = pygame.image.load("Heart50.png").convert_alpha()
            screen.blit(self.heart, (120 + 50*i, 7))
        screen.blit(text_life, (0,0))
        screen.blit(text_score, (0,50))
        screen.blit(text_walls_speed, (0,100))
        screen.blit(text_time, (0,150))





class Time:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.tick = 0
        self.time = 0

    def fps(self, fps, count):
        self.clock.tick(fps)
        self.tick += 1
        if self.tick == 60:
            if count:
                self.time += 1
            self.tick = 0







class Button:
    def __init__(self, title, color, display_x, display_y, time, width, height, title_size, title_color, title_x, title_y):
        self.title = title
        self.color = color
        self.display_x = display_x
        self.display_y = display_y
        self.time = time
        self.width = width
        self.height = height
        self.title_size = title_size
        self.title_color = title_color
        self.title_color_i = title_color
        self.title_x = title_x
        self.title_y = title_y
        self.size = [self.display_x, self.display_y, self.width, self.height]
        pygame.font.init()
        self.my_font = pygame.font.SysFont('Comic Sans MS', self.title_size)
        self.title_show = self.my_font.render(f'{self.title}', False, self.title_color)
        self.button = pygame.draw.rect(screen, self.color, self.size)

    def update(self, color):
        self.mouse_pos = pygame.mouse.get_pos()
        if self.size[0] <= self.mouse_pos[0] <= self.size[0] + self.width and self.size[1] <= self.mouse_pos[1] <= self.size[1] + self.height:
            self.color = (0, 0, 255)
            self.title_color = (0, 0, 150)
            self.size = [self.display_x - 5, self.display_y - 5, self.width + 10, self.height + 10]
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.color = (100, 100, 255)
                    self.size = [self.display_x - 10, self.display_y - 10, self.width + 20, self.height + 20]
                if event.type == pygame.MOUSEBUTTONUP:
                    return True
                else:
                    return False
        else:
            self.color = color
            self.title_color = self.title_color_i
            self.size = [self.display_x, self.display_y, self.width, self.height]
            return False

    def draw(self, screen, start):
        if start:
            self.size[0] += -25 * math.sin(((2*math.pi)/120)*(self.time.tick))
            self.size[1] += -25 * math.sin(((2*math.pi)/120)*(self.time.tick))
            self.size[2] += 50 * math.sin(((2*math.pi)/120)*(self.time.tick))
            self.size[3] += 50 * math.sin(((2*math.pi)/120)*(self.time.tick))
        self.button = pygame.draw.rect(screen, self.color, self.size)
        self.title_show = self.my_font.render(f'{self.title}', False, self.title_color)
        screen.blit(self.title_show, (self.title_x, self.title_y))
        








class Menu:
    def __init__(self, display_x, display_y, time):
        self.display_x = display_x
        self.display_y = display_y
        self.time = time
        self.start_title_size = 100
        self.start_color = (0, 255, 0)
        self.startb = Button('Start', self.start_color, self.display_x/2 - 400, self.display_y/2 - 100, self.time, 800, 200, self.start_title_size, (0, 100, 0), self.display_x/2 - 150, self.display_y/2 - self.start_title_size * 0.75)
        self.titles_size = 50
        self.quit_color = (50, 50, 50)
        self.quit = Button('Quit', self.quit_color, self.display_x/2 - 200, self.display_y/2 + 100, self.time, 400, 100, self.titles_size, (25, 25, 25), self.display_x/2 - 175, self.display_y/2 + 150 - self.titles_size * 0.75)
        self.restart_color = (50, 50, 50)
        self.restart = Button('Restart', self.quit_color, self.display_x/2 - 200, self.display_y/2 - 50, self.time, 400, 100, self.titles_size, (25, 25, 25), self.display_x/2 - 175, self.display_y/2 - self.titles_size * 0.75)
        self.resume = (50, 50, 50)
        self.resume = Button('Resume', self.quit_color, self.display_x/2 - 200, self.display_y/2 - 200, self.time, 400, 100, self.titles_size, (25, 25, 25), self.display_x/2 - 175, self.display_y/2 - 150 - self.titles_size * 0.75)

    def start(self, screen):
        self.startb.draw(screen, True)
        if self.startb.update(self.start_color):
            return True
        else:
            return False

    def pause(self, screen):
        self.resume.draw(screen, False)
        if self.resume.update(self.quit_color):
            self.is_resume = True
        else:
            self.is_resume = False
        
        self.restart.draw(screen, False)
        if self.restart.update(self.quit_color):
            self.is_restart = True
        else:
            self.is_restart = False
        
        self.quit.draw(screen, False)
        if self.quit.update(self.quit_color):
            self.is_quit = True
        else:
            self.is_quit = False

        return self.is_resume, self.is_restart, self.is_quit
    
    def end(self, screen):
        self.restart.draw(screen, False)
        if self.restart.update(self.quit_color):
            self.is_restart = True
        else:
            self.is_restart = False
        
        self.quit.draw(screen, False)
        if self.quit.update(self.quit_color):
            self.is_quit = True
        else:
            self.is_quit = False

        return self.is_restart, self.is_quit
        
        





class Item:
    def __init__(self, player, wall_g, wall_c, display_x, display_y, image):
        self.player = player
        self.wall_g = wall_g
        self.wall_c = wall_c
        self.display_x = display_x
        self.display_y = display_y
        self.image = image
        self.co = [self.display_x, random.randint(0, self.display_y - 100)]
        self.rect = self.image.get_rect(x=self.co[0], y=self.co[1])
        self.spawn = True

    def update(self):
        for w in self.wall_g:
            self.spawn += not w.rect.colliderect(self.rect)
        if self.spawn:
            self.co[0] += -self.wall_g[0].speed
        
        if self.player.rect[1] - 100 < self.co[1] < self.player.rect[1] + 100 and self.player.rect[0] - 100 < self.co[0] < self.player.rect[0] + 100:
            self.co = [self.display_x, 0]
            return True
        else:
            return False
        
    def draw(self, screen):
        screen.blit(self.image, self.co)









class Items:
    def __init__(self, player, wall_g, wall_c, display_x, display_y, wall_spawner):
        self.player = player
        self.wall_g = wall_g
        self.wall_c = wall_c
        self.display_x = display_x
        self.display_y = display_y
        self.wall_spawner = wall_spawner
        self.heart = pygame.image.load("Heart(resized).png").convert_alpha()
        self.life = Item(self.player, self.wall_g, self.wall_c, self.display_x, self.display_y, self.heart)
        self.life_spawn = False
        self.clock = pygame.image.load("Horloge(resized).png").convert_alpha()
        self.time = Item(self.player, self.wall_g, self.wall_c, self.display_x, self.display_y, self.clock)
        self.time_spawn = False

    def update(self):
        if random.randint(0, 3600) == 0 and self.player.life < 3:
            self.life_spawn = True
        if self.life_spawn:
            if self.life.update():
                self.life_spawn = False
                if self.player.life < 3:
                    self.player.life += 1
                self.life.__init__(self.player, self.wall_g, self.wall_c, self.display_x, self.display_y, self.heart)
            else:
                if self.life.co[0] < -100:
                    self.life_spawn = False
                    self.life.__init__(self.player, self.wall_g, self.wall_c, self.display_x, self.display_y, self.heart)
        
        if random.randint(0, 1200) == 0:
            self.time_spawn = True
        if self.time_spawn:
            if self.time.update():
                self.time_spawn = False
                for w in self.wall_g:
                    if w.speed > 5:
                        w.speed += -1
                for w in self.wall_c:
                    if w.speed > 5:
                        w.speed += -1    
                if self.wall_spawner.random_spawn_recurrence > 1:
                    self.wall_spawner.random_spawn_recurrence += int(self.wall_g[0].speed/2)
                if self.wall_spawner.spawn_recurrence > 1:
                    self.wall_spawner.spawn_recurrence += int(self.wall_g[0].speed/2)
                self.time.__init__(self.player, self.wall_g, self.wall_c, self.display_x, self.display_y, self.clock)
            else:
                if self.time.co[0] < -100:
                    self.time_spawn = False
                    self.time.__init__(self.player, self.wall_g, self.wall_c, self.display_x, self.display_y, self.clock)
    
    def draw(self, screen):
        self.life.draw(screen)
        self.time.draw(screen)










class Cloud:
    def __init__(self, display_x, display_y):
        self.display_x = display_x
        self.display_y = display_y
        self.cloud_choose = random.randint(1,4)
        if self.cloud_choose == 1:
            self.cloud = pygame.image.load("Nuage1.png").convert_alpha()
        elif self.cloud_choose == 2:
            self.cloud = pygame.image.load("Nuage2.png").convert_alpha()
        elif self.cloud_choose == 3:
            self.cloud = pygame.image.load("Nuage3.png").convert_alpha()
        else:
            self.cloud = pygame.image.load("Nuage4.png").convert_alpha()
        self.speed = random.random()
        self.height = random.randint(0, self.display_x * 0.20)
        self.co = [self.display_x, self.height]
    
    def update(self):
        self.co[0] += -self.speed
        if self.co[0] <= -300:
            self.cloud_choose = random.randint(1,4)
            if self.cloud_choose == 1:
                self.cloud = pygame.image.load("Nuage1.png").convert_alpha()
            elif self.cloud_choose == 2:
                self.cloud = pygame.image.load("Nuage2.png").convert_alpha()
            elif self.cloud_choose == 3:
                self.cloud = pygame.image.load("Nuage3.png").convert_alpha()
            else:
                self.cloud = pygame.image.load("Nuage4.png").convert_alpha()
            self.speed = random.random()
            self.height = random.randint(0, self.display_x * 0.20)
            self.co = [self.display_x, self.height]

    def draw(self, screen):
        screen.blit(self.cloud, self.co)









class Ground:
    def __init__(self, display_x, display_y, wall):
        self.display_x = display_x
        self.display_y = display_y
        self.wall = wall
        self.grass1 = pygame.image.load("Ground.png").convert_alpha()
        self.grass2 = pygame.image.load("Ground.png").convert_alpha()
        self.grass3 = pygame.image.load("Ground.png").convert_alpha()
        self.co1 = [0, self.display_y - 200]
        self.co2 = [1323, self.display_y - 200]
        self.co3 = [2646, self.display_y - 200]

    def update(self):
        self.co1[0] += -self.wall[0].speed
        self.co2[0] += -self.wall[0].speed
        self.co3[0] += -self.wall[0].speed
        if self.co1[0] < -1323:
            self.co1[0] = self.co3[0] + 1323
        if self.co2[0] < -1323:
            self.co2[0] = self.co2[0] + 1323
        if self.co3[0] < -1323:
            self.co3[0] = self.co1[0] + 1323


    def draw(self, screen):
        screen.blit(self.grass1, self.co1)
        screen.blit(self.grass2, self.co2)
        screen.blit(self.grass3, self.co3)










class Game:
    def __init__ (self, screen, display_x, display_y):
        self.display_x = display_x
        self.display_y = display_y
        self.screen = screen
        self.player = Player(self.display_x, self.display_y)
        self.time = Time()
        self.walls_g = [Wall_g(self.player, self.time, self.display_x, self.display_y) for i in range(0,5)]
        self.walls_c = [Wall_c(self.player, self.time, self.display_x, self.display_y) for i in range(0,5)]
        self.wall_spawner = Wall_spawner(self.walls_g, self.walls_c, self.time)
        self.items = Items(self.player, self.walls_g, self.walls_c, self.display_x, self.display_y, self.wall_spawner)
        self.hud = HUD(self.player, self.walls_g, self.time)
        self.menu = Menu(self.display_x, self.display_y, self.time)
        self.clouds = [Cloud(self.display_x, self.display_y) for i in range(0,4)]
        self.ground = Ground(self.display_x, self.display_y, self.walls_g)
        self.start = True
        self.echap = False
        self.end = False

    def handling_events (self):
        #Quitter le jeu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            #Saut
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.player.touch_floor:
                    self.player.velocity[1] += -15
                    self.player.touch_floor = False
                elif event.key == pygame.K_SPACE and self.player.double_jump:
                    self.player.velocity[1] += -15
                    self.player.double_jump = False
                #Dash vers le bas
                if event.key == pygame.K_s:
                    self.player.velocity[1] = 50
                #Echap
                if event.key == pygame.K_ESCAPE:
                    self.echap = not self.echap

        #Mouvements droite/guauche
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            if self.player.velocity[0] > -6:
                self.player.velocity[0] += -2
        if keys[pygame.K_d]:
            if self.player.velocity[0] < 6:
                self.player.velocity[0] += 2

        #Longueur du saut
        if keys[pygame.K_SPACE]:
            self.player.velocity[1] += -0.5
            self.start = False
    
    def update(self):
        for c in self.clouds:
            c.update()
        self.player.move()
        self.player.physic()
        self.wall_spawner.update()
        for w in self.walls_g:
            self.hud.score += w.move()
        for w in self.walls_c:
            self.hud.score += w.move()
        self.items.update()
        self.ground.update()
        #Mort
        damage = self.walls_g[0].physic() and self.walls_g[1].physic() and self.walls_g[2].physic() and self.walls_g[3].physic() and self.walls_g[4].physic() and self.walls_c[0].physic() and self.walls_c[1].physic() and self.walls_c[2].physic() and self.walls_c[3].physic() and self.walls_c[4].physic()
        if not damage and not self.player.recovery_time:
            self.player.life += -1
            self.player.recovery_time = True
            if self.player.life == 0:
                self.end = True

    def display(self):
        self.screen.fill((150, 150, 255))
        self.ground.draw(self.screen)
        for c in self.clouds:
            c.draw(self.screen)
        self.player.draw(self.screen)
        for wall in self.walls_g:
            wall.draw(self.screen)
        for wall in self.walls_c:
            wall.draw(self.screen)
        self.hud.draw(self.screen)
        self.items.draw(self.screen)
        
        if self.start:
            if self.menu.start(self.screen):
                self.start = False
                self.player.velocity[1] += -30
        
        if self.echap and not self.start and not self.end:
            self.pause = self.menu.pause(self.screen)
            if self.pause[0]:
                self.echap = False
            if self.pause[1]:
                self.__init__(screen, x, y)
            if self.pause[2]:
                pygame.quit()
        
        if self.end:
            self.end_menu = self.menu.end(self.screen)
            if self.end_menu[0]:
                self.__init__(screen, x, y)
            if self.end_menu[1]:
                pygame.quit()
        
        pygame.display.flip()
    
    def run(self):
        while True:
            while self.start:
                self.handling_events()
                self.display()
                self.time.fps(60, False)
            while self.echap:
                self.handling_events()
                self.display()
                self.time.fps(60, False)
            while self.end:
                self.handling_events()
                self.display()
                self.time.fps(60, False)
            self.handling_events()
            self.update()
            self.display()
            self.time.fps(60, True)




pygame.init()
co = pygame.display.get_desktop_sizes()
coo = co[0]
x = coo[0]
y = coo[1]
screen = pygame.display.set_mode((x, y))
game = Game(screen, x, y)
game.run()

pygame.quit()