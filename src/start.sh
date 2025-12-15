@echo off
REM Ativa o ambiente virtual
call venv\Scripts\activate

REM Define variáveis de ambiente
set FLASK_APP=app.py
set FLASK_ENV=development

REM Roda a aplicação
flask run
pause
