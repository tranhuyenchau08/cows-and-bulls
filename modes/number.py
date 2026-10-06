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

        self.reset()

    def getDigits(self, num):
        return [int(i) for i in str(num)]

    def noDuplicates(self, num):
        num_li = self.getDigits(num)
        if len(num_li) == len(set(num_li)):
            return True
        else:
            return False

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
        self.generate_secret()

    def validate_guess(self, guess):
        if not isinstance(guess, str):
            return False, "Vui lòng nhập chuỗi ký tự."

        if not guess.isdigit():
            return False, "Dự đoán chỉ được chứa các chữ số."

        if len(guess) != self.length:
            return False, f"Dự đoán phải có độ dài {self.length} chữ số."

        if len(set(guess)) != len(guess):
            return False, "Dự đoán không được có chữ số lặp lại."

        return True, "Hợp lệ"

    def check_guess(self, guess):
        is_valid, msg = self.validate_guess(guess)
        if not is_valid:
            return {"status": "error", "message": msg}

        bulls = 0
        cows = 0
        for i in range(self.length):
            if guess[i] == self.secret[i]:
                bulls += 1
            elif guess[i] in self.secret:
                cows += 1

        self.turns_left -= 1

        is_correct = (bulls == self.length)
        game_over = is_correct or (self.turns_left <= 0)

        turn_result = {
            "guess": guess,
            "bulls": bulls,
            "cows": cows,
            "is_correct": is_correct,
            "attempts_left": self.turns_left,
            "game_over": game_over
        }

        self.history.append(turn_result)

        return turn_result


if __name__ == "__main__":
    game = NumberGame(difficulty="Easy")

    print(f"Game đã bắt đầu! Chế độ: {game.difficulty}")
    print(f"Bạn cần đoán chuỗi {game.length} chữ số không trùng lặp. Bạn có {game.max_turns} lượt.")

    while game.turns_left > 0:
        user_input = input(f"\nNhập số dự đoán của bạn (còn {game.turns_left} lượt): ")

        response = game.check_guess(user_input)

        if "status" in response and response["status"] == "error":
            print(f"Lỗi: {response['message']}")
            continue

        print(f"Kết quả: {response['bulls']} Bulls, {response['cows']} Cows")

        if response["is_correct"]:
            print("Chúc mừng! Bạn đã thắng.")
            break

        if response["game_over"]:
            print(f"Game Over! Đáp án bí mật là {game.secret}.")
            break

