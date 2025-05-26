import pygame
import sys

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

TITLE_FONT = pygame.font.Font(None, 74)
BUTTON_FONT = pygame.font.Font(None, 36)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Spaceship Settings")

background_image = pygame.image.load("Images/background.jpg").convert()

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

def spaceship_settings_menu():
    ships = [
        pygame.image.load("Images/spaceship1.png").convert_alpha(),
        pygame.image.load("Images/spaceship2.png").convert_alpha(),
        pygame.image.load("Images/spaceship3.png").convert_alpha()
    ]
    ships = [pygame.transform.scale(s, (100, 100)) for s in ships]
    selected = 0  # default spaceship1
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
                if back_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
        pygame.display.flip()

if __name__ == "__main__":
    spaceship_settings_menu()
