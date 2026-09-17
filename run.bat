@echo off
echo Установка необходимых библиотек (это нужно только в первый раз)...
python -m pip install keyboard pyperclip deep-translator

echo.
echo Запуск переводчика...
python translator.py

pause
