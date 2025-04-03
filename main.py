import pygame

#init pygame
pygame.init()

#game window
screen = pygame.display.set_mode((800, 700))  #width: x, height: y
pygame.display.set_caption("Space Invaders")

# main game loop
running = True
while running:
    #for now black color background
    screen.fill((0, 0, 0))

    #event handling for game quiting
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #updating the display
    pygame.display.update()

#closing game
pygame.quit()
