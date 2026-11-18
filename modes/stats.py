
import json
from pathlib import Path
from datetime import datetime
import requests

API_URL = "http://127.0.0.1:8000"

class StatsManager:
    def __init__(self, filename="player_stats.json"):
        self.file_path = Path(__file__).resolve().parent.parent / filename
        self.data = self._default_data()
        self.current_username = None
        self.server_data = None
        self.load()

    @staticmethod
    def _default_data():
        return {
            "total_games": 0,
            "wins": 0,
            "losses": 0,
            "total_score": 0,
            "best_score": 0,
            "current_streak": 0,
            "best_streak": 0,
            "number": {
                "games": 0,
                "wins": 0,
                "losses": 0,
                "score": 0,
                "best_score": 0,
            },
            "word": {
                "games": 0,
                "wins": 0,
                "losses": 0,
                "score": 0,
                "best_score": 0,
            },
            "history": [],
        }

    def load(self):
        """Load saved statistics, or create default data."""
        if not self.file_path.exists():
            self.save()
            return

        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                saved = json.load(file)

            defaults = self._default_data()
            defaults.update(saved)

            for mode in ("number", "word"):
                if not isinstance(defaults.get(mode), dict):
                    defaults[mode] = self._default_data()[mode]
                else:
                    mode_defaults = self._default_data()[mode]
                    mode_defaults.update(defaults[mode])
                    defaults[mode] = mode_defaults

            if not isinstance(defaults.get("history"), list):
                defaults["history"] = []

            self.data = defaults

        except (OSError, json.JSONDecodeError, TypeError):
            self.data = self._default_data()

    def save(self):
        """Write statistics to JSON."""
        try:
            self.file_path.parent.mkdir(parents=True, exist_ok=True)

            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump(
                    self.data,
                    file,
                    indent=4,
                    ensure_ascii=False,
                )
        except OSError as error:
            print(f"Could not save statistics: {error}")

    def record_result(self, mode, difficulty, won, score):
        """Save the result of one completed game."""
        mode = mode.lower()

        if mode not in ("number", "word"):
            raise ValueError("mode must be 'number' or 'word'")

        score = max(0, int(score))
        won = bool(won)

        # Update winning streak and calculate bonus
        if won:
            self.data["current_streak"] += 1
            self.data["best_streak"] = max(
                self.data["best_streak"],
                self.data["current_streak"],
            )

            streak = self.data["current_streak"]

            # Winning bonus
            score += 50

            # Streak bonus
            if streak == 2:
                score += 30
            elif streak >= 3:
                score += 50

        else:
            self.data["current_streak"] = 0

        self.data["total_games"] += 1
        self.data["total_score"] += score

        if won:
            self.data["wins"] += 1
        else:
            self.data["losses"] += 1

        mode_stats = self.data[mode]
        mode_stats["games"] += 1
        mode_stats["score"] += score

        if won:
            mode_stats["wins"] += 1
        else:
            mode_stats["losses"] += 1

        mode_stats["best_score"] = max(
            mode_stats["best_score"],
            score,
        )

        self.data["best_score"] = max(
            self.data["best_score"],
            score,
        )

        self.data["history"].append({
            "mode": mode.title(),
            "difficulty": str(difficulty).title(),
            "result": "Win" if won else "Loss",
            "score": score,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        })

        # Keep the most recent 100 games
        self.data["history"] = self.data["history"][-100:]

        self.save()

        return score

    def register_server(self, username, password):
        try:
            response = requests.post(
                f"{API_URL}/api/register",
                json={
                    "username": username,
                    "password": password
                },
                timeout=5
            )
            response.raise_for_status()
            data = response.json()

            return data.get("success", False), data.get("message", "Registration failed!")

        except requests.exceptions.RequestException:
            return False, "Could not connect to the server!"

    def login_server(self, username, password):
        try:
            response = requests.post(
                f"{API_URL}/api/login",
                json={
                    "username": username,
                    "password": password
                },
                timeout=5
            )
            response.raise_for_status()
            data = response.json()

            if data.get("success", False):
                self.current_username = username
                self.server_data = self.fetch_player_stats(username)

                if self.server_data is None:
                    self.server_data = self._default_data()

            return data.get("success", False), data.get("message", "Login failed!")

        except requests.exceptions.RequestException:
            return False, "Could not connect to the server!"

    def fetch_player_stats(self, username):
        try:
            response = requests.get(
                f"{API_URL}/api/player/{username}",
                timeout=5
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            print("Could not fetch player statistics:", e)
            return None

    def refresh_player_stats(self, username=None):
        if username is None:
            username = self.current_username

        if not username:
            return

        new_data = self.fetch_player_stats(username)

        if new_data is not None:
            self.server_data = new_data

    def fetch_global_leaderboard(self):
        try:
            response = requests.get(
                f"{API_URL}/api/leaderboard",
                timeout=5
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException:
            print("Could not load the leaderboard from the server!")
            return []
        

    def submit_score_server(
        self, player_name, mode, difficulty, result, target, attempts, score
    ):
        try:
            response = requests.post(
                f"{API_URL}/api/submit-score",
                json={
                    "player_name": player_name,
                    "mode": mode,
                    "difficulty": difficulty,
                    "result": result,
                    "target": str(target),
                    "attempts": attempts,
                    "score": score
                },
                timeout=5
            )
            response.raise_for_status()
            print("Score submitted successfully!")
            return True

        except requests.exceptions.RequestException as e:
            print("Could not submit score to the server:", e)
            return False

    def get_summary(self):
        """Return statistics for the currently logged-in player."""

        data = self.server_data if self.server_data is not None else self.data

        total = data["total_games"]
        wins = data["wins"]

        win_rate = round(wins / total * 100, 1) if total else 0.0

        # Convert server history to the format used by the UI
        history = []

        for item in data.get("history", []):
            history.append({
                "mode": item.get("mode", "").title(),
                "difficulty": item.get("difficulty", "Unknown"),
                "result": item.get("result", "").title(),
                "score": item.get("score", 0),
                "date": item.get("date", item.get("played_at", ""))
            })

        return {
            "total_games": total,
            "wins": wins,
            "losses": data["losses"],
            "total_score": data["total_score"],
            "best_score": data["best_score"],
            "win_rate": win_rate,
            "number": data["number"].copy(),
            "word": data["word"].copy(),
            "history": list(reversed(history)),
        }


# Shared stats manager used by both game modes
stats_manager = StatsManager()
