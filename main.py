import pygame

from modes.number_mode import NumberMode
from modes.word_mode import WordMode


# =========================
# INITIALIZE PYGAME
# =========================

pygame.init()


# =========================
# CONFIG
# =========================

WIDTH = 1000
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cow and Bulls")

clock = pygame.time.Clock()


# =========================
# COLORS
# =========================

BACKGROUND = (245, 235, 210)
TEXT_COLOR = (50, 40, 30)

BUTTON_COLOR = (120, 170, 100)
BUTTON_HOVER = (150, 200, 130)


# =========================
# FONTS
# =========================

title_font = pygame.font.Font(None, 80)
button_font = pygame.font.Font(None, 45)


# =========================
# GAME STATE
# =========================

current_menu = "main"


# =========================
# CREATE GAME MODES
# =========================

number_mode = NumberMode(screen)
word_mode = WordMode(screen)


# =========================
# BUTTON FUNCTION
# =========================

def draw_button(rect, text, mouse_pos):

    if rect.collidepoint(mouse_pos):
        color = BUTTON_HOVER
    else:
        color = BUTTON_COLOR

    pygame.draw.rect(
        screen,
        color,
        rect,
        border_radius=15
    )

    text_surface = button_font.render(
        text,
        True,
        TEXT_COLOR
    )

    screen.blit(
        text_surface,
        text_surface.get_rect(
            center=rect.center
        )
    )


# =========================
# BUTTONS
# =========================

game_mode_button = pygame.Rect(
    350, 300, 300, 70
)

quit_button = pygame.Rect(
    350, 400, 300, 70
)

number_mode_button = pygame.Rect(
    350, 250, 300, 70
)

word_mode_button = pygame.Rect(
    350, 350, 300, 70
)

back_button = pygame.Rect(
    350, 450, 300, 70
)


# =========================
# MAIN LOOP
# =========================

running = True

while running:

    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():

        # =====================
        # CLOSE WINDOW
        # =====================

        if event.type == pygame.QUIT:
            running = False
            continue


        # =====================
        # ESC
        # =====================

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:

                if current_menu == "number":
                    current_menu = "mode"

                elif current_menu == "word":
                    current_menu = "mode"

                elif current_menu == "mode":
                    current_menu = "main"

                elif current_menu == "main":
                    running = False

                continue


        # =====================
        # MOUSE CLICK
        # =====================

        if event.type != pygame.MOUSEBUTTONDOWN:
            continue


        # =====================
        # MAIN MENU
        # =====================

        if current_menu == "main":

            if game_mode_button.collidepoint(event.pos):

                print("Opening GAME MODE")
                current_menu = "mode"

            elif quit_button.collidepoint(event.pos):

                print("QUIT")
                running = False


        # =====================
        # GAME MODE MENU
        # =====================

        elif current_menu == "mode":

            if number_mode_button.collidepoint(event.pos):

                print("Opening NUMBER MODE")
                current_menu = "number"

            elif word_mode_button.collidepoint(event.pos):

                print("Opening WORD MODE")
                current_menu = "word"

            elif back_button.collidepoint(event.pos):

                print("Back to MAIN MENU")
                current_menu = "main"


        # =====================
        # NUMBER MODE
        # =====================

        elif current_menu == "number":

            result = number_mode.handle_events(event)

            if result == "back":
                current_menu = "mode"


        # =====================
        # WORD MODE
        # =====================

        elif current_menu == "word":

            result = word_mode.handle_events(event)

            if result == "back":
                current_menu = "mode"


    # =========================
    # DRAW CURRENT SCREEN
    # =========================

    if current_menu == "main":

        screen.fill(BACKGROUND)

        title = title_font.render(
            "COW AND BULLS",
            True,
            TEXT_COLOR
        )

        screen.blit(
            title,
            title.get_rect(
                center=(WIDTH // 2, 150)
            )
        )

        draw_button(
            game_mode_button,
            "GAME MODE",
            mouse_pos
        )

        draw_button(
            quit_button,
            "QUIT",
            mouse_pos
        )


    elif current_menu == "mode":

        screen.fill(BACKGROUND)

        title = title_font.render(
            "GAME MODE",
            True,
            TEXT_COLOR
        )

        screen.blit(
            title,
            title.get_rect(
                center=(WIDTH // 2, 130)
            )
        )

        draw_button(
            number_mode_button,
            "NUMBER MODE",
            mouse_pos
        )

        draw_button(
            word_mode_button,
            "WORD MODE",
            mouse_pos
        )

        draw_button(
            back_button,
            "BACK",
            mouse_pos
        )


    elif current_menu == "number":

        number_mode.draw()


    elif current_menu == "word":

        word_mode.draw()


    # =========================
    # UPDATE DISPLAY
    # =========================

    pygame.display.flip()

    clock.tick(60)


# =========================
# QUIT
# =========================

pygame.quit()

