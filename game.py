import pygame
import time  # Import time module for tracking firing rate
import subprocess
from pause import pause_menu   # Import the pause_menu function
import random  # Import random for enemy spawn positions
from game_over_screen import game_over_screen

#spaceship sound by Knoplund on freesound.org
#space sound by VABsounds on freesound.org
#boss laugh sound by supersound23 on freesound.org
#other sounds forgot to credit, sorry :(

def load_selected_ship():
    try:
        with open("selected_ship.txt", "r") as f:
            return int(f.read().strip())
    except:
        return 1  # default

def game(selected_ship=1):
    pygame.init()

    #game window
    screen = pygame.display.set_mode((800, 700))  #width: x, height: y
    pygame.display.set_caption("Space Invaders")

    #load backgorund image
    background = pygame.image.load('Images/background.jpg')

    #--------------PLAYER SECTION-----------------
    #load spaceship image
    spaceship = pygame.image.load(f'Images/spaceship{selected_ship}.png').convert_alpha()
    spaceship = pygame.transform.scale(spaceship, (100, 100))  #50x50 pixels 
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

    # Load blaster sound
    blaster_sound = pygame.mixer.Sound('Sounds/blaster_sound.wav')
    # Load button click sound
    button_click_sound = pygame.mixer.Sound('Sounds/button_click.wav')

    #background starting position
    background_y1 = 0
    background_y2 = -background.get_height()

    # Player HP
    player_hp = 100
    hp_font = pygame.font.Font(None, 36)  # Font for displaying HP

    # Player Rockets
    rocket_count = 25 # Initial rocket count
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

    # Background music
    pygame.mixer.music.load('Sounds/background.wav')  # Dodaj svojo glasbeno datoteko v Sounds/
    pygame.mixer.music.set_volume(0.1)  # Max volume
    pygame.mixer.music.play(-1)  # Loop indefinitely

    # Shield necessary settings
    shield_kill_counter = 0
    shield_active = False
    shield_image = pygame.image.load('Images/shield.png').convert_alpha()
    shield_image = pygame.transform.scale(shield_image, (60, 60))  # slightly larger than ship
    
    # Load health orb image
    health_orb_image = pygame.image.load('Images/health.png').convert_alpha()
    health_orb_image = pygame.transform.scale(health_orb_image, (50, 50))  # Bigger orb
    health_orbs = []  # List to store active health orbs
    
    # Load ammo drop image
    ammo_drop_image = pygame.image.load('Images/ammo_drop.png').convert_alpha()
    ammo_drop_image = pygame.transform.scale(ammo_drop_image, (50, 50))
    ammo_sound = pygame.mixer.Sound('Sounds/ammo_pickup_sfx.mp3')
    ammo_drops = []
    ammo_drop_spawn_rate = 10  # seconds between possible spawns
    last_ammo_drop_spawn = 0
    ammo_drop_speed = 0.1
    ammo_drop_spawn_chance = 0.35; # 35%

    # Load heal sound
    heal_sound = pygame.mixer.Sound('Sounds/heal_sound.wav')

    enemies_destroyed = 0  # Counter for destroyed enemies

    # Boss settings
    boss_image = pygame.image.load('Images/final-boss.png').convert_alpha()
    boss_image = pygame.transform.scale(boss_image, (120, 120))  # Boss is bigger
    boss_image = pygame.transform.rotate(boss_image, 180)  # Rotate the boss image
    boss_hp_max = 100
    boss_active = False
    boss = None  # [x, y, dx, dy, hp]
    boss_projectiles = []
    boss_projectile_speed = projectile_speed * 1.2
    boss_projectile_size = 21
    boss_projectile_image = pygame.transform.scale(enemy_projectile_image, (boss_projectile_size*1.5, boss_projectile_size*3))
    boss_spawned_at = 0
    boss_last_shot = 0  # <-- dodano za boss cooldown

    # Load boss spawn sound
    boss_spawn_sound = pygame.mixer.Sound('Sounds/boss-spawn.wav')

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
                blaster_sound.play()  # Play blaster sound
                last_fired = current_time
                rocket_count -= 1  # Deduct one rocket
        
        #shield activation
        if keys[pygame.K_f] and shield_kill_counter >= 4 and not shield_active:
            shield_active = True
            shield_kill_counter = 0 # Reset the counter after activation
        
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
            button_click_sound.play()
            pause_menu(screen)  # Call the pause menu and pass the screen
            continue  # Resume the game loop after the pause menu is closed

        #showing spaceship image
        screen.blit(spaceship, (spaceship_x, spaceship_y))

        # showing shield if active
        if shield_active:
            screen.blit(shield_image, (spaceship_x - 5, spaceship_y - 5))  # Adjust for alignment

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

        # Ammo drop spawning
        if current_time - last_ammo_drop_spawn >= ammo_drop_spawn_rate:
            if random.random() < ammo_drop_spawn_chance:  # % chance to spawn each interval
                ammo_x = random.randint(0, 800 - 50)
                ammo_drops.append([ammo_x, 0])  # Start at top of screen
            last_ammo_drop_spawn = current_time

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
                        if not shield_active:
                            shield_kill_counter += 1
                            if shield_kill_counter > 4:
                                shield_kill_counter = 4  # Cap the counter at 4
                        # Health orb drop logic
                        enemies_destroyed += 1
                        if enemies_destroyed % 3 == 0:
                            # Drop a health orb at the enemy's position
                            health_orbs.append([enemy[0] + 10, enemy[1] + 10])
                    break

        # Update and draw health orbs
        for orb in health_orbs:
            orb[1] += 0.08  # Slower descent speed

        # Update ammo drops
        for drop in ammo_drops:
            drop[1] += ammo_drop_speed  # Move down

        # Check for collision between player and health orbs
        for orb in health_orbs[:]:
            if (spaceship_x < orb[0] < spaceship_x + spaceship_width and
                spaceship_y < orb[1] < spaceship_y + spaceship_height):
                player_hp = min(player_hp + 10, 100)  # Heal 10 HP, max 100
                heal_sound.play()  # Play heal sound
                health_orbs.remove(orb)

        # Check for collision between player and ammo drops
        for drop in ammo_drops[:]:
            if (spaceship_x < drop[0] < spaceship_x + spaceship_width and
                spaceship_y < drop[1] < spaceship_y + spaceship_height):
                rocket_count += random.randint(5, 15)
                ammo_sound.play()
                ammo_drops.remove(drop)
            elif drop[1] > 700:
                ammo_drops.remove(drop)  # Remove if off screen

        # Draw health orbs
        for orb in health_orbs:
            screen.blit(health_orb_image, (orb[0], orb[1]))

        # Draw ammo drops
        for drop in ammo_drops:
            screen.blit(ammo_drop_image, (drop[0], drop[1]))

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
                if shield_active:
                    shield_active = False  # Absorb one hit due to shield activation
                else:
                    player_hp -= 10  # Reduce player HP by 10
                enemy_projectiles.remove(projectile)  # Remove the projectile

        # Boss spawn logic
        if not boss_active and enemies_destroyed > 0 and enemies_destroyed % 10 == 0:
            boss_x = random.randint(0, 800 - 120)
            boss_y = 10
            boss_dx = random.uniform(0.08, 0.15) * random.choice([-1, 1])
            boss_dy = random.uniform(0.05, 0.1)
            boss = [boss_x, boss_y, boss_dx, boss_dy, boss_hp_max]
            boss_active = True
            boss_spawned_at = enemies_destroyed
            boss_last_shot = time.time()  # reset cooldown
            boss_spawn_sound.play()  # Play boss spawn sound

        # Boss movement and drawing
        if boss_active and boss:
            boss[0] += boss[2]
            boss[1] += boss[3]
            # Keep boss within screen
            if boss[0] <= 0 or boss[0] >= 800 - 120:
                boss[2] = -boss[2]
            if boss[1] <= 0 or boss[1] >= 700 * 0.3 - 120:
                boss[3] = -boss[3]
            screen.blit(boss_image, (boss[0], boss[1]))
            # Boss health bar
            boss_health_bar_width = 120
            boss_health_bar_height = 12
            boss_health_ratio = boss[4] / boss_hp_max
            pygame.draw.rect(screen, (255, 0, 0), (boss[0], boss[1] - 18, boss_health_bar_width, boss_health_bar_height))
            pygame.draw.rect(screen, (0, 0, 255), (boss[0], boss[1] - 18, boss_health_bar_width * boss_health_ratio, boss_health_bar_height))

            # Boss fires one projectile every 1.5 seconds
            if time.time() - boss_last_shot >= 1.5:
                boss_projectiles.append([boss[0] + 60, boss[1] + 120])
                boss_last_shot = time.time()

        # Boss projectile movement
        for bp in boss_projectiles:
            bp[1] += boss_projectile_speed
        boss_projectiles = [bp for bp in boss_projectiles if bp[1] < 700]

        # Draw boss projectiles
        for bp in boss_projectiles:
            screen.blit(boss_projectile_image, (bp[0], bp[1]))

        # Boss projectile collision with player
        for bp in boss_projectiles[:]:
            if spaceship_x < bp[0] < spaceship_x + spaceship_width and spaceship_y < bp[1] < spaceship_y + spaceship_height:
                if shield_active:
                    shield_active = False
                else:
                    player_hp -= 40  # Boss projectile does 40 damage
                boss_projectiles.remove(bp)

        # Boss hit by player projectile
        if boss_active and boss:
            for projectile in projectiles[:]:
                if boss[0] - 10 < projectile[0] < boss[0] + 130 and boss[1] - 10 < projectile[1] < boss[1] + 130:
                    boss[4] -= 10
                    projectiles.remove(projectile)
                    if boss[4] <= 0:
                        boss_active = False
                        boss = None
                        high_score += 150
                        rocket_count += 15
                        shield_active = True
                        shield_kill_counter = 0
                        boss_projectiles.clear()
                        enemies_destroyed += 1

        # If player HP reaches 0, stop the game and show the "Game Over" screen
        if player_hp <= 0:
            # Reset boss state for next game
            boss_active = False
            boss = None
            boss_projectiles.clear()
            pygame.mixer.music.stop()  # Stop the background music
            game_over_screen(screen, high_score)
            return

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
        
        # Draw shield status at the top-left corner
        if shield_active:
            shield_text = rocket_font.render("Shield: Active", True, (0, 191, 255))  # Deep Sky Blue
        elif shield_kill_counter >= 4:
            shield_text = rocket_font.render("Shield is ready! Press F to activate", True, (0, 191, 255))
        else:
            shield_text = rocket_font.render(f"Shield: {shield_kill_counter}/4", True, (0, 191, 255))
        screen.blit(shield_text, (20, 20))  # Top-left corner

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