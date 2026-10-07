"""
Model layer — Password Generator MVC
Responsável pela lógica de negócio: geração, validação,
cálculo de entropia, força e tempo estimado de quebra.
"""

import hashlib
import math
import string


class PasswordModel:
    """Encapsula a lógica de geração de senhas baseada em hash SHA-256."""

    MIN_LENGTH = 4
    MAX_LENGTH = 20

    LOWERCASE    = string.ascii_lowercase          # 26 chars
    UPPERCASE    = string.ascii_uppercase          # 26 chars
    DIGITS       = string.digits                   # 10 chars
    SPECIAL_CHARS = "!@#$%^&*()_+-=[]{}|;:,.<>?/" # 29 chars
    ALL_CHARACTERS = LOWERCASE + UPPERCASE + DIGITS + SPECIAL_CHARS  # 91 chars

    # Velocidade de referência: RTX 4090 atacando NTLM (hash rápido)
    # Fonte: Hive Systems Password Table 2024 (~350 bilhões/s para NTLM)
    _GUESSES_PER_SECOND: int = 350_000_000_000

    # ------------------------------------------------------------------ #
    #  Validação                                                           #
    # ------------------------------------------------------------------ #

    def validate_inputs(self, length: int, key1: str, key2: str, reference: str) -> None:
        """
        Valida os parâmetros de entrada.

        Raises:
            ValueError: Se qualquer parâmetro for inválido.
        """
        if not (self.MIN_LENGTH <= length <= self.MAX_LENGTH):
            raise ValueError(
                f"O comprimento deve ser entre {self.MIN_LENGTH} e {self.MAX_LENGTH}."
            )
        if not key1 or not key2 or not reference:
            raise ValueError("Todos os campos devem ser preenchidos.")

    # ------------------------------------------------------------------ #
    #  Geração                                                             #
    # ------------------------------------------------------------------ #

    def generate(self, length: int, key1: str, key2: str, reference: str) -> str:
        """
        Gera uma senha determinística baseada nos parâmetros fornecidos.

        Returns:
            A senha gerada como string.
        """
        seed = f"{key1}{key2}{reference}"
        hash_seed = hashlib.sha256(seed.encode()).hexdigest()

        # Garante ao menos um caractere de cada categoria
        password = [
            self.LOWERCASE   [int(hash_seed[0],  16) % len(self.LOWERCASE)],
            self.UPPERCASE   [int(hash_seed[1],  16) % len(self.UPPERCASE)],
            self.DIGITS      [int(hash_seed[2],  16) % len(self.DIGITS)],
            self.SPECIAL_CHARS[int(hash_seed[3], 16) % len(self.SPECIAL_CHARS)],
        ]

        for i in range(length - 4):
            password.append(
                self.ALL_CHARACTERS[int(hash_seed[i + 4], 16) % len(self.ALL_CHARACTERS)]
            )

        return "".join(sorted(password, key=lambda x: hash_seed))

    # ------------------------------------------------------------------ #
    #  Análise de força                                                    #
    # ------------------------------------------------------------------ #

    def get_entropy(self, length: int) -> float:
        """Calcula a entropia da senha em bits (charset fixo de 91 chars)."""
        return length * math.log2(len(self.ALL_CHARACTERS))

    def get_strength(self, length: int) -> tuple[str, str, float]:
        """
        Retorna (label, cor_hex, percentual_0_a_1) baseado na entropia.

        Limiares baseados no mercado de segurança (NIST SP 800-63B / Hive Systems):
          < 35 bits  → Muito Fraca
          35-51 bits → Fraca
          52-64 bits → Moderada
          65-84 bits → Forte
          85-104 bits→ Muito Forte
          ≥ 105 bits → Extremamente Forte
        """
        entropy = self.get_entropy(length)
        max_entropy = self.get_entropy(self.MAX_LENGTH)
        percent = min(entropy / max_entropy, 1.0)

        if entropy < 35:
            return "Muito Fraca",         "#E53935", percent
        elif entropy < 52:
            return "Fraca",               "#FB8C00", percent
        elif entropy < 65:
            return "Moderada",            "#FDD835", percent
        elif entropy < 85:
            return "Forte",               "#7CB342", percent
        elif entropy < 105:
            return "Muito Forte",         "#43A047", percent
        else:
            return "Extremamente Forte",  "#1B5E20", percent

    # ------------------------------------------------------------------ #
    #  Tempo estimado de quebra                                            #
    # ------------------------------------------------------------------ #

    def estimate_crack_time(self, length: int) -> str:
        """
        Estima o tempo médio para quebrar a senha num ataque offline
        usando uma GPU de alta performance (RTX 4090, hash NTLM).

        Fonte de referência: Hive Systems Password Table 2024.
        """
        charset_size = len(self.ALL_CHARACTERS)
        total_combinations = charset_size ** length
        avg_attempts = total_combinations / 2          # ataque aleatório uniforme
        seconds = avg_attempts / self._GUESSES_PER_SECOND
        return self._format_seconds(seconds)

    @staticmethod
    def _format_seconds(seconds: float) -> str:
        """Converte segundos em string legível em português."""
        if seconds < 1:
            return "Instantaneamente (< 1 segundo)"

        MINUTE =        60
        HOUR   =      3_600
        DAY    =     86_400
        MONTH  =  2_592_000   # 30 dias
        YEAR   = 31_536_000   # 365 dias

        if seconds < MINUTE:
            v = int(seconds)
            return f"{v} segundo{'s' if v > 1 else ''}"
        if seconds < HOUR:
            v = int(seconds / MINUTE)
            return f"{v} minuto{'s' if v > 1 else ''}"
        if seconds < DAY:
            v = int(seconds / HOUR)
            return f"{v} hora{'s' if v > 1 else ''}"
        if seconds < MONTH:
            v = int(seconds / DAY)
            return f"{v} dia{'s' if v > 1 else ''}"
        if seconds < YEAR:
            v = int(seconds / MONTH)
            return f"{v} {'meses' if v > 1 else 'mês'}"
        if seconds < YEAR * 1_000:
            v = int(seconds / YEAR)
            return f"{v} ano{'s' if v > 1 else ''}"
        if seconds < YEAR * 1_000_000:
            v = int(seconds / (YEAR * 1_000))
            return f"{v} mil ano{'s' if v > 1 else ''}"
        if seconds < YEAR * 1_000_000_000:
            v = int(seconds / (YEAR * 1_000_000))
            return f"{v} {'milhões' if v > 1 else 'milhão'} de anos"

        v = seconds / (YEAR * 1_000_000_000)
        return f"{v:,.0f} bilhões de anos"
