from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Я бот для конвертации стикеров в фото/видео, работы с картинками, доменами и чатом.\n"
        "Напиши /help, чтобы посмотреть все команды."
    )


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "<b>Команды:</b>\n"
        "/start — запуск бота\n"
        "/help — список команд\n"
        "/ping — проверка работы бота\n"
        "/vid — ответом на стикер: фото (.png) или видео (.mp4)\n"
        "/quote — ответом на сообщение: карточка-цитата\n"
        "/meme верх | низ — ответом на фото: мем\n"
        "/invert — ответом на фото: инверсия цветов\n"
        "/grayscale — ответом на фото: чёрно-белое фото\n"
        "/resize ШxВ — ответом на фото: ресайз (например 512x512)\n"
        "/domain имя[.зона] — разбор домена и подбор вариантов\n"
        "/zones — справочник популярных доменных зон\n"
        "/info — ответом на сообщение/стикер/фото: инфо\n"
        "/stats — топ активности в чате\n"
        "/mystats — твоя статистика в чате\n"
        "/roll [мин-макс] — случайное число\n"
        "/coin — орёл или решка\n"
        "/choose а | б | в — выбор из вариантов\n"
        "/reverse текст — текст задом наперёд\n"
        "/mock текст — текст в стиле sPoNgEbOb\n"
        "/count [текст] — подсчёт слов и символов",
        parse_mode="HTML",
    )


@router.message(Command("ping"))
async def cmd_ping(message: Message):
    await message.answer("pong! Бот работает стабильно.")
