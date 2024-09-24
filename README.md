# Annot8 Keypress & Screenshot Capture Script

## Overview

This script captures user keypresses and screenshots during an interactive session, creating a step-by-step tutorial in Markdown format. It listens for keyboard events, saves screenshots from the clipboard, and tracks keypresses to provide a comprehensive record of actions performed during the session.

## Features

- **Keypress Logging**: Tracks and logs keypresses, converting them into readable text.
- **Screenshot Capture**: Automatically saves screenshots copied to the clipboard in a dedicated directory.
- **Markdown Generation**: Creates a Markdown file (`tutorial.md`) with each step, including keypress context and linked screenshots.
- **F9 for Step Completion**: Press `F9` to mark the end of a step, logging the current keypresses and screenshot.
- **Shift & Caps Lock Handling**: Accurately processes uppercase characters based on `SHIFT` and `CAPS LOCK` status.

## Requirements

- Python 3.x
- `evdev` library for capturing keypresses:
  ```bash
  pip install evdev
  ```
- Wayland clipboard tools (`wl-paste`, `wl-copy`) for managing clipboard images.
- Linux-based environment (uses `evdev` and Wayland).

## Installation

1. Clone the project or download the script.
2. Install the dependencies (e.g., `evdev` for keypress capturing and Wayland utilities for clipboard handling).
3. Make sure the script is executed on a Linux system with access to keyboard devices.

## How to Run

1. **Prepare your environment**:
   - Ensure the keyboard input device path is correct (`device_path` variable).
   - The screenshot tools must be installed (`wl-paste` and `wl-copy`).
   
2. **Run the script**:
   ```bash
   python3 annot8.py
   ```

3. **Usage**:
   - Perform your actions on the keyboard.
   - Press `Print Screen` to copy a screenshot to the clipboard.
   - Press `F9` to save the current step (including keypresses and the screenshot).
   - The script will save keypresses and screenshots in sequence, and a Markdown file (`tutorial.md`) will be generated.

4. **Stopping the script**:
   - Press `Ctrl+C` to stop the script and generate the Markdown file with all recorded steps.

## Output

- **Markdown File**: A file named `tutorial.md` will be generated in the project directory with the following format for each step:
   ```markdown
   ## Step 1: step description
   **Context**: hello my friend [screenshot_path]
   ```

- **Screenshots**: Screenshots are saved in the `screenshots/` folder with filenames based on step numbers and timestamps.

## Limitations

- The script is designed for Linux environments using the Wayland display server. It may not work on Windows or macOS without modifications.
- It does not handle input devices that are not keyboards.
- Caps Lock handling is global and affects all text until toggled off.
