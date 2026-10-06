import random

class WordGame:
    
    def __init__(self):
        self.difficulty="easy"
        self.word_length=4
        self.word_list=[]
        self.secret_word=""
        self.max_turns=10
        self.attempts_left=10
        self.history=[]
        self.is_game_over=False
        self.is_win=False
        self.load_words()
        self.generate_secret()

    def load_words(self):
        try:
            with open("data/words.txt", "r") as file:
                for line in file:
                    word = line.strip()
                    if len(word)==self.word_length and len(set(word))==self.word_length:
                        self.word_list.append(word)
        except FileNotFoundError:
            print("File not found")

    def generate_secret(self):
        self.secret_word = random.choice(list(self.word_list)).upper()

    def validate_guess(self,guess):
        guess=guess.upper()
        if len(guess)!=self.word_length:
            return False,f"Từ đoán phải có {self.word.length} chữ cái."
        if not guess.isalpha():
            return False,f"Từ đoán chỉ được chứa chữ cái."
        if len(set(guess))!=len(guess):
            return False,"Từ đoán không được có chữ cái lặp lại."
        return True,""

    def check_guess(self,guess):
        guess=guess.upper()
        valid,message=self.validate_guess(guess)
        if not valid:
            return False,message
        self.attempts_left-=1
        bulls=0
        cows=0
        for i in range(self.word_length):
            if guess[i]==self.secret_word[i]:
                bulls+=1
            elif guess[i] in self.secret_word:
                cows+=1
        if bulls==self.word_length:
            self.is_win=True
            self.is_game_over=True
            status="win"
        elif self.attempts_left==0:
            self.is_game_over=True
            status="lose"
        else:
            status="continue"
        result={
            "guess":guess,
            "bulls":bulls,
            "cows":cows,
            "attempts_left":self.attempts_left,
            "is_game_over":self.is_game_over,
            "status":status
        }
        self.history.append(result)
        return result

    def reset(self):
        self.generate_secret()
        self.attempts_left=self.max_turns
        self.history=[]
        self.is_game_over=False
        self.is_win=False


def print_history(game):
    if not game.history:
        print("Chưa có lượt đoán nào.")
        return
    print("--- Lịch sử đoán ---")
    for n,h in enumerate(game.history,start=1):
        print(f"{n}. {h['guess']} -> Bulls: {h['bulls']}, Cows: {h['cows']}")


if __name__=="__main__":
    game=WordGame()
    print("   Cows and Bulls   ")
    print(f"Đoán từ có {game.word_length} chữ cái,không lặp chữ")
    print(f"Bạn có {game.max_turns} lượt đoán. Gõ 'history' để xem lại các lượt đã đoán, gõ 'quit' để thoát.\n")
    while True:
        guess=input(f"[Còn {game.attempts_left} lượt đoán] Nhập từ đoán: ").upper()
        if guess=='QUIT':
            print("Đã thoát trò chơi")
            break
        if guess=='HISTORY':
            print_history(game)
        result=game.check_guess(guess)
        if isinstance(result,tuple):
            print(result[1])
            continue
        if result["status"]=="win":
            print("Chinh xac!Ban da thang!")
        elif result["status"]=="lose":
            print(f"Het luot!Ban da thua! Từ bí mật là {game.secret_word} ")
        else:
            print(f"Bulls: {result['bulls']}, Cows: {result['cows']}")
        if game.is_game_over:
            while True:
                again=input("Gõ 'y' để chơi lại ván mới, 'n' để hết thúc, 'history' để xem lại các lần đoán: ").lower()
                if again=="history":
                    print_history(game)
                    continue
                break
            if again=="y":
                game.reset()
            else:
                print("Kết thúc trò chơi")
                break





