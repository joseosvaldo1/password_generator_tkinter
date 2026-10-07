"""
main.py — Ponto de entrada da aplicação Password Generator (MVC).
Instancia Model, View e Controller, depois inicia o loop da GUI.
"""

import tkinter as tk
from pathlib import Path

from mvc.model import PasswordModel
from mvc.view import PasswordView
from mvc.controller import PasswordController


def main() -> None:
    root = tk.Tk()

    # Aplica o ícone da janela (Windows)
    try:
        icon_path = Path(__file__).parent / "icon.ico"
        root.iconbitmap(str(icon_path))
    except Exception:
        pass  # Ignora se o arquivo não for encontrado

    model = PasswordModel()
    view = PasswordView(root)
    PasswordController(model, view)   # o controller registra os eventos

    root.mainloop()


if __name__ == "__main__":
    main()
