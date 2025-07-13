import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.methods import DeleteWebhook
from aiogram.types import Message
from openai import OpenAI


TOKEN = '7554503664:AAFM9TR2BDio4uvLjCykmBnvXLarbBxVVNA' 

logging.basicConfig(level=logging.INFO)
bot = Bot(TOKEN)
dp = Dispatcher()


# ОБРАБОТЧИК КОМАНДЫ СТАРТ
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer('Привет дружище! Я бот с нейросетью, отправь свой запрос', parse_mode = 'HTML')


# ОБРАБОТЧИК ЛЮБОГО ТЕКСТОВОГО СООБЩЕНИЯ
@dp.message(lambda message: message.text)
async def filter_messages(message: Message):
    client = OpenAI(
    base_url = "https://openrouter.ai/api/v1",
    api_key = "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"
    )

    completion = client.chat.completions.create(
    model="mistralai/mistral-small-3.1-24b-instruct:free/api",
    messages=[
        {"role": "user", "content": message.text}
    ]
    )
    text = completion.choices[0].message.content

    await message.answer(text, parse_mode = "Markdown")


async def main():
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
