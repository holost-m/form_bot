from aiogram import Router
from aiogram import Bot
from aiogram import F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.types import CallbackQuery

from keyboards.user_keyboards import UserKeyBoardManager

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
    print(tg_id)

    await message.answer(
        text='Бот работает'
    )

@router.message()
async def process_question(callback: CallbackQuery):
    """
    Обрабатывает первые 5 вопросов
    с заполнением информации о пользователе
    """
    tg_id: int = callback.message.from_user.id

    # Сохранили полученный ответ

    # Если надо переключили состояние


    # Сформировали вопрос и клавитуру
    text, reply_markup = UserKeyBoardManager.get_keyboard()



    await callback.message.answer(text=text,
                                  reply_markup=reply_markup)


@router.message()
async def get_user_result(message: Message):
    """
    Возвращает пользователю результат прохождения теста
    """

    await message.answer(
        text='Результат теста'
    )