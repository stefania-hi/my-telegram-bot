# bot.py — Урок 2: Бот с премиум-доступом
from aiogram import Bot, Dispatcher
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart 
import asyncio
# 🔑 Вставь сюда свой токен от @BotFather
BOT_TOKEN = "8369963950:AAEyXFD8zBPFdcj77FZ0G_dOE8QcawcTflM"
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
# Основная клавиатура
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📺 Дорамы")],
        [KeyboardButton(text="📚 Книги")],
        [KeyboardButton(text="🧶 Вязание")],
        [KeyboardButton(text="💎 Премиум-доступ")]
    ],
    resize_keyboard=True
)
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "Привет! 👋 Я помогу найти лучшие книги, дорамы и идеи для вязания.\nВыбери категорию:",
        reply_markup=main_keyboard
    )
@dp.message()
async def handle_choice(message: Message):
    text = message.text.strip()
    if text == "📚 Книги":
        await message.answer(
            "📖 Бесплатная рекомендация:\n"
            "• «451 градус по Фаренгейту» — дистопия о цензуре и свободе мысли.\n\n"
            "Хочешь свежие новинки? Напиши «Премиум»!"
        )
    elif text == "📺 Дорамы":
        await message.answer(
            "📺 Бесплатная подборка:\n"
            "• «Itaewon Class» — история борьбы и мести\n"
            "• «Crash Landing on You» — любовь через границы\n\n"
            "Хочешь еженедельные рекомендации? Напиши «Премиум»!"
        )
    elif text == "🧶 Вязание":
        await message.answer(
            "🧶 Идея на сегодня:\n"
            "• Вязаные носки с узором «ёлочка»\n"
            "• Пряжа: 100% шерсть, спицы №3\n\n"
            "Хочешь PDF-схемы? Напиши «Премиум»!"
        )
    elif text == "💎 Премиум-доступ":
        await message.answer(
            "✨ Премиум-подписка за 99 ₽/мес:\n"
            "✅ Еженедельные подборки\n"
            "✅ Эксклюзивный контент\n"
            "✅ Ранний доступ\n\n"
            "Напиши «Хочу премиум» — пришлю инструкцию!"
        )
    elif text == "Хочу премиум":
        await message.answer(
            "Отлично! 💎\n"
            "1. Переведи 99 ₽ на СБП: +7 (XXX) XXX-XX-XX\n"
            "2. Пришли скриншот перевода\n"
            "3. Я вручную выдам тебе доступ!\n"
            "P.S. Первым 10 — скидка 50% (49 ₽) 🎁"
        )
    else:
        await message.answer("Используйте кнопки ниже 👇", reply_markup=main_keyboard)
async def main():
    print("✅ Бот запущен!")
    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(main())