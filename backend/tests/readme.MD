## Estrutura

```
tests/
├── unit/                 
│   ├── test_gemini.py
│   ├── test_promptConfig.py
│   └── test_app.py
└── integration/
    ├── test_pesquiar.py
    ├── test_normalizar_ingredientes.py
    └── test_receitas.py
```

## Necessidades para testes

1. **Entre na pasta /tests**:

   ```bash
   cd backend/tests
   ```

2. **Crie e ative um ambiente virtual**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows use: venv\Scripts\activate
   ```

3. **Instale as dependências**:

   ```bash
   pip install -r reqTestes.txt
   ```

4. **Execute os testes**:

   ```bash
   cd ..
   python -m pytest 
   ```

5. **Rode o coverage**:

   ```bash
   GEMINI_API_KEY=sua_chave_aqui python -m pytest --cov=backend --cov-report=html
   ```

6. **Acesse o relatório html**:

   ```text
   Acesse o path do arquivo index.html gerado na pasta htmlcov/
   ```


## Criação de testes

1. **Crie um arquivo teste dentro da pasta unit/ ou integration/**:

   ```bash
   tests/unit/test_exemplo.py
   tests/integration/test_exemplo.py
   ```

**Importe o arquivo desejado e produza o teste**:

   ```python
   # tests/unit/test_exemplo.py

   from app.utils.exemplo import soma

   def test_soma():
       assert soma(3, 4) == 7
       assert soma(-1, 1) == 0

   ```

**Produza o fixture para rotas Flask**:

   ```python
   # tests/integration/test_exemplo.py

   import pytest
   from flask import Flask
   from backend.routes.exemplo import exemploBlueprint

   @pytest.fixture
   def client():
       app = Flask(__name__)
       app.register_blueprint(exemploBlueprint)
       app.config['TESTING'] = True
       with app.test_client() as client:
           yield client

   def test_rota_exemplo(client):
      response = client.get('/api/exemplo')
      assert response.status_code == 200
      assert response.json['mensagem'] == 'Olá mundo!'
   ```

**Produza Mocks quando arquivos/funções usam APIs**:

   ```python
   # tests/unit/test_api.py

   from unittest.mock import patch
   from app.api import chamar_ia

   @patch('app.api.modelo.generate_content')
   def test_chamada_ia(mock_generate):
      mock_generate.return_value.text = "Resposta mockada"
      resposta = chamar_ia("prompt")
      assert resposta == "Resposta mockada"
   ```