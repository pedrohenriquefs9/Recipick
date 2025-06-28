
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

Dentro da pasta `backend/`, duplique o arquivo `.env.example` e renomeie para `.env`. Em seguida, adicione sua chave da API Gemini:

```text
GEMINI_API_KEY=sua_chave_aqui
```

## 2. Crie e ative um ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # No Windows use: venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute o servidor

```bash
python app.py
```

### Frontend

```bash
cd frontend
```

### 1. Instale as dependências

```bash
npm install
```

### 2. Execute o servidor

```bash
npm start
```

### Acessando a aplicação

Abra seu navegador e acesse:

```text
http://localhost:5173
```

## Funcionalidades

- Adicione ingredientes por chat ou clique
- Remova ingredientes individualmente com "×"
- Geração automática de receitas com IA
- Correção de erros de digitação nos ingredientes
- Formatação limpa com markdown (negrito, listas)
- Busca por nome de receitas via chatbot

## Licença

O ReciPick é licenciado sob a licença [MIT](LICENSE).

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests. Consulte o arquivo [CONTRIBUTING.md](CONTRIBUTING.md) para mais detalhes sobre como contribuir.

---
Desenvolvido por estudantes do CIn - Centro de Informática da UFPE.
