import sqlite3
import os
import json

DB_NAME = 'database/form_bot.db'


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

    def clear_all(self) -> None:
        """
            Удаление всех записей из таблицы.
            :return: None
        """
        sql = f"DELETE FROM {self.table_name}"
        executor(sql)


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

class Question(Table):
    table_name = 'Question'
    fields = [
        'number',
        'question',
        'answer_choise'
    ]

    def select_where(self,
                     conditions_and=None,
                     conditions_or=None):

        return super().select_where(conditions_and, conditions_or)

    def get_question(self, number):
        question: dict = super().select_where(
            conditions_and=[('number', '=', number)]
        )[0]

        # Формат словаря или списка
        question['answer_choise'] = json.loads(question['answer_choise'])
        return question



class AnswerTest(Table):
    table_name = 'Answer_test'
    fields = [
        'id',
        'tg_id',
        'number',
        'answer'
    ]

    def get_last_answer(self, tg_id):
        sql = f"""
        SELECT MAX("number") AS max_number
        FROM {self.table_name}
        WHERE "tg_id" = ?
        """
        result = executor(sql, (tg_id,))
        return result[0]['max_number'] if result else None

    def save(self, tg_id, number, answer):
        dct_values = {
            'tg_id': tg_id,
            'number': number,
            'answer': answer}
        super().insert(dct_values)

    def user_result(self, tg_id) -> list[dict]:
        """
        Получить ответы пользователя

        """
        result = super().select_where(
            conditions_and=[('tg_id', '=', str(tg_id))]
        )
        return result



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
    x = 1

