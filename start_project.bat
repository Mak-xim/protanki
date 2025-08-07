@echo off
cd /d "%~dp0"

echo Активируем виртуальное окружение...
call .venv\Scripts\activate.bat

echo Устанавливаем зависимости (если нужно)...
pip install -r requirements.txt

echo Запускаем сервер Django...
python manage.py runserver 8000

pause