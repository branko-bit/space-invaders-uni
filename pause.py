import pygame
import sys
import subprocess  # Import subprocess to run the main.py script
import main

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Fonts
pygame.font.init()
TITLE_FONT = pygame.font.Font(None, 74)
BUTTON_FONT = pygame.font.Font(None, 36)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders - Pause Menu")

button_click_sound = pygame.mixer.Sound('Sounds/button_click.wav')

background_image = pygame.image.load("Images/background.jpg").convert()

def draw_text(text, font, color, surface, x, y):
    """Helper function to draw text on the screen."""
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

def pause_menu(screen):
    """Pause menu loop."""
    while True:
        # Draw the background image
        screen.blit(background_image, (0, 0))  # Use blit to draw the image at the top-left corner

        # Draw title
        draw_text("Space Invaders", TITLE_FONT, WHITE, screen, SCREEN_WIDTH // 2, 100)

        # Draw buttons
        continue_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 75, 200, 50)
        settings_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50)
        main_menu_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 75, 200, 50)
        
        pygame.draw.rect(screen, GRAY, continue_button)
        draw_text("Continue", BUTTON_FONT, BLACK, screen, continue_button.centerx, continue_button.centery)
        pygame.draw.rect(screen, GRAY, settings_button)
        draw_text("Settings", BUTTON_FONT, BLACK, screen, settings_button.centerx, settings_button.centery)
        pygame.draw.rect(screen, GRAY, main_menu_button)
        draw_text("Main Menu", BUTTON_FONT, BLACK, screen, main_menu_button.centerx, main_menu_button.centery)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if continue_button.collidepoint(event.pos):
                    button_click_sound.play()  # Play button click sound
                    print("Continue clicked!")
                    # Resume game.py to start the game
                    return  # Exit the pause menu loop
                elif settings_button.collidepoint(event.pos):
                    button_click_sound.play()  # Play button click sound
                    print("Settings clicked!")
                    # Add logic to open settings
                elif main_menu_button.collidepoint(event.pos):
                    button_click_sound.play()  # Play button click sound
                    main.main_menu()  # Call the main menu function from main.py

        pygame.display.flip()

if __name__ == "__main__":
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Space Invaders - Pause Menu")
    pause_menu(screen)