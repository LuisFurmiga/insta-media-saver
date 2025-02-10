import tkinter as tk
from tkinter import ttk, messagebox
import threading
from download import download_story, download_post  # Importa as funções do arquivo principal
from dotenv import load_dotenv
import os

# Carregar as variáveis do arquivo .env
load_dotenv()

# Recuperar o caminho da sessão do .env
SESSION_FILE = os.getenv("INSTALOADER_SESSION_FILE")
USERNAME_ENV = os.getenv("INSTALOADER_USERNAME")

if not SESSION_FILE:
    messagebox.showerror("Erro", "Caminho da sessão não encontrado no arquivo .env. Certifique-se de realizar o login primeiro.")
    exit()

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

BUTTON_WIDTH = 17
LABEL_WIDTH = 22
ENTRY_WIDTH = 30
SCREEN_WIDTH = 350
SCREEN_HEIGHT = 175
SCREEN_SIZE = f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}"

# Interface Gráfica
root = tk.Tk()
root.title("Downloader de Instagram")
root.geometry(SCREEN_SIZE)
root.resizable(False, False)

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




