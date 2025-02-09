# O que faz?
# 1 - Normaliza a frase base e o salt
#   - Remove acentos e caracteres não alfanuméricos.
# 2 - Aplica substituições da frase chave
#   - Usa o subst_dict para trocar caracteres da frase base.
# 3 - Mistura a senha com o salt
#   - Isso dificulta ataques previsíveis.
# 4 - Garante o comprimento da senha
#   - Corta ou preenche até atingir pwd_length.
# 5 - Adiciona caracteres especiais, se ativado
#   - Para aumentar a força da senha.

import string
import hashlib
import unicodedata

class PasswordGenerator:
    '''
    Usado hashlib.sha256() na função _mix_with_salt().

    Em vez de embaralhar aleatoriamente, converte a entrada em um hash fixo.
    Isso garante que a mesma base_phrase e salt sempre gerem a mesma senha.
    Usado hashlib.md5() na função _add_special_chars().

    Em vez de selecionar caracteres especiais aleatoriamente, pego os valores do hash MD5.
    Isso garante que a escolha dos caracteres especiais seja determinística.
    A senha final agora é sempre a mesma para as mesmas entradas.
    '''

    def __init__(self, base_phrase: str, subst_dict: dict, salt: str = "", pwd_length: int = 16, extended_chars: bool = False):
        """Inicializa a classe com os parâmetros necessários para gerar a senha."""
        self.base_phrase = self._normalize_text(base_phrase)
        self.salt = self._normalize_text(salt)
        self.subst_dict = subst_dict
        self.pwd_length = pwd_length
        self.extended_chars = extended_chars


    def _normalize_text(self, text: str) -> str:
        """Normaliza o texto removendo acentos e pontuações, deixando apenas letras e números."""
        text = ''.join(c for c in unicodedata.normalize('NFKD', text) if not unicodedata.combining(c))
        text = text.lower()
        text = ''.join(c for c in text if c.isalnum())  # Remove pontuação
        return text


    def _apply_substitutions(self, text: str) -> str:
        """Substitui os caracteres da base_phrase de acordo com subst_dict."""
        return ''.join(self.subst_dict.get(char, char) for char in text)


    def _mix_with_salt(self, text: str) -> str:
        """Mistura a frase base transformada com o salt de forma determinística."""
        hash_input = (text + self.salt).encode("utf-8")
        hashed = hashlib.sha256(hash_input).hexdigest()  # Gera um hash da entrada
        return hashed[:self.pwd_length]  # Usa os primeiros caracteres do hash como senha base


    def _add_special_chars(self, text: str) -> str:
        """Adiciona caracteres especiais de forma determinística."""
        if not self.extended_chars:
            return text

        special_chars = "!#$%&()*+-;<=>?@^_{|}~"
        hash_input = text.encode("utf-8")
        hashed = hashlib.md5(hash_input).hexdigest()  # Usa um hash MD5 para previsibilidade

        text_list = list(text)
        for i in range(min(len(text) // 4, len(special_chars))):
            index = int(hashed[i], 16) % len(text_list)  # Determina o índice com base no hash
            text_list[index] = special_chars[i % len(special_chars)]

        return ''.join(text_list)


    def generate_password(self) -> str:
        """Gera a senha segura aplicando todas as transformações de forma determinística."""
        transformed = self._apply_substitutions(self.base_phrase)
        mixed = self._mix_with_salt(transformed)
        final_password = self._add_special_chars(mixed)
        return final_password

'''
    Teste

if __name__ == "__main__":
    from config_generator import ConfigGenerator

    base_phrase = "Minha senha super secreta"
    key_phrase = "Chave de segurança"
    salt = "Salt único"

    config = ConfigGenerator(key_phrase)
    subst_dict = config.get_subst_dict()

    password_generator = PasswordGenerator(
        base_phrase=base_phrase,
        subst_dict=subst_dict,
        salt=salt,
        pwd_length=16,
        extended_chars=True
    )

    senha1 = password_generator.generate_password()
    senha2 = password_generator.generate_password()

    print("Senha 1:", senha1)
    print("Senha 2:", senha2)

    print("Senhas iguais?" , senha1 == senha2)  # Deve ser True

'''