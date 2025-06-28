
# ReciPick – Assistente de Receitas com IA

Este é um projeto full-stack que utiliza **React (frontend)** e **Flask + Gemini API (backend)** para sugerir receitas com base nos ingredientes que o usuário informa. Também permite buscar por receitas específicas, simulando uma conversa com um chatbot.

---

## Pré-requisitos

Antes de começar, garanta que você tenha os seguintes softwares instalados na sua máquina:

Python (versão 3.8 ou superior)

Node.js (versão 18 ou superior, que inclui o npm)

Git

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

Mova o requirements.txt: Se o arquivo requirements.txt estiver na raiz do projeto, mova-o para dentro da pasta backend/

Ainda dentro da pasta `backend/`, basta executar:

```bash
start.bat
```

Este script irá automaticamente:
- Criar e ativar um ambiente virtual `venv`
- Instalar as dependências do Python
- Iniciar o servidor local Flask

---

### 4. Configure o Frontend (Aplicação React)

Navegue até a pasta do frontend: A partir da raiz do projeto, execute:

```
cd recipick-front
```

Instale as Dependências (npm install): Este comando é como a "lista de compras" do seu projeto. Ele lê o package.json e baixa todas as bibliotecas que o React precisa para funcionar.

```
npm install
```

Gere a Versão de Produção (npm run build): Este comando é como "assar o bolo". Ele pega todo o seu código React e o compila em uma pasta dist/ otimizada, que é a versão final do seu site que o servidor Flask irá usar.

```
npm run build
```

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
