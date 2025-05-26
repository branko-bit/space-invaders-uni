import pygame
import sys
import subprocess  
import game
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

pygame.font.init()
TITLE_FONT = pygame.font.Font(None, 74)
BUTTON_FONT = pygame.font.Font(None, 36)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders - Main Menu")

settings_icon = pygame.image.load("Images/settings_icon.png").convert_alpha()
exit_icon = pygame.image.load("Images/exit_icon.png").convert_alpha()

settings_icon = pygame.transform.scale(settings_icon, (50, 50))
exit_icon = pygame.transform.scale(exit_icon, (50, 50))

background_image = pygame.image.load("Images/background.jpg").convert()

# Load button click sound
button_click_sound = pygame.mixer.Sound('Sounds/button_click.wav')

# Load and play menu music (loop)
pygame.mixer.music.load('Sounds/main-menu.wav')  # Dodaj svojo glasbeno datoteko v Sounds/
pygame.mixer.music.set_volume(1.0)  # Set to maximum volume (100%)
pygame.mixer.music.play(-1)  # Loop indefinitely

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

selected_ship = 1  # default spaceship1

def spaceship_settings_menu():
    global selected_ship
    ships = [
        pygame.image.load("Images/spaceship1.png").convert_alpha(),
        pygame.image.load("Images/spaceship2.png").convert_alpha(),
        pygame.image.load("Images/spaceship3.png").convert_alpha()
    ]
    ships = [pygame.transform.scale(s, (100, 100)) for s in ships]
    selected = selected_ship - 1
    running = True
    while running:
        screen.blit(background_image, (0, 0))
        draw_text("Choose your spaceship", TITLE_FONT, WHITE, screen, SCREEN_WIDTH // 2, 100)
        for i, ship in enumerate(ships):
            x = SCREEN_WIDTH // 2 - 160 + i * 160
            y = SCREEN_HEIGHT // 2 - 50
            screen.blit(ship, (x, y))
            border_color = (0,255,0) if i == selected else (255,255,255)
            pygame.draw.rect(screen, border_color, (x-5, y-5, 110, 110), 4)
            draw_text(f"{i+1}", BUTTON_FONT, WHITE, screen, x+50, y+120)
        back_button = pygame.Rect(20, 20, 120, 40)
        pygame.draw.rect(screen, GRAY, back_button)
        draw_text("Back", BUTTON_FONT, BLACK, screen, back_button.centerx, back_button.centery)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                for i in range(3):
                    x = SCREEN_WIDTH // 2 - 160 + i * 160
                    y = SCREEN_HEIGHT // 2 - 50
                    if x <= mx <= x+100 and y <= my <= y+100:
                        selected = i
                        selected_ship = i + 1
                if back_button.collidepoint(event.pos):
                    return
        pygame.display.flip()

def main_menu():
    global selected_ship
    menu_music_playing = True
    while True:
        screen.blit(background_image, (0, 0)) 

        draw_text("Space Invaders", TITLE_FONT, WHITE, screen, SCREEN_WIDTH // 2, 100)

        play_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 25, 200, 50)
        spaceship_settings_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 50)
        settings_button_rect = pygame.Rect(20, 20, 50, 50)
        exit_button_rect = pygame.Rect(20, 80, 50, 50)

        pygame.draw.rect(screen, GRAY, play_button)
        draw_text("Play Game", BUTTON_FONT, BLACK, screen, play_button.centerx, play_button.centery)

        pygame.draw.rect(screen, GRAY, spaceship_settings_button)
        draw_text("Settings", BUTTON_FONT, BLACK, screen, spaceship_settings_button.centerx, spaceship_settings_button.centery)

        screen.blit(settings_icon, (settings_button_rect.x, settings_button_rect.y))
        screen.blit(exit_icon, (exit_button_rect.x, exit_button_rect.y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    button_click_sound.play()
                    if menu_music_playing:
                        pygame.mixer.music.stop()
                        menu_music_playing = False
                    print("Play Game clicked!")
                    game.game(selected_ship)
                elif spaceship_settings_button.collidepoint(event.pos):
                    button_click_sound.play()
                    spaceship_settings_menu()
                elif settings_button_rect.collidepoint(event.pos):
                    button_click_sound.play()
                    if menu_music_playing:
                        pygame.mixer.music.stop()
                        menu_music_playing = False
                    print("Settings clicked!")
                elif exit_button_rect.collidepoint(event.pos):
                    button_click_sound.play()
                    if menu_music_playing:
                        pygame.mixer.music.stop()
                        menu_music_playing = False
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()

if __name__ == "__main__":
    main_menu()