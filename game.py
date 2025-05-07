import pygame
import time  # Import time module for tracking firing rate
import subprocess
from pause import pause_menu   # Import the pause_menu function
import random  # Import random for enemy spawn positions
from game_over_screen import game_over_screen

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

    # Player HP
    player_hp = 100
    hp_font = pygame.font.Font(None, 36)  # Font for displaying HP

    # Player Rockets
    rocket_count = 10
    rocket_font = pygame.font.Font(None, 36)  # Font for displaying rocket count

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

    # High Score
    high_score = 0
    score_font = pygame.font.Font(None, 36)  # Font for displaying the high score

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
        if keys[pygame.K_SPACE] and rocket_count > 0:  # Only fire if rockets are available
            current_time = time.time()
            if current_time - last_fired >= fire_rate:  #check if enough time has passed
                #adding new projectile at spaceship coordinates
                projectiles.append([spaceship_x + spaceship_width // 2 - projectile_size // 2, spaceship_y])
                last_fired = current_time
                rocket_count -= 1  # Deduct one rocket

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
            enemy_hp = 30  # Set initial HP for the enemy
            enemies.append([enemy_x, enemy_y, enemy_dx, enemy_dy, enemy_hp])  # Add enemy with movement speeds and HP
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

        # Detect collisions between projectiles and enemies
        for projectile in projectiles[:]:
            for enemy in enemies[:]:
                # Increase the hitbox by expanding the collision area
                if enemy[0] - 10 < projectile[0] < enemy[0] + 60 and enemy[1] - 10 < projectile[1] < enemy[1] + 60:
                    enemy[4] -= 10  # Reduce enemy HP by 10
                    projectiles.remove(projectile)  # Remove the projectile
                    if enemy[4] <= 0:  # If enemy HP reaches 0, remove the enemy
                        enemies.remove(enemy)
                        high_score += 10  # Increase high score by 10
                        rocket_count += 4  # Award 4 rockets for killing an enemy
                    break

        # Draw enemies and their health bars
        for enemy in enemies:
            screen.blit(enemy_image, (enemy[0], enemy[1]))

            # Draw health bar
            health_bar_width = 50
            health_bar_height = 5
            health_ratio = enemy[4] / 30  # Calculate health ratio (current HP / max HP)
            health_bar_color = (0, 255, 0)
            pygame.draw.rect(screen, (255, 0, 0), (enemy[0], enemy[1] - 10, health_bar_width, health_bar_height))  # Red background
            pygame.draw.rect(screen, health_bar_color, (enemy[0], enemy[1] - 10, health_bar_width * health_ratio, health_bar_height))  # Green foreground

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

        # Detect collisions between enemy projectiles and the player
        for projectile in enemy_projectiles[:]:
            if spaceship_x < projectile[0] < spaceship_x + spaceship_width and spaceship_y < projectile[1] < spaceship_y + spaceship_height:
                player_hp -= 10  # Reduce player HP by 10
                enemy_projectiles.remove(projectile)  # Remove the projectile

        # If player HP reaches 0, stop the game and show the "Game Over" screen
        if player_hp <= 0:
            game_over_screen(screen, high_score)  # Pass the screen and high score to the game over screen
            return  # Exit the game loop and return to the main menu

        # Draw enemy projectiles
        for projectile in enemy_projectiles:
            screen.blit(enemy_projectile_image, (projectile[0], projectile[1]))

        # Draw high score at the bottom-left corner
        score_text = score_font.render(f"Score: {high_score}", True, (255, 255, 0))  # Yellow text
        screen.blit(score_text, (20, 700 - 40))  # Position at bottom-left corner

        # Draw player HP at the bottom-right corner
        hp_text = hp_font.render(f"HP: {player_hp}", True, (0, 255, 0))  # Green text
        screen.blit(hp_text, (800 - 120, 700 - 40))  # Position at bottom-right corner

        # Draw rocket count at the top-right corner
        rocket_text = rocket_font.render(f"Rockets: {rocket_count}", True, (255, 255, 255))  # White text
        screen.blit(rocket_text, (800 - 150, 20))  # Position at top-right corner

        # If rocket count is 0, display a warning message
        if rocket_count == 0:
            no_rockets_text = rocket_font.render("Out of Rockets!", True, (255, 0, 0))  # Red text
            screen.blit(no_rockets_text, (800 // 2 - 100, 700 - 80))  # Display at the bottom center

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