import asyncio
import hashlib
import os
from aiogram import Bot, Dispatcher
from aiogram.types import InlineQuery, InputTextMessageContent, InlineQueryResultArticle
from google import genai

# Забираем ключи из настроек системы (Environment Variables)
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

client = genai.Client(api_key=GEMINI_API_KEY)
MODEL_ID = 'gemini-2.5-flash'

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

@dp.inline_query()
async def inline_handler(query: InlineQuery):
    text = query.query or ""
    if len(text) < 2: return

    try:
        response = client.models.generate_content(model=MODEL_ID, contents=text)
        answer = response.text
    except Exception as e:
        answer = f"Ошибка: {e}"

    result_id = hashlib.md5(text.encode()).hexdigest()
    
    # Улучшенный формат
    formatted_text = (
        f"🔍 *Ваш запрос:* {text}\n"
        f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
        f"🤖 *Ответ Gemini:* \n\n{answer}\n"
        f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
        f"⚡️ _Модель: {MODEL_ID}_"
    )

    item = InlineQueryResultArticle(
        id=result_id,
        title="✨ Спросить Gemini 2.5",
        description=text[:50],
        input_message_content=InputTextMessageContent(
            message_text=formatted_text,
            parse_mode="Markdown"
        )
    )
    await query.answer([item], cache_time=5)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
