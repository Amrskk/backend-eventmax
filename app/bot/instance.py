from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from app.core.config import settings
from aiogram.client.default import DefaultBotProperties

bot = Bot(
    token=settings.TELEGRAM_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML) #изменение под новую вурсию aiogram
)
dp = Dispatcher(storage=MemoryStorage())
