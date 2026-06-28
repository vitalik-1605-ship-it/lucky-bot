import asyncio
import random

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, BotCommand


BOT_TOKEN = "8885414223:AAEZo8_hVg7jj5Yx5us1rQBj2vl2gX2cq_Y"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


private_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎲 Кубик"), KeyboardButton(text="🎰 Автомат")],
        [KeyboardButton(text="🪙 Монетка"), KeyboardButton(text="🎯 Дартс")],
        [KeyboardButton(text="🏀 Баскетбол"), KeyboardButton(text="⚽ Футбол")],
        [KeyboardButton(text="🎳 Боулинг"), KeyboardButton(text="🎱 Магический шар")],
        [KeyboardButton(text="✍️ Свой выбор")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите действие"
)


def is_private(message: types.Message):
    return message.chat.type == "private"


@dp.message(Command("start"))
async def start(message: types.Message):
    if is_private(message):
        await message.answer(
            "🎲 Lucky Bot запущен.\n\n"
            "Выбери режим на панели снизу:",
            reply_markup=private_keyboard
        )
    else:
        await message.answer(
            "🎲 Lucky Bot работает в группе через команды:\n\n"
            "/dice — кубик\n"
            "/slot — автомат\n"
            "/coin — монетка\n"
            "/dart — дартс\n"
            "/basket — баскетбол\n"
            "/football — футбол\n"
            "/bowling — боулинг\n"
            "/ball — магический шар\n"
            "/custom — свой выбор"
        )


@dp.message(Command("help"))
async def help_command(message: types.Message):
    await start(message)


@dp.message(Command("dice"))
@dp.message(lambda message: is_private(message) and message.text == "🎲 Кубик")
async def dice(message: types.Message):
    await message.answer_dice(emoji="🎲")


@dp.message(Command("slot"))
@dp.message(lambda message: is_private(message) and message.text == "🎰 Автомат")
async def slot(message: types.Message):
    await message.answer_dice(emoji="🎰")


@dp.message(Command("dart"))
@dp.message(lambda message: is_private(message) and message.text == "🎯 Дартс")
async def dart(message: types.Message):
    await message.answer_dice(emoji="🎯")


@dp.message(Command("basket"))
@dp.message(lambda message: is_private(message) and message.text == "🏀 Баскетбол")
async def basket(message: types.Message):
    await message.answer_dice(emoji="🏀")


@dp.message(Command("football"))
@dp.message(lambda message: is_private(message) and message.text == "⚽ Футбол")
async def football(message: types.Message):
    await message.answer_dice(emoji="⚽")


@dp.message(Command("bowling"))
@dp.message(lambda message: is_private(message) and message.text == "🎳 Боулинг")
async def bowling(message: types.Message):
    await message.answer_dice(emoji="🎳")


@dp.message(Command("coin"))
@dp.message(lambda message: is_private(message) and message.text == "🪙 Монетка")
async def coin(message: types.Message):
    result = random.choice(["Орёл", "Решка"])
    await message.answer(f"🪙 Выпало: {result}")


@dp.message(Command("ball"))
@dp.message(lambda message: is_private(message) and message.text == "🎱 Магический шар")
async def magic_ball(message: types.Message):
    answers = [
        "Да",
        "Нет",
        "Скорее всего",
        "Сомневаюсь",
        "Точно да",
        "Точно нет",
        "Попробуй ещё раз",
        "Лучше не рисковать",
        "Шансы хорошие",
        "Ответ неясен"
    ]

    await message.answer(f"🎱 {random.choice(answers)}")


@dp.message(Command("custom"))
@dp.message(lambda message: is_private(message) and message.text == "✍️ Свой выбор")
async def custom_start(message: types.Message):
    await message.answer(
        "Напиши варианты через запятую ответом на это сообщение.\n\n"
        "Пример:\n"
        "перекрут, all-in кейс, mystery"
    )


@dp.message()
async def custom_reply_or_ignore(message: types.Message):
    text = message.text or ""

    if message.reply_to_message:
        replied_text = message.reply_to_message.text or ""

        if "Напиши варианты через запятую" in replied_text:
            if "," not in text:
                await message.answer("варианты должны быть написаны чрз запятую дебил")
                return

            options = [option.strip() for option in text.split(",") if option.strip()]

            if len(options) < 2:
                await message.answer("варианты должны быть написаны чрз запятую дебил")
                return

            result = random.choice(options)
            await message.answer(f"🎯 Рандом выбрал:\n\n👉 {result}")
            return

    if is_private(message):
        await message.answer(
            "Пользуйся кнопками на панели снизу.\n\n"
            "Для своего рандома нажми «✍️ Свой выбор».",
            reply_markup=private_keyboard
        )


async def set_commands():
    commands = [
        BotCommand(command="start", description="Запустить Lucky Bot"),
        BotCommand(command="help", description="Показать помощь"),
        BotCommand(command="dice", description="Кубик"),
        BotCommand(command="slot", description="Казино автомат"),
        BotCommand(command="coin", description="Монетка"),
        BotCommand(command="dart", description="Дартс"),
        BotCommand(command="basket", description="Баскетбол"),
        BotCommand(command="football", description="Футбол"),
        BotCommand(command="bowling", description="Боулинг"),
        BotCommand(command="ball", description="Магический шар"),
        BotCommand(command="custom", description="Свой выбор")
    ]

    await bot.set_my_commands(commands)


async def main():
    await set_commands()
    print("Lucky Bot запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())