from aiogram import Router
from aiogram import Bot
from aiogram import F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.types import CallbackQuery

from keyboards.user_keyboards import UserKeyBoardManager
from service.state_manager import (filter_on_question,
                                   filter_on_result,
                                   StateManager)

# Инициализируем роутер для обработки пользовательских сообщений
router = Router()


# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart())
async def process_start_command(message: Message):
    """
    Проверяем, что пользователя нет в БД.
    Если есть, то обновляем редис и переводим на необходимый вопрос.

    Если пользователя нет в БД, то создаем запись в редис и переводим на первый вопрос
    """
    tg_id: int = message.from_user.id


    # Сформировали вопрос и клавитуру
    text, reply_markup = UserKeyBoardManager.get_keyboard(tg_id)

    # это если надо подменить клавиатуру
    await message.answer(text=text, reply_markup=reply_markup)

@router.callback_query(filter_on_question)
async def process_question(callback: CallbackQuery):
    """
    Обрабатывает первые 5 вопросов
    с заполнением информации о пользователе
    """
    tg_id: int = callback.message.from_user.id
    print(callback.data)

    # Сохранили полученный ответ и переключили состояние
    sm = StateManager(tg_id)
    sm.save_answer(tg_id, callback.data)


    # Сформировали вопрос и клавиатуру
    text, reply_markup = UserKeyBoardManager.get_keyboard(tg_id)

    # Отправили клавиатуру
    await callback.message.edit_text(text=text, reply_markup=reply_markup)



@router.callback_query(filter_on_result)
async def get_user_result(callback: CallbackQuery):
    """
    Возвращает пользователю результат прохождения теста
    """

    await callback.message.answer(
        text='Результат теста'
    )