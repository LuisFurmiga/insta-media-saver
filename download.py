import instaloader
import os

# Função para exibir mensagens de debug
DEBUG_SWITCH = False
def debug_text(text):
    if DEBUG_SWITCH:
        print(text)

def download_story(username, story_id=None, session_file=None):
    loader = instaloader.Instaloader()

    # Desativar o download de JSONs (metadados)
    loader.download_metadata = False

    # Carregar a sessão salva
    if session_file:
        debug_text(f"Carregando sessão de: {session_file}")
        try:
            loader.load_session_from_file(username=username, filename=session_file)
            debug_text(f"Logado com a sessão salva em {session_file}")
        except Exception as e:
            debug_text(f"Erro ao carregar a sessão: {e}")
            return
    else:
        debug_text("Aviso: Nenhuma sessão foi fornecida. Apenas conteúdo público será acessível.")

    try:
        # Obter perfil do usuário
        debug_text(f"Buscando stories do usuário: {username}...")
        profile = instaloader.Profile.from_username(loader.context, username)
        debug_text(f"Perfil encontrado: {profile.username}")

        # Baixar stories
        stories = loader.get_stories(userids=[profile.userid]) # Necessário login
        if not stories:
            debug_text("Nenhum story disponível para download.")
            return

        for story in stories:
            for item in story.get_items():
                if story_id:
                    # Baixar apenas o story com ID especificado
                    if str(item.mediaid) == story_id:
                        download_story_item(loader, item, username, f"{username}_story_{story_id}")
                        debug_text(f"Story com ID {story_id} baixado com sucesso!")
                        return
                else:
                    # Baixar todos os stories
                    download_story_item(loader, item, username, f"{username}_stories")
        debug_text("Todos os stories foram baixados com sucesso!")
    except Exception as e:
        debug_text(f"Erro ao baixar stories: {e}")

def download_story_item(loader, item, username, target_folder):
    """Baixa o item do story e remove miniaturas associadas."""
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)  # Certificar que o diretório existe

    if item.is_video:
        debug_text(f"Baixando vídeo com ID {item.mediaid}...")
    else:
        debug_text(f"Baixando imagem com ID {item.mediaid}...")

    loader.download_storyitem(item, target=target_folder)
    clean_extras(target_folder)

def clean_extras(target_folder):
    """Remove imagens JPG associadas a vídeos MP4."""
    if not os.path.exists(target_folder):
        return  # Ignorar se o diretório não existir
    
    """Remove arquivos extras JSONs."""
    for file in os.listdir(target_folder):
        if file.endswith(".mp4"):
            # Localiza e remove a miniatura associada ao vídeo
            thumbnail_file = file.replace(".mp4", ".jpg")
            thumbnail_path = os.path.join(target_folder, thumbnail_file)
            if os.path.exists(thumbnail_path):
                os.remove(thumbnail_path)
                debug_text(f"Miniatura removida: {thumbnail_path}")
        if file.endswith(".json.xz"):
            if not file.endswith("_UTC.jpg"):  # Manter imagens principais
                file_path = os.path.join(target_folder, file)
                os.remove(file_path)
                debug_text(f"Arquivo extra removido: {file_path}")

def download_post(post_url, session_file=None):
    """Baixa uma postagem do Instagram pelo link"""
    loader = instaloader.Instaloader()

    if session_file:
        debug_text(f"Carregando sessão de: {session_file}")
        try:
            loader.load_session_from_file(username=os.getenv("INSTALOADER_USERNAME"), filename=session_file)
            debug_text(f"Logado com a sessão salva em {session_file}")
        except Exception as e:
            debug_text(f"Erro ao carregar a sessão: {e}")
            return
    else:
        debug_text("Aviso: Nenhuma sessão foi fornecida. Apenas conteúdo público será acessível.")

    try:
        debug_text(f"Baixando post: {post_url}...")
        target_folder = "instagram_post_"+post_url.split("/")[-2]
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)  # Certificar que o diretório existe
        loader.download_post(instaloader.Post.from_shortcode(loader.context, post_url.split("/")[-2]), target=target_folder)
        clean_extras(target_folder)
        debug_text("Download da postagem concluído!")
    except Exception as e:
        debug_text(f"Erro ao baixar a postagem: {e}")
