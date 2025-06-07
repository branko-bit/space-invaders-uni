import pygame
import sys
import subprocess  
import game
import json
import os
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

LEADERBOARD_FILE = "leaderboard.json"

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

def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    try:
        with open(LEADERBOARD_FILE, "r", encoding="utf-8") as f:
            data = f.read().strip()
            if not data:
                return []
            return json.loads(data)
    except Exception:
        return []

def save_leaderboard(leaderboard):
    with open(LEADERBOARD_FILE, "w", encoding="utf-8") as f:
        json.dump(leaderboard, f, indent=2)

def add_to_leaderboard(name, score):
    leaderboard = load_leaderboard()
    updated = False
    for entry in leaderboard:
        if entry["name"] == name:
            if score > entry["score"]:
                entry["score"] = score  # Update only if new score is higher
            updated = True
            break
    if not updated:
        leaderboard.append({"name": name, "score": score})
    leaderboard = sorted(leaderboard, key=lambda x: x["score"], reverse=True)[:10]  # Keep top 10
    save_leaderboard(leaderboard)

def leaderboard_screen(surface, leaderboard):
    # Lower the leaderboard by increasing the y-coordinates
    draw_text("Leaderboard", BUTTON_FONT, WHITE, surface, 150, 180)  # was 120
    for idx, entry in enumerate(leaderboard[:10]):
        text = f"{idx+1}. {entry['name']} - {entry['score']}"
        draw_text(text, BUTTON_FONT, WHITE, surface, 150, 220 + idx * 30)  # was 160 + idx*30

def name_input_screen():
    input_box = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 25, 300, 50)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ""
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = True
                else:
                    active = False
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        if text.strip():
                            return text.strip()
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    elif len(text) < 12:
                        text += event.unicode
        color = color_active if active else color_inactive
        screen.blit(background_image, (0, 0))
        draw_text("Enter your name:", BUTTON_FONT, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60)
        pygame.draw.rect(screen, color, input_box, 2)
        txt_surface = BUTTON_FONT.render(text, True, WHITE)
        screen.blit(txt_surface, (input_box.x + 10, input_box.y + 10))
        pygame.display.flip()

def main_menu():
    global selected_ship
    menu_music_playing = True
    leaderboard = load_leaderboard()
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

        # Draw leaderboard on the left side
        leaderboard_screen(screen, leaderboard)

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
                    player_name = name_input_screen()
                    # Play the game and get the score
                    score = game.game(selected_ship, player_name)
                    if score is not None:
                        add_to_leaderboard(player_name, score)
                        leaderboard = load_leaderboard()
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