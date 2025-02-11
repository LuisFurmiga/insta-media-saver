# Insta-Media-Saver

Insta-Media-Saver é uma ferramenta para baixar stories e postagens do Instagram utilizando o Instaloader. Ele permite que os usuários façam login, salvem a sessão e realizem o download de mídias através de uma interface gráfica.

## 📌 Recursos
- Baixar **stories** de qualquer usuário com perfil público ou que **você segue** do Instagram.
- Baixar **postagens** públicas ou privadas.
- Login com **suporte a 2FA (autenticação de dois fatores)**.
- Interface gráfica amigável com abas separadas para **stories** e **postagens**.
- Salvamento automático da sessão para evitar necessidade de login repetitivo.
- Possibilidade de baixar um story específico informando seu **ID**.
- **Logout seguro**, que remove a sessão salva automaticamente.

## 🚀 Instalação

### 1. Clone este repositório:
```sh
 git clone https://github.com/LuisFurmiga/insta-media-saver.git
 cd Insta-Media-Saver
```

### 2. Instale as dependências:
Execute:
```sh
python requirements.py
```
Isso instalará os pacotes necessários automaticamente.

### 3. Execute a tela de login para salvar a sessão:
```sh
python login.py
```
Digite seu nome de usuário e senha do Instagram. Se a autenticação de dois fatores estiver ativada, será solicitado o código 2FA.

### 4. Execute a interface principal:
```sh
python gui.py
```

## 📥 Uso

1. **Login**: A primeira vez que rodar o programa, faça login com `login.py`. Isso irá salvar sua sessão.
2. **Baixar Stories**:
   - Informe o **username** da conta desejada.
   - Se quiser baixar um story específico, informe o **ID** do story.
   - Clique em **"Baixar Stories"**.
3. **Baixar Postagens**:
   - Cole a URL do post.
   - Clique em **"Baixar Postagem"**.
4. **Logout**:
   - Clique no botão de logout na interface principal.
   - Sua sessão será apagada e você precisará refazer o login.

## 🛠 Tecnologias Utilizadas
- **Python 3**
- **Instaloader** (para baixar mídias do Instagram)
- **Tkinter** (para interface gráfica)
- **Python-dotenv** (para gerenciar sessões de login)
- **Threading** (para downloads assíncronos)

## 📄 Estrutura do Projeto
```
Insta-Media-Saver/
│── download.py        # Lógica de download de stories e postagens
│── gui.py             # Interface gráfica principal
│── login.py           # Tela de login e salvamento de sessão
│── requirements.py    # Instalação automática de pacotes
│── session.py         # Gerenciamento de sessão
│── .env               # Arquivo onde a sessão e usuário são salvos
│── requirements.txt   # Lista de pacotes necessários
```

## ❗ Notas
- Apenas stories de perfis públicos ou de contas que **você segue** podem ser baixados.
- O uso excessivo pode levar a **bloqueios temporários** no Instagram.
- Certifique-se de **usar um IP confiável**, pois múltiplos logins suspeitos podem resultar em restrições da conta.

---
Se tiver alguma dúvida, abra uma issue no repositório! 💪
