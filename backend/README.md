# ReciPick (Backend)

Este é o backend do ReciPick, um aplicativo de gerenciamento de receitas.

## Começando

Para começar a usar o backend do ReciPick, siga estes passos:

1. **Clone o repositório**:

   ```bash
   git clone https://github.com/pedrohenriquefs9/Recipick
   cd Recipick/backend
   ```

2. **Instale as dependências**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Crie o arquivo `.env`**:
    Dentro da pasta `backend/`, duplique o arquivo `.env.example` e renomeie para `.env`. Em seguida, adicione sua chave da API Gemini e as origens permitidas. Por exemplo:

    ```text
    GEMINI_API_KEY=your_api_key_here
    ALLOWED_ORIGINS=http://localhost:5173
    GOOGLE_API_KEY=your_google_api_key_here
    CUSTOM_SEARCH_ENGINE_ID=your_ID_search_engine_here
    ```

4. **Volte ao diretório raiz e execute o servidor**:

   ```bash
   cd ..
   python -m backend.app
   ```

5. **Acessar o projeto**:

   Navegue para `http://localhost:5000` no seu navegador da web para ver o backend em ação.
