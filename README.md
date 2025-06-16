
# ReciPick – Assistente de Receitas com IA

Este é um projeto full-stack que utiliza **React (frontend)** e **Flask + Gemini API (backend)** para sugerir receitas com base nos ingredientes que o usuário informa. Também permite buscar por receitas específicas, simulando uma conversa com um chatbot.

---

## Pré-requisitos

- [Python](https://www.python.org/) (3.8 ou superior)
- Conta no [Google AI Studio](https://makersuite.google.com/app) com chave da API Gemini

> O `Node.js` só é necessário se você for alterar o frontend e quiser rodar `npm run build`. A versão já compilada está pronta para uso.

---

## Como rodar localmente (Windows)

### 1. Clone o projeto

```bash
git clone https://github.com/seu-usuario/recipick.git
cd recipick/backend
```

### 2. Crie o arquivo `.env`

Dentro da pasta `backend/`, crie um arquivo `.env` com:

```
GEMINI_API_KEY=sua_chave_aqui
```

---

### 3. Execute o script de inicialização

Ainda dentro da pasta `backend/`, basta executar:

```bash
start.bat
```

Este script irá automaticamente:
- Criar e ativar um ambiente virtual `venv`
- Instalar as dependências do Python
- Iniciar o servidor local Flask

---

## Acesse o app

Abra seu navegador em: [http://localhost:5000](http://localhost:5000)

---

## Funcionalidades

- Adicione ingredientes por chat ou clique
- Remova ingredientes individualmente com "×"
- Geração automática de receitas com IA
- Correção de erros de digitação nos ingredientes
- Formatação limpa com markdown (negrito, listas)
- Busca por nome de receitas via chatbot

---

## Não versionar os seguintes arquivos:

- `backend/.env`
- `backend/venv/`
- `frontend/node_modules/`

---

## Licença

Este projeto é acadêmico/demonstrativo, sem fins lucrativos.
