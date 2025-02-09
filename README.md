# Gerador de Senhas Seguras

Este projeto é um gerador de senhas seguras baseado em frases fornecidas pelo usuário. O sistema permite criar senhas fortes e fáceis de lembrar, garantindo previsibilidade para a mesma entrada.

## 📌 Funcionalidades
- **Geração de senhas a partir de frases**
- **Uso de um salt para aumentar a entropia**
- **Opção de incluir caracteres especiais**
- **Análise da força da senha gerada**
- **Interface gráfica para facilitar o uso**

---

## 🛠 Requisitos
O programa é desenvolvido em **Python** e usa as seguintes bibliotecas:
- `tkinter` (nativo do Python, para interface gráfica)
- `argparse` (para execução via linha de comando)
- `hashlib` (para geração determinística de senhas)
- `unicodedata` (para normalização de texto)

Caso precise instalar o Python, baixe a versão mais recente em: [Python Downloads](https://www.python.org/downloads/)

---

## 🚀 Como Executar o Programa
### 🔹 Opção 1: Linha de Comando (CLI)
Para executar o programa via terminal, use o seguinte comando:

```sh
python main.py --base_phrase "Sua frase base" --key_phrase "Sua chave de segurança" --salt "Seu salt" --pwd_length 16 --extended_chars
```

**Parâmetros disponíveis:**
- `--base_phrase` → Frase base para gerar a senha (Obrigatório)
- `--key_phrase` → Frase chave para a substituição de caracteres (Obrigatório)
- `--salt` → Frase opcional para aumentar a entropia
- `--pwd_length` → Comprimento da senha (mínimo 8, padrão 16)
- `--extended_chars` → Se ativado, inclui caracteres especiais

**Exemplo de uso:**
```sh
python main.py --base_phrase "Minha senha secreta" --key_phrase "Chave de segurança" --salt "Salt seguro" --pwd_length 16 --extended_chars
```

### 🔹 Opção 2: Interface Gráfica (GUI)
Caso prefira uma interface visual, execute o arquivo `gui.py`:

```sh
python gui.py
```

Isso abrirá uma janela onde você pode inserir as frases e gerar sua senha sem precisar do terminal.

---

## ⚠ Tratamento de Erros
Caso ocorra um erro, o programa exibirá uma mensagem explicativa. Os principais erros tratados incluem:
- Frase base ou frase chave vazias
- Comprimento da senha menor que 8 caracteres
- Problemas na geração da senha

---

## 📌 Melhorias Futuras
- Adicionar um botão para copiar a senha para a área de transferência
- Melhorar o design da interface gráfica
- Criar um modo de armazenamento seguro para senhas geradas

---

## 📄 Licença
Este projeto é distribuído sob a licença MIT.

