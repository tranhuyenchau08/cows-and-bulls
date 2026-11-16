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

- Python 3.12 (for running from source)
- Pygame
- Other dependencies listed in `requirements.txt`, if available

## Run from source

Clone or download the project, then open a terminal in the project folder:

```bash
pip install -r requirements.txt
python main.py
```

If `requirements.txt` has not been created yet, install the required packages manually.

## Run the Windows application

After building with PyInstaller, open:

```text
dist/CowsAndBulls/CowsAndBulls.exe
```

Keep the other files and folders inside `dist/CowsAndBulls` together with the executable.

## Build the application

Install PyInstaller:

```bash
pip install pyinstaller
```

Build:

```bash
pyinstaller --noconfirm --clean --windowed --onedir --name CowsAndBulls main.py
```

The output will be in the `dist` folder.

## Project structure

```text
cows-and-bulls/
├── main.py
├── modes/
│   ├── number_mode.py
│   ├── word_mode.py
│   └── ...
├── README.md
└── ...
```

## Notes

- Test the executable on Windows before sharing it.
- Include required images, sounds, fonts, and data files in the packaged application.
- Do not separate the executable from its supporting files when using the `onedir` build.