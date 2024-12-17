import threading
from colorama import init, Fore
import random
from db_func_create import *

from loop import *
from frame import texts

# Флаг для управления потоком анимации
running_event = threading.Event()
running_event.set()

# Функция для обработки ввода
def handle_input():
    while running_event.is_set():
        user_input = input(Fore.GREEN + "Введите команду > ")
        
        if user_input == "-h" or user_input == "--help":
            print(Fore.YELLOW + "Команды:\n -n : создать новую запись\n list : показать все записи\n exit : выйти из программы")
        
        elif user_input == "list":
            print(Fore.CYAN + "Список всех записей:")
            user_name_select()
        
        elif user_input == "exit":
            print("Завершаем программу...")
            running_event.clear()  # Останавливаем программу
            break
        
        elif user_input == "-n":
            name = input("Введите имя пользователя: ")
            task_name = input("Введите название задачи: ")
            user_name_insert(name, task_name)

        elif user_input == "s":
            user_name = input("Введите имя пользователя: ").strip()
            user_name_select_task(user_name)
        

        else:
            print(Fore.RED + f"Неизвестная команда: {user_input}")







# Основная функция программы
def main():
    init(autoreset=True)  # Инициализация colorama
    print(Fore.CYAN + "\n______________________Добро пожаловать в программу_____________________")
    
    # Выбор случайного текста для анимации
    random_text = random.choice(texts)
    print(random_text)

    print(Fore.MAGENTA + "Привет, я простой помощник!")

    
     # Запускаем поток анимации
    animation_thread = threading.Thread(target=loop_text)

    # Запускаем анимацию и ждем её завершения
    animation_thread.start()
    animation_thread.join()  # Ожидаем завершения анимации

    # После завершения анимации, запускаем поток для ввода данных
    input_thread = threading.Thread(target=handle_input)
    input_thread.start()

    # Ожидаем завершения потока ввода
    input_thread.join()

    running_event.clear()  # Останавливаем анимацию (если нужно)
  
    print("\nПрограмма завершена.")

if __name__ == "__main__":
    main()
