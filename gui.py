from dotenv import load_dotenv # type: ignore
from download import download_story, download_post  # Importa as funções do arquivo principal
from session import check_session_valid # type: ignore
from tkinter import ttk, messagebox
import os
import subprocess
import sys
import threading
import tkinter as tk

# Criar a interface Tk antes de verificar a sessão
root = tk.Tk()
root.withdraw()  # Esconde a janela enquanto a verificação acontece

# Carregar as variáveis do arquivo .env
ENV_FILE = ".env"
load_dotenv(ENV_FILE)

# Recuperar o caminho da sessão do .env
SESSION_FILE = os.getenv("INSTALOADER_SESSION_FILE")
USERNAME_ENV = os.getenv("INSTALOADER_USERNAME")

def close_gui():
    root.quit()  # Fecha a interface gráfica
    root.update()  # Garante que a interface seja encerrada antes do próximo comando
    try:
        if sys.platform == "win32":
            subprocess.Popen(["python", "login.py"])  # Abre login.py sem bloquear a execução
        else:
            pass
    except Exception as e:
        print(f"Erro ao abrir login.py: {e}")
    sys.exit(0)  # Ao invés de os._exit(0)

def logout():
    """Função para realizar logout, remover sessão e redirecionar para login.py"""
    confirm = messagebox.askyesno("Confirmar Logout", "Tem certeza que deseja sair?")
    if confirm:
        try:
            if SESSION_FILE and os.path.exists(SESSION_FILE):
                os.remove(SESSION_FILE)  # Remove o arquivo da sessão
                os.remove(ENV_FILE) # Remove o arquivo .env
            messagebox.showinfo("Logout", "Logout realizado com sucesso!")
            close_gui()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao realizar logout: {e}")

def update_status(message):
    status_label.config(text=message)
    root.update_idletasks()

def start_download_story():
    """Inicia o download de stories em uma thread separada."""
    username = username_entry.get().strip()
    story_id = story_id_entry.get().strip()

    if not username:
        messagebox.showerror("Erro", "Por favor, insira o nome de usuário.")
        return

    update_status("Baixando stories...")
    threading.Thread(
        target=run_download_story, args=(username, story_id), daemon=True
    ).start()

def run_download_story(username, story_id):
    """Função que executa o download de stories e exibe mensagens na interface."""
    try:
        download_story(username, story_id if story_id else None, SESSION_FILE)
        update_status("Download de stories concluído!")
        messagebox.showinfo("Sucesso", "Download de stories concluído com sucesso!")
    except Exception as e:
        update_status("Erro ao baixar stories!")
        messagebox.showerror("Erro", f"Erro ao realizar o download: {e}")

def start_download_post():
    """Inicia o download de postagens em uma thread separada."""
    post_url = post_url_entry.get().strip()

    if not post_url:
        messagebox.showerror("Erro", "Por favor, insira a URL da postagem.")
        return

    update_status("Baixando postagem...")
    threading.Thread(
        target=run_download_post, args=(post_url,), daemon=True
    ).start()

def run_download_post(post_url):
    """Função que executa o download de postagens e exibe mensagens na interface."""
    try:
        download_post(post_url, SESSION_FILE)
        update_status("Download de postagem concluído!")
        messagebox.showinfo("Sucesso", "Download da postagem concluído com sucesso!")
        update_status("")
    except Exception as e:
        update_status("Erro ao baixar postagem!")
        messagebox.showerror("Erro", f"Erro ao realizar o download: {e}")

def empty_line(frame, row, column):
    """Cria uma linha vazia para espaçamento."""
    ttk.Label(frame, text="").grid(row=row, column=column, pady=5)

if not check_session_valid(USERNAME_ENV, SESSION_FILE):
    print("Sessão inválida ou inexistente. Abrindo tela de login...")
    close_gui()
else:
    print("Sessão válida encontrada. Abrindo GUI...")
    root.deiconify()  # Mostra a janela novamente

BUTTON_WIDTH = 17
LABEL_WIDTH = 22
ENTRY_WIDTH = 30
SCREEN_WIDTH = 350
SCREEN_HEIGHT = 200
SCREEN_SIZE = f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}"

# Interface Gráfica
root.title("Downloader de Instagram")
root.geometry(SCREEN_SIZE)
root.resizable(False, False)

# Barra superior com usuário logado
frame_top = ttk.Frame(root)
frame_top.pack(fill="x")
user_label = ttk.Label(frame_top, text=f"Usuário logado: {USERNAME_ENV}", anchor="w")
user_label.pack(side="left", padx=10)
logout_button = ttk.Button(frame_top, text="Logout", command=logout)
logout_button.pack(side="right", padx=10)

# Criando as abas
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

# Aba de Stories
frame_stories = ttk.Frame(notebook, padding="10")
notebook.add(frame_stories, text="Baixar Stories")

# Campo de username
ttk.Label(frame_stories, text="Username do Instagram:", width=LABEL_WIDTH).grid(row=0, column=0, sticky=tk.W, pady=5)
username_entry = ttk.Entry(frame_stories, width=ENTRY_WIDTH)
username_entry.grid(row=0, column=1, pady=5)

# Campo de ID do story (opcional)
ttk.Label(frame_stories, text="ID do Story (opcional):", width=LABEL_WIDTH).grid(row=1, column=0, sticky=tk.W, pady=5)
story_id_entry = ttk.Entry(frame_stories, width=ENTRY_WIDTH)
story_id_entry.grid(row=1, column=1, pady=5)

# Botão para baixar stories
download_story_button = ttk.Button(frame_stories, text="Baixar Stories", width=BUTTON_WIDTH, command=start_download_story)
download_story_button.grid(row=2, column=0, columnspan=2, pady=10)

# Aba de Postagens
frame_posts = ttk.Frame(notebook, padding="10")
notebook.add(frame_posts, text="Baixar Postagens")

# Campo de URL de post
ttk.Label(frame_posts, text="URL da Postagem:", width=LABEL_WIDTH).grid(row=0, column=0, sticky=tk.W, pady=5)
post_url_entry = ttk.Entry(frame_posts, width=ENTRY_WIDTH)
post_url_entry.grid(row=0, column=1, pady=5)

# Linha vazia para espaçamento
empty_line(frame_posts, 1, 0)

# Botão para baixar postagens
download_post_button = ttk.Button(frame_posts, text="Baixar Postagem", width=BUTTON_WIDTH, command=start_download_post)
download_post_button.grid(row=2, column=0, columnspan=2, pady=10)

# Status Label
status_label = ttk.Label(root, text="", anchor="center")
status_label.pack()

root.mainloop()
