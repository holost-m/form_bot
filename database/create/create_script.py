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
        date_start TEXT,  -- Дата начала работы (хранится как текст)
        date_finish TEXT  -- Дата окончания работы (хранится как текст)
    )
''')

# Создание таблицы Question
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Question (
        number INTEGER PRIMARY KEY,
        question TEXT, -- текст вопроса
        answer_choise TEXT -- варианты ответа словарь или список
    )
''')

# Создание таблицы Answer_test
# Ответы на вопросы 6-15 пользователей
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Answer_test (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tg_id INTEGER,
        number INTEGER, 
        answer TEXT, -- ответы в формате словаря или список с одной строкой
        FOREIGN KEY (tg_id) REFERENCES User(tg_id),
        FOREIGN KEY (number) REFERENCES Question(number)
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