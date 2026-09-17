import keyboard
import pyperclip
import time
import threading
from deep_translator import MyMemoryTranslator
import pystray
from PIL import Image, ImageDraw
import sys
import os

# Настройки
HOTKEY = 'ctrl+alt+t'
DELAY = 0.05

def process_translation():
    try:
        # Принудительно отпускаем модификаторы
        keyboard.release('ctrl')
        keyboard.release('alt')
        keyboard.release('shift')
        time.sleep(0.1)
        
        # Очищаем буфер
        pyperclip.copy('')
        
        # 1. Выделяем всю строку
        keyboard.send('end')
        time.sleep(DELAY)
        keyboard.send('shift+home')
        time.sleep(DELAY)
        
        # 2. Копируем в буфер (используем ctrl+insert)
        keyboard.send('ctrl+insert')
        
        # Ждем текст в буфере
        text_to_translate = ""
        for _ in range(10):
            time.sleep(0.05)
            text = pyperclip.paste()
            if text:
                text_to_translate = text
                break
        
        if not text_to_translate or text_to_translate.isspace():
            keyboard.send('right')
            return
            
        # 4. Переводим
        translator = MyMemoryTranslator(source='ru-RU', target='en-US')
        translated_text = translator.translate(text_to_translate)
        
        # 5. Кладем перевод в буфер
        pyperclip.copy(translated_text)
        time.sleep(0.1)
        
        # 6. Вставляем перевод (shift+insert)
        keyboard.send('shift+insert')
        
    except Exception as e:
        pass # В фоновом режиме ошибки просто игнорируем, чтобы не крашить приложение

def on_hotkey_pressed():
    threading.Thread(target=process_translation, daemon=True).start()

def create_image():
    # Создаем простую иконку (синий квадрат с белой буквой T)
    width = 64
    height = 64
    color_bg = (41, 128, 185)
    color_fg = (255, 255, 255)
    
    image = Image.new('RGB', (width, height), color_bg)
    dc = ImageDraw.Draw(image)
    
    # Рисуем букву "T"
    dc.rectangle((width // 4, height // 4, width * 3 // 4, height // 4 + 8), fill=color_fg)
    dc.rectangle((width // 2 - 4, height // 4, width // 2 + 4, height * 3 // 4), fill=color_fg)
    
    return image

def exit_action(icon, item):
    icon.stop()
    os._exit(0)

def main():
    # Регистрируем хоткей
    keyboard.add_hotkey(HOTKEY, on_hotkey_pressed)
    
    # Настраиваем иконку в трее
    image = create_image()
    menu = pystray.Menu(
        pystray.MenuItem('AutoTranslator', lambda: None, enabled=False),
        pystray.MenuItem('Выход', exit_action)
    )
    icon = pystray.Icon("AutoTranslator", image, "AutoTranslator (Ctrl+Alt+T)", menu)
    
    # Запускаем приложение в трее (этот метод блокирует поток, пока приложение работает)
    icon.run()

if __name__ == '__main__':
    main()
