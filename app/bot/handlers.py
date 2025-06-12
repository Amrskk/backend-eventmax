from aiogram import F
from aiogram.types import Message
from .instance import dp, bot
from .logic import search_db, save_to_db, ask_openrouter

@dp.message(F.text)
async def handle_message(msg: Message):
    user_input = msg.text.strip()

    # Если в группе — проверка упоминания
    if msg.chat.type in ("group", "supergroup"):
        bot_info = await bot.get_me()
        if f"@{bot_info.username}" not in msg.text:
            return

    # teach: вопрос :: ответ
    if user_input.lower().startswith("teach:"):
        try:
            _, pair = user_input.split("teach:", 1)
            q, a = map(str.strip, pair.split("::"))
            save_to_db(q, a)
            await msg.answer("Инфа добавлена в бдшку")
        except Exception:
            await msg.answer("Неверный формат. Используй:\nteach: вопрос :: ответ")
        return

    # Векторный поиск
    cached = search_db(user_input)
    if cached:
        await msg.answer(cached)
        return

    # OpenRouter генерация
    try:
        reply = await ask_openrouter(user_input)
        await msg.answer(reply)
        save_to_db(user_input, reply)
    except Exception as e:
        await msg.answer(f"Ошибка: {e}")
