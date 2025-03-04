"""
    Формирование клавиатур для ответов на вопросы
"""

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from database.db_operations import (User,
                                    Question,
                                    AnswerTest,
                                    Admin)
from service.state_manager import StateManager


def question_about(answers: list) -> InlineKeyboardMarkup:
    """
    Формирование простой клавиатуры вопросов о пользователе
    """
    buttons = []
    for answer in answers:
        button = InlineKeyboardButton(
            text=answer,
            callback_data=answer
        )
        buttons.append([button])
    return InlineKeyboardMarkup(inline_keyboard=buttons)



class UserKeyBoardManager:
    """
    Класс умеет ходить в БД и FSM
    """

    @classmethod
    def question_about(cls, answers: list) -> InlineKeyboardMarkup:
        """
        Формирование простой клавиатуры вопросов о пользователе
        """
        buttons = []
        for answer in answers:
            button = InlineKeyboardButton(
                text=answer,
                callback_data=answer
            )
            buttons.append([button])
        return InlineKeyboardMarkup(inline_keyboard=buttons)

    @classmethod
    def question_test(cls, answers: dict) -> InlineKeyboardMarkup:
        """
        Формирование клавитуры теста
        """
        buttons = []
        for priority, answer in answers.items():
            button = InlineKeyboardButton(
                text=answer,
                callback_data=str(priority)
            )
            buttons.append([button])
        return InlineKeyboardMarkup(inline_keyboard=buttons)

    @classmethod
    def get_keyboard(cls, tg_id):
        """
            Вернет необходимый объект клавиатуры в зависимости
            от состояния пользователя
        """
        # Получим необходимый номер вопроса
        state_manager = StateManager(tg_id)


        # Получим текст вопроса и варианты ответов
        question = Question.get_question(state_manager.number)

        # Если это 6-15 вопросы, то надо убрать уже отвеченные
        if state_manager.number > 5:
            for key, value in state_manager.priority.items():
                if value != '0':
                    question['answer_choise'].pop(int(key))

        if state_manager.number < 6:
            return (question['question'],
                    cls.question_about(question['answer_choise']))
        else:
            return (question['question'],
                    cls.question_test(question['answer_choise']))


