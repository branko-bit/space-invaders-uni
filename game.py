import pygame
import time  # Import time module for tracking firing rate
import subprocess
from pause import pause_menu   # Import the pause_menu function
import random  # Import random for enemy spawn positions

def game():
    #init pygame
    pygame.init()

    #game window
    screen = pygame.display.set_mode((800, 700))  #width: x, height: y
    pygame.display.set_caption("Space Invaders")

    #load backgorund image
    background = pygame.image.load('Images/background.jpg')

    #--------------PLAYER SECTION-----------------
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

    #---------------ENEMY SECTION------------------
    # Enemy settings
    enemy_image = pygame.image.load('Images/enemy.png').convert_alpha()
    enemy_image = pygame.transform.scale(enemy_image, (50, 50))
    enemies = []
    enemy_spawn_rate = 3  # spawn rate v sekundah
    last_enemy_spawn = 0  # Timestamp of the last enemy spawn
    enemy_speed_range = (0.05, 0.2)  # Random speed range for movement
    enemy_direction_change_rate = 1.0  # Change direction every 1 second
    last_direction_change = 0  # Timestamp of the last direction change
    enemy_projectile_size = 7

    # Enemy projectile settings
    enemy_projectile_image = pygame.image.load('Images/enemy_laser.png').convert_alpha()
    enemy_projectile_image = pygame.transform.scale(enemy_projectile_image, (enemy_projectile_size, enemy_projectile_size*4))
    enemy_projectiles = []  # List to store enemy projectiles
    enemy_fire_intervals = {}  # Dictionary to track random fire intervals for each enemy

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

        #-----------------ENEMY SECTION-----------------
        current_time = time.time()
        if current_time - last_enemy_spawn >= enemy_spawn_rate and len(enemies) < 5:
            enemy_x = random.randint(0, 800 - 50)  # Random x position within screen width
            enemy_y = random.randint(0, int(700 * 0.3) - 50)  # Random y position within the top 30% of the screen
            enemy_dx = random.uniform(*enemy_speed_range) * random.choice([-1, 1])  # Random horizontal speed
            enemy_dy = random.uniform(*enemy_speed_range) * random.choice([-1, 1])  # Random vertical speed
            enemies.append([enemy_x, enemy_y, enemy_dx, enemy_dy])  # Add enemy with movement speeds
            enemy_fire_intervals[len(enemies) - 1] = current_time + random.uniform(1, 3)  # Set random fire time
            last_enemy_spawn = current_time

        # Update enemy positions
        if current_time - last_direction_change >= enemy_direction_change_rate:
            for enemy in enemies:
                enemy[2] = random.uniform(*enemy_speed_range) * random.choice([-1, 1])  # Change horizontal speed
                enemy[3] = random.uniform(*enemy_speed_range) * random.choice([-1, 1])  # Change vertical speed
            last_direction_change = current_time

        for enemy in enemies:
            enemy[0] += enemy[2]  # Move enemy horizontally
            enemy[1] += enemy[3]  # Move enemy vertically

            # Keep enemies within the top 30% of the screen
            if enemy[0] <= 0 or enemy[0] >= 800 - 50:
                enemy[2] = -enemy[2]  # Reverse horizontal direction if hitting screen edges
            if enemy[1] <= 0 or enemy[1] >= 700 * 0.3 - 50:
                enemy[3] = -enemy[3]  # Reverse vertical direction if hitting top or bottom bounds

        # Enemies fire projectiles at random intervals
        for i, enemy in enumerate(enemies):
            if i in enemy_fire_intervals and current_time >= enemy_fire_intervals[i]:
                enemy_projectiles.append([enemy[0], enemy[1] + 10])  # Adjust projectile position closer to the enemy
                enemy_fire_intervals[i] = current_time + random.uniform(2, 4)  # Reset random fire time

        # Update enemy projectile positionsa
        for projectile in enemy_projectiles:
            projectile[1] += projectile_speed  # Move downward

        # Remove enemy projectiles that move off-screen
        enemy_projectiles = [p for p in enemy_projectiles if p[1] < 700]

        # Draw enemies
        for enemy in enemies:
            screen.blit(enemy_image, (enemy[0], enemy[1]))

        # Draw enemy projectiles
        for projectile in enemy_projectiles:
            screen.blit(enemy_projectile_image, (projectile[0], projectile[1]))

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