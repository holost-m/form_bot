import sqlite3
import os

DB_NAME = 'form_bot.db'


def executor(sql: str, args: tuple | None =None):
    """
    Выполняет запрос к БД.
    Открывает и закрывает соединение гарантированно.

    :param sql: строка запроса
    :param args: аргументы

    :return: None
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        # выполняем операцию
        if args:
            cursor.execute(sql, args)
        else:
            cursor.execute(sql)

        # получаем ответ
        # Если это запрос SELECT, возвращаем результаты
        if sql.strip().upper().startswith("SELECT"):
            # Получаем названия столбцов
            columns = [column[0] for column in cursor.description]
            results = cursor.fetchall()
            # Создаем список словарей
            return [dict(zip(columns, row)) for row in results]
        else:
            return None  # Возвращаем None для других запросов

    except Exception as ex:
        raise ex
    finally:
        conn.commit()
        conn.close()



class Table:
    table_name = None

    @staticmethod
    def __get_condition(conditions_and=None,
                        conditions_or=None) -> str:
        """
        Возвращает условия WHERE.
        Условия представляют собой список кортежей из 3 элементов вида
        ('столбец', 'операция', 'значение')

        Например, ('sex', '=', 'Мужской').

        Можно передавать только conditions_and или conditions_or.
        Вместе нельзя.

        :param conditions_and: условия для перечисления через AND
        :param conditions_or: условия для перечисления через OR

        :return: str
        """
        supported_operations = ('=', '!=', '<',
                                '>', '<=', '>=',
                                'IS', 'IS NOT', 'LIKE')

        if conditions_and and conditions_or:
            raise Exception('Переданы некорректные условия. Table.__get_condition')

        conditions = []
        condition = ''

        # Формируем AND
        if conditions_and:
            for condition in conditions_and:
                column, operation, value = condition

                if operation not in supported_operations:
                    raise ValueError(f"Операция '{operation}' не поддерживается.")

                conditions.append(f'"{column}" {operation} {value}')

            condition = " AND ".join(conditions)

        # Формируем OR
        if conditions_or:
            for condition in conditions_and:
                column, operation, value = condition

                if operation not in supported_operations:
                    raise ValueError(f"Операция '{operation}' не поддерживается.")

                conditions.append(f'"{column}" {operation} {value}')

            condition = " OR ".join(conditions)
        return condition

    def select_all(self):
        """
        Получение всех записей таблицы
        :return:
        """
        sql = f"SELECT * FROM {self.table_name}"
        return executor(sql)

    def select_where(self,
                     conditions_and=None,
                     conditions_or=None) -> list:
        """
        Получение данных по условиям.

        :return: список словарей строк
        """

        condition = self.__get_condition(conditions_and,
                                         conditions_or)

        # Формируем финальный SQL-запрос
        sql = f"SELECT * FROM {self.table_name}"
        if condition:
            sql += " WHERE " + condition

        return executor(sql)


    def update_where(self,
                     set_value,
                     conditions_and=None,
                     conditions_or=None) -> None:
        """
        Обновление значений по условию

        :param set_values: кортеж (поле, значение)
        :param conditions_and:
        :param conditions_or:
        :return:
        """

        condition = self.__get_condition(conditions_and,
                                         conditions_or)

        update_query = f"""
        UPDATE {self.table_name}
        SET {set_value[0]} = ?
        """
        if condition:
            update_query += " WHERE " + condition

        executor(update_query, set_value[1])

    def insert(self, dct_values):
        """
        Вставка переданных значений

        :param dct_values: словарь поле: значение
        :return: None
        """

        # задаем названия столбцов
        columns = ', '.join(f'"{key}"' for key in dct_values.keys())

        # ? - в место которых будут значения
        placeholders = ', '.join('?' for _ in dct_values)

        # вставляемые значения
        values: tuple = tuple(dct_values.values())

        insert_query = f"""INSERT INTO {self.table_name} 
                           ({columns})
                           VALUES ({placeholders})"""

        # вставка
        executor(insert_query, values)


class User(Table):
    table_name = 'User'
    fields = [
        'tg_id',
        'sex',
        'age',
        'region',
        'education',
        'work_position',
        'date_start',
        'date_finish'
    ]

class QuestionAbout(Table):
    table_name = 'Question_about'
    fields = [
        'number',
        'column',
        'question',
        'answer_choise'
    ]

    def select_where(self,
                     conditions_and=None,
                     conditions_or=None):

        return super().select_where(conditions_and, conditions_or)

    def get_question(self, number):
        if not isinstance(number, int):
            return None
        else:
            return super().select_where(conditions_and=[('number', '=', number)])


class QuestionTest(Table):
    table_name = 'Question_test'
    fields = [
        'number',
        'question',
        'answer_choise'
    ]


class AnswerTest(Table):
    table_name = 'Answer_test'
    fields = [
        'id',
        'tg_id',
        'number',
        'answer'
    ]


class Admin(Table):
    table_name = 'Admin'
    fields = [
        'tg_id'
    ]

    def admins(self) -> list:
        """
        Получить список tg_id админов

        :return:
        """
        return self.select_all()

if __name__ == '__main__':
    print(Admin().select_all())
    print(QuestionAbout().get_question(2))
    x = 1

