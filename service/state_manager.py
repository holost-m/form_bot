from aiogram.types import Message
from copy import copy
import json

from database.db_operations import (User,
                                    Question,
                                    AnswerTest,
                                    Admin)
from states.user_states import FSM

class StateManager:
    """
    Класс для управления состояниями.
    Выделен в отдельную сущность потому что
    умеет работать и с БД и с FSM
    """
    @property
    def number(self) -> int:
        """
            Номер вопроса
        """
        return int(self._state['number'])

    @property
    def priority(self) -> dict:
        """
        Словарь состояний
        """
        copy_state = copy(self._state)
        copy_state.pop('number')
        return copy_state

    def __init__(self, tg_id):
        self.tg_id: str = tg_id
        self._state: dict = self._get_state(tg_id)

    def _get_state(self, tg_id):
        """
            Получить состояние пользователя
        """
        if not FSM.has_state(str(tg_id)):
            # Пользователя нет, надо его восстановить
            number = AnswerTest().get_last_answer(tg_id)
            if number:
                FSM.restore(tg_id, int(number) + 1)
            else:
                # Пользователь еще вообще не отвечал
                FSM.init_state(tg_id)

        return FSM.get_data(tg_id)

    def save_answer(self, tg_id, data):
        if self.number < 6:
            # сохранили ответ в БД и переключили состояние
            AnswerTest().save(tg_id, self.number, data)
            self.next_state()
        else:
            # Получим больший приоритет
            max_priority = max(self.priority.values())
            # выставляем следующий приоритет для записи
            current_priority = int(max_priority) + 1
            FSM.set_priority(tg_id, data, current_priority)
            print('current_priority', current_priority)
            # если ответили на все вопросы то переключаем состояние
            if current_priority == 5:
                # Для этой категории вопросов сохраняет в БД словарь приоритетов
                dct_priority = FSM.get_data(tg_id)
                dct_priority.pop('number')
                dct_priority = json.dumps(dct_priority)

                AnswerTest().save(tg_id, self.number, dct_priority)
                self.next_state()
                print('self.next_state()', self.number)

    def next_state(self):
        FSM.next_state(self.tg_id)
        self._state: dict = self._get_state(self.tg_id)

def filter_on_question(callback):
    tg_id: int = callback.message.from_user.id
    sm = StateManager(tg_id)
    return sm.number <= 15

def filter_on_result(callback):
    tg_id: int = callback.message.from_user.id
    sm = StateManager(tg_id)
    return sm.number > 15

