import sqlite3
import os

# Определите путь к файлу базы данных на уровень выше
db_path = os.path.join('.', 'form_bot.db')

# Подключение к базе данных (или создание новой)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Создание таблицы User
# информация о пользователях в т.ч. из вопросов анкеты
cursor.execute('''
    CREATE TABLE IF NOT EXISTS User (
        tg_id INTEGER PRIMARY KEY,
        sex TEXT,
        age INTEGER,
        region TEXT,
        education TEXT,
        work_position TEXT,
        date_start TEXT,  -- Дата начала работы (хранится как текст)
        date_finish TEXT  -- Дата окончания работы (хранится как текст)
    )
''')

# Создание таблицы Question_about
# вопросы о пользователе от 1 до 5
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Question_about (
        number INTEGER PRIMARY KEY, -- от 1 до 5
        column TEXT, -- захардкоженное название колонки таблицы User
        question TEXT, -- текст вопроса
        answer_choise TEXT -- варианты ответа список
    )
''')


# Создание таблицы Question_test
# Непосредственно вопросы анекеты от 6 до 15
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Question_test (
        number INTEGER PRIMARY KEY, -- от 6 до 15
        question TEXT, -- текст вопроса
        answer_choise TEXT -- варианты ответа словарь
    )
''')

# Создание таблицы Answer_test
# Ответы на вопросы 6-15 пользователей
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Answer_test (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tg_id INTEGER,
        number INTEGER, 
        answer TEXT, -- ответы в формате словаря 
        FOREIGN KEY (tg_id) REFERENCES User(tg_id),
        FOREIGN KEY (number) REFERENCES Question_test(number)
    )
''')

# Создание таблицы Admin
# Список администраторов с правами получения отчетов
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Admin (
        tg_id INTEGER PRIMARY KEY
    )
''')

# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()

print("Файл БД успешно создан.")