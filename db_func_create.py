import sqlite3
import time
from colorama import init, Fore


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



# Функция таймера
def timer_task(task_name):
    start_time = time.time()
    print(Fore.YELLOW + f"Таймер для задачи '{task_name}' запущен. Нажмите 'Enter', чтобы остановить.")
    input(Fore.GREEN + "Остановить задачу и завершить таймер? > ")
    elapsed_time = round(time.time() - start_time)
    print(Fore.CYAN + f"Задача '{task_name}' завершена! Время: {elapsed_time} секунд.")
    return elapsed_time


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
