"""
Controller layer — Password Generator MVC
Medeia Model e View: trata eventos da UI, invoca a lógica de negócio
e atualiza a View com os resultados.
"""

import pyperclip

from mvc.model import PasswordModel
from mvc.view import PasswordView


class PasswordController:
    """
    Conecta a View ao Model.
    Registra callbacks dos botões e do slider, orquestra o fluxo de dados.
    """

    def __init__(self, model: PasswordModel, view: PasswordView) -> None:
        self.model = model
        self.view = view
        self._bind_events()
        # Força a renderização dos widgets antes de atualizar a barra
        self.view.root.update_idletasks()
        self._refresh_strength()          # exibe força inicial

    # ------------------------------------------------------------------ #
    #  Registro de eventos                                                 #
    # ------------------------------------------------------------------ #

    def _bind_events(self) -> None:
        # Botões
        self.view.btn_generate.config(command=self.on_generate)
        self.view.btn_copy.config(command=self.on_copy)
        self.view.btn_clear.config(command=self.on_clear)

        # Slider: atualiza label de comprimento e indicador de força em tempo real
        self.view.scale_length.config(command=self._on_slider_change)

    # ------------------------------------------------------------------ #
    #  Handlers internos                                                   #
    # ------------------------------------------------------------------ #

    def _on_slider_change(self, value: str) -> None:
        """Chamado pelo Scale a cada movimento. Atualiza UI de força."""
        length = int(float(value))
        self.view.update_length_label(length)
        self._refresh_strength(length)

    def _refresh_strength(self, length: int | None = None) -> None:
        """Recalcula e exibe força + tempo de quebra para o comprimento atual."""
        if length is None:
            length = self.view.get_length()
        label, color, percent = self.model.get_strength(length)
        crack_time = self.model.estimate_crack_time(length)
        self.view.update_strength(label, color, percent)
        self.view.update_crack_time(crack_time)

    # ------------------------------------------------------------------ #
    #  Handlers públicos (botões)                                          #
    # ------------------------------------------------------------------ #

    def on_generate(self) -> None:
        """Lê as entradas, valida, gera a senha e atualiza a View."""
        length = self.view.get_length()
        key1   = self.view.get_key1()
        key2   = self.view.get_key2()
        ref    = self.view.get_reference()

        try:
            self.model.validate_inputs(length, key1, key2, ref)
        except ValueError as exc:
            self.view.show_error(str(exc))
            return

        password = self.model.generate(length, key1, key2, ref)
        self.view.show_password(password)

    def on_copy(self) -> None:
        """Copia a senha exibida para a área de transferência."""
        text = self.view.get_result_text()
        if text:
            pyperclip.copy(text)
            self.view.show_info("Copiado", "Senha copiada para a área de transferência!")
        else:
            self.view.show_warning("Sem Senha", "Nenhuma senha para copiar!")

    def on_clear(self) -> None:
        """Limpa os campos de entrada e o resultado."""
        self.view.clear_inputs()
        self.view.clear_result()
