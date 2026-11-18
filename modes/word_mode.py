
import pygame

from modes.word import WordGame
from modes.effects import sound_effects
from modes.stats import stats_manager


class WordMode:
    def __init__(self, screen, difficulty="Easy", username="", theme=None):
        self.screen = screen
        self.username = username
        self.difficulty = difficulty.lower()
        self.game = WordGame(self.difficulty)
        self.result_saved = False
        self.score = 0

        # Fonts
        self.title_font = pygame.font.SysFont("georgia", 52, bold=True)
        self.text_font = pygame.font.SysFont("consolas", 20)
        self.small_font = pygame.font.SysFont("consolas", 20)
        self.input_font = pygame.font.SysFont("consolas", 24)
        self.button_font = pygame.font.SysFont("consolas", 24, bold=True)

        # Load Cow and Bull icons once
        self.cow_icon = pygame.image.load(
            "assets/cow_icon.png"
        ).convert_alpha()

        self.bull_icon = pygame.image.load(
            "assets/bull_icon.png"
        ).convert_alpha()

        self.cow_icon = pygame.transform.smoothscale(
            self.cow_icon, (24, 24)
        )

        self.bull_icon = pygame.transform.smoothscale(
            self.bull_icon, (24, 24)
        )

        # Theme
        if theme is None:
            theme = {
                "background": (246, 237, 220),
                "text": (65, 48, 38),
                "button": (137, 164, 112),
                "hover": (166, 193, 139),
            }

        self.background = theme["background"]
        self.text_color = theme["text"]
        self.button_color = theme["button"]
        self.button_hover = theme["hover"]

        # Derived colors
        self.card_color = self.blend_color(
            self.background, (255, 255, 255), 0.75
        )

        self.input_hint_color = self.blend_color(
            self.text_color, self.background, 0.45
        )

        self.input_border = self.blend_color(
            self.text_color, self.background, 0.55
        )

        self.input_active_border = self.button_color

        self.white = (255, 250, 240)

        # Input
        self.input_text = ""
        self.input_active = False

        # Messages
        self.message = "Enter your guess and press ENTER."
        self.message_color = self.text_color

        # Input layout
        self.input_box = pygame.Rect(100, 445, 650, 52)
        self.submit_button = pygame.Rect(770, 445, 150, 52)

        # Navigation button
        self.back_button = pygame.Rect(35, 615, 180, 50)

        # Game-over buttons
        self.replay_button = pygame.Rect(75, 550, 250, 55)
        self.change_button = pygame.Rect(375, 550, 250, 55)
        self.menu_button = pygame.Rect(675, 550, 250, 55)

        # Guess history scrolling
        self.history_area = pygame.Rect(160, 145, 680, 285)
        self.history_scroll = 0

    @staticmethod
    def blend_color(color1, color2, amount):
        return tuple(
            int(color1[i] * (1 - amount) + color2[i] * amount)
            for i in range(3)
        )

    def calculate_score(self, won):
        if not won:
            return 0

        difficulty = str(self.game.difficulty).lower()

        base_scores = {
            "easy": 100,
            "normal": 150,
            "hard": 200,
        }

        max_turns = {
            "easy": 10,
            "normal": 8,
            "hard": 7,
        }

        base_score = base_scores.get(difficulty, 100)
        total_turns = max_turns.get(difficulty, 10)

        turns_left = max(
            0,
            getattr(self.game, "attempts_left", 0)
        )

        turns_left = min(turns_left, total_turns)

        bonus = round(turns_left / total_turns * 100)

        return base_score + bonus

    def save_finished_game(self, won):
        if self.result_saved:
            return

        self.score = self.calculate_score(won)

        self.score = stats_manager.record_result(
            mode="word",
            difficulty=self.game.difficulty,
            won=won,
            score=self.score,
        )

        stats_manager.submit_score_server(
            player_name=self.username,
            mode="word",
            difficulty=self.difficulty,
            result="win" if won else "loss",
            target=str(self.game.secret_word),
            attempts=len(self.game.history),
            score=self.score,
        )

        stats_manager.refresh_player_stats(self.username)

        self.result_saved = True

    @staticmethod
    def format_result(bulls, cows):
        bull_word = "Bull" if bulls == 1 else "Bulls"
        cow_word = "Cow" if cows == 1 else "Cows"

        return f"{bulls} {bull_word}, {cows} {cow_word}"

    def submit_guess(self):
        if self.game.is_game_over:
            return

        guess = self.input_text.strip().upper()

        if not guess:
            sound_effects.play("wrong")
            self.message = "Please enter a word."
            self.message_color = self.text_color
            return

        result = self.game.check_guess(guess)
        self.input_text = ""

        if isinstance(result, tuple):
            sound_effects.play("wrong")
            self.message = str(result[1])
            self.message_color = (180, 55, 45)
            return

        if result.get("status") == "error":
            sound_effects.play("wrong")
            self.message = result.get(
                "message", "Invalid guess."
            )
            self.message_color = (180, 55, 45)
            return

        card_height = 58
        card_spacing = 8

        content_height = len(self.game.history) * (
            card_height + card_spacing
        )

        self.history_scroll = max(
            0,
            content_height - self.history_area.height
        )

        bulls = result["bulls"]
        cows = result["cows"]

        self.message = (
            f'{result.get("guess", guess)}: '
            f'{self.format_result(bulls, cows)}'
        )
        self.message_color = self.text_color

        if result.get("won") or result.get("status") == "win":
            sound_effects.play("win")
            self.message = (
                f"YOU WIN! Answer: {self.game.secret_word}"
            )
            self.message_color = (45, 120, 55)
            self.save_finished_game(True)

        elif result.get("status") == "lose":
            sound_effects.play("lose")
            self.message = (
                f"GAME OVER! Answer: {self.game.secret_word}"
            )
            self.message_color = (180, 55, 45)
            self.save_finished_game(False)

        else:
            sound_effects.play("click")

    def handle_events(self, event):
        if event.type == pygame.MOUSEWHEEL:
            if self.history_area.collidepoint(
                pygame.mouse.get_pos()
            ):
                card_height = 58
                card_spacing = 8

                content_height = len(self.game.history) * (
                    card_height + card_spacing
                )

                max_scroll = max(
                    0,
                    content_height - self.history_area.height
                )

                self.history_scroll -= event.y * 30

                self.history_scroll = max(
                    0,
                    min(self.history_scroll, max_scroll)
                )

        if event.type == pygame.KEYDOWN:
            if self.game.is_game_over:
                return None

            if event.key == pygame.K_RETURN:
                if self.input_active:
                    self.submit_guess()

            elif event.key == pygame.K_BACKSPACE:
                if self.input_active:
                    self.input_text = self.input_text[:-1]

            elif event.unicode.isalpha():
                if (
                    self.input_active
                    and len(self.input_text) < self.game.word_length
                ):
                    self.input_text += event.unicode.upper()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button != 1:
                return None

            if self.game.is_game_over:
                if self.replay_button.collidepoint(event.pos):
                    self.game.reset()
                    self.history_scroll = 0

                    self.result_saved = False
                    self.score = 0

                    self.input_text = ""
                    self.input_active = False
                    self.message = (
                        "Enter your guess and press ENTER."
                    )
                    self.message_color = self.text_color

                    sound_effects.play("click")

                elif self.change_button.collidepoint(event.pos):
                    sound_effects.play("click")
                    return "difficulty"

                elif self.menu_button.collidepoint(event.pos):
                    sound_effects.play("click")
                    return "menu"

            else:
                if self.input_box.collidepoint(event.pos):
                    self.input_active = True
                    sound_effects.play("click")

                elif self.submit_button.collidepoint(event.pos):
                    self.submit_guess()

                elif self.back_button.collidepoint(event.pos):
                    sound_effects.play("click")
                    return "difficulty"

                else:
                    self.input_active = False

        return None

    def draw_button(self, rect, text, mouse_pos):
        color = (
            self.button_hover
            if rect.collidepoint(mouse_pos)
            else self.button_color
        )

        pygame.draw.rect(
            self.screen,
            color,
            rect,
            border_radius=12
        )

        label = self.button_font.render(
            text,
            True,
            self.white
        )

        self.screen.blit(
            label,
            label.get_rect(center=rect.center)
        )

    def draw(self, mouse_pos=None):
        self.screen.fill(self.background)

        if mouse_pos is None:
            mouse_pos = (-1, -1)

        # Title
        title = self.title_font.render(
            "WORD MODE",
            True,
            self.text_color
        )

        self.screen.blit(
            title,
            title.get_rect(center=(500, 55))
        )

        # Game information
        info_text = (
            f"Difficulty: {self.game.difficulty.title()}   |   "
            f"Letters: {self.game.word_length}   |   "
            f"Turns left: {self.game.attempts_left}"
        )

        info = self.text_font.render(
            info_text,
            True,
            self.text_color
        )

        self.screen.blit(
            info,
            info.get_rect(center=(500, 110))
        )

        # Guess history
        history_start_y = 155
        card_height = 58
        card_spacing = 8

        self.screen.set_clip(self.history_area)

        for index, item in enumerate(self.game.history):
            card_y = (
                history_start_y
                + index * (card_height + card_spacing)
                - self.history_scroll
            )

            card_rect = pygame.Rect(
                180, card_y, 640, card_height
            )

            pygame.draw.rect(
                self.screen,
                self.card_color,
                card_rect,
                border_radius=12
            )

            pygame.draw.rect(
                self.screen,
                self.input_border,
                card_rect,
                width=2,
                border_radius=12
            )

            guess_label = self.small_font.render(
                f"GUESS #{index + 1}",
                True,
                self.button_color
            )

            self.screen.blit(
                guess_label,
                (200, card_y + 7)
            )

            guess_text = self.small_font.render(
                str(item["guess"]),
                True,
                self.text_color
            )

            self.screen.blit(
                guess_text,
                (200, card_y + 27)
            )

            total_letters = max(1, len(str(item["guess"])))

            # Cow bar
            self.screen.blit(
                self.cow_icon,
                (430, card_y + 17)
            )

            cow_bar = pygame.Rect(
                460, card_y + 23, 105, 10
            )

            pygame.draw.rect(
                self.screen,
                (215, 205, 185),
                cow_bar,
                border_radius=5
            )

            pygame.draw.rect(
                self.screen,
                (155, 175, 125),
                (
                    460,
                    card_y + 23,
                    int(105 * item["cows"] / total_letters),
                    10
                ),
                border_radius=5
            )

            cow_text = self.small_font.render(
                str(item["cows"]),
                True,
                (95, 120, 75)
            )

            self.screen.blit(
                cow_text,
                (570, card_y + 17)
            )

            # Bull bar
            self.screen.blit(
                self.bull_icon,
                (610, card_y + 17)
            )

            bull_bar = pygame.Rect(
                640, card_y + 23, 105, 10
            )

            pygame.draw.rect(
                self.screen,
                (215, 205, 185),
                bull_bar,
                border_radius=5
            )

            pygame.draw.rect(
                self.screen,
                (180, 120, 75),
                (
                    640,
                    card_y + 23,
                    int(105 * item["bulls"] / total_letters),
                    10
                ),
                border_radius=5
            )

            bull_text = self.small_font.render(
                str(item["bulls"]),
                True,
                (145, 90, 55)
            )

            self.screen.blit(
                bull_text,
                (750, card_y + 17)
            )

        self.screen.set_clip(None)

        # Input area
        if not self.game.is_game_over:
            pygame.draw.rect(
                self.screen,
                self.card_color,
                self.input_box,
                border_radius=8
            )

            border_color = (
                self.input_active_border
                if self.input_active
                else self.input_border
            )

            pygame.draw.rect(
                self.screen,
                border_color,
                self.input_box,
                width=2,
                border_radius=8
            )

            if self.input_text:
                display_text = self.input_text
                display_color = self.text_color
            else:
                display_text = "Type your word..."
                display_color = self.input_hint_color

            entered = self.input_font.render(
                display_text,
                True,
                display_color
            )

            self.screen.blit(
                entered,
                entered.get_rect(
                    midleft=(
                        self.input_box.x + 14,
                        self.input_box.centery
                    )
                )
            )

            self.draw_button(
                self.submit_button,
                "GUESS",
                mouse_pos
            )

        # Status message
        message_y = (
            455 if self.game.is_game_over else 535
        )

        message = self.small_font.render(
            self.message,
            True,
            self.message_color
        )

        message_rect = message.get_rect(
            center=(500, message_y)
        )

        self.screen.blit(message, message_rect)

        # Game-over screen
        if self.game.is_game_over:
            score_color = (
                (125, 100, 75)
                if self.game.is_win
                else self.text_color
            )

            score_text = self.text_font.render(
                f"FINAL SCORE: {self.score}",
                True,
                score_color
            )

            self.screen.blit(
                score_text,
                score_text.get_rect(center=(500, 495))
            )

            self.draw_button(
                self.replay_button,
                "PLAY AGAIN",
                mouse_pos
            )

            self.draw_button(
                self.change_button,
                "CHANGE LEVEL",
                mouse_pos
            )

            self.draw_button(
                self.menu_button,
                "MAIN MENU",
                mouse_pos
            )

        else:
            self.draw_button(
                self.back_button,
                "BACK",
                mouse_pos
            )
