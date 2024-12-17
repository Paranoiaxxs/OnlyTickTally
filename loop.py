# loop.py

import threading
import time
from colorama import init, Fore
import random
from db_func_create import *



# Инициализация colorama
init(autoreset=True)

# Используем threading.Event для управления состоянием анимации
running_event = threading.Event()

# Пример анимации
def loop_text():
    running_event.set()  # Устанавливаем флаг, что анимация активна
    text = "C ONLY TICK TALLY -- ДОСТИГАЙ СВОЕЙ ЦЕЛИ!"  # Текст, который будет анимироваться
    try:
        for i in range(len(text)):
            if not running_event.is_set():
                break
            char = text[i]
            if i % 2 == 0:
                char = char.lower()
            else:
                char = char.upper()  # Чередуем большие и маленькие буквы

            # Создаем строку с изменяющимися буквами
            animated_text = text[:i] + char + text[i + 1:]
            print(f"\r{animated_text}", end='', flush=True)
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nАнимация остановлена.")