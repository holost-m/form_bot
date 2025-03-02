from aiogram import Router
from aiogram import Bot
from aiogram import F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.types import CallbackQuery

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
async def question_about(message: Message):
    """
    Обрабатывает первые 5 вопросов
    с заполнением информации о пользователе
    """


    await message.answer(
        text='Пользовательский вопрос'
    )


@router.message()
async def question_test(message: Message):
    """
    Обрабатывает анкетные 6-15 вопросы
    """

    await message.answer(
        text='Пользовательский вопрос'
    )