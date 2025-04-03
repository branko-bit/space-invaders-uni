import pygame

#init pygame
pygame.init()

#game window
screen = pygame.display.set_mode((800, 700))  #width: x, height: y
pygame.display.set_caption("Space Invaders")

#load backgorund image
background = pygame.image.load('Images/background.jpg')

#background starting position
background_y1 = 0
background_y2 = -background.get_height()

# main game loop
running = True
while running:
    #backgorund movement speed setting
    scroll_speed = 0.3
    background_y1 += scroll_speed
    background_y2 += scroll_speed

    #resetting background image for movement effect
    if background_y1 >= background.get_height():
        background_y1 = -background.get_height()
    if background_y2 >= background.get_height():
        background_y2 = -background.get_height()

    screen.blit(background, (0, background_y1))
    screen.blit(background, (0, background_y2))

    #event handling for game quiting
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #updating the display
    pygame.display.update()

#closing game
pygame.quit()
