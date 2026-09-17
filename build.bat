@echo off
echo Installing dependencies...
python -m pip install keyboard pyperclip pystray Pillow pyinstaller mouse translators

echo.
echo Building executable...
python -m PyInstaller --noconsole --onefile --name AutoTranslator translator.py

echo.
echo Build complete! The executable is in the 'dist' folder.
