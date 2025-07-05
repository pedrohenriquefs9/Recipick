## Necessidades para testes

1. **Instale as dependências**:

   ```bash
   cd backend/tests/
   pip install -r reqTestes.txt
   ```

3. **Execute os testes**:

   ```bash
   cd ..
   python -m pytest 
   ```

4. **Rode o coverage**:

   ```bash
   export GEMINI_API_KEY=sua_chave_aqui
   python -m pytest --cov=backend --cov-report=html
   ```

5. **Acesse o relatório html**:

   ```text
   Acesse o path do arquivo index.html gerado na pastta htmlcov/
   ```
