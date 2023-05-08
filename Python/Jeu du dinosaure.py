import pygame, random

pygame.init()

screen = pygame.display.set_mode((1800, 900))
player = pygame.image.load("Ballon de plage(resized).png").convert()

#Score
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)
score = 0
score_past = 1
speed = 1

first_rectx = random.randint(5, 7) * 300
first_rect2x = random.randint(5, 7) * 300

#Mur sol
rect_height = random.randint(100, 700)
recty = 900 - rect_height
rectx = 1800
if first_rectx - first_rect2x > 300 or first_rect2x - first_rectx > 300:
    rectx = first_rectx
rectx_save = 1800
vrectx = -2


#Mur plafond
rect2_height = random.randint(100, 700)
rect2y = 0
rect2x = 2100
if first_rectx - first_rect2x > 300 or first_rect2x - first_rectx > 300:
    rect2x = first_rect2x
rect2x_save = 2100
vrect2x = -2



clock = pygame.time.Clock()

vx = 0
vy = 0

x = 0
y = 0

touch_floor = False
double_jump = False

running = True

while running:

    screen.fill((0, 0, 0))
    
    
    #Apparition/Disparition du murs sol
    if rectx + 100 < 0:
        first_rectx = random.randint(6, 7) * 300
        if rectx == rect2x:
            rect2x = rect2x + 300
        rect_height = random.randint(100, 700)
        recty = 900 - rect_height
        rectx = first_rectx
        rectx_save = first_rectx
        score += 1
        if score == score_past * 3:
            vrectx += -1
            speed = -vrectx
            score_past = score
    pygame.draw.rect(screen, (100, 100, 100), (rectx, recty, 100, rect_height))
    rectx += vrectx
    #Apparition/Disparition du murs plafond
    if rect2x + 100 < 0:
        first_rect2x = random.randint(6, 7) * 300
        if rectx == rect2x:
            rect2x = rect2x + 300
        rect2_height = random.randint(100, 700)
        rect2y = 0
        rect2x = first_rect2x
        rect2x_save = first_rect2x
        score += 1
        if score == score_past * 3:
            vrectx += -1
            speed = -vrectx
            score_past = score
    pygame.draw.rect(screen, (100, 100, 100), (rect2x, rect2y, 100, rect2_height))
    rect2x += vrectx
    if rectx == rect2x:
            rect2x = rect2x + 300


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and touch_floor:
                vy += -20
            elif event.key == pygame.K_SPACE and double_jump:
                vy += -25
                double_jump = False
            if event.key == pygame.K_s:
                vy += 50
            
    
    
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_q]:
        if vx > -10:
            vx += -2
    if pressed[pygame.K_d]:
        if vx < 10:
            vx += 2
    #if pressed[pygame.K_DOWN]:
        #vy += 3
    #if pressed[pygame.K_UP]:
        #vy += -3

    #Accélération
    x += vx
    y += vy

    #Gravité
    vy += 1

    #Frottement sol
    if vx > 0:
            vx += -1
    if vx < 0:
            vx += 1
    
    #Collisions
    #Sol
    if y > 800:
        vy = 0
        y = 800
    #Activation des pouvoirs
    if y >= 800:
        touch_floor = True
        double_jump = True
    else:
        touch_floor = False

    #Limitites du terrain
    if x > 1800:
        vx = 0
        x = 1800
    if x < 0:
        vx = 0
        x = 0

    #Collisions objects
    #Mur sol
    if x + 100 > rectx and x < rectx and y + 50 > recty or x > rectx and x < rectx + 100 and y + 50> recty:
        if x + 100 > rectx and x < rectx and y + 100 > recty:
            x = rectx - 100
            running = False
        if x > rectx and x < rectx + 100 and y + 100 > recty:
            x = rectx + 100
            running = False
    if x + 100 > rectx and x < rectx and y + 100 > recty or x > rectx and x < rectx + 100 and y + 100 > recty:
        vy = 0
        y = recty - 100
        x += vrectx * 2
        touch_floor = True
        double_jump = True

    #Mur plafond
    if x + 100 > rect2x and x < rect2x and y < rect2_height or x > rect2x and x < rect2x + 100 and y < rect2_height:
        if x + 100 > rect2x and x < rect2x and y < rect2_height:
            x = rect2x - 100
            running = False
        if x > rect2x and x < rect2x + 100 and y < rect2_height :
            x = rect2x + 100
            running = False
    

    text_surface = my_font.render(f'Score : {score}', False, (255, 255, 255))
    text_surface2 = my_font.render(f'Vitesse : {speed}', False, (255, 255, 255))
    screen.blit(text_surface, (0,0))
    screen.blit(text_surface2, (0,30))
    screen.blit(player, (x, y))
    pygame.display.flip()
    clock.tick(60)

clock.tick(600)
pygame.quit