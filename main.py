import pygame
import sys
import subprocess  # Import subprocess to run the main.py script

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
pygame.display.set_caption("Space Invaders - Main Menu")

# Load images for buttons
settings_icon = pygame.image.load("Images/settings_icon.png").convert_alpha()  # Replace with your actual image path
exit_icon = pygame.image.load("Images/exit_icon.png").convert_alpha()          # Replace with your actual image path

# Scale images to fit buttons
settings_icon = pygame.transform.scale(settings_icon, (50, 50))
exit_icon = pygame.transform.scale(exit_icon, (50, 50))

background_image = pygame.image.load("Images/background.jpg").convert()

def draw_text(text, font, color, surface, x, y):
    """Helper function to draw text on the screen."""
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

def main_menu():
    """Main menu loop."""
    while True:
        # Draw the background image
        screen.blit(background_image, (0, 0))  # Use blit to draw the image at the top-left corner

        # Draw title
        draw_text("Space Invaders", TITLE_FONT, WHITE, screen, SCREEN_WIDTH // 2, 100)

        # Draw buttons
        play_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 25, 200, 50)
        settings_button_rect = pygame.Rect(20, 20, 50, 50)
        exit_button_rect = pygame.Rect(20, 80, 50, 50)

        pygame.draw.rect(screen, GRAY, play_button)
        draw_text("Play Game", BUTTON_FONT, BLACK, screen, play_button.centerx, play_button.centery)

        # Draw icons for settings and exit
        screen.blit(settings_icon, (settings_button_rect.x, settings_button_rect.y))
        screen.blit(exit_icon, (exit_button_rect.x, exit_button_rect.y))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    print("Play Game clicked!")
                    # Run main.py to start the game
                    subprocess.Popen(["python", "main.py"], shell=True)
                elif settings_button_rect.collidepoint(event.pos):
                    print("Settings clicked!")
                    # Add logic to open settings
                elif exit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()

if __name__ == "__main__":
    main_menu()