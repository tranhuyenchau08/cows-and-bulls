import random


class NumberGame:
    def __init__(self, difficulty="Easy"):
        self.difficulty = difficulty.capitalize()

        if self.difficulty == "Easy":
            self.length = 4
            self.max_turns = 10
        elif self.difficulty == "Normal":
            self.length = 5
            self.max_turns = 8
        elif self.difficulty == "Hard":
            self.length = 6
            self.max_turns = 7
        else:
            self.length = 4
            self.max_turns = 10

        self.secret = ""
        self.turns_left = self.max_turns
        self.history = []
        self.game_over = False
        self.won = False

        self.reset()

    def getDigits(self, num):
        return [int(i) for i in str(num)]

    def noDuplicates(self, num):
        num_li = self.getDigits(num)
        return len(num_li) == len(set(num_li))

    def generate_secret(self):
        min_val = 10 ** (self.length - 1)
        max_val = (10 ** self.length) - 1

        while True:
            num = random.randint(min_val, max_val)
            if self.noDuplicates(num):
                self.secret = str(num)
                return self.secret

    def reset(self):
        self.turns_left = self.max_turns
        self.history = []
        self.game_over = False
        self.won = False
        self.generate_secret()

    def validate_guess(self, guess):
        if not isinstance(guess, str):
            return False, "Please enter a valid string."

        if not guess.isdigit():
            return False, "Your guess must contain digits only."

        if len(guess) != self.length:
            return False, (
                f"Your guess must contain exactly "
                f"{self.length} digits."
            )

        if len(set(guess)) != len(guess):
            return False, "Digits cannot be repeated."

        return True, "Valid"

    def check_guess(self, guess):
        if self.game_over:
            return {
                "status": "error",
                "message": "The game is over. Please start a new game."
            }

        is_valid, msg = self.validate_guess(guess)

        if not is_valid:
            return {
                "status": "error",
                "message": msg
            }

        bulls = 0
        cows = 0

        for i in range(self.length):
            if guess[i] == self.secret[i]:
                bulls += 1
            elif guess[i] in self.secret:
                cows += 1

        self.turns_left -= 1

        is_correct = bulls == self.length

        if is_correct:
            self.won = True
            self.game_over = True
        elif self.turns_left <= 0:
            self.won = False
            self.game_over = True

        turn_result = {
            "status": "ok",
            "guess": guess,
            "bulls": bulls,
            "cows": cows,
            "is_correct": is_correct,
            "attempts_left": self.turns_left,
            "game_over": self.game_over,
            "won": self.won,
        }

        self.history.append(turn_result)

        return turn_result


if __name__ == "__main__":
    game = NumberGame(difficulty="Easy")

    print(f"Game started! Difficulty: {game.difficulty}")
    print(
        f"Guess a {game.length}-digit number with no repeated digits. "
        f"You have {game.max_turns} attempts."
    )

    while not game.game_over:
        user_input = input(
            f"\nEnter your guess "
            f"({game.turns_left} attempts left): "
        )

        response = game.check_guess(user_input)

        if response["status"] == "error":
            print(f"Error: {response['message']}")
            continue

        print(
            f"Result: {response['bulls']} Bulls, "
            f"{response['cows']} Cows"
        )

    if game.won:
        print("YOU WIN! Congratulations!")
    else:
        print(f"GAME OVER! The secret number was {game.secret}.")
