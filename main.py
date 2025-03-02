import asyncio

from aiogram import Bot, Dispatcher

# импорт файлов проекта

from handlers import (user_handlers)
from settings import TOKEN



# Функция конфигурирования и запуска бота
async def main():

    # Инициализируем бот и диспетчер
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    # Регистриуем роутеры в диспетчере
    dp.include_router(user_handlers.router)


    print('Bot is running')
    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())