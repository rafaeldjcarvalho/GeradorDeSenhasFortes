# O que faz?
# 1 - Recebe uma frase chave (key_phrase)
#       - Essa frase define como os caracteres serão substituídos.
# 2 - Gera um dicionário de substituição
#       - Exemplo: Se a key_phrase for "segurança máxima", a classe pode criar um dicionário do tipo
#           - {'a': 'x', 'b': 'w', 'c': 'z', ...}
#       - Ou seja, cada letra pode ser substituída por outra com base na frase fornecida.
# 3 - Normaliza a entrada
#       - Remove acentos, espaços duplicados e pontuações para garantir que a entrada seja consistente.
# 4 - Garante que todas as letras do alfabeto tenham substituições únicas
#       - Se a key_phrase não for longa o suficiente, podemos completar com caracteres aleatórios.

import string
import unicodedata
import hashlib

class ConfigGenerator:

    # Recebe a frase chave e chama métodos para normalizar e gerar o dicionário de substituição.
    def __init__(self, key_phrase: str):
        """Inicializa a classe com a frase chave e gera o dicionário de substituições."""
        self.key_phrase = self._normalize_text(key_phrase)
        self.subst_dict = self._generate_subst_dict()


    # Remove acentos usando unicodedata.normalize()
    # Converte para minúsculas
    # Remove espaços duplicados e pontuação
    # Exemplo: "Máximo Segurança!!" → "maximoseguranca"
    def _normalize_text(self, text: str) -> str:
        """Normaliza o texto removendo acentos, espaços e transformando tudo em minúsculas."""
        text = ''.join(c for c in unicodedata.normalize('NFKD', text) if not unicodedata.combining(c))
        text = text.lower()
        text = ''.join(c for c in text if c.isalnum())  # Remove pontuação
        return text


    # Cria um alfabeto base (a-z)
    # Extrai caracteres únicos da frase chave
    # Garante que todas as letras do alfabeto tenham substituições
    # Embaralha para aumentar a entropia
    # Cria um dicionário de substituições
    # Exemplo de saída: {'a': 'z', 'b': 'k', 'c': 'm', ..., 'z': 'q'}
    def _generate_subst_dict(self) -> dict:
        """Cria um dicionário de substituições baseado na frase chave de forma determinística."""
        alphabet = list(string.ascii_lowercase)
        key_chars = list(dict.fromkeys(self.key_phrase))  # Remove duplicatas mantendo a ordem

        # Se a frase chave não for longa o suficiente, completa com o restante do alfabeto
        for char in alphabet:
            if char not in key_chars:
                key_chars.append(char)

        # Garante ordem fixa para o dicionário gerado usando um hash
        key_string = "".join(key_chars)
        hashed = hashlib.sha256(key_string.encode()).hexdigest()

        # Usa o hash para gerar um deslocamento determinístico
        offset = int(hashed[:4], 16) % len(alphabet)
        shuffled_chars = key_chars[offset:] + key_chars[:offset]

        return {orig: new for orig, new in zip(alphabet, shuffled_chars)}


    # Retorna o dicionário gerado.
    def get_subst_dict(self) -> dict:
        """Retorna o dicionário de substituições gerado."""
        return self.subst_dict

'''
    Teste

if __name__ == "__main__":
    key_phrase = "Segurança Máxima"
    config = ConfigGenerator(key_phrase)
    print("Dicionário de substituição gerado:")
    print(config.get_subst_dict())
'''

