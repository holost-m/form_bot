from aiogram import Router
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
from service.result_builder import ExelResult

router = Router()

def is_admin(message: Message):
    """
    Фильтр вернет True, если команду вызвал админ
    """
    return True


@router.message(Command("result"), is_admin)
async def handle_result_command(message: Message):
    exel_result = ExelResult()
    exel_result.create_file_result()

    # Создание объекта InputFile
    input_file = FSInputFile(exel_result.file_name)

    # Отправка файла
    await message.answer_document(document=input_file)