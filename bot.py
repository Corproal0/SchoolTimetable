
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand
from config import BOT_TOKEN
from database import add_schedule_entry, get_today_schedule, hide_schedule, init_db

async def main():
    # Инициализация бота и диспетчера
    bot = Bot(token=BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Функция для установки команд бота
    async def set_commands(bot: Bot):
        commands = [
            BotCommand(command="start", description="Начать использование"),
            BotCommand(command="help", description="Получить справку"),
            BotCommand(command="add_lesson", description="Добавить урок в расписание"),
            BotCommand(command="schedule", description="Показать расписание на сегодня"),
            BotCommand(command="hide_lesson", description="Скрыть урок из расписания")
        ]
        await bot.set_my_commands(commands)

    # Обработчик команды "start" и "help"
    async def send_welcome(message: Message):
        await message.answer("Привет! Вот что я могу:\n"
                             "/add_lesson - Добавить урок в расписание (формат: Предмет : Преподаватель : Кабинет)\n"
                             "/schedule - Показать расписание на сегодня\n"
                             "/hide_lesson - Скрыть урок из расписания (формат: Номер урока)")

    # Обработчик команды "add_lesson"
    async def add_schedule_command(message: Message):
        try:
            args = message.text.split(" ")[1:]
            if len(args) != 3:
                await message.reply("Формат должен быть: Предмет : Преподаватель : Кабинет")
                return

            subject, teachers, classroom = args
            result, msg = add_schedule_entry(subject, teachers, classroom)
            await message.answer(msg)
        except Exception as e:
            await message.answer(f"Ошибка: {e}")

    # Обработчик команды "schedule"
    async def today_schedule_command(message: Message):
        schedule_messages = get_today_schedule()
        if not schedule_messages:
            await message.answer("На сегодня уроков нет.")
        else:
            reply_message = "Расписание на сегодня:\n" + "\n".join(schedule_messages)
            await message.answer(reply_message)

    # Обработчик команды "hide_lesson"
    async def hide_schedule_command(message: Message):
        try:
            lesson_number = int(message.text.split(" ")[1])
            result_message = hide_schedule(lesson_number)
            await message.answer(result_message)
        except ValueError:
            await message.answer("Пожалуйста, укажите номер урока.")
        except Exception as e:
            await message.answer(f"Ошибка: {e}")

    # Регистрация обработчиков
    dp.message.register(send_welcome, Command(commands=["start", "help"]))
    dp.message.register(add_schedule_command, Command(commands=["add_lesson"]))
    dp.message.register(today_schedule_command, Command(commands=["schedule"]))
    dp.message.register(hide_schedule_command, Command(commands=["hide_lesson"]))

    # Установка команд бота
    await set_commands(bot)

    # Инициализация базы данных
    init_db()
    print("База данных успешно инициализирована.")

    # Запуск polling
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
