import sys
import os
import winreg
import keyboard
import pyperclip
import time
import threading
from deep_translator import MyMemoryTranslator
import pystray
from PIL import Image, ImageDraw

HOTKEY = 'ctrl+alt+t'
DELAY = 0.05

typed_buffer = []

def add_to_startup():
    try:
        if getattr(sys, 'frozen', False):
            exe_path = sys.executable
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_ALL_ACCESS)
            try:
                winreg.QueryValueEx(key, "AutoTranslator")
            except FileNotFoundError:
                winreg.SetValueEx(key, "AutoTranslator", 0, winreg.REG_SZ, f'"{exe_path}"')
            winreg.CloseKey(key)
    except Exception:
        pass

def key_hook(event):
    global typed_buffer
    if event.event_type == keyboard.KEY_DOWN:
        # Игнорируем шорткаты и управляющие клавиши
        if keyboard.is_pressed('ctrl') or keyboard.is_pressed('alt') or keyboard.is_pressed('windows'):
            return
            
        name = event.name
        if not name:
            return
            
        if name == 'backspace':
            if typed_buffer:
                typed_buffer.pop()
        elif name == 'space':
            typed_buffer.append(' ')
        elif name in ('enter', 'esc', 'up', 'down', 'left', 'right', 'tab', 'home', 'end', 'page up', 'page down'):
            # Если пользователь переключился на другую строку или отменил ввод - очищаем память
            typed_buffer.clear()
        elif len(name) == 1:
            char = name
            if keyboard.is_pressed('shift'):
                char = char.upper()
            typed_buffer.append(char)

def process_translation():
    global typed_buffer
    try:
        # Принудительно отпускаем модификаторы
        keyboard.release('ctrl')
        keyboard.release('alt')
        keyboard.release('shift')
        time.sleep(0.1)
        
        text_to_translate = "".join(typed_buffer)
        used_buffer = False
        
        if text_to_translate and not text_to_translate.isspace():
            used_buffer = True
        else:
            # ФОЛБЭК: если мы ничего не печатали, пробуем скопировать выделенный мышкой текст
            pyperclip.copy('')
            keyboard.send('ctrl+insert')
            time.sleep(0.1)
            text_to_translate = pyperclip.paste()
            
        if not text_to_translate or text_to_translate.isspace():
            return
            
        # Если текст взят из нашей памяти, физически стираем его с экрана бэкспейсами
        if used_buffer:
            for _ in range(len(typed_buffer)):
                keyboard.send('backspace')
                time.sleep(0.005) # мизерная пауза, чтобы консоль не проглотила нажатия
            typed_buffer.clear()
            
        # Переводим
        translator = MyMemoryTranslator(source='ru-RU', target='en-US')
        translated_text = translator.translate(text_to_translate)
        
        # Вставляем
        pyperclip.copy(translated_text)
        time.sleep(0.1)
        keyboard.send('shift+insert')
        
    except Exception as e:
        pass

def on_hotkey_pressed():
    threading.Thread(target=process_translation, daemon=True).start()

def create_image():
    width = 64
    height = 64
    color_bg = (41, 128, 185)
    color_fg = (255, 255, 255)
    image = Image.new('RGB', (width, height), color_bg)
    dc = ImageDraw.Draw(image)
    dc.rectangle((width // 4, height // 4, width * 3 // 4, height // 4 + 8), fill=color_fg)
    dc.rectangle((width // 2 - 4, height // 4, width // 2 + 4, height * 3 // 4), fill=color_fg)
    return image

def exit_action(icon, item):
    icon.stop()
    os._exit(0)

def main():
    add_to_startup()
    
    # 1. Запускаем "кейлоггер" (шпиона за текстом)
    keyboard.hook(key_hook)
    
    # 2. Регистрируем хоткей
    keyboard.add_hotkey(HOTKEY, on_hotkey_pressed)
    
    # 3. Запускаем в трее
    image = create_image()
    menu = pystray.Menu(
        pystray.MenuItem('AutoTranslator', lambda: None, enabled=False),
        pystray.MenuItem('Выход', exit_action)
    )
    icon = pystray.Icon("AutoTranslator", image, "AutoTranslator (Ctrl+Alt+T)", menu)
    icon.run()

if __name__ == '__main__':
    main()
