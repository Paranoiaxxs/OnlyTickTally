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

# Функция для обработки ввода
def handle_input():
    while True:
        user_input = input(Fore.GREEN + "Введите команду > ")
        if user_input == "-h" or user_input == "--help":
            print("Это простая программа, если хотите создать новую задачу, используйте команду -n.")
        elif user_input == "list":
            print(user_name_select())
        elif user_input == "exit":
            running_event.clear()  # Сигнализируем об остановке программы
            break  # Прерываем цикл ввода
        else:
            print(f"Неизвестная команда: {user_input}")
        if running_event.is_set():
            print(Fore.GREEN + "Введите команду > ")

def main():
    print(Fore.CYAN + "\n           ______________________Добро пожаловать в программу_____________________")
    
    # Выбор случайного текста для анимации
    texts = [r'''

   ___         _          _____  _        _      _____         _  _
  /___\ _ __  | | _   _  /__   \(_)  ___ | | __ /__   \  __ _ | || | _   _
 //  //| '_ \ | || | | |   / /\/| | / __|| |/ /   / /\/ / _` || || || | | |
/ \_// | | | || || |_| |  / /   | || (__ |   <   / /   | (_| || || || |_| |
\___/  |_| |_||_| \__, |  \/    |_| \___||_|\_\  \/     \__,_||_||_| \__, |
                  |___/                                              |___/
''']
    random_text = random.choice(texts)
    print(random_text)

    print("Привет, я простой помощник")

    # Запускаем потоки
    animation_thread = threading.Thread(target=loop_text)
    input_thread = threading.Thread(target=handle_input)

    # Запускаем оба потока
    animation_thread.start()
    input_thread.start()

    # Ожидаем завершения потока ввода
    input_thread.join()

    # После завершения потока ввода останавливаем анимацию
    running_event.clear()  # Останавливаем анимацию
    animation_thread.join()

    print("\nПрограмма завершена.")

if __name__ == "__main__":
    main()
