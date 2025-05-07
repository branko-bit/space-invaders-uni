import pygame
import sys

def game_over_screen(screen, high_score):
    pygame.font.init()

    # Fonts for text
    game_over_font = pygame.font.Font(None, 74)
    score_font = pygame.font.Font(None, 36)
    button_font = pygame.font.Font(None, 36)

    while True:
        screen.fill((0, 0, 0))  # Black background

        # Display "GAME OVER" text
        game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))  # Red text
        game_over_rect = game_over_text.get_rect(center=(800 // 2, 700 // 2 - 100))
        screen.blit(game_over_text, game_over_rect)

        # Display high score
        score_text = score_font.render(f"High Score: {high_score}", True, (255, 255, 0))  # Yellow text
        score_rect = score_text.get_rect(center=(800 // 2, 700 // 2 - 40))
        screen.blit(score_text, score_rect)

        # Display "Main Menu" button
        main_menu_button = pygame.Rect(800 // 2 - 100, 700 // 2 + 50, 200, 50)
        pygame.draw.rect(screen, (200, 200, 200), main_menu_button)
        button_text = button_font.render("Main Menu", True, (0, 0, 0))
        button_text_rect = button_text.get_rect(center=main_menu_button.center)
        screen.blit(button_text, button_text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if main_menu_button.collidepoint(event.pos):
                    return  # Exit the game_over_screen and return to the main menu

        pygame.display.flip()
