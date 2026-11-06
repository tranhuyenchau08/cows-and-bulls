import os
import random

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WORDS_PATH = os.path.join(BASE_DIR, "words.txt")

DIFFICULTIES = {
    "easy": {"word_length": 4, "max_turns": 10},
    "normal": {"word_length": 5, "max_turns": 8},
    "hard": {"word_length": 6, "max_turns": 7},
}


class WordGame:

    def __init__(self, difficulty="easy"):
        self.word_list = []
        self.secret_word = ""
        self.set_difficulty(difficulty)

    def set_difficulty(self, difficulty):
        difficulty = difficulty.lower()

        if difficulty not in DIFFICULTIES:
            raise ValueError(f"Invalid difficulty: {difficulty}")

        config = DIFFICULTIES[difficulty]
        self.difficulty = difficulty
        self.word_length = config["word_length"]
        self.max_turns = config["max_turns"]

        self.load_words()

        if not self.word_list:
            raise ValueError(
                f"No valid {self.word_length}-letter words found in "
                f"{WORDS_PATH}."
            )

        self.reset()

    def load_words(self):
        self.word_list = []

        try:
            with open(WORDS_PATH, "r", encoding="utf-8") as file:
                for line in file:
                    word = line.strip().upper()

                    if (
                        len(word) == self.word_length
                        and word.isalpha()
                        and len(set(word)) == self.word_length
                    ):
                        self.word_list.append(word)

        except FileNotFoundError:
            print(f"Error: Word list file not found: {WORDS_PATH}")

    def generate_secret(self):
        self.secret_word = random.choice(self.word_list)

    def validate_guess(self, guess):
        if not isinstance(guess, str):
            return False, "Please enter a valid word."

        guess = guess.strip().upper()

        if not guess.isalpha():
            return False, "Your guess must contain letters only."

        if len(guess) != self.word_length:
            return False, (
                f"Your guess must contain exactly "
                f"{self.word_length} letters."
            )

        if len(set(guess)) != len(guess):
            return False, "Letters cannot be repeated."

        return True, ""

    def check_guess(self, guess):
        if self.is_game_over:
            return False, "The game is over. Please start a new game."

        guess = guess.strip().upper()
        valid, message = self.validate_guess(guess)

        if not valid:
            return False, message

        self.attempts_left -= 1

        bulls = 0
        cows = 0

        for i in range(self.word_length):
            if guess[i] == self.secret_word[i]:
                bulls += 1
            elif guess[i] in self.secret_word:
                cows += 1

        if bulls == self.word_length:
            self.is_win = True
            self.is_game_over = True
            status = "win"

        elif self.attempts_left == 0:
            self.is_game_over = True
            status = "lose"

        else:
            status = "continue"

        result = {
            "guess": guess,
            "bulls": bulls,
            "cows": cows,
            "attempts_left": self.attempts_left,
            "is_game_over": self.is_game_over,
            "status": status,
        }

        self.history.append(result)
        return result

    def reset(self):
        self.generate_secret()
        self.attempts_left = self.max_turns
        self.history = []
        self.is_game_over = False
        self.is_win = False


def print_history(game):
    if not game.history:
        print("No guesses have been made yet.")
        return

    print("--- Guess History ---")

    for n, history_item in enumerate(game.history, start=1):
        print(
            f"{n}. {history_item['guess']} -> "
            f"Bulls: {history_item['bulls']}, "
            f"Cows: {history_item['cows']}"
        )


def choose_difficulty():
    while True:
        choice = input(
            "Choose difficulty (easy / normal / hard): "
        ).strip().lower()

        if choice in DIFFICULTIES:
            return choice

        print("Invalid choice. Please try again.")


def print_intro(game):
    print(f"Difficulty: {game.difficulty.capitalize()}")
    print(
        f"Guess a {game.word_length}-letter word "
        "with no repeated letters."
    )
    print(
        f"You have {game.max_turns} attempts. "
        "Type 'history' to view previous guesses "
        "or 'quit' to exit.\n"
    )


if __name__ == "__main__":
    print("Cows and Bulls")

    game = WordGame(choose_difficulty())
    print_intro(game)

    while True:
        guess = input(
            f"[{game.attempts_left} attempts left] Enter your guess: "
        ).strip().upper()

        if guess == "QUIT":
            print("You have exited the game.")
            break

        if guess == "HISTORY":
            print_history(game)
            continue

        result = game.check_guess(guess)

        if isinstance(result, tuple):
            print(f"Error: {result[1]}")
            continue

        if result["status"] == "win":
            print("Correct! You win!")

        elif result["status"] == "lose":
            print(
                f"Out of attempts! You lose. "
                f"The secret word was {game.secret_word}."
            )

        else:
            print(
                f"Bulls: {result['bulls']}, "
                f"Cows: {result['cows']}"
            )

        if game.is_game_over:
            while True:
                again = input(
                    "'y': play again | 'm': change difficulty | "
                    "'n': quit | 'history': view history: "
                ).strip().lower()

                if again == "history":
                    print_history(game)
                    continue

                if again in ("y", "m", "n"):
                    break

                print("Invalid choice. Please enter y, m, n, or history.")

            if again == "y":
                game.reset()

            elif again == "m":
                game.set_difficulty(choose_difficulty())
                print_intro(game)

            else:
                print("Game ended.")
                break