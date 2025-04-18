import pygame
import time  # Import time module for tracking firing rate
import subprocess
from pause import pause_menu   # Import the pause_menu function

def game():
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

    #active projectiles list
    projectiles = []

    #projectiles settings
    projectile_size = 60 # 9x9 pixel size
    projectile_speed = .7

    #load projectile image + resize 
    projectile_image = pygame.image.load('Images/projectiles.png').convert_alpha()
    projectile_image = pygame.transform.scale(projectile_image, (projectile_size, projectile_size))
    projectile_image = pygame.transform.rotate(projectile_image, 180)

    #firing rate
    last_fired = 0  #timestamp last fired
    fire_rate = 0.3  #space between firing 

    #background starting position
    background_y1 = 0
    background_y2 = -background.get_height()

    running = True
    while running:
        #backgorund movement speed setting
        scroll_speed = 0.1
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

        #projectiles firing
        if keys[pygame.K_SPACE]:
            current_time = time.time()
            if current_time - last_fired >= fire_rate:  #check if enough time has passed
                #adding new projectile at spaceship coordinates
                projectiles.append([spaceship_x + spaceship_width // 2 - projectile_size // 2, spaceship_y])
                last_fired = current_time

        #updating projectile positions
        for projectile in projectiles:
            projectile[1] -= projectile_speed  #moving up

        #removing projectiles that are no longer visible
        projectiles = [p for p in projectiles if p[1] > 0]

        #showing projectiles
        for projectile in projectiles:
            screen.blit(projectile_image, (projectile[0], projectile[1]))

        #moving spaceship with wasd
        if keys[pygame.K_w] and spaceship_y > 700 // 2:  #restrict movement to lower 50% of screen
            spaceship_y -= spaceship_speed
        if keys[pygame.K_s] and spaceship_y < 700 - spaceship_height:
            spaceship_y += spaceship_speed
        if keys[pygame.K_a] and spaceship_x > 0:
            spaceship_x -= spaceship_speed
        if keys[pygame.K_d] and spaceship_x < 800 - spaceship_width:
            spaceship_x += spaceship_speed
        if keys[pygame.K_ESCAPE]:
            pause_menu(screen)  # Call the pause menu and pass the screen
            continue  # Resume the game loop after the pause menu is closed

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


if __name__ == "__main__":
    game()