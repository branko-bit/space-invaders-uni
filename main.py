import pygame

#init pygame
pygame.init()

#game window
screen = pygame.display.set_mode((800, 700))  #width: x, height: y
pygame.display.set_caption("Space Invaders")

#load backgorund image
background = pygame.image.load('Images/background.jpg')

#load spaceship image
spaceship = pygame.image.load('Images/spaceship.png').convert_alpha()
spaceship = pygame.transform.scale(spaceship, (50, 50))  #50x50 pixels 
spaceship_width = spaceship.get_width()
spaceship_height = spaceship.get_height()

#inital spaceship position
spaceship_x = (800 - spaceship_width) // 2 #center horizontally
spaceship_y = 700 - spaceship_height - 10  # place near bottom of screen

#space ship movement speed
spaceship_speed = .5

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

    #getting pressed keys input
    keys = pygame.key.get_pressed()

    #moving spaceship with wasd
    if keys[pygame.K_w] and spaceship_y > 700 // 2:  #restrict movement to lower 50% of screen
        spaceship_y -= spaceship_speed
    if keys[pygame.K_s] and spaceship_y < 700 - spaceship_height:
        spaceship_y += spaceship_speed
    if keys[pygame.K_a] and spaceship_x > 0:
        spaceship_x -= spaceship_speed
    if keys[pygame.K_d] and spaceship_x < 800 - spaceship_width:
        spaceship_x += spaceship_speed

    #showing spaceship image
    screen.blit(spaceship, (spaceship_x, spaceship_y))

    #event handling for game quiting
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #updating the display
    pygame.display.update()

#closing game
pygame.quit()
