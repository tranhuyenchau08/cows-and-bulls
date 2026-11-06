
import json
from pathlib import Path
from datetime import datetime


class StatsManager:
    def __init__(self, filename="player_stats.json"):
        # Save the file in the project root directory
        self.file_path = Path(__file__).resolve().parent.parent / filename
        self.data = self._default_data()
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

    def get_summary(self):
        """Return summary statistics for the UI."""
        total = self.data["total_games"]
        wins = self.data["wins"]

        win_rate = round(wins / total * 100, 1) if total else 0.0

        return {
            "total_games": total,
            "wins": wins,
            "losses": self.data["losses"],
            "total_score": self.data["total_score"],
            "best_score": self.data["best_score"],
            "win_rate": win_rate,
            "number": self.data["number"].copy(),
            "word": self.data["word"].copy(),
            "history": list(reversed(self.data["history"])),
        }


# Shared stats manager used by both game modes
stats_manager = StatsManager()
