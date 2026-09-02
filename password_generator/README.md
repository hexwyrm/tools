# Hexwyrm's PassWord Generator (PWG)

Hexwyrm's PassWord Generator (PWG) is a simple, cross‑platform GUI tool for generating strong, customizable passwords. It’s designed as a lightweight cybersecurity utility for learning, experimentation, and everyday use.

---

## Features

- **Character set selection**
  - Uppercase letters (`A–Z`)
  - Lowercase letters (`a–z`)
  - Numbers (`0–9`)
  - Symbols (punctuation / special characters)
- **Configurable length**
  - Password length range: `1–55` characters
  - Default length: `16` characters
- **Cross‑platform GUI**
  - Built with Python and Tkinter
  - Intended to run on Linux, Windows, and macOS (where Tkinter is available)
- **User‑friendly interface**
  - Generate button to create a new password
  - Output field is centered and read‑only (can be selected but not edited)
  - One‑click “Copy to Clipboard” button

---

## Requirements

### Running from source
- **Python 3.8+**
- **Tkinter** installed and available for your Python environment

Most systems include Tkinter by default. Some Linux distributions require installing it manually:

- **Arch / RebornOS:**

  ```bash
  sudo pacman -S tk
  ```

- **Debian / Ubuntu Based:**

  ```bash
  sudo apt install tk
  ```

- **Fedora Based:**

  ```bash
  sudo dnf install tk
  ```

---

## Running the files:

**Python**:
- run the py file -

  ```bash
  python pwg.py
  ```

- Run the linux ELF file -

  ```bash
  chmod +x pwg
  ./pwg
  ```

---

## Usage
1. Select one or more character options (uppercase, lowercase, numbers, symbols).

2. Choose the desired password length using the spinbox (1–55).

3. Click Generate Password to create a new password.

4. The generated password will appear in the centered, read‑only field.

5. Click Copy to Clipboard to copy the password.

**Note**: If no character types are selected, PWG will display an error prompting you to choose at least one.

---

## Building PWG Into a Standalone Executable
PWG can be compiled into a standalone binary for Linux or Windows using PyInstaller.

**Linux Build Instructions**
Install PyInstaller using pipx (recommended for Arch‑based systems):

  ```bash
  sudo pacman -S python-pipx
  pipx ensurepath
  pipx install pyinstaller
  ```

  Build the binary:

  ```bash
  pyinstaller --noconsole --onefile pwg.py
  ```

  The executable will appear in:

  ```bash
  dist/pwg
  ```

  Make it executable (if needed):

  ```bash
  chmod +x dist/pwg
  ```

**Windows Build Instructions**

  Install PyInstaller:

  ```bash
  pip install pyinstaller
  ```

  Build the .exe:

  ```bash
  pyinstaller --noconsole --onefile pwg.py
  ```

  The Windows executable will appear in:

  ```bash
  dist\pwg.exe
  ```
---

## License
This project is licensed under the Apache License 2.0.
See the LICENSE file for details.

---

## Author:
Hexwyrm
