@echo off
echo Installing dependencies...
python -m pip install keyboard pyperclip deep-translator pystray Pillow pyinstaller mouse "googletrans==4.0.0-rc1"

echo.
echo Building executable...
python -m PyInstaller --noconsole --onefile --name AutoTranslator translator.py

echo.
echo Build complete! The executable is in the 'dist' folder.
