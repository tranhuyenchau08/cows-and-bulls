
import pygame

from modes.number_mode import NumberMode
from modes.word_mode import WordMode
from modes.effects import sound_effects
from modes.stats import stats_manager

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

# Canvas giữ nguyên bố cục gốc
screen = pygame.Surface((WIDTH, HEIGHT))

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

current_menu = "login"
selected_mode = None
number_mode = None
word_mode = None


input_username = ""
input_password = ""
active_input = "username"
auth_message = ""
auth_mode = "login"


username_box = pygame.Rect(350, 220, 300, 50)
password_box = pygame.Rect(350, 310, 300, 50)
submit_auth_button = pygame.Rect(350, 400, 300, 55)
switch_auth_button = pygame.Rect(350, 470, 300, 45)


def perform_auth():
    global current_menu, auth_message
    if not input_username or not input_password:
        auth_message = "Vui long nhap day du thong tin!"
        return
        
    if auth_mode == "login":
        success, msg = stats_manager.login_server(input_username, input_password)
    else:
        success, msg = stats_manager.register_server(input_username, input_password)
        
    auth_message = msg
    if success:
        current_menu = "main"


def draw_auth_screen(mouse_pos):
    screen.fill(BACKGROUND)
    title_text = "LOGIN" if auth_mode == "login" else "REGISTER"
    draw_title(title_text, 100)

    input_font = pygame.font.Font(None, 36)
    label_font = pygame.font.Font(None, 28)
    msg_font = pygame.font.Font(None, 24)

    # Username Label & Box
    u_label = label_font.render("Username:", True, TEXT_COLOR)
    screen.blit(u_label, (350, 195))
    u_color = (255, 255, 255) if active_input == "username" else (230, 230, 230)
    pygame.draw.rect(screen, u_color, username_box, border_radius=8)
    pygame.draw.rect(screen, TEXT_COLOR, username_box, 2, border_radius=8)
    u_surface = input_font.render(input_username, True, TEXT_COLOR)
    screen.blit(u_surface, (username_box.x + 10, username_box.y + 12))

    # Password Label & Box
    p_label = label_font.render("Password:", True, TEXT_COLOR)
    screen.blit(p_label, (350, 285))
    p_color = (255, 255, 255) if active_input == "password" else (230, 230, 230)
    pygame.draw.rect(screen, p_color, password_box, border_radius=8)
    pygame.draw.rect(screen, TEXT_COLOR, password_box, 2, border_radius=8)
    p_surface = input_font.render("*" * len(input_password), True, TEXT_COLOR)
    screen.blit(p_surface, (password_box.x + 10, password_box.y + 12))

    # Error / Success Message
    if auth_message:
        msg_color = (200, 50, 50) if "thanh cong" not in auth_message.lower() else (50, 150, 50)
        msg_surface = msg_font.render(auth_message, True, msg_color)
        screen.blit(msg_surface, msg_surface.get_rect(center=(WIDTH // 2, 375)))

    btn_text = "SUBMIT LOGIN" if auth_mode == "login" else "SUBMIT REGISTER"
    switch_text = "Switch to Register" if auth_mode == "login" else "Switch to Login"
    
    draw_button(submit_auth_button, btn_text, mouse_pos)
    draw_button(switch_auth_button, switch_text, mouse_pos)
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

    text_surface = button_font.render(
        text,
        True,
        TEXT_COLOR
    )

    screen.blit(
        text_surface,
        text_surface.get_rect(center=rect.center)
    )


def draw_title(text, y=130):
    title = title_font.render(text, True, TEXT_COLOR)
    screen.blit(
        title,
        title.get_rect(center=(WIDTH // 2, y))
    )



def draw_stats_screen(mouse_pos):
    screen.fill(BACKGROUND)
    draw_title("STATISTICS", 42)

    stats = stats_manager.get_summary()

    # Fonts
    label_font = pygame.font.Font(None, 25)
    value_font = pygame.font.SysFont("consolas", 38, bold=True)
    number_font = pygame.font.SysFont("consolas", 26, bold=True)
    section_font = pygame.font.Font(None, 28)
    row_font = pygame.font.SysFont("consolas", 20)

    # UI colors
    card_color = (255, 250, 238)
    muted_color = (125, 115, 98)
    green_color = (105, 155, 100)
    red_color = (205, 105, 90)
    gold_color = (215, 165, 65)
    purple_color = (135, 120, 175)

    def draw_card(rect, accent_color):
        pygame.draw.rect(
            screen, card_color, rect, border_radius=16
        )
        # Small colored accent along the top
        accent_rect = pygame.Rect(
            rect.x + 12, rect.y + 8, rect.width - 24, 5
        )
        pygame.draw.rect(
            screen, accent_color, accent_rect, border_radius=3
        )

    def draw_text(text, font, color, pos):
        surface = font.render(str(text), True, color)
        screen.blit(surface, pos)

    # --- Summary cards ---
    summary_cards = [
        ("TOTAL GAMES", stats["total_games"], green_color),
        ("WIN RATE", f'{stats["win_rate"]}%', gold_color),
        ("TOTAL SCORE", stats["total_score"], purple_color),
        ("BEST SCORE", stats["best_score"], red_color),
    ]

    card_width = 210
    card_height = 105
    gap = 20
    start_x = (WIDTH - (card_width * 4 + gap * 3)) // 2

    for i, (label, value, accent) in enumerate(summary_cards):
        rect = pygame.Rect(
            start_x + i * (card_width + gap), 75,
            card_width, card_height
        )
        draw_card(rect, accent)

        label_surface = label_font.render(label, True, muted_color)
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

    # --- Number and Word mode cards ---
    mode_title_font = pygame.font.Font(None, 34)
    mode_title = mode_title_font.render(
        "GAME MODES", True, TEXT_COLOR
    )
    screen.blit(
        mode_title,
        mode_title.get_rect(center=(WIDTH // 2, 215))
    )

    mode_cards = [
        ("NUMBER MODE", stats["number"], green_color, 65),
        ("WORD MODE", stats["word"], purple_color, 515),
    ]

    for title, mode_stats, accent, x in mode_cards:
        rect = pygame.Rect(x, 238, 420, 95)
        draw_card(rect, accent)

        draw_text(title, section_font, TEXT_COLOR, (x + 18, 258))

        details = (
            f'Games: {mode_stats["games"]}  '
            f'Wins: {mode_stats["wins"]}  '
            f'Losses: {mode_stats["losses"]}'
        )

        details_font = pygame.font.SysFont("consolas", 20)
        draw_text(details, details_font, muted_color, (x + 18, 296))

        best_text = f'Best: {mode_stats["best_score"]}'
        best_surface = number_font.render(
            best_text, True, accent
        )
        screen.blit(
            best_surface,
            (x + 420 - best_surface.get_width() - 18, 258)
        )

    # --- Recent games ---
    recent_title_font = pygame.font.Font(None, 34)
    recent_title = recent_title_font.render(
        "RECENT GAMES", True, TEXT_COLOR
    )
    screen.blit(
        recent_title,
        recent_title.get_rect(center=(WIDTH // 2, 365))
    )

    history = stats["history"][:5]

    if not history:
        empty_rect = pygame.Rect(55, 390, 890, 45)
        pygame.draw.rect(
            screen, card_color, empty_rect, border_radius=12
        )
        empty_surface = row_font.render(
            "No games played yet - play a round to see your stats!",
            True, muted_color
        )
        screen.blit(
            empty_surface,
            empty_surface.get_rect(center=empty_rect.center)
        )
    else:
        for i, game in enumerate(history):
            y = 390 + i * 42
            rect = pygame.Rect(55, y, 890, 36)

            pygame.draw.rect(
                screen, card_color, rect, border_radius=10
            )

            date_mode = (
                f'{game["date"]}  |  '
                f'{game["mode"]} - {game["difficulty"]}'
            )
            draw_text(
                date_mode, row_font, TEXT_COLOR, (70, y + 9)
            )

            
            score_label_font = pygame.font.SysFont("consolas", 20)

            score_label = score_label_font.render(
                "Score:", True, muted_color
            )
            score_value = score_label_font.render(
                str(game["score"]), True, muted_color
            )

            score_x = rect.right - 250

            screen.blit(score_label, (score_x, y + 9))
            screen.blit(
                score_value,
                (score_x + score_label.get_width() + 8, y + 9)
            )


            is_win = str(game["result"]).lower() == "win"
            result_text = str(game["result"]).upper()
            result_color = green_color if is_win else red_color

            pill = pygame.Rect(rect.right - 100, y + 4, 85, 28)
            pygame.draw.rect(
                screen, result_color, pill, border_radius=9
            )

            result_surface = label_font.render(
                result_text, True, (255, 255, 255)
            )
            screen.blit(
                result_surface,
                result_surface.get_rect(center=pill.center)
            )

    # Back button
    draw_button(stats_back_button, "BACK", mouse_pos)

# LEADERBOARD SCREEN
    
def draw_leaderboard_screen(mouse_pos):
    screen.fill(BACKGROUND)
    draw_title("LEADERBOARD", 42)

    leaderboard = stats_manager.fetch_global_leaderboard()

    

    card_color = (255, 250, 238)
    muted_color = (125, 115, 98)
    gold_color = (215, 165, 65)
    green_color = (105, 155, 100)

    title_font = pygame.font.Font(None, 28)
    row_font = pygame.font.SysFont("consolas", 20)

    # Column headings
    headings = [
        ("RANK", 100),
        ("PLAYER", 250),
        ("BEST SCORE", 500),
        ("TOTAL WINS", 750),
    ]

    for heading, x in headings:
        text_surface = title_font.render(
            heading, True, muted_color
        )
        screen.blit(text_surface, (x, 150))

    if not leaderboard:
        empty_text = row_font.render(
            "No scores yet. Play a game first!",
            True, muted_color
        )
        screen.blit(
            empty_text,
            empty_text.get_rect(center=(WIDTH // 2, 250))
        )

    else:
        for i, game in enumerate(leaderboard):
            y = 195 + i * 65

            row_rect = pygame.Rect(55, y, 890, 52)
            pygame.draw.rect(
                screen, card_color, row_rect,
                border_radius=12
            )

            rank_color = gold_color if i == 0 else TEXT_COLOR

            rank_text = row_font.render(f"#{i + 1}", True, rank_color)
            name_text = row_font.render(str(game.get("player_name", "Unknown")), True, TEXT_COLOR)
            score_text = row_font.render(str(game.get("best_score", 0)), True, green_color)
            wins_text = row_font.render(str(game.get("wins", 0)), True, TEXT_COLOR)

            screen.blit(rank_text, (100, y + 15))
            screen.blit(name_text, (250, y + 15))
            screen.blit(score_text, (500, y + 15))
            screen.blit(wins_text, (750, y + 15))

    draw_button(leaderboard_back_button, "BACK", mouse_pos)



# =========================
# BUTTONS
# =========================

game_mode_button = pygame.Rect(350, 260, 300, 65)
stats_button = pygame.Rect(350, 345, 300, 60)
leaderboard_button = pygame.Rect(350, 425, 300, 60)
quit_button = pygame.Rect(350, 505, 300, 60)
stats_back_button = pygame.Rect(350, 610, 300, 55)
leaderboard_back_button = pygame.Rect(350, 610, 300, 55)

number_mode_button = pygame.Rect(350, 250, 300, 70)
word_mode_button = pygame.Rect(350, 350, 300, 70)
mode_back_button = pygame.Rect(350, 450, 300, 70)

easy_button = pygame.Rect(350, 230, 300, 65)
normal_button = pygame.Rect(350, 320, 300, 65)
hard_button = pygame.Rect(350, 410, 300, 65)
difficulty_back_button = pygame.Rect(350, 500, 300, 65)

sound_button = pygame.Rect(790, 20, 190, 45)

# =========================
# RESIZE HELPERS
# =========================

def get_display_geometry():
    window_width, window_height = window.get_size()

    scale = min(
        window_width / WIDTH,
        window_height / HEIGHT
    )

    display_width = max(1, int(WIDTH * scale))
    display_height = max(1, int(HEIGHT * scale))

    offset_x = (window_width - display_width) // 2
    offset_y = (window_height - display_height) // 2

    return scale, display_width, display_height, offset_x, offset_y


def get_canvas_mouse_pos():
    scale, _, _, offset_x, offset_y = get_display_geometry()

    mouse_x, mouse_y = pygame.mouse.get_pos()

    canvas_x = int((mouse_x - offset_x) / scale)
    canvas_y = int((mouse_y - offset_y) / scale)

    return canvas_x, canvas_y


def convert_mouse_event(event):
    scale, _, _, offset_x, offset_y = get_display_geometry()

    x = int((event.pos[0] - offset_x) / scale)
    y = int((event.pos[1] - offset_y) / scale)

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
    global number_mode, word_mode, current_menu

    try:
        if selected_mode == "number":
            number_mode = NumberMode(screen, difficulty)
            current_menu = "number"

        elif selected_mode == "word":
            word_mode = WordMode(screen, difficulty)
            current_menu = "word"

    except Exception as error:
        print("Error starting game:", repr(error))


# =========================
# MAIN LOOP
# =========================

running = True

while running:
    mouse_pos = get_canvas_mouse_pos()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
            break

        # -------------------------
        # WINDOW RESIZE
        # -------------------------

        if event.type == pygame.VIDEORESIZE:
            new_width = max(MIN_WIDTH, event.w)
            new_height = max(MIN_HEIGHT, event.h)

            window = pygame.display.set_mode(
                (new_width, new_height),
                pygame.RESIZABLE
            )
            continue

        # -------------------------
        # KEYBOARD EVENTS
        # -------------------------

        if event.type == pygame.KEYDOWN:
            # GÕ PHÍM KHI Ở MÀN HÌNH LOGIN / REGISTER
            if current_menu == "login":
                if event.key == pygame.K_TAB:
                    active_input = "password" if active_input == "username" else "username"
                elif event.key == pygame.K_BACKSPACE:
                    if active_input == "username":
                        input_username = input_username[:-1]
                    else:
                        input_password = input_password[:-1]
                elif event.key == pygame.K_RETURN:
                    perform_auth()
                else:
                    if len(event.unicode) > 0 and event.unicode.isprintable():
                        if active_input == "username" and len(input_username) < 15:
                            input_username += event.unicode
                        elif active_input == "password" and len(input_password) < 20:
                            input_password += event.unicode
                continue  # Bỏ qua kiểm tra ESC khi đang gõ text
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

                elif current_menu == "mode":
                    current_menu = "main"

                elif current_menu == "main":
                    running = False

                elif current_menu == "stats":
                    current_menu = "main"

                continue

        # -------------------------
        # MOUSE EVENTS
        # -------------------------

        if event.type == pygame.MOUSEBUTTONDOWN:
            event = convert_mouse_event(event)


            # CLICK CHUỘT MÀN HÌNH LOGIN / REGISTER
            if current_menu == "login":
                if username_box.collidepoint(event.pos):
                    active_input = "username"
                elif password_box.collidepoint(event.pos):
                    active_input = "password"
                elif submit_auth_button.collidepoint(event.pos):
                    sound_effects.play("click")
                    perform_auth()
                elif switch_auth_button.collidepoint(event.pos):
                    sound_effects.play("click")
                    auth_mode = "register" if auth_mode == "login" else "login"
                    auth_message = ""
                continue


            # SOUND ON/OFF
            if current_menu in (
                "main",
                "mode",
                "number_difficulty",
                "word_difficulty"
            ) and sound_button.collidepoint(event.pos):
                sound_effects.toggle()
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

                elif quit_button.collidepoint(event.pos):
                    sound_effects.play("click")
                    running = False

            # STATISTICS SCREEN
            elif current_menu == "stats":
                if stats_back_button.collidepoint(event.pos):
                    sound_effects.play("click")
                    current_menu = "main"

            #LEADERBOAD SCREEN
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

        # Forward keyboard events to active game modes.
        # Keep keyboard input working even when the window is resized.
        if current_menu == "number" and number_mode is not None:
            number_mode.handle_events(event)

        elif current_menu == "word" and word_mode is not None:
            word_mode.handle_events(event)

    # =========================
    # DRAW SCREEN
    # =========================

    mouse_pos = get_canvas_mouse_pos()

    if current_menu == "login":
        draw_auth_screen(mouse_pos)

    elif current_menu == "main":
        screen.fill(BACKGROUND)
        draw_title("COWS AND BULLS", 150)

        draw_button(
            game_mode_button, "GAME MODE", mouse_pos
        )

        draw_button(
            stats_button, "STATISTICS", mouse_pos
        )

        draw_button(
            leaderboard_button, "LEADERBOARD", mouse_pos
        )

        draw_button(
            quit_button, "QUIT", mouse_pos
        )

    elif current_menu == "stats":
        draw_stats_screen(mouse_pos)

    elif current_menu == "leaderboard":
        draw_leaderboard_screen(mouse_pos)

    elif current_menu == "mode":
        screen.fill(BACKGROUND)
        draw_title("CHOOSE GAME MODE")

        draw_button(
            number_mode_button, "NUMBER MODE", mouse_pos
        )
        draw_button(
            word_mode_button, "WORD MODE", mouse_pos
        )
        draw_button(
            mode_back_button, "BACK", mouse_pos
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
            difficulty_back_button, "BACK", mouse_pos
        )

    elif current_menu == "number":
        number_mode.draw(mouse_pos)

    elif current_menu == "word":
        word_mode.draw(mouse_pos)

    # =========================
    # SOUND BUTTON
    # =========================

    if current_menu in (
        "main",
        "mode",
        "number_difficulty",
        "word_difficulty"
    ):
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

    # =========================
    # DISPLAY
    # =========================

    present_screen()
    pygame.display.flip()
    clock.tick(60)


pygame.quit()
