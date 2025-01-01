import sqlite3
import time
from colorama import init, Fore
from pynput import keyboard


# Конект соединения с базой данных
conn = sqlite3.connect('tick1.db', check_same_thread=False)
cursor = conn.cursor()

# Создание таблицы, если она не существует
cursor.execute('''CREATE TABLE IF NOT EXISTS users
               (id INTEGER PRIMARY KEY, user_name TEXT, task_name TEXT, time_task INT)''')
conn.commit()
print('Таблица создана успешно!')




# Функция для вставки пользователя
def user_name_insert(name, task_name, time_task):
    try:
        cursor.execute("INSERT INTO users (user_name, task_name, time_task) VALUES (?, ?, ?)", (name, task_name,time_task))
        conn.commit()
        print("Запись успешно добавлена!")
    except sqlite3.Error as e:
        print(f"Ошибка при добавлении пользователя: {e}")


def timer_task(task_name):
    start_time = time.time()  # время начала работы таймера
    paused_time = 0  # Общее время паузы
    is_paused = False
    pause_start = None  # Время начала текущей паузы

    def on_press(key):
        nonlocal is_paused, paused_time, pause_start, running
        try:
            if hasattr(key, 'char') and key.char == 'b':  # задачу завершаем 
                # Если таймер на паузе, добавляем время текущей паузы
                if is_paused:
                    paused_time += time.time() - pause_start
                elapsed_time = round(time.time() - start_time - paused_time)  # Итоговое время без учёта пауз
                print(Fore.CYAN + f"\nЗадача '{task_name}' завершена! Время: {elapsed_time} секунд.")
                running = False
                return False  # Завершает слушатель
            elif key == keyboard.Key.enter:  # Пауза/продолжение
                if is_paused:  # Если таймер был на паузе
                    is_paused = False
                    paused_time += time.time() - pause_start  # увеличиваем общее время паузы
                    pause_start = None  # Сбрасываем время начала паузы
                    print(Fore.GREEN + "Таймер продолжен.")
                else:  # Если таймер работает
                    is_paused = True
                    pause_start = time.time()  # Фиксируем начало паузы
                    print(Fore.MAGENTA + "\nТаймер на паузе. Нажмите 'Enter' для продолжения.")
        except AttributeError:
            pass

    print(Fore.YELLOW + f"Таймер для задачи '{task_name}' запущен.")
    print(Fore.GREEN + "Нажмите 'Enter' для паузы или 'b' для завершения задачи.")
    running = True

    with keyboard.Listener(on_press=on_press) as listener:
        while running:
            if not is_paused:  # Таймер продолжает работать только если не на паузе
                time.sleep(0.1)  # Уменьшаем нагрузку на процессор
        listener.join()

    return round(time.time() - start_time - paused_time)


# Функция для выборки пользователей
def user_name_select():
    try:
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        if rows:  # Если есть данные
            for row in rows:
                print(f"User ID: {row[0]}, User Name: {row[1]}, Task Name: {row[2]}, Time time {row[3]}")
        else:
            print("Нет пользователей в базе данных.")
    except sqlite3.Error as e:
        print(f"Ошибка при выборке данных: {e}")



# Функция для выборки конкретных задач юзера 
def user_name_select_task(user_name):
    try:
        # Выбираем только задачи пользователя
        # cursor.execute(f"SELECT * FROM users {(user_name)}") 

        cursor.execute("SELECT task_name, time_task FROM users WHERE user_name = ?", (user_name,))
        rows = cursor.fetchall()
        
        if rows:  # Если найдены задачи
            print(f"Задачи пользователя {user_name} :")
            for idx, row in enumerate(rows, start=1):
                print(f"{idx}. {row[0]}, {row[1]}")  # Каждая задача выводится с номером
        else:
            print(f"Пользователь '{user_name}' не найден или у него нет задач.")
    except sqlite3.Error as e:
        print(f"Ошибка при выборке задач: {e}")
