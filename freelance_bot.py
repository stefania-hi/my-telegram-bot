# freelance_bot.py — шаблон для продажи под заказ
import asyncio
import json
from pathlib import Path
from aiogram import Bot, Dispatcher
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, Contact
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# 🔑 Токен будет заменяться при развёртывании
BOT_TOKEN = "8370797164:AAFLPrKrm4xaZK5pf_L-4oT6tjpDxhK16_U"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

class OrderState(StatesGroup):
    waiting_for_name = State()
    waiting_for_contact = State()

def get_main_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📋 Услуги")],
            [KeyboardButton(text="💬 Вопросы")],
            [KeyboardButton(text="📩 Заявка")]
        ],
        resize_keyboard=True
    )

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "Здравствуйте! 👋\nЯ — помощник [Имя/Название].\nЧем могу помочь?",
        reply_markup=get_main_kb()
    )

@dp.message(lambda m: m.text == "📋 Услуги")
async def services(message: Message):
    await message.answer(
        "🔹 Услуга 1: ...\n"
        "🔹 Услуга 2: ...\n"
        "🔹 Услуга 3: ...\n\n"
        "Напишите «Заявка», чтобы заказать!"
    )

@dp.message(lambda m: m.text == "💬 Вопросы")
async def faq(message: Message):
    await message.answer(
        "❓ Сколько стоит?\n— От 2 000 ₽\n"
        "❓ Сроки?\n— 1–3 дня\n"
        "❓ Есть примеры?\n— Да, в портфолио!"
    )

@dp.message(lambda m: m.text == "📩 Заявка")
async def start_order(message: Message, state: FSMContext):
    await message.answer("Пожалуйста, напишите ваше имя:")
    await state.set_state(OrderState.waiting_for_name)

@dp.message(OrderState.waiting_for_name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📱 Отправить контакт", request_contact=True)]],
        resize_keyboard=True
    )
    await message.answer("Теперь отправьте ваш номер:", reply_markup=kb)
    await state.set_state(OrderState.waiting_for_contact)

# Используем проверку message.contact вместо ContactFilter
@dp.message(OrderState.waiting_for_contact)
async def get_contact(message: Message, state: FSMContext):
    if message.contact:
        data = await state.get_data()
        name = data["name"]
        phone = message.contact.phone_number
        user_id = message.from_user.id

        # Сохраняем заявку
        (DATA_DIR / f"{user_id}.json").write_text(
            json.dumps({"name": name, "phone": phone, "user_id": user_id}, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

        await message.answer(
            "Спасибо! 🙌\nМы свяжемся с вами в ближайшее время!",
            reply_markup=get_main_kb()
        )
        await state.clear()
    else:
        # Пользователь не отправил контакт — просим повторить
        await message.answer("Пожалуйста, отправьте ваш номер телефона через кнопку «📱 Отправить контакт».")

@dp.message()
async def echo(message: Message):
    await message.answer("Используйте кнопки ниже 👇", reply_markup=get_main_kb())

async def main():
    print("✅ Бот для заказа запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())