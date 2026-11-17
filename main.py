
import pygame

from modes.number_mode import NumberMode
from modes.word_mode import WordMode
from modes.effects import sound_effects
from modes.stats import stats_manager
from modes.server import start_api_server

pygame.init()

# =========================
# CONFIG
# =========================

WIDTH = 1000
HEIGHT = 700

MIN_WIDTH = 700
MIN_HEIGHT = 490

window = pygame.display.set_mode(
    (WIDTH, HEIGHT),
    pygame.RESIZABLE
)
pygame.display.set_caption("Cows and Bulls")

clock = pygame.time.Clock()
screen = pygame.Surface((WIDTH, HEIGHT))

# Load cow and bull sprites
cow_image = pygame.image.load(
    "assets/cow.png"
).convert_alpha()

bull_image = pygame.image.load(
    "assets/bull.png"
).convert_alpha()

cow_image = pygame.transform.smoothscale(
    cow_image, (230, 230)
)

bull_image = pygame.transform.smoothscale(
    bull_image, (230, 230)
)

# =========================
# COLORS / THEMES
# =========================

THEMES = [
    {
        "name": "CREAM",
        "background": (246, 237, 220),
        "text": (65, 48, 38),
        "button": (137, 164, 112),
        "hover": (166, 193, 139),
    },
    {
        "name": "MINT",
        "background": (225, 240, 229),
        "text": (45, 70, 58),
        "button": (112, 160, 139),
        "hover": (145, 190, 165),
    }
]

current_theme = 0

BACKGROUND = THEMES[0]["background"]
TEXT_COLOR = THEMES[0]["text"]
BUTTON_COLOR = THEMES[0]["button"]
BUTTON_HOVER = THEMES[0]["hover"]


def apply_theme():
    global BACKGROUND
    global TEXT_COLOR
    global BUTTON_COLOR
    global BUTTON_HOVER

    theme = THEMES[current_theme]

    BACKGROUND = theme["background"]
    TEXT_COLOR = theme["text"]
    BUTTON_COLOR = theme["button"]
    BUTTON_HOVER = theme["hover"]


# =========================
# FONTS
# =========================

main_font = pygame.font.SysFont("consolas", 20)

title_font = pygame.font.SysFont(
    "consolas", 54, bold=True
)

button_font = pygame.font.SysFont(
    "consolas", 24, bold=True
)

# =========================
# GAME STATE
# =========================

current_menu = "welcome"
current_username = ""
selected_mode = None

number_mode = None
word_mode = None

input_username = ""
input_password = ""
active_input = None

show_password = False
auth_message = ""
auth_mode = "login"

# =========================
# INPUT BOXES
# =========================

username_box = pygame.Rect(350, 220, 300, 50)
password_box = pygame.Rect(350, 310, 300, 50)

toggle_password_button = pygame.Rect(
    660, 310, 100, 50
)

submit_auth_button = pygame.Rect(
    350, 400, 300, 55
)

switch_auth_button = pygame.Rect(
    350, 470, 300, 45
)


# =========================
# AUTHENTICATION
# =========================

def perform_auth():
    global current_menu
    global auth_message
    global current_username

    if not input_username or not input_password:
        auth_message = "Please enter both username and password!"
        return

    if auth_mode == "login":
        success, msg = stats_manager.login_server(
            input_username,
            input_password
        )
    else:
        success, msg = stats_manager.register_server(
            input_username,
            input_password
        )

    auth_message = msg

    if success:
        current_username = input_username
        current_menu = "main"


# =========================
# MASCOT
# =========================

def draw_mascot(x, y, is_bull=False):

    pygame.draw.ellipse(
        screen, (115, 85, 65),
        (x - 48, y - 15, 25, 35)
    )

    pygame.draw.ellipse(
        screen, (115, 85, 65),
        (x + 23, y - 15, 25, 35)
    )

    pygame.draw.circle(
        screen, (255, 245, 220), (x, y), 38
    )

    if is_bull:
        pygame.draw.polygon(
            screen, (225, 190, 120),
            [
                (x - 22, y - 28),
                (x - 38, y - 55),
                (x - 5, y - 32)
            ]
        )

        pygame.draw.polygon(
            screen, (225, 190, 120),
            [
                (x + 22, y - 28),
                (x + 38, y - 55),
                (x + 5, y - 32)
            ]
        )

    pygame.draw.circle(
        screen, TEXT_COLOR, (x - 13, y - 8), 4
    )

    pygame.draw.circle(
        screen, TEXT_COLOR, (x + 13, y - 8), 4
    )

    pygame.draw.ellipse(
        screen, (220, 155, 145),
        (x - 19, y + 8, 38, 22)
    )


# =========================
# WELCOME SCREEN
# =========================

def draw_welcome_screen(mouse_pos):

    screen.fill(BACKGROUND)

    cows_font = pygame.font.Font(
        "assets/BerkshireSwash-Regular.ttf", 150
    )

    cows_text = cows_font.render(
        "COWS", True, TEXT_COLOR
    )

    screen.blit(
        cows_text,
        cows_text.get_rect(
            center=(WIDTH // 2, 110)
        )
    )

    bulls_font = pygame.font.Font(
        "assets/BerkshireSwash-Regular.ttf", 150
    )

    bulls_text = bulls_font.render(
        "BULLS", True, TEXT_COLOR
    )

    screen.blit(
        bulls_text,
        bulls_text.get_rect(
            center=(WIDTH // 2, 430)
        )
    )

    cow_rect = cow_image.get_rect(
        center=(WIDTH // 2 - 180, 270)
    )

    screen.blit(cow_image, cow_rect)

    bull_rect = bull_image.get_rect(
        center=(WIDTH // 2 + 180, 270)
    )

    screen.blit(bull_image, bull_rect)

    amp_font = pygame.font.SysFont(
        "segoe script", 140,
        bold=True, italic=True
    )

    amp_text = amp_font.render(
        "&", True, TEXT_COLOR
    )

    screen.blit(
        amp_text,
        amp_text.get_rect(
            center=(WIDTH // 2, 270)
        )
    )

    draw_button(
        welcome_login_button, "LOGIN", mouse_pos
    )

    draw_button(
        welcome_register_button, "REGISTER", mouse_pos
    )

    note = main_font.render(
        "Don't have an account? Choose REGISTER!",
        True, TEXT_COLOR
    )

    screen.blit(
        note,
        note.get_rect(center=(WIDTH // 2, 620))
    )


# =========================
# AUTH SCREEN
# =========================

def draw_auth_screen(mouse_pos):

    screen.fill(BACKGROUND)

    title_text = (
        "LOGIN"
        if auth_mode == "login"
        else "REGISTER"
    )

    draw_title(title_text, 100)

    input_font = main_font
    label_font = main_font
    msg_font = main_font

    # Username
    u_label = label_font.render(
        "Username:", True, TEXT_COLOR
    )

    screen.blit(u_label, (350, 195))

    u_color = (
        (255, 255, 255)
        if active_input == "username"
        else (230, 230, 230)
    )

    pygame.draw.rect(
        screen, u_color,
        username_box, border_radius=8
    )

    u_border = (
        (142, 170, 130)
        if active_input == "username"
        else (195, 170, 140)
    )

    pygame.draw.rect(
        screen,
        u_border,
        username_box,
        3 if active_input == "username" else 2,
        border_radius=8
    )

    u_surface = input_font.render(
        input_username, True, TEXT_COLOR
    )

    u_rect = u_surface.get_rect(
        midleft=(
            username_box.x + 10,
            username_box.centery
        )
    )

    screen.blit(u_surface, u_rect)

    # Password
    p_label = label_font.render(
        "Password:", True, TEXT_COLOR
    )

    screen.blit(p_label, (350, 285))

    p_color = (
        (255, 255, 255)
        if active_input == "password"
        else (230, 230, 230)
    )

    pygame.draw.rect(
        screen, p_color,
        password_box, border_radius=8
    )

    p_border = (
        (142, 170, 130)
        if active_input == "password"
        else (195, 170, 140)
    )

    pygame.draw.rect(
        screen,
        p_border,
        password_box,
        3 if active_input == "password" else 2,
        border_radius=8
    )

    password_text = (
        input_password
        if show_password
        else "*" * len(input_password)
    )

    p_surface = input_font.render(
        password_text, True, TEXT_COLOR
    )

    p_rect = p_surface.get_rect(
        midleft=(
            password_box.x + 10,
            password_box.centery
        )
    )

    screen.blit(p_surface, p_rect)

    toggle_text = (
        "HIDE"
        if show_password
        else "SHOW"
    )

    draw_button(
        toggle_password_button,
        toggle_text,
        mouse_pos
    )

    # Error / Success Message
    if auth_message:

        msg_color = (
            (50, 150, 50)
            if any(
                word in auth_message.lower()
                for word in ("successful", "success")
            )
            else (200, 50, 50)
        )

        msg_surface = msg_font.render(
            auth_message, True, msg_color
        )

        screen.blit(
            msg_surface,
            msg_surface.get_rect(
                center=(WIDTH // 2, 375)
            )
        )

    btn_text = (
        "SUBMIT LOGIN"
        if auth_mode == "login"
        else "SUBMIT REGISTER"
    )

    draw_button(
        submit_auth_button,
        btn_text,
        mouse_pos
    )

    draw_button(
        switch_auth_button,
        "BACK TO WELCOME",
        mouse_pos
    )


# =========================
# BUTTON FUNCTION
# =========================

def draw_button(rect, text, mouse_pos):

    color = (
        BUTTON_HOVER
        if rect.collidepoint(mouse_pos)
        else BUTTON_COLOR
    )

    pygame.draw.rect(
        screen,
        color,
        rect,
        border_radius=15
    )

    pygame.draw.rect(
        screen,
        (85, 105, 70),
        rect,
        2,
        border_radius=15
    )

    text_surface = button_font.render(
        text, True, TEXT_COLOR
    )

    screen.blit(
        text_surface,
        text_surface.get_rect(center=rect.center)
    )


# =========================
# TITLE FUNCTION
# =========================

def draw_title(text, y=130):

    shadow = title_font.render(
        text, True, (110, 85, 55)
    )

    title = title_font.render(
        text, True, TEXT_COLOR
    )

    shadow_rect = shadow.get_rect(
        center=(WIDTH // 2 + 4, y + 4)
    )

    title_rect = title.get_rect(
        center=(WIDTH // 2, y)
    )

    screen.blit(shadow, shadow_rect)
    screen.blit(title, title_rect)


# =========================
# HOW TO PLAY SCREEN
# =========================

def draw_how_to_play_screen(mouse_pos):

    screen.fill(BACKGROUND)

    draw_title("HOW TO PLAY", 65)

    card_color = (255, 250, 238)
    accent_green = (105, 155, 100)
    accent_purple = (135, 120, 175)
    muted_color = (125, 115, 98)

    # Number Mode Card
    number_card = pygame.Rect(65, 145, 420, 390)

    pygame.draw.rect(
        screen, card_color, number_card, border_radius=18
    )

    pygame.draw.rect(
        screen, accent_green,
        (85, 160, 380, 6), border_radius=3
    )

    number_title = pygame.font.SysFont(
        "consolas", 28, bold=True
    )

    number_heading = number_title.render(
        "NUMBER MODE", True, accent_green
    )

    screen.blit(
        number_heading,
        number_heading.get_rect(
            center=(number_card.centerx, 215)
        )
    )

    number_lines = [
        "1. Guess the secret number.",
        "",
        "2. Enter a number and submit.",
        "",
        "3. Bulls: Correct digit and",
        "   correct position.",
        "",
        "4. Cows: Correct digit but",
        "   wrong position.",
        "",
        "5. Use the clues to improve",
        "   your next guess!"
    ]

    y = 260

    for line in number_lines:

        text_surface = main_font.render(
            line, True, TEXT_COLOR
        )

        screen.blit(text_surface, (100, y))
        y += 21

    # Word Mode Card
    word_card = pygame.Rect(515, 145, 420, 390)

    pygame.draw.rect(
        screen, card_color, word_card, border_radius=18
    )

    pygame.draw.rect(
        screen, accent_purple,
        (535, 160, 380, 6), border_radius=3
    )

    word_heading = number_title.render(
        "WORD MODE", True, accent_purple
    )

    screen.blit(
        word_heading,
        word_heading.get_rect(
            center=(word_card.centerx, 215)
        )
    )

    word_lines = [
        "1. Guess the secret word.",
        "",
        "2. Enter a word and submit.",
        "",
        "3. Bulls: Correct letter and",
        "   correct position.",
        "",
        "4. Cows: Correct letter but",
        "   wrong position.",
        "",
        "5. Use the clues to find",
        "   the secret word!"
    ]

    y = 260

    for line in word_lines:

        text_surface = main_font.render(
            line, True, TEXT_COLOR
        )

        screen.blit(text_surface, (550, y))
        y += 21

    # Bottom note
    note = main_font.render(
        "Have fun and good luck!",
        True,
        muted_color
    )

    screen.blit(
        note,
        note.get_rect(
            center=(WIDTH // 2, 565)
        )
    )

    draw_button(
        how_to_play_back_button,
        "BACK TO MENU",
        mouse_pos
    )


# =========================
# SETTINGS SCREEN
# =========================

def draw_settings_screen(mouse_pos):

    screen.fill(BACKGROUND)

    draw_title("SETTINGS", 100)

    card_color = (255, 250, 238)
    muted_color = (125, 115, 98)

    # Settings card
    settings_card = pygame.Rect(
        200, 165, 600, 390
    )

    pygame.draw.rect(
        screen,
        card_color,
        settings_card,
        border_radius=20
    )

    # Account label
    account_title = main_font.render(
        "CURRENT ACCOUNT",
        True,
        muted_color
    )

    screen.blit(
        account_title,
        account_title.get_rect(
            center=(WIDTH // 2, 215)
        )
    )

    account_name = pygame.font.SysFont(
        "consolas", 28, bold=True
    ).render(
        current_username if current_username else "Guest",
        True,
        TEXT_COLOR
    )

    screen.blit(
        account_name,
        account_name.get_rect(
            center=(WIDTH // 2, 255)
        )
    )

    # Theme label
    theme_label = main_font.render(
        "THEME",
        True,
        TEXT_COLOR
    )

    screen.blit(
        theme_label,
        theme_label.get_rect(
            center=(WIDTH // 2, 310)
        )
    )

    theme_text = (
        "CURRENT: " + THEMES[current_theme]["name"]
    )

    draw_button(
        theme_button,
        theme_text,
        mouse_pos
    )

    # Sound toggle
    sound_text = (
        "SOUND: ON"
        if sound_effects.enabled
        else "SOUND: OFF"
    )

    draw_button(
        sound_button,
        sound_text,
        mouse_pos
    )

    # Logout
    draw_button(
        logout_button,
        "LOG OUT",
        mouse_pos
    )

    # Back
    draw_button(
        settings_back_button,
        "BACK TO MENU",
        mouse_pos
    )


# =========================
# STATISTICS SCREEN
# =========================

def draw_stats_screen(mouse_pos):

    screen.fill(BACKGROUND)
    draw_title("STATISTICS", 42)

    stats = stats_manager.get_summary()

    label_font = main_font
    value_font = main_font
    number_font = main_font
    section_font = main_font
    row_font = main_font

    card_color = (255, 250, 238)
    muted_color = (125, 115, 98)
    green_color = (105, 155, 100)
    red_color = (205, 105, 90)
    gold_color = (215, 165, 65)
    purple_color = (135, 120, 175)

    def draw_card(rect, accent_color):

        pygame.draw.rect(
            screen,
            card_color,
            rect,
            border_radius=16
        )

        accent_rect = pygame.Rect(
            rect.x + 12,
            rect.y + 8,
            rect.width - 24,
            5
        )

        pygame.draw.rect(
            screen,
            accent_color,
            accent_rect,
            border_radius=3
        )

    def draw_text(text, font, color, pos):

        surface = font.render(
            str(text), True, color
        )

        screen.blit(surface, pos)

    # Summary cards
    summary_cards = [
        ("TOTAL GAMES", stats["total_games"], green_color),
        ("WIN RATE", f'{stats["win_rate"]}%', gold_color),
        ("TOTAL SCORE", stats["total_score"], purple_color),
        ("BEST SCORE", stats["best_score"], red_color),
    ]

    card_width = 210
    card_height = 105
    gap = 20

    start_x = (
        WIDTH - (card_width * 4 + gap * 3)
    ) // 2

    for i, (label, value, accent) in enumerate(summary_cards):

        rect = pygame.Rect(
            start_x + i * (card_width + gap),
            75,
            card_width,
            card_height
        )

        draw_card(rect, accent)

        label_surface = label_font.render(
            label, True, muted_color
        )

        screen.blit(
            label_surface,
            label_surface.get_rect(
                center=(rect.centerx, rect.y + 35)
            )
        )

        value_surface = value_font.render(
            str(value), True, TEXT_COLOR
        )

        screen.blit(
            value_surface,
            value_surface.get_rect(
                center=(rect.centerx, rect.y + 72)
            )
        )

    # Game modes
    mode_title_font = pygame.font.Font(None, 34)

    mode_title = mode_title_font.render(
        "GAME MODES", True, TEXT_COLOR
    )

    screen.blit(
        mode_title,
        mode_title.get_rect(
            center=(WIDTH // 2, 215)
        )
    )

    mode_cards = [
        ("NUMBER MODE", stats["number"], green_color, 65),
        ("WORD MODE", stats["word"], purple_color, 515),
    ]

    for title, mode_stats, accent, x in mode_cards:

        rect = pygame.Rect(x, 238, 420, 95)

        draw_card(rect, accent)

        draw_text(
            title,
            section_font,
            TEXT_COLOR,
            (x + 18, 258)
        )

        details = (
            f'Games: {mode_stats["games"]}  '
            f'Wins: {mode_stats["wins"]}  '
            f'Losses: {mode_stats["losses"]}'
        )

        draw_text(
            details,
            main_font,
            muted_color,
            (x + 18, 296)
        )

        best_text = (
            f'Best: {mode_stats["best_score"]}'
        )

        best_surface = number_font.render(
            best_text, True, accent
        )

        screen.blit(
            best_surface,
            (
                x + 420 - best_surface.get_width() - 18,
                258
            )
        )

    # Recent games
    recent_title_font = pygame.font.Font(None, 34)

    recent_title = recent_title_font.render(
        "RECENT GAMES", True, TEXT_COLOR
    )

    screen.blit(
        recent_title,
        recent_title.get_rect(
            center=(WIDTH // 2, 365)
        )
    )

    history = stats["history"][:5]

    if not history:

        empty_rect = pygame.Rect(
            55, 390, 890, 45
        )

        pygame.draw.rect(
            screen,
            card_color,
            empty_rect,
            border_radius=12
        )

        empty_surface = row_font.render(
            "No games played yet - play a round to see your stats!",
            True,
            muted_color
        )

        screen.blit(
            empty_surface,
            empty_surface.get_rect(
                center=empty_rect.center
            )
        )

    else:

        for i, game in enumerate(history):

            y = 390 + i * 42

            rect = pygame.Rect(
                55, y, 890, 36
            )

            pygame.draw.rect(
                screen,
                card_color,
                rect,
                border_radius=10
            )

            date_mode = (
                f'{game["date"]}  |  '
                f'{game["mode"]} - {game["difficulty"]}'
            )

            draw_text(
                date_mode,
                row_font,
                TEXT_COLOR,
                (70, y + 9)
            )

            score_label = row_font.render(
                "Score:", True, muted_color
            )

            score_value = row_font.render(
                str(game["score"]), True, muted_color
            )

            score_x = rect.right - 250

            screen.blit(
                score_label,
                (score_x, y + 9)
            )

            screen.blit(
                score_value,
                (
                    score_x + score_label.get_width() + 8,
                    y + 9
                )
            )

            is_win = (
                str(game["result"]).lower() == "win"
            )

            result_text = str(
                game["result"]
            ).upper()

            result_color = (
                green_color if is_win else red_color
            )

            pill = pygame.Rect(
                rect.right - 100,
                y + 4,
                85,
                28
            )

            pygame.draw.rect(
                screen,
                result_color,
                pill,
                border_radius=9
            )

            result_surface = label_font.render(
                result_text,
                True,
                (255, 255, 255)
            )

            screen.blit(
                result_surface,
                result_surface.get_rect(
                    center=pill.center
                )
            )

    draw_button(
        stats_back_button,
        "BACK",
        mouse_pos
    )


# =========================
# LEADERBOARD SCREEN
# =========================

def draw_leaderboard_screen(mouse_pos):

    screen.fill(BACKGROUND)
    draw_title("LEADERBOARD", 42)

    leaderboard = stats_manager.fetch_global_leaderboard()

    card_color = (255, 250, 238)
    muted_color = (125, 115, 98)
    gold_color = (215, 165, 65)
    green_color = (105, 155, 100)

    row_font = main_font

    headings = [
        ("RANK", 100),
        ("PLAYER", 250),
        ("BEST SCORE", 500),
        ("TOTAL WINS", 750),
    ]

    for heading, x in headings:

        text_surface = row_font.render(
            heading, True, muted_color
        )

        screen.blit(
            text_surface,
            (x, 150)
        )

    if not leaderboard:

        empty_text = row_font.render(
            "No scores yet. Play a game first!",
            True,
            muted_color
        )

        screen.blit(
            empty_text,
            empty_text.get_rect(
                center=(WIDTH // 2, 250)
            )
        )

    else:

        for i, game in enumerate(leaderboard):

            y = 195 + i * 65

            row_rect = pygame.Rect(
                55, y, 890, 52
            )

            pygame.draw.rect(
                screen,
                card_color,
                row_rect,
                border_radius=12
            )

            rank_color = (
                gold_color if i == 0 else TEXT_COLOR
            )

            rank_text = row_font.render(
                f"#{i + 1}", True, rank_color
            )

            name_text = row_font.render(
                str(game.get("player_name", "Unknown")),
                True,
                TEXT_COLOR
            )

            score_text = row_font.render(
                str(game.get("best_score", 0)),
                True,
                green_color
            )

            wins_text = row_font.render(
                str(game.get("wins", 0)),
                True,
                TEXT_COLOR
            )

            screen.blit(rank_text, (100, y + 15))
            screen.blit(name_text, (250, y + 15))
            screen.blit(score_text, (500, y + 15))
            screen.blit(wins_text, (750, y + 15))

    draw_button(
        leaderboard_back_button,
        "BACK",
        mouse_pos
    )


# =========================
# BUTTONS
# =========================

# Main menu buttons
game_mode_button = pygame.Rect(350, 220, 300, 55)
stats_button = pygame.Rect(350, 290, 300, 55)
leaderboard_button = pygame.Rect(350, 360, 300, 55)
settings_menu_button = pygame.Rect(350, 430, 300, 55)
how_to_play_button = pygame.Rect(350, 500, 300, 55)
quit_button = pygame.Rect(350, 570, 300, 55)

# Settings buttons
theme_button = pygame.Rect(350, 345, 300, 55)
sound_button = pygame.Rect(350, 420, 300, 55)
logout_button = pygame.Rect(350, 495, 300, 55)
settings_back_button = pygame.Rect(350, 610, 300, 55)

# Other buttons
how_to_play_back_button = pygame.Rect(350, 610, 300, 55)

stats_back_button = pygame.Rect(
    350, 610, 300, 55
)

leaderboard_back_button = pygame.Rect(
    350, 610, 300, 55
)

welcome_login_button = pygame.Rect(
    300, 550, 180, 55
)

welcome_register_button = pygame.Rect(
    520, 550, 180, 55
)

number_mode_button = pygame.Rect(
    350, 250, 300, 70
)

word_mode_button = pygame.Rect(
    350, 350, 300, 70
)

mode_back_button = pygame.Rect(
    350, 450, 300, 70
)

easy_button = pygame.Rect(
    350, 230, 300, 65
)

normal_button = pygame.Rect(
    350, 320, 300, 65
)

hard_button = pygame.Rect(
    350, 410, 300, 65
)

difficulty_back_button = pygame.Rect(
    350, 500, 300, 65
)


# =========================
# RESIZE HELPERS
# =========================

def get_display_geometry():

    window_width, window_height = window.get_size()

    scale = min(
        window_width / WIDTH,
        window_height / HEIGHT
    )

    display_width = max(
        1, int(WIDTH * scale)
    )

    display_height = max(
        1, int(HEIGHT * scale)
    )

    offset_x = (
        window_width - display_width
    ) // 2

    offset_y = (
        window_height - display_height
    ) // 2

    return (
        scale,
        display_width,
        display_height,
        offset_x,
        offset_y
    )


def get_canvas_mouse_pos():

    scale, _, _, offset_x, offset_y = (
        get_display_geometry()
    )

    mouse_x, mouse_y = pygame.mouse.get_pos()

    canvas_x = int(
        (mouse_x - offset_x) / scale
    )

    canvas_y = int(
        (mouse_y - offset_y) / scale
    )

    return canvas_x, canvas_y


def convert_mouse_event(event):

    scale, _, _, offset_x, offset_y = (
        get_display_geometry()
    )

    x = int(
        (event.pos[0] - offset_x) / scale
    )

    y = int(
        (event.pos[1] - offset_y) / scale
    )

    return pygame.event.Event(
        event.type,
        {
            **event.dict,
            "pos": (x, y)
        }
    )


def present_screen():

    scale, display_width, display_height, offset_x, offset_y = (
        get_display_geometry()
    )

    window.fill(BACKGROUND)

    scaled_screen = pygame.transform.smoothscale(
        screen,
        (display_width, display_height)
    )

    window.blit(
        scaled_screen,
        (offset_x, offset_y)
    )


# =========================
# START GAME
# =========================


def start_game(difficulty):

    global number_mode
    global word_mode
    global current_menu
    global current_username

    try:

        if selected_mode == "number":

            number_mode = NumberMode(
                screen,
                difficulty,
                current_username,
                THEMES[current_theme]
            )

            current_menu = "number"

        elif selected_mode == "word":

            word_mode = WordMode(
                screen,
                difficulty,
                current_username,
                THEMES[current_theme]
            )

            current_menu = "word"

    except Exception as error:

        print(
            "Error starting game:",
            repr(error)
        )


# =========================
# MAIN LOOP
# =========================

# Start API server automatically
if not start_api_server():
    print("Warning: API server could not be started!")


running = True

while running:

    mouse_pos = get_canvas_mouse_pos()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False
            break

        # WINDOW RESIZE
        if event.type == pygame.VIDEORESIZE:

            new_width = max(
                MIN_WIDTH, event.w
            )

            new_height = max(
                MIN_HEIGHT, event.h
            )

            window = pygame.display.set_mode(
                (new_width, new_height),
                pygame.RESIZABLE
            )

            continue

        # KEYBOARD EVENTS
        if event.type == pygame.KEYDOWN:

            if current_menu == "login":

                if event.key == pygame.K_TAB:

                    active_input = (
                        "password"
                        if active_input == "username"
                        else "username"
                    )

                elif event.key == pygame.K_BACKSPACE:

                    if active_input == "username":
                        input_username = input_username[:-1]

                    elif active_input == "password":
                        input_password = input_password[:-1]

                elif event.key == pygame.K_RETURN:

                    perform_auth()

                else:

                    if (
                        len(event.unicode) > 0
                        and event.unicode.isprintable()
                    ):

                        if (
                            active_input == "username"
                            and len(input_username) < 15
                        ):

                            input_username += event.unicode

                        elif (
                            active_input == "password"
                            and len(input_password) < 20
                        ):

                            input_password += event.unicode

                continue

            if event.key == pygame.K_ESCAPE:

                if current_menu == "number":
                    current_menu = "number_difficulty"

                elif current_menu == "word":
                    current_menu = "word_difficulty"

                elif current_menu in (
                    "number_difficulty",
                    "word_difficulty"
                ):
                    current_menu = "mode"

                elif current_menu in (
                    "mode",
                    "stats",
                    "leaderboard",
                    "how_to_play",
                    "settings"
                ):
                    current_menu = "main"

                elif current_menu == "main":
                    running = False

                continue

        # MOUSE EVENTS
        if event.type == pygame.MOUSEBUTTONDOWN:

            event = convert_mouse_event(event)

            # WELCOME SCREEN
            if current_menu == "welcome":

                if welcome_login_button.collidepoint(event.pos):

                    sound_effects.play("click")

                    auth_mode = "login"
                    auth_message = ""
                    active_input = None
                    show_password = False

                    current_menu = "login"

                elif welcome_register_button.collidepoint(event.pos):

                    sound_effects.play("click")

                    auth_mode = "register"
                    auth_message = ""
                    active_input = None
                    show_password = False

                    current_menu = "login"

                continue

            # LOGIN / REGISTER
            if current_menu == "login":

                if username_box.collidepoint(event.pos):

                    active_input = "username"

                elif password_box.collidepoint(event.pos):

                    active_input = "password"

                elif toggle_password_button.collidepoint(event.pos):

                    show_password = not show_password

                elif submit_auth_button.collidepoint(event.pos):

                    active_input = None

                    sound_effects.play("click")

                    perform_auth()

                elif switch_auth_button.collidepoint(event.pos):

                    active_input = None

                    sound_effects.play("click")

                    auth_message = ""
                    current_menu = "welcome"

                else:

                    active_input = None

                continue

            # MAIN MENU
            if current_menu == "main":

                if game_mode_button.collidepoint(event.pos):

                    sound_effects.play("click")
                    current_menu = "mode"

                elif stats_button.collidepoint(event.pos):

                    sound_effects.play("click")
                    current_menu = "stats"

                elif leaderboard_button.collidepoint(event.pos):

                    sound_effects.play("click")
                    current_menu = "leaderboard"

                elif settings_menu_button.collidepoint(event.pos):

                    sound_effects.play("click")
                    current_menu = "settings"

                elif how_to_play_button.collidepoint(event.pos):

                    sound_effects.play("click")
                    current_menu = "how_to_play"

                elif quit_button.collidepoint(event.pos):

                    sound_effects.play("click")
                    running = False

            # SETTINGS
            elif current_menu == "settings":

                if theme_button.collidepoint(event.pos):

                    sound_effects.play("click")

                    current_theme = 1 - current_theme
                    apply_theme()

                elif sound_button.collidepoint(event.pos):

                    sound_effects.toggle()


                elif logout_button.collidepoint(event.pos):

                    sound_effects.play("click")

                    current_username = ""
                    input_username = ""
                    input_password = ""
                    active_input = None
                    auth_message = ""
                    show_password = False
                    auth_mode = "login"

                    current_menu = "welcome"

                elif settings_back_button.collidepoint(event.pos):

                    sound_effects.play("click")
                    current_menu = "main"

            # HOW TO PLAY
            elif current_menu == "how_to_play":

                if how_to_play_back_button.collidepoint(event.pos):

                    sound_effects.play("click")
                    current_menu = "main"

            # STATISTICS
            elif current_menu == "stats":

                if stats_back_button.collidepoint(event.pos):

                    sound_effects.play("click")
                    current_menu = "main"

            # LEADERBOARD
            elif current_menu == "leaderboard":

                if leaderboard_back_button.collidepoint(event.pos):

                    sound_effects.play("click")
                    current_menu = "main"

            # CHOOSE GAME MODE
            elif current_menu == "mode":

                if number_mode_button.collidepoint(event.pos):

                    sound_effects.play("click")

                    selected_mode = "number"
                    current_menu = "number_difficulty"

                elif word_mode_button.collidepoint(event.pos):

                    sound_effects.play("click")

                    selected_mode = "word"
                    current_menu = "word_difficulty"

                elif mode_back_button.collidepoint(event.pos):

                    sound_effects.play("click")
                    current_menu = "main"

            # CHOOSE DIFFICULTY
            elif current_menu in (
                "number_difficulty",
                "word_difficulty"
            ):

                if easy_button.collidepoint(event.pos):

                    sound_effects.play("click")
                    start_game("Easy")

                elif normal_button.collidepoint(event.pos):

                    sound_effects.play("click")
                    start_game("Normal")

                elif hard_button.collidepoint(event.pos):

                    sound_effects.play("click")
                    start_game("Hard")

                elif difficulty_back_button.collidepoint(event.pos):

                    sound_effects.play("click")
                    current_menu = "mode"

            # NUMBER GAME
            elif current_menu == "number":

                result = number_mode.handle_events(event)

                if result in ("back", "difficulty"):

                    current_menu = "number_difficulty"

                elif result == "menu":

                    current_menu = "main"

            # WORD GAME
            elif current_menu == "word":

                result = word_mode.handle_events(event)

                if result in ("back", "difficulty"):

                    current_menu = "word_difficulty"

                elif result == "menu":

                    current_menu = "main"

            continue

        # FORWARD KEYBOARD EVENTS TO GAME MODES
        if current_menu == "number" and number_mode is not None:

            number_mode.handle_events(event)

        elif current_menu == "word" and word_mode is not None:

            word_mode.handle_events(event)

    # =========================
    # DRAW SCREEN
    # =========================

    mouse_pos = get_canvas_mouse_pos()

    if current_menu == "welcome":

        draw_welcome_screen(mouse_pos)

    elif current_menu == "login":

        draw_auth_screen(mouse_pos)

    elif current_menu == "main":

        screen.fill(BACKGROUND)

        draw_title("COWS AND BULLS", 130)

        draw_button(
            game_mode_button,
            "GAME MODE",
            mouse_pos
        )

        draw_button(
            stats_button,
            "STATISTICS",
            mouse_pos
        )

        draw_button(
            leaderboard_button,
            "LEADERBOARD",
            mouse_pos
        )

        draw_button(
            settings_menu_button,
            "SETTINGS",
            mouse_pos
        )

        draw_button(
            how_to_play_button,
            "HOW TO PLAY",
            mouse_pos
        )

        draw_button(
            quit_button,
            "QUIT",
            mouse_pos
        )

    elif current_menu == "settings":

        draw_settings_screen(mouse_pos)

    elif current_menu == "how_to_play":

        draw_how_to_play_screen(mouse_pos)

    elif current_menu == "stats":

        draw_stats_screen(mouse_pos)

    elif current_menu == "leaderboard":

        draw_leaderboard_screen(mouse_pos)

    elif current_menu == "mode":

        screen.fill(BACKGROUND)

        draw_title("CHOOSE GAME MODE")

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
            mode_back_button,
            "BACK",
            mouse_pos
        )

    elif current_menu in (
        "number_difficulty",
        "word_difficulty"
    ):

        screen.fill(BACKGROUND)

        if current_menu == "number_difficulty":

            draw_title("NUMBER - DIFFICULTY")

        else:

            draw_title("WORD - DIFFICULTY")

        draw_button(easy_button, "EASY", mouse_pos)
        draw_button(normal_button, "NORMAL", mouse_pos)
        draw_button(hard_button, "HARD", mouse_pos)

        draw_button(
            difficulty_back_button,
            "BACK",
            mouse_pos
        )

    elif current_menu == "number":

        number_mode.draw(mouse_pos)

    elif current_menu == "word":

        word_mode.draw(mouse_pos)

    # DISPLAY
    present_screen()

    pygame.display.flip()

    clock.tick(60)


pygame.quit()
