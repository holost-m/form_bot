import redis
from copy import copy

red = redis.Redis(host='localhost', port=6379, db=0)

class FSM:
    initial_hash: dict = {'number': '1',
                              '1': '0',
                              '2': '0',
                              '3': '0',
                              '4': '0',
                              '5': '0'}

    @staticmethod
    def __decoder(redis_dict: dict) -> dict:
        """
        Декодируем байтовые значения словаря, полученного из redis
        """
        return {key.decode('utf-8'): value.decode('utf-8') for key, value in redis_dict.items()}

    @classmethod
    def init_state(cls, tg_id):
        """
        Инициализация пользователя.
        Он зашел в первый раз
        """
        red.hset(str(tg_id),
                 mapping=FSM.initial_hash)

    @classmethod
    def get_number(cls, tg_id):
        """
        Вернет текущий номер вопроса пользователя
        """
        number = red.hget(str(tg_id), 'number')
        if number:
            number = int(number)
        return number

    @classmethod
    def restore(cls, tg_id, number):
        """
        Восстановит состояние пользователя до то того как он вышел
        """
        current_hash = copy(FSM.initial_hash)
        current_hash['number'] = str(number)

        red.hset(str(tg_id),
                 mapping=current_hash)

    @classmethod
    def next_state(cls, tg_id):
        """
        Переход на следующий вопрос.
        Обнуление ответов - приориетов
        """
        number = int(red.hget(str(tg_id), 'number'))
        number += 1
        current_hash = copy(FSM.initial_hash)
        current_hash['number'] = str(number)

        red.hset(str(tg_id),
                 mapping=current_hash)

    @classmethod
    def get_data(cls, tg_id):
        """
        Возвращение текущего словаря
        """
        result = red.hgetall(str(tg_id))
        return cls.__decoder(result)

    @classmethod
    def set_priority(cls, tg_id, key, priority):
        """
        Установит текущий приоритет
        """
        red.hset(str(tg_id), str(key), str(priority))

    @classmethod
    def has_state(cls, tg_id) -> bool:
        return red.exists(str(tg_id))