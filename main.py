# O que faz?
# 1 - Recebe os parâmetros do usuário via CLI
# 2 - Usa argparse para capturar:
#   --base_phrase → Frase base
#   --key_phrase → Frase chave
#   --salt → Salt opcional
#   --pwd_length → Tamanho da senha
#   --extended_chars → Usa caracteres especiais?
# 3 - Gera a senha
# 4 - Usa ConfigGenerator para criar o dicionário de substituição.
# 5 - Usa PasswordGenerator para criar a senha segura.
# 6 - Analisa a força da senha
# 7 - Usa PasswordStrength para calcular o nível de segurança.
# 8 - Exibe a senha gerada e a análise
# 9 - Exibe a senha, força e tempo estimado para quebra.

import argparse
import sys
from modules.config_generator import ConfigGenerator
from modules.password_generator import PasswordGenerator
from modules.password_strenght import PasswordStrength


def validar_entrada(base_phrase, key_phrase, salt, pwd_length):
    """Verifica se os parâmetros fornecidos são válidos."""
    
    if not base_phrase.strip():
        raise ValueError("A frase base não pode estar vazia.")

    if not key_phrase.strip():
        raise ValueError("A frase chave não pode estar vazia.")

    if pwd_length < 8:
        raise ValueError("O comprimento da senha deve ser pelo menos 8 caracteres.")

    if len(base_phrase) < 4:
        raise ValueError("A frase base deve ter pelo menos 4 caracteres.")

    if len(key_phrase) < 4:
        raise ValueError("A frase chave deve ter pelo menos 4 caracteres.")

    if len(salt) < 2:
        raise ValueError("O salt deve ter pelo menos 2 caracteres.")


def main():
    """Função principal que processa os argumentos, gera a senha e analisa sua força."""
    # Configura a CLI para receber parâmetros.
    parser = argparse.ArgumentParser(description="Gerador de Senhas Seguras")

    # Definição dos argumentos esperados na CLI
    '''
        Argumentos CLI esperados

    --base_phrase (obrigatório) → Frase base.
    --key_phrase (obrigatório) → Frase chave.
    --salt (opcional) → String extra para embaralhar a senha.
    --pwd_length (opcional, padrão 16) → Tamanho da senha.
    --extended_chars (flag) → Se ativado, adiciona caracteres especiais.
    '''
    parser.add_argument("--base_phrase", required=True, help="Frase base para gerar a senha")
    parser.add_argument("--key_phrase", required=True, help="Frase chave usada para criar as regras de substituição")
    parser.add_argument("--salt", default="", help="Salt opcional para aumentar a entropia da senha")
    parser.add_argument("--pwd_length", type=int, default=16, help="Comprimento da senha gerada (padrão: 16 caracteres)")
    parser.add_argument("--extended_chars", action="store_true", help="Usar caracteres especiais na senha")

    try:
        # Parseia os argumentos fornecidos pelo usuário
        args = parser.parse_args()

        # Validação de entrada
        validar_entrada(args.base_phrase, args.key_phrase, args.salt, args.pwd_length)

        # Debug temporário para verificar entrada
        #print("\n=== DEBUG: Entradas do Usuário ===")
        #print(f"Base Phrase: '{args.base_phrase}'")
        #print(f"Key Phrase: '{args.key_phrase}'")
        #print(f"Salt: '{args.salt}'")
        #print(f"Password Length: {args.pwd_length}")
        #print(f"Extended Chars: {args.extended_chars}")
        #print("==================================\n")

        # Geração do dicionário de substituição
        config = ConfigGenerator(args.key_phrase)
        subst_dict = config.get_subst_dict()

        # Debug: Garantir que o subst_dict seja sempre o mesmo
        #print("\n=== DEBUG: Dicionário de Substituição ===")
        #print(subst_dict)
        #print("========================================\n")

        # Geração da senha
        password_generator = PasswordGenerator(
            base_phrase=args.base_phrase,
            subst_dict=subst_dict,
            salt=args.salt,
            pwd_length=args.pwd_length,
            extended_chars=args.extended_chars
        )
        generated_password = password_generator.generate_password()

        # Análise da força da senha
        strength_checker = PasswordStrength(generated_password)
        analysis = strength_checker.get_password_analysis()

        # Exibição dos resultados
        print("\n=== Gerador de Senhas Seguras ===")
        print(f"Senha gerada: {generated_password}")
        print(f"Comprimento da senha: {analysis['length']}")
        print(f"Força da senha (0..100): {analysis['score']} ({analysis['security_level']})")
        print(f"Tempo estimado para quebra: {analysis['crack_time']}")
        print("=================================\n")

    except ValueError as ve:
        print(f"\n[ERRO]: {ve}")
        sys.exit(1)  # Sai com código de erro

    except Exception as e:
        print(f"\n[ERRO INESPERADO]: Ocorreu um erro inesperado: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
