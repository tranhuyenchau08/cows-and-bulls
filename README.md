# Cows and Bulls

A number guessing game built with Python and Pygame.

## Features

- Number Mode
- Word Mode
- Multiple difficulty levels
- Sound effects with ON/OFF control
- Multiple visual themes
- Player statistics and leaderboard

## Requirements

- Python 3.12
- Pygame
- Other dependencies listed in requirements.txt, if available

## Run from source

1. Open the project folder.
2. Open PowerShell or Command Prompt.
3. Install the required packages by running:

pip install -r requirements.txt

4. Start the game:

python main.py

If requirements.txt does not exist, install the required packages manually.

## Run the Windows application

After building the application, open:

dist/CowsAndBulls/CowsAndBulls.exe

Keep all supporting files and folders inside dist/CowsAndBulls together with the executable.

## Build the application

Install PyInstaller:

pip install pyinstaller

Build the application:

pyinstaller --noconfirm --clean --windowed --onedir --name CowsAndBulls main.py

The output will be available in the dist folder.

## Project structure

cows-and-bulls/
- main.py
- modes/
  - number_mode.py
  - word_mode.py
  - other mode files
- README.md
- other project files

## Notes

- Test the executable on Windows before sharing it.
- Include all required images, sounds, fonts, and data files in the packaged application.
- Do not separate the executable from its supporting files when using the onedir build.