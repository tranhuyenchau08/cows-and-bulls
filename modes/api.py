from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Literal, Optional
from datetime import datetime
import json
import os

app = FastAPI(title="Cows & Bulls Leaderboard API")
DATA_FILE = "leaderboard.json"

# --- Schemas nhận dữ liệu từ Client ---
class MatchResult(BaseModel):
    player_name: str
    mode: Literal["number", "word"]  # Chỉ nhận 1 trong 2 chế độ
    result: Literal["win", "loss"]
    target: str                     # Đáp án (ví dụ: "4821" hoặc "PYTHON")
    attempts: int                   # Số lượt đoán
    score: int                      # Điểm đạt được trong lượt chơi này

class UserAuth(BaseModel):
    username: str
    password: str

# --- Helper Functions ---
def load_data() -> dict:
    # ĐÃ SỬA: Khởi tạo mặc định có cả "accounts" và "players"
    default_structure = {"accounts": {}, "players": {}}
    if not os.path.exists(DATA_FILE):
        return default_structure
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            # Đảm bảo luôn có 2 key chính
            if "accounts" not in data:
                data["accounts"] = {}
            if "players" not in data:
                data["players"] = {}
            return data
        except json.JSONDecodeError:
            return default_structure

def save_data(data: dict):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def init_player_stats() -> dict:
    """Khởi tạo cấu trúc dữ liệu ban đầu đúng theo template của bạn"""
    return {
        "total_games": 0,
        "wins": 0,
        "losses": 0,
        "total_score": 0,
        "best_score": 0,
        "current_streak": 0,
        "best_streak": 0,
        "number": {"games": 0, "wins": 0, "losses": 0, "score": 0, "best_score": 0},
        "word": {"games": 0, "wins": 0, "losses": 0, "score": 0, "best_score": 0},
        "history": []
    }

# --- API Endpoints ---


@app.post("/api/register")
def register(user: UserAuth):
    db = load_data()
    accounts = db["accounts"]
    
    if user.username in accounts:
        return {"success": False, "message": "Tên tài khoản đã tồn tại!"}
    
    accounts[user.username] = user.password
    
    
    # Khởi tạo stats cho người chơi mới
    players = db["players"]
    if user.username not in players:
        players[user.username] = init_player_stats()
        
    save_data(db)
    return {"success": True, "message": "Đăng ký thành công!"}

@app.post("/api/login")
def login(user: UserAuth):
    db = load_data()
    accounts = db["accounts"]
    
    if user.username not in accounts:
        return {"success": False, "message": "Tài khoản không tồn tại!"}
    
    if accounts[user.username] != user.password:
        return {"success": False, "message": "Mật khẩu không chính xác!"}
        
    return {"success": True, "message": "Đăng nhập thành công!"}
@app.post("/api/submit-score")
def submit_score(data: MatchResult):
    db = load_data()
    players = db["players"]
    
    # Lấy thông tin người chơi hoặc khởi tạo mới nếu chưa tồn tại
    player = players.get(data.player_name, init_player_stats())

    # Đảm bảo mode_stats tồn tại
    if data.mode not in player:
        player[data.mode] = {"games": 0, "wins": 0, "losses": 0, "score": 0, "best_score": 0}

    mode_stats = player[data.mode]

    # 1. Cập nhật chỉ số chung
    player["total_games"] += 1
    player["total_score"] += data.score
    
    # 2. Cập nhật chỉ số theo Mode (number / word)
    mode_stats["games"] += 1
    mode_stats["score"] += data.score
    
    if data.result == "win":
        player["wins"] += 1
        mode_stats["wins"] += 1
        player["current_streak"] += 1
        
        # Cập nhật streak cao nhất
        if player["current_streak"] > player["best_streak"]:
            player["best_streak"] = player["current_streak"]
            
        # Cập nhật best score chung & best score mode
        if data.score > player["best_score"]:
            player["best_score"] = data.score
        if data.score > mode_stats["best_score"]:
            mode_stats["best_score"] = data.score
            
    else:  # loss
        player["losses"] += 1
        mode_stats["losses"] += 1
        player["current_streak"] = 0  # Đứt chuỗi thắng
        
    # 3. Thêm bản ghi vào lịch sử (giữ tối đa 20 trận gần nhất)
    history_item = {
        "mode": data.mode,
        "result": data.result,
        "target": data.target,
        "attempts": data.attempts,
        "score": data.score,
        "played_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    if "history" not in player:
        player["history"] = []

    player["history"].insert(0, history_item)
    player["history"] = player["history"][:20]
    
    # Lưu lại vào file JSON
    players[data.player_name] = player
    save_data(db)
    
    return {
        "message": "Cập nhật kỷ lục thành công!",
        "player_name": data.player_name,
        "current_streak": player["current_streak"],
        "best_score": player["best_score"]
    }

@app.get("/api/leaderboard")
def get_leaderboard(mode: Optional[str] = None):
    """
    Lấy Top 10 người chơi có điểm cao nhất.
    Có thể lọc theo mode: /api/leaderboard?mode=number hoặc /api/leaderboard?mode=word
    """
    db = load_data()
    players = db["players"]
    
    leaderboard = []
    for name, stats in players.items():
        if mode in ["number", "word"]:
            score = stats[mode]["best_score"]
            wins = stats[mode]["wins"]
            games = stats[mode]["games"]
        else:
            score = stats["best_score"]
            wins = stats["wins"]
            games = stats["total_games"]
            
        leaderboard.append({
            "player_name": name,
            "best_score": score,
            "wins": wins,
            "total_games": games
        })
        
    # Sắp xếp giảm dần theo điểm cao nhất (best_score)
    leaderboard.sort(key=lambda x: x["best_score"], reverse=True)
    return leaderboard[:10]

@app.get("/api/player/{player_name}")
def get_player_stats(player_name: str):
    """Lấy toàn bộ thông tin thống kê của 1 người chơi cụ thể"""
    db = load_data()
    players = db["players"]
    if player_name not in players:
        raise HTTPException(status_code=404, detail="Không tìm thấy người chơi này!")
    return players[player_name]

if __name__ == "__main__":
    import uvicorn
    # host="0.0.0.0" để các máy khác trong mạng LAN truy cập được
    uvicorn.run(app, host="0.0.0.0", port=8000)