import redis
import json

red = redis.Redis(host='localhost', port=6379, db=0)

class FSM:

    @classmethod
    def init_state(cls, tg_id):
        """
        Инициализация пользователя.
        Он зашел в первый раз
        """
        red.hset(str(tg_id), 'number', '1')

    @classmethod
    def get_number(cls, tg_id):
        """
        Вернет текущий номер вопроса пользователя
        """
        number = red.hget(str(tg_id), 'number')
        if number:
            number = int(number)
        return

    @classmethod
    def restore(cls, tg_id, number):
        """
        Восстановит состояние пользователя до то того как он вышел
        """

        red.hset(str(tg_id), 'number', '1')

    @classmethod
    def next_state(cls):
        """
        Переход на следующий вопрос.
        Обнуление ответов - приориетов
        """
        pass

    @classmethod
    def get_priority(cls):
        """
        Возвращение текущего словаря приоритетов
        """

    @classmethod
    def set_priority(cls, tg_id, key, priority):
        """
        Установит текущий приоритет
        """
        red.hset(str(tg_id), str(key), str(priority))
