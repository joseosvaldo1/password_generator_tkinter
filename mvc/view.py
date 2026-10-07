"""
View layer — Password Generator MVC
Responsável exclusivamente pela interface gráfica (Tkinter).
Não contém lógica de negócio nem chamadas diretas ao Model.
"""

import tkinter as tk
from tkinter import ttk


# ── Paleta de cores ──────────────────────────────────────────────────────────
BG        = "#1E1E2E"   # fundo principal (dark)
BG_CARD   = "#2A2A3E"   # fundo dos cards
FG        = "#CDD6F4"   # texto principal
FG_DIM    = "#7F849C"   # texto secundário
ACCENT    = "#CBA6F7"   # roxo/lilás de destaque
ENTRY_BG  = "#313244"   # fundo dos campos
ENTRY_FG  = "#CDD6F4"
BTN_GEN   = "#A6E3A1"   # verde
BTN_COPY  = "#89B4FA"   # azul
BTN_CLR   = "#F38BA8"   # vermelho/rosa
BTN_FG    = "#1E1E2E"   # texto dos botões (escuro)

BAR_BG    = "#45475A"   # fundo da barra de força


class PasswordView:
    """
    Constrói e expõe todos os widgets da janela principal.
    Os callbacks dos botões e do slider são configurados pelo Controller.
    """

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self._build_window()
        self._build_widgets()

    # ------------------------------------------------------------------ #
    #  Janela                                                              #
    # ------------------------------------------------------------------ #

    def _build_window(self) -> None:
        self.root.title("Password Generator")
        self.root.geometry("360x750")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)

    # ------------------------------------------------------------------ #
    #  Widgets                                                             #
    # ------------------------------------------------------------------ #

    def _build_widgets(self) -> None:
        self._build_title()
        self._build_slider()
        self._build_strength_section()
        self._build_fields()
        self._build_buttons()
        self._build_result()

    # ── Título ──────────────────────────────────────────────────────────

    def _build_title(self) -> None:
        tk.Label(
            self.root,
            text="🔐  Password Generator",
            font=("Arial", 17, "bold"),
            bg=BG, fg=ACCENT,
        ).pack(pady=(18, 4))

        tk.Label(
            self.root,
            text="Senhas determinísticas com SHA-256",
            font=("Arial", 9),
            bg=BG, fg=FG_DIM,
        ).pack(pady=(0, 12))

    # ── Slider de comprimento ────────────────────────────────────────────

    def _build_slider(self) -> None:
        frame = tk.Frame(self.root, bg=BG_CARD, bd=0, relief="flat",
                         padx=14, pady=10)
        frame.pack(fill="x", padx=18, pady=(0, 6))

        # Linha superior: label + valor atual
        top = tk.Frame(frame, bg=BG_CARD)
        top.pack(fill="x")

        tk.Label(top, text="Comprimento da senha",
                 font=("Arial", 10), bg=BG_CARD, fg=FG).pack(side="left")

        self.lbl_length_val = tk.Label(
            top, text="12",
            font=("Arial", 11, "bold"),
            bg=BG_CARD, fg=ACCENT,
        )
        self.lbl_length_val.pack(side="right")

        # Variável compartilhada com o Controller
        self.var_length = tk.IntVar(value=12)

        self.scale_length = tk.Scale(
            frame,
            from_=4, to=20,
            orient=tk.HORIZONTAL,
            variable=self.var_length,
            showvalue=False,
            length=300,
            bg=BG_CARD, fg=FG,
            activebackground=ACCENT,
            highlightthickness=0,
            troughcolor=BAR_BG,
            sliderrelief="flat",
        )
        self.scale_length.pack(fill="x", pady=(4, 0))

        # Rótulos min / max
        minmax = tk.Frame(frame, bg=BG_CARD)
        minmax.pack(fill="x")
        tk.Label(minmax, text="4",  font=("Arial", 8), bg=BG_CARD, fg=FG_DIM).pack(side="left")
        tk.Label(minmax, text="20", font=("Arial", 8), bg=BG_CARD, fg=FG_DIM).pack(side="right")

    # ── Seção de força ───────────────────────────────────────────────────

    def _build_strength_section(self) -> None:
        frame = tk.Frame(self.root, bg=BG_CARD, padx=14, pady=10)
        frame.pack(fill="x", padx=18, pady=(0, 6))

        # Linha: "Força:" + valor
        row = tk.Frame(frame, bg=BG_CARD)
        row.pack(fill="x", pady=(0, 6))

        tk.Label(row, text="Força:",
                 font=("Arial", 10), bg=BG_CARD, fg=FG).pack(side="left")

        self.lbl_strength = tk.Label(
            row, text="—",
            font=("Arial", 10, "bold"),
            bg=BG_CARD, fg=FG_DIM,
        )
        self.lbl_strength.pack(side="right")

        # Barra de força (Canvas)
        self._bar_canvas = tk.Canvas(
            frame,
            width=300, height=14,
            bg=BAR_BG, bd=0,
            highlightthickness=0,
        )
        self._bar_canvas.pack(fill="x")
        self._bar_rect = self._bar_canvas.create_rectangle(
            0, 0, 0, 14, fill=ACCENT, outline=""
        )

        # Linha: tempo estimado
        time_row = tk.Frame(frame, bg=BG_CARD)
        time_row.pack(fill="x", pady=(8, 0))

        tk.Label(time_row, text="⏱  Tempo para quebrar:",
                 font=("Arial", 9), bg=BG_CARD, fg=FG_DIM).pack(side="left")

        self.lbl_crack_time = tk.Label(
            time_row, text="—",
            font=("Arial", 9, "bold"),
            bg=BG_CARD, fg=FG,
        )
        self.lbl_crack_time.pack(side="right")

        # Nota sobre referência
        tk.Label(
            frame,
            text="* RTX 4090 · ataque NTLM offline · Hive Systems 2024",
            font=("Arial", 7), bg=BG_CARD, fg=FG_DIM,
        ).pack(anchor="e", pady=(3, 0))

    # ── Campos de texto ──────────────────────────────────────────────────

    def _build_fields(self) -> None:
        frame = tk.Frame(self.root, bg=BG_CARD, padx=14, pady=10)
        frame.pack(fill="x", padx=18, pady=(0, 6))

        for label_text, attr in [
            ("Key 1",     "entry_key1"),
            ("Key 2",     "entry_key2"),
            ("Reference", "entry_reference"),
        ]:
            tk.Label(frame, text=label_text,
                     font=("Arial", 9), bg=BG_CARD, fg=FG_DIM).pack(anchor="w")

            entry = tk.Entry(
                frame,
                bg=ENTRY_BG, fg=ENTRY_FG,
                insertbackground=FG,
                relief="flat",
                font=("Consolas", 11),
            )
            entry.pack(fill="x", pady=(2, 8), ipady=4)
            setattr(self, attr, entry)

    # ── Botões ───────────────────────────────────────────────────────────

    def _build_buttons(self) -> None:
        frame = tk.Frame(self.root, bg=BG)
        frame.pack(fill="x", padx=18, pady=(0, 6))

        btn_cfg = [
            ("🔑  Gerar Senha",   "btn_generate", BTN_GEN),
            ("📋  Copiar",        "btn_copy",      BTN_COPY),
            ("🗑  Limpar",        "btn_clear",     BTN_CLR),
        ]

        for text, attr, color in btn_cfg:
            btn = tk.Button(
                frame,
                text=text,
                font=("Arial", 10, "bold"),
                bg=color, fg=BTN_FG,
                activebackground=color,
                relief="flat",
                cursor="hand2",
                pady=6,
            )
            btn.pack(fill="x", pady=3)
            setattr(self, attr, btn)

    # ── Resultado ────────────────────────────────────────────────────────

    def _build_result(self) -> None:
        frame = tk.Frame(self.root, bg=BG_CARD, padx=14, pady=10)
        frame.pack(fill="x", padx=18, pady=(0, 14))

        tk.Label(frame, text="Senha Gerada",
                 font=("Arial", 9), bg=BG_CARD, fg=FG_DIM).pack(anchor="w")

        self.label_result = tk.Label(
            frame,
            text="",
            font=("Consolas", 13, "bold"),
            bg=BG_CARD, fg=ACCENT,
            wraplength=300,
        )
        self.label_result.pack(anchor="w", pady=(4, 0))

    # ------------------------------------------------------------------ #
    #  API pública — leitura                                               #
    # ------------------------------------------------------------------ #

    def get_length(self) -> int:
        """Retorna o valor atual do slider."""
        return self.var_length.get()

    def get_key1(self) -> str:
        return self.entry_key1.get()

    def get_key2(self) -> str:
        return self.entry_key2.get()

    def get_reference(self) -> str:
        return self.entry_reference.get()

    def get_result_text(self) -> str:
        return self.label_result.cget("text")

    # ------------------------------------------------------------------ #
    #  API pública — escrita                                               #
    # ------------------------------------------------------------------ #

    def update_length_label(self, value: int) -> None:
        """Atualiza o label que mostra o comprimento atual."""
        self.lbl_length_val.config(text=str(value))

    def update_strength(self, label: str, color: str, percent: float) -> None:
        """
        Atualiza a barra de força e o label de texto.

        Args:
            label:   Texto descritivo (ex.: 'Forte').
            color:   Cor hex da barra (ex.: '#7CB342').
            percent: Fração 0.0–1.0 do preenchimento da barra.
        """
        self.lbl_strength.config(text=label, fg=color)

        bar_width = int(self._bar_canvas.winfo_width() * percent)
        # Garante largura mínima visível
        bar_width = max(bar_width, 6)
        self._bar_canvas.coords(self._bar_rect, 0, 0, bar_width, 14)
        self._bar_canvas.itemconfig(self._bar_rect, fill=color)

    def update_crack_time(self, time_str: str) -> None:
        """Atualiza o label de tempo estimado de quebra."""
        self.lbl_crack_time.config(text=time_str)

    def show_password(self, password: str) -> None:
        self.label_result.config(text=password)

    def clear_result(self) -> None:
        self.label_result.config(text="")

    def clear_inputs(self) -> None:
        """Limpa Key 1, Key 2 e Reference (o slider mantém o valor)."""
        self.entry_key1.delete(0, tk.END)
        self.entry_key2.delete(0, tk.END)
        self.entry_reference.delete(0, tk.END)

    def show_error(self, message: str) -> None:
        from tkinter import messagebox
        messagebox.showerror("Erro", message)

    def show_info(self, title: str, message: str) -> None:
        from tkinter import messagebox
        messagebox.showinfo(title, message)

    def show_warning(self, title: str, message: str) -> None:
        from tkinter import messagebox
        messagebox.showwarning(title, message)
