
# ReciPick – Assistente de Receitas com IA

Este é um projeto full-stack que utiliza **React (frontend)** e **Flask + Gemini API (backend)** para sugerir receitas com base nos ingredientes que o usuário informa. Também permite buscar por receitas específicas, simulando uma conversa com um chatbot.

---

## Pré-requisitos

- [Python](https://www.python.org/) (3.8 ou superior)
- [Node.js](https://nodejs.org/) (22 ou superior)
- Conta no [Google AI Studio](https://makersuite.google.com/app) com chave da API Gemini

---

## Executando o projeto

### 1. Clone o projeto

```bash
git clone https://github.com/seu-usuario/recipick.git
cd recipick
```

### Backend

```bash
cd backend
```

### 1. Crie o arquivo `.env`

Dentro da pasta `backend/`, duplique o arquivo `.env.example` e renomeie para `.env`. Em seguida, adicione sua chave da API Gemini e as origens permitidas. Por exemplo:

```text
GEMINI_API_KEY=
ALLOWED_ORIGINS=http://localhost:5173
GOOGLE_API_KEY=your_google_api_key_here
CUSTOM_SEARCH_ENGINE_ID=your_ID_search_engine_here
DATABASE_URL=postgresql://postgres:[SUA_SENHA]@[HOSTNAME_DO_PROJETO]/postgres
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Volte ao diretório raiz e execute o servidor

```bash
cd ..
python -m backend.app
```

### Frontend

```bash
cd recipick-front
```

### 1. Instale as dependências

```bash
npm install
```

### 2. Crie o arquivo `.env`
Dentro da pasta `recipick-front/`, duplique o arquivo `.env.example` e renomeie para `.env`. Em seguida, adicione a URL da API. Por exemplo:

```text
VITE_API_URL=http://localhost:5000/api
```

### 3. Execute o servidor de desenvolvimento

```bash
npm run dev
```

### Acessando a aplicação

Abra seu navegador e acesse:

```text
http://localhost:5173
```

## Funcionalidades

-   Geração Inteligente de Receitas:** Forneça uma lista de ingredientes e receba 5 sugestões de pratos, desde os mais clássicos aos mais criativos.
-   Sistema de Múltiplos Chats:** Crie e gerencie várias conversas. Salve uma lista de ingredientes para carnes, outra para sobremesas, e volte a elas quando quiser.
-   Personalização Avançada:** Cada chat possui configurações individuais de dieta (onívora, vegetariana, vegana), complexidade, estilo e porções.
-   Interface Conversacional:** Interaja com o assistente para refinar os resultados. Adicione ou remova ingredientes e peça novas ideias sem perder o histórico.
-   Gerenciamento de Chats:** Renomeie, favorite ou remova conversas para manter seu espaço organizado.
-   Busca de Imagens Otimizada:** As imagens das receitas são buscadas através de uma API dedicada (`Foodish API`), garantindo relevância e carregamento rápido.
-   Autenticação Segura:** Sistema completo de registro e login para que seus chats e preferências fiquem salvos e seguros.
-   Design Totalmente Responsivo:** A experiência foi cuidadosamente desenhada para funcionar perfeitamente em desktops, tablets e celulares.

## Tecnologias Utilizadas

Frontend
React: Biblioteca para construção da interface de usuário.

- Vite: Ferramenta de build para um desenvolvimento rápido e otimizado.

- Tailwind CSS: Framework CSS para estilização ágil e responsiva.

- React Router: Para gerenciamento das rotas da aplicação.

- Axios: Para realizar as chamadas HTTP para o backend.

Backend
Python: Linguagem de programação principal.

- Flask: Micro-framework para a construção da API.

- Gemini API: Modelo de IA do Google para a geração inteligente das receitas.

- SQLAlchemy: ORM para interação com o banco de dados.

- PostgreSQL: Banco de dados relacional para armazenamento dos dados.

## Licença

O ReciPick é licenciado sob a licença [MIT](LICENSE).

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests. Consulte o arquivo [CONTRIBUTING.md](CONTRIBUTING.md) para mais detalhes sobre como contribuir.

---
Desenvolvido por estudantes do CIn - Centro de Informática da UFPE.
