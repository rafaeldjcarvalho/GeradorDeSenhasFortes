# O que faz?
# Recebe uma senha e calcula um score de 0 a 100
#   - Penaliza senhas fracas (curtas, repetitivas, previsíveis).
#   - Recompensa senhas fortes (longas, diversas, imprevisíveis).
#   - Define um nível de segurança para a senha
#       Exemplo:
#           0-20 → "Muito Fraca"
#           21-40 → "Fraca"
#           41-60 → "Moderada"
#           61-80 → "Forte"
#           81-100 → "Muito Forte"
#   - Estima o tempo para quebra da senha por força bruta
#   - Baseado no número de combinações possíveis.

import string
import math

class PasswordStrength:

    # Recebe a senha e chama os métodos para análise.
    def __init__(self, password: str):
        """Inicializa a classe com a senha e calcula sua força."""
        self.password = password
        self.length = len(password)
        self.char_types = self._analyze_character_types()
        self.score = self._calculate_score()
        self.security_level = self._get_security_level()
        self.crack_time = self._estimate_crack_time()


    # Conta letras maiúsculas, minúsculas, números e caracteres especiais.
    def _analyze_character_types(self) -> dict:
        """
        Analisa quais tipos de caracteres a senha possui.
        Retorna um dicionário com as contagens.
        """
        types = {
            "uppercase": 0,
            "lowercase": 0,
            "digits": 0,
            "special": 0
        }
        special_chars = set(string.punctuation)

        for char in self.password:
            if char.isupper():
                types["uppercase"] += 1
            elif char.islower():
                types["lowercase"] += 1
            elif char.isdigit():
                types["digits"] += 1
            elif char in special_chars:
                types["special"] += 1

        return types


    # Adiciona pontos por comprimento e diversidade de caracteres.
    # Penaliza senhas previsíveis (exemplo: apenas números).
    def _calculate_score(self) -> int:
        """
        Calcula um score de 0 a 100 baseado no comprimento e variedade da senha.
        """
        score = 0

        # Comprimento
        score += min(self.length * 4, 40)  # Máximo 40 pontos por comprimento

        # Diversidade de caracteres
        if self.char_types["uppercase"] > 0:
            score += 10
        if self.char_types["lowercase"] > 0:
            score += 10
        if self.char_types["digits"] > 0:
            score += 15
        if self.char_types["special"] > 0:
            score += 25

        # Penalidades por repetições e padrões simples
        if self.password.isdigit() or self.password.isalpha():
            score -= 20  # Apenas números ou apenas letras são penalizados

        return max(0, min(score, 100))  # Garante que o score esteja entre 0 e 100


    # Retorna "Muito Fraca", "Fraca", "Moderada", "Forte", ou "Muito Forte".
    def _get_security_level(self) -> str:
        """
        Define a classificação da senha baseada no score.
        """
        if self.score < 20:
            return "Muito Fraca"
        elif self.score < 40:
            return "Fraca"
        elif self.score < 60:
            return "Moderada"
        elif self.score < 80:
            return "Forte"
        else:
            return "Muito Forte"


    # Calcula o tempo necessário para quebrar a senha usando força bruta.
    def _estimate_crack_time(self) -> str:
        """
        Estima o tempo necessário para quebrar a senha por força bruta.
        """
        num_symbols = sum(self.char_types.values())  # Quantidade de símbolos distintos usados
        num_combinations = math.pow(num_symbols, self.length)  # Número total de combinações possíveis

        # Assume que um ataque de força bruta pode testar 10 milhões de senhas por segundo
        crack_seconds = num_combinations / 10_000_000

        # Converte tempo para formato legível
        if crack_seconds < 60:
            return "Menos de 1 minuto"
        elif crack_seconds < 3600:
            return f"{int(crack_seconds // 60)} minutos"
        elif crack_seconds < 86400:
            return f"{int(crack_seconds // 3600)} horas"
        elif crack_seconds < 31536000:
            return f"{int(crack_seconds // 86400)} dias"
        elif crack_seconds < 3.154e+8:
            return f"{int(crack_seconds // 31536000)} anos"
        else:
            return f"Aproximadamente {int(crack_seconds // 3.154e+8)} séculos"


    # Retorna um dicionário com a análise completa.
    def get_password_analysis(self) -> dict:
        """
        Retorna um dicionário com a análise completa da senha.
        """
        return {
            "password": self.password,
            "length": self.length,
            "score": self.score,
            "security_level": self.security_level,
            "crack_time": self.crack_time
        }

'''
    Teste

if __name__ == "__main__":
    password = "XkY!2p%t&Wq@E#"
    #password = "12345678"

    strength_checker = PasswordStrength(password)
    analysis = strength_checker.get_password_analysis()

    print("Análise da senha:")
    for key, value in analysis.items():
        print(f"{key}: {value}")
'''
