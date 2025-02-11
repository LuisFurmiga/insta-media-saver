from dotenv import load_dotenv, set_key # type: ignore
from session import check_session_valid # type: ignore
from tkinter import ttk, messagebox
import instaloader # type: ignore
import os
import subprocess
import sys
import tkinter as tk

# Carregar as variáveis do arquivo .env
ENV_FILE = ".env"
load_dotenv(ENV_FILE)

# Recuperar o caminho da sessão do .env
SESSION_FILE = os.getenv("INSTALOADER_SESSION_FILE")
USERNAME_ENV = os.getenv("INSTALOADER_USERNAME")

def close_login():
    root.quit()  # Fecha a interface gráfica
    root.update()  # Garante que a interface seja encerrada antes do próximo comando
    try:
        if sys.platform == "win32":
            subprocess.Popen(["python", "gui.py"])  # Abre gui.py sem bloquear a execução
        else:
            pass
    except Exception as e:
        print(f"Erro ao abrir login.py: {e}")
    sys.exit(0)  # Ao invés de os._exit(0)

# Função para salvar o caminho da sessão no .env
def save_session_to_env(username):
    session_dir = os.getcwd()
    session_file = os.path.join(session_dir, f"session-{username}")

    set_key(ENV_FILE, "INSTALOADER_SESSION_FILE", session_file)
    set_key(ENV_FILE, "INSTALOADER_USERNAME", username)

# Função para salvar sessão e atualizar o .env
def save_login_session(loader, username):
    session_dir = os.getcwd()
    session_file = os.path.join(session_dir, f"session-{username}")

    # Salvar sessão no arquivo
    loader.save_session_to_file(filename=session_file)

    # Salvar caminho da sessão no .env
    save_session_to_env(username)

    # Exibir mensagem de sucesso e fechar a interface
    messagebox.showinfo("Sucesso", "Login realizado com sucesso e sessão salva!")
    close_login()

# Solicitar o código 2FA
def ask_2fa_code(loader, username):
    code_2fa_window = tk.Toplevel(root)
    code_2fa_window.title("Autenticação 2FA")
    code_2fa_window.geometry("300x125")
    code_2fa_window.resizable(False, False)  # Impede redimensionamento

    ttk.Label(code_2fa_window, text="Digite o código 2FA:").pack(pady=10)
    code_2fa_entry = ttk.Entry(code_2fa_window, width=30)
    code_2fa_entry.pack(pady=5)

    def submit_2fa():
        code_2fa = code_2fa_entry.get().strip()
        if not code_2fa:
            messagebox.showerror("Erro", "Código 2FA é necessário.")
            return
        try:
            loader.two_factor_login(code_2fa)
            save_session_to_env(username)
            messagebox.showinfo("Sucesso", "Login com 2FA realizado com sucesso!")
            code_2fa_window.destroy()  # Fecha a janela do 2FA
            root.destroy()  # Fecha a janela principal
        except Exception as e:
            messagebox.showerror("Erro", f"Erro no login com 2FA: {e}")

    ttk.Button(code_2fa_window, text="Enviar", command=submit_2fa).pack(pady=10)
    code_2fa_window.transient(root)  # Define como dependente da janela principal
    code_2fa_window.grab_set()      # Bloqueia interação com outras janelas
    code_2fa_window.mainloop()

# Função para realizar o login
def perform_login():
    username = username_entry.get().strip()
    password = password_entry.get().strip()

    if not username or not password:
        messagebox.showerror("Erro", "Por favor, preencha o nome de usuário e a senha.")
        return

    loader = instaloader.Instaloader()

    try:
        loader.login(username, password)
        save_login_session(loader, username)
    except instaloader.exceptions.TwoFactorAuthRequiredException:
        ask_2fa_code(loader, username)
        save_login_session(loader, username)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao realizar login: {e}")

def start_login():
    if check_session_valid(USERNAME_ENV, SESSION_FILE):
        print("Sessão válida encontrada. Abrindo GUI...")
        close_login()
    print("Sessão inválida ou inexistente. Abrindo tela de login...")
    root.mainloop()

BUTTON_WIDTH = 17
LABEL_WIDTH = 13
ENTRY_WIDTH = 30
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 120
SCREEN_SIZE = f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}"

# Interface gráfica
root = tk.Tk()
root.title("Login no Instaloader")
root.geometry(SCREEN_SIZE)
root.resizable(False, False)

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Campo de username
ttk.Label(frame, text="Username:", width=LABEL_WIDTH).grid(row=0, column=0, sticky=tk.W, pady=5)
username_entry = ttk.Entry(frame, width=ENTRY_WIDTH)
username_entry.grid(row=0, column=1, pady=5)

# Campo de senha
ttk.Label(frame, text="Senha:",width=LABEL_WIDTH).grid(row=1, column=0, sticky=tk.W, pady=5)
password_entry = ttk.Entry(frame, width=ENTRY_WIDTH, show="*")
password_entry.grid(row=1, column=1, pady=5)

# Botão de login
login_button = ttk.Button(frame, text="Login", command=perform_login)
login_button.grid(row=2, column=0, columnspan=2, pady=10)

start_login()
