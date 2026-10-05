# Cow and Bulls - Team Plan

## 1. Team Members

### Member 1 - Main Developer

Responsibilities:

* Main menu
* Game mode menu
* UI design
* Gameplay interface
* Gameplay animations
* Main game framework
* main.py

### Member 2 - Number Mode Developer

Responsibilities:

* Number Mode game logic
* Number guessing system
* Cow and Bull calculation for Number Mode
* modes/number_mode.py

### Member 3 - Word Mode Developer

Responsibilities:

* Word Mode game logic
* Word guessing system
* Cow and Bull calculation for Word Mode
* modes/word_mode.py


## 2. Project Structure

cows-and-bulls/
├── main.py
├── modes/
│   ├── __init__.py
│   ├── number_mode.py
│   └── word_mode.py
├── TEAM.md
└── README.md



## 3. Git Rules

1. Pull the latest code before starting work.
2. Member 1 mainly works on main.py.
3. Member 2 mainly works on modes/number_mode.py.
4. Member 3 mainly works on modes/word_mode.py.
5. Do not modify another member's main working file without discussing it first.
6. Commit changes with a clear commit message.
7. Push changes after finishing a task.
8. If a conflict happens, discuss it with the team before resolving it.

## 4. Development Workflow

Before working:

git pull

After finishing work:

git add .
git commit -m "Describe your changes"
git push



## 5. Current Development Plan

### Phase 1 - Project Framework

* Create main menu
* Create game mode menu
* Add Number Mode
* Add Word Mode
* Add menu navigation
* Add ESC navigation

### Phase 2 - Game Logic

* Implement Number Mode
* Implement Word Mode
* Implement Cow and Bull calculation
* Connect gameplay logic with the main game

### Phase 3 - Gameplay UI

* Design Number Mode interface
* Design Word Mode interface
* Add input interface
* Add guess history
* Add Cow/Bull result display

### Phase 4 - Animation and Polish

* Add gameplay animations
* Add win animation
* Add wrong-answer feedback
* Add sound effects
* Improve UI
* Test the complete game


## 6. Team Rule

Each member should focus on their assigned part.

If a change requires modifying another member's file, discuss it with the team first.
