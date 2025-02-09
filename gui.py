'''
    A GUI terá:

- Caixas de entrada para a Frase Base, Frase Chave e Salt.
- Um campo numérico para escolher o tamanho da senha.
- Uma opção de ativar caracteres especiais.
- Um botão para gerar a senha.
- Um campo onde a senha gerada será exibida.

'''

import tkinter as tk
from tkinter import messagebox
from modules.config_generator import ConfigGenerator
from modules.password_generator import PasswordGenerator
from modules.password_strenght import PasswordStrength

def gerar_senha():
    """Função chamada ao clicar no botão 'Gerar Senha'."""
    base_phrase = entry_base.get().strip()
    key_phrase = entry_key.get().strip()
    salt = entry_salt.get().strip()
    pwd_length = pwd_length_var.get()
    extended_chars = extended_chars_var.get()

    # Validação básica
    if not base_phrase or not key_phrase:
        messagebox.showerror("Erro", "Frase Base e Frase Chave são obrigatórias!")
        return
    
    if pwd_length < 8:
        messagebox.showerror("Erro", "O comprimento da senha deve ser pelo menos 8 caracteres.")
        return

    # Geração do dicionário de substituição
    config = ConfigGenerator(key_phrase)
    subst_dict = config.get_subst_dict()

    # Geração da senha
    password_generator = PasswordGenerator(
        base_phrase=base_phrase,
        subst_dict=subst_dict,
        salt=salt,
        pwd_length=pwd_length,
        extended_chars=extended_chars
    )

    generated_password = password_generator.generate_password()

    # Análise da força da senha
    strength_checker = PasswordStrength(generated_password)
    analysis = strength_checker.get_password_analysis()

    # Exibir a senha e detalhes na interface
    entry_password.config(state="normal")
    entry_password.delete(0, tk.END)
    entry_password.insert(0, generated_password)
    entry_password.config(state="readonly")

    lbl_strength.config(text=f"Força: {analysis['score']} ({analysis['security_level']})")
    lbl_crack_time.config(text=f"Tempo estimado para quebra: {analysis['crack_time']}")

# Criando a janela principal
root = tk.Tk()
root.title("Gerador de Senhas Seguras")
root.geometry("500x400")

# Frase Base
tk.Label(root, text="Frase Base:").pack(pady=5)
entry_base = tk.Entry(root, width=50)
entry_base.pack()

# Frase Chave
tk.Label(root, text="Frase Chave:").pack(pady=5)
entry_key = tk.Entry(root, width=50)
entry_key.pack()

# Salt (opcional)
tk.Label(root, text="Salt (opcional):").pack(pady=5)
entry_salt = tk.Entry(root, width=50)
entry_salt.pack()

# Comprimento da Senha
tk.Label(root, text="Comprimento da Senha:").pack(pady=5)
pwd_length_var = tk.IntVar(value=16)
entry_length = tk.Spinbox(root, from_=8, to=64, textvariable=pwd_length_var, width=5)
entry_length.pack()

# Checkbox para caracteres especiais
extended_chars_var = tk.BooleanVar()
chk_extended = tk.Checkbutton(root, text="Incluir Caracteres Especiais", variable=extended_chars_var)
chk_extended.pack(pady=5)

# Botão de gerar senha
btn_generate = tk.Button(root, text="Gerar Senha", command=gerar_senha, bg="green", fg="white")
btn_generate.pack(pady=10)

# Campo de saída da senha gerada (readonly)
tk.Label(root, text="Senha Gerada:").pack(pady=5)
entry_password = tk.Entry(root, width=50, state="readonly")
entry_password.pack()

# Labels para exibir força e tempo de quebra
lbl_strength = tk.Label(root, text="")
lbl_strength.pack(pady=5)

lbl_crack_time = tk.Label(root, text="")
lbl_crack_time.pack(pady=5)

# Rodar a interface gráfica
root.mainloop()
