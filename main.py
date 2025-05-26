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

def main_menu():
    menu_music_playing = True  # Flag to track if menu music is playing
    while True:
        screen.blit(background_image, (0, 0)) 

        draw_text("Space Invaders", TITLE_FONT, WHITE, screen, SCREEN_WIDTH // 2, 100)

        play_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 25, 200, 50)
        settings_button_rect = pygame.Rect(20, 20, 50, 50)
        exit_button_rect = pygame.Rect(20, 80, 50, 50)

        pygame.draw.rect(screen, GRAY, play_button)
        draw_text("Play Game", BUTTON_FONT, BLACK, screen, play_button.centerx, play_button.centery)

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
                    game.game()
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