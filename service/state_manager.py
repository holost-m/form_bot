from aiogram.types import Message
from copy import copy

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
        return int(self._state['number'])

    @property
    def priority(self) -> dict:
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
        if not FSM.has_state(tg_id):
            # Пользователя нет, надо его восстановить
            number = AnswerTest().get_last_answer(tg_id)
            if number:
                FSM.restore(tg_id, int(number) + 1)
            else:
                # Пользователь еще вообще не отвечал
                FSM.init_state(tg_id)

        return FSM.get_data(tg_id)

