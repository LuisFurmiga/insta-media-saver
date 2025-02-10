# Insta-Media-Saver

Insta-Media-Saver é uma ferramenta para baixar stories e postagens do Instagram utilizando o Instaloader. Ele permite que os usuários façam login, salvem a sessão e realizem o download de mídias através de uma interface gráfica.

## 📌 Recursos
- Baixar **stories** de qualquer usuário com perfil público ou que VOCÊ SEGUE do Instagram.
- Baixar **postagens** públicas ou privadas.
- Login com **suporte a 2FA (autenticação de dois fatores)**.
- Interface gráfica amigável com abas separadas para **stories** e **postagens**.
- Salvamento automático da sessão para evitar necessidade de login repetitivo.

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

1. **Login**: A primeira vez que rodar o programa, faça login com `login.py`.
2. **Baixar Stories**:
   - Informe o **username** da conta desejada.
   - Se quiser baixar um story específico, informe o **ID** do story.
   - Clique em **"Baixar Stories"**.
3. **Baixar Postagens**:
   - Cole a URL do post.
   - Clique em **"Baixar Postagem"**.

## 🛠 Tecnologias Utilizadas
- **Python 3**
- **Instaloader** (para baixar mídias do Instagram)
- **Tkinter** (para interface gráfica)
- **Python-dotenv** (para gerenciar sessões de login)

## 📄 Estrutura do Projeto
```
Insta-Media-Saver/
│── download.py        # Lógica de download de stories e postagens
│── gui.py             # Interface gráfica principal
│── login.py           # Tela de login e salvamento de sessão
│── requirements.py    # Instalação automática de pacotes
│── .env               # Arquivo onde a sessão e usuário são salvos
│── requirements.txt   # Lista de pacotes necessários
```

## ❗ Notas
- Apenas stories de perfis públicos ou de contas que VOCÊ SEGUE podem ser baixados.
- O uso excessivo pode levar a **bloqueios temporários** no Instagram.
