import instaloader
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import simpledialog
import os
from dotenv import load_dotenv, set_key

# Nome do arquivo .env
ENV_FILE = ".env"

# Carregar as variáveis do arquivo .env
def load_session_from_env():
    load_dotenv(ENV_FILE)
    session_file = os.getenv("INSTALOADER_SESSION_FILE")
    username = os.getenv("INSTALOADER_USERNAME")
    return session_file, username

# Função para salvar o caminho da sessão no .env
def save_session_to_env(username):
    session_dir = os.path.join(os.path.expanduser("~"), "AppData", "Local", "Instaloader")
    session_file = os.path.join(session_dir, f"session-{username}")

    if not os.path.exists(session_dir):
        os.makedirs(session_dir)

    # Salvar o caminho no arquivo .env
    set_key(ENV_FILE, "INSTALOADER_SESSION_FILE", session_file)
    # Salvar o nome de usuário no arquivo .env
    set_key(ENV_FILE, "INSTALOADER_USERNAME", username)
    messagebox.showinfo("Sucesso", f"Login salvo em {session_file}")

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
        save_session_to_env(username)
        messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
        root.destroy()  # Fechar a janela após o login bem-sucedido
    except instaloader.exceptions.TwoFactorAuthRequiredException:
        ask_2fa_code(loader, username)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao realizar login: {e}")

# Interface gráfica
root = tk.Tk()
root.title("Login no Instaloader")
root.geometry("300x120")
root.resizable(False, False)

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Campo de username
ttk.Label(frame, text="Username:").grid(row=0, column=0, sticky=tk.W, pady=5)
username_entry = ttk.Entry(frame, width=30)
username_entry.grid(row=0, column=1, pady=5)

# Campo de senha
ttk.Label(frame, text="Senha:").grid(row=1, column=0, sticky=tk.W, pady=5)
password_entry = ttk.Entry(frame, width=30, show="*")
password_entry.grid(row=1, column=1, pady=5)

# Botão de login
login_button = ttk.Button(frame, text="Login", command=perform_login)
login_button.grid(row=2, column=0, columnspan=2, pady=10)

root.mainloop()
