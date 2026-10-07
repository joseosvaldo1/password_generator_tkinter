# Password Generator

> A deterministic, SHA-256-based desktop password manager built with Python and Tkinter — featuring real-time strength analysis and estimated crack time.

![Python](https://img.shields.io/badge/Python-3.13%2B-blue?logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-informational)
![Architecture](https://img.shields.io/badge/Architecture-MVC-blueviolet)
![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?logo=windows)
![License](https://img.shields.io/badge/License-MIT-green)

---

## Overview

**Password Generator** derives strong, reproducible passwords from two secret keys and a site reference using the **SHA-256** hashing algorithm. No passwords are ever stored — the same combination of inputs always produces the same output, making the tool both secure and predictable for its owner.

The application is structured following the **Model-View-Controller (MVC)** pattern, features a dark-themed GUI, and ships as a single-file Windows executable — no Python installation required for end users.

---

## Features

- 🔐 **Deterministic generation** — SHA-256 seed ensures reproducibility without storage
- 🎚️ **Length slider** — choose password length from **4 to 20 characters**
- 📊 **Real-time strength meter** — color-coded bar updated instantly as you move the slider
- ⏱️ **Estimated crack time** — calculated against a modern GPU attack profile (RTX 4090 · NTLM · Hive Systems 2024)
- 📋 **One-click copy** — copies the generated password to the clipboard via `pyperclip`
- 🌙 **Dark theme** — Catppuccin Mocha color palette
- 📦 **Standalone executable** — packaged with PyInstaller, no dependencies needed at runtime

---

## Password Strength Reference

Strength levels are based on **Shannon entropy** (bits) and calibrated to offline attack speeds from the [Hive Systems Password Table 2024](https://www.hivesystems.com/blog/are-your-passwords-in-the-green).

| Length | Entropy | Strength | Estimated Crack Time (RTX 4090) |
|:------:|:-------:|----------|--------------------------------|
| 4 | 26 bits | 🔴 Very Weak | Instantly |
| 6–7 | 39–46 bits | 🟠 Weak | Seconds – Hours |
| 8–9 | 52–59 bits | 🟡 Moderate | Hours – 1 Year |
| 10–12 | 65–78 bits | 🟢 Strong | Years – Thousands of years |
| 13–15 | 85–98 bits | 🟩 Very Strong | Millions of years |
| 16–20 | 105–131 bits | 🌲 Extremely Strong | Billions of years |

> Attack model: **~350 billion guesses/second** (NTLM hash, single RTX 4090). Real-world times may vary depending on hash algorithm and hardware.

---

## Architecture

The project follows a strict **MVC** separation of concerns:

```
project_password_generator_v2.0/
│
├── main.py                  # Entry point — wires Model, View and Controller
├── icon.ico                 # Application icon (multi-resolution)
├── requirements.txt         # Runtime + build dependencies
├── PasswordGenerator.spec   # PyInstaller build configuration
│
├── mvc/
│   ├── __init__.py
│   ├── model.py             # Business logic: generation, entropy, crack-time estimation
│   ├── view.py              # Tkinter GUI — zero business logic
│   └── controller.py        # Event handling and M↔V mediation
│
├── dist/
│   └── PasswordGenerator.exe  # Standalone Windows executable
│
└── venv/                    # Local virtual environment (not committed)
```

| Layer | File | Responsibility |
|-------|------|----------------|
| **Model** | `mvc/model.py` | SHA-256 generation, entropy calculation, crack-time formatting |
| **View** | `mvc/view.py` | All Tkinter widgets, layout, and public read/write API |
| **Controller** | `mvc/controller.py` | Event binding, slider callbacks, M↔V orchestration |

---

## Getting Started

### Prerequisites

- Python **3.13+**
- Windows 10/11 (for the packaged `.exe`)

### Run from source

```bash
# 1. Clone the repository
git clone https://github.com/your-username/project_password_generator_v2.0.git
cd project_password_generator_v2.0

# 2. Create and activate the virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run
python main.py
```

### Run the standalone executable

Download `PasswordGenerator.exe` from the [`dist/`](./dist) folder and double-click — no installation required.

---

## Building the Executable

```bash
# With the virtual environment activated:
pyinstaller PasswordGenerator.spec --distpath=".\dist" --workpath=".\build" --noconfirm
```

Build flags used:

| Flag | Value | Description |
|------|-------|-------------|
| `console` | `False` | No terminal window (windowed mode) |
| Mode | `onefile` | Everything bundled into a single `.exe` |
| `icon` | `icon.ico` | Application icon embedded in the executable |
| `optimize` | `2` | Bytecode optimization (`-OO` — removes docstrings) |
| `upx` | `True` | UPX compression if available |

---

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `pyperclip` | 1.9.0 | Clipboard copy |
| `Pillow` | 11.1.0 | Icon image processing |
| `pyinstaller` | 6.22.3 | Executable packaging |
| `tkinter` | built-in | GUI framework |
| `hashlib` | built-in | SHA-256 hashing |

---

## How It Works

1. The user provides **Key 1**, **Key 2**, and a **Reference** (e.g., the website name).
2. These are concatenated into a seed string: `key1 + key2 + reference`.
3. The seed is hashed with **SHA-256**, producing a 64-character hexadecimal digest.
4. Each hex digit is mapped to a character from a specific set (lowercase, uppercase, digits, special characters), guaranteeing at least one character from each category.
5. The remaining characters are drawn from the full 91-character pool.
6. The final password is deterministically shuffled using the hash as a sort key.

> The same inputs **always** produce the same password. No data is saved to disk.

---

## Security Notes

- Passwords are never written to disk or transmitted over a network.
- The deterministic nature means the tool functions as a **stateless password manager** — your master keys are the only secret to protect.
- Strength estimates assume an **offline brute-force attack** against a fast hash (NTLM). Real-world security also depends on where and how the password is used.

---

## License

Distributed under the **MIT License**. See [`LICENSE`](./LICENSE) for details.
