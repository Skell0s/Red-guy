import pygame

pygame.init()
screen = pygame.display.set_mode((1800, 900))
player = pygame.image.load("Ballon de plage(resized).png").convert()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.player.convert_alpha
    screen.blit(player, (0, 0))
    pygame.display.flip()