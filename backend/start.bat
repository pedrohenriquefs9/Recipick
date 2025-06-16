
@echo off
echo Ativando ambiente virtual...
python -m venv venv
call venv\Scripts\activate
echo Instalando dependências...
pip install -r requirements.txt
echo Criando arquivo .env com chave de exemplo...
IF NOT EXIST .env (
  echo GEMINI_API_KEY=sua_chave_aqui > .env
)
echo Iniciando servidor Flask...
python app.py
pause
