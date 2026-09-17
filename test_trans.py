from deep_translator import MyMemoryTranslator

text = "Привет, как дела? Сегодня хорошая погода."
try:
    print(MyMemoryTranslator(source='ru-RU', target='en-US').translate(text))
except Exception as e:
    print(f"Error: {e}")
