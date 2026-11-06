
import pygame

from modes.number import NumberGame
from modes.effects import sound_effects
from modes.stats import stats_manager


class NumberMode:
    def __init__(self, screen, difficulty="Easy"):
        self.screen = screen
        self.difficulty = difficulty
        self.game = NumberGame(difficulty)
        self.result_saved = False
        self.score = 0

        # Fonts
        self.title_font = pygame.font.SysFont(
            "arial", 48, bold=True
        )
        self.text_font = pygame.font.SysFont("arial", 25)
        self.small_font = pygame.font.SysFont("arial", 21)
        self.input_font = pygame.font.SysFont("consolas", 30)

        # Colors
        self.background = (245, 235, 210)
        self.text_color = (50, 40, 30)
        self.button_color = (120, 170, 100)
        self.button_hover = (150, 200, 130)
        self.input_hint_color = (145, 145, 145)
        self.white = (255, 255, 255)

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
        self.replay_button = pygame.Rect(75, 480, 250, 55)
        self.change_button = pygame.Rect(375, 480, 250, 55)
        self.menu_button = pygame.Rect(675, 480, 250, 55)

    
    def calculate_score(self, won):
        if not won:
            return 0

        difficulty = str(self.game.difficulty).lower()

        base_scores = {
            "easy": 100,
            "normal": 150,
            "hard": 200,
        }

        base_score = base_scores.get(difficulty, 100)

        turns_left = getattr(
            self.game,
            "turns_left",
            getattr(self.game, "attempts_left", 0),
        )

        return base_score + max(0, turns_left) * 20

    
    def save_finished_game(self, won):
        if self.result_saved:
            return

        self.score = self.calculate_score(won)

        self.score = stats_manager.record_result(
            mode="number",
            difficulty=self.game.difficulty,
            won=won,
            score=self.score,
        )

        self.result_saved = True



    @staticmethod
    def format_result(bulls, cows):
        bull_word = "Bull" if bulls == 1 else "Bulls"
        cow_word = "Cow" if cows == 1 else "Cows"

        return f"{bulls} {bull_word}, {cows} {cow_word}"

    
    def submit_guess(self):
        if self.game.game_over:
            return

        guess = self.input_text.strip()

        if not guess:
            sound_effects.play("wrong")
            self.message = "Please enter a guess."
            self.message_color = self.text_color
            return

        result = self.game.check_guess(guess)
        self.input_text = ""

        if result["status"] == "error":
            sound_effects.play("wrong")
            self.message = result["message"]
            self.message_color = (180, 55, 45)
            return

        bulls = result["bulls"]
        cows = result["cows"]

        self.message = (
            f'{result["guess"]}: '
            f'{self.format_result(bulls, cows)}'
        )
        self.message_color = self.text_color

        if result["won"]:
            sound_effects.play("win")
            self.message = (
                f"YOU WIN! Answer: {self.game.secret}"
            )
            self.message_color = (45, 120, 55)

            # Them: luu ket qua khi thang
            self.save_finished_game(True)

        elif result["game_over"]:
            sound_effects.play("lose")
            self.message = (
                f"GAME OVER! Answer: {self.game.secret}"
            )
            self.message_color = (180, 55, 45)

            # Them: luu ket qua khi thua
            self.save_finished_game(False)

        else:
            sound_effects.play("click")


    def handle_events(self, event):
        # Keyboard input
        if event.type == pygame.KEYDOWN:
            if self.game.game_over:
                return None

            if event.key == pygame.K_RETURN:
                self.submit_guess()

            elif event.key == pygame.K_BACKSPACE:
                if self.input_active:
                    self.input_text = self.input_text[:-1]

            elif event.unicode.isdigit():
                if (
                    self.input_active
                    and len(self.input_text) < self.game.length
                ):
                    self.input_text += event.unicode

        # Mouse input
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button != 1:
                return None

            if self.game.game_over:
                if self.replay_button.collidepoint(event.pos):
                    self.game.reset()
                    # Reset score tracking for the new game
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

        label = self.text_font.render(
            text,
            True,
            self.text_color
        )

        self.screen.blit(
            label,
            label.get_rect(center=rect.center)
        )

    def draw(self, mouse_pos=None):
        self.screen.fill(self.background)

        # main.py passes mouse coordinates in canvas space.
        # Fallback is useful if draw() is called independently.
        if mouse_pos is None:
            mouse_pos = (-1, -1)

        # Title
        title = self.title_font.render(
            "NUMBER MODE",
            True,
            self.text_color
        )
        self.screen.blit(
            title,
            title.get_rect(center=(500, 55))
        )

        # Game information
        info_text = (
            f"Difficulty: {self.game.difficulty}   |   "
            f"Digits: {self.game.length}   |   "
            f"Turns left: {self.game.turns_left}"
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
        history_start_y = 145
        history_spacing = 25

        for index, item in enumerate(self.game.history[-10:]):
            line = (
                f'{item["guess"]}  -  '
                f'{self.format_result(item["bulls"], item["cows"])}'
            )

            surface = self.small_font.render(
                line,
                True,
                self.text_color
            )

            self.screen.blit(
                surface,
                surface.get_rect(
                    center=(
                        500,
                        history_start_y + index * history_spacing
                    )
                )
            )

        # Input area
        if not self.game.game_over:
            pygame.draw.rect(
                self.screen,
                self.white,
                self.input_box,
                border_radius=8
            )

            border_color = (
                self.button_color
                if self.input_active
                else self.text_color
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
                display_text = "Type your guess..."
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
        message_y = 390 if self.game.game_over else 535

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
        if self.game.game_over:
            # Final score
            score_text = self.text_font.render(
                f"FINAL SCORE: {self.score}",
                True,
                (45, 120, 55) if self.game.won else self.text_color
            )

            self.screen.blit(
                score_text,
                score_text.get_rect(center=(500, 435))
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
