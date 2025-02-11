import instaloader # type: ignore
import os

def check_session_valid(username, session_file):
    if not session_file or not os.path.exists(session_file):
        return False

    loader = instaloader.Instaloader()
    try:
        loader.load_session_from_file(username, session_file)
        return True
    except Exception as e:
        print(f"Erro ao carregar sessão: {e}")
        return False
