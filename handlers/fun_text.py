import random
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("roll"))
async def cmd_roll(message: Message):
    raw = (message.text or "").replace("/roll", "", 1).strip()
    low, high = 1, 100
    if raw:
        cleaned = raw.replace(" ", "")
        if "-" in cleaned:
            parts = cleaned.split("-", 1)
            try:
                low, high = int(parts[0]), int(parts[1])
            except ValueError:
                await message.answer("Пример: <code>/roll 1-50</code>", parse_mode="HTML")
                return
        else:
            try:
                high = int(cleaned)
            except ValueError:
                await message.answer("Пример: <code>/roll 20</code> или <code>/roll 1-50</code>", parse_mode="HTML")
                return

    if low > high:
        low, high = high, low

    num = random.randint(low, high)
    await message.answer(f"🎲 Выпало число: <b>{num}</b> (диапазон {low}..{high})", parse_mode="HTML")


@router.message(Command("coin"))
async def cmd_coin(message: Message):
    side = random.choice(["Орёл", "Решка"])
    await message.answer(f"🪙 Монетка: <b>{side}</b>", parse_mode="HTML")


@router.message(Command("choose"))
async def cmd_choose(message: Message):
    raw = (message.text or "").replace("/choose", "", 1).strip()
    options = [opt.strip() for opt in raw.split("|") if opt.strip()]
    if len(options) < 2:
        await message.answer("Укажи минимум 2 варианта через <code>|</code>: <code>/choose пицца | бургер | суши</code>", parse_mode="HTML")
        return
    choice = random.choice(options)
    await message.answer(f"🎯 Выбираю: <b>{choice}</b>", parse_mode="HTML")


@router.message(Command("reverse"))
async def cmd_reverse(message: Message):
    text = (message.text or "").replace("/reverse", "", 1).strip()
    if not text and message.reply_to_message:
        text = (message.reply_to_message.text or message.reply_to_message.caption or "").strip()
    if not text:
        await message.answer("Напиши <code>/reverse текст</code> или ответь на сообщение.", parse_mode="HTML")
        return
    await message.answer(text[::-1])


@router.message(Command("mock"))
async def cmd_mock(message: Message):
    text = (message.text or "").replace("/mock", "", 1).strip()
    if not text and message.reply_to_message:
        text = (message.reply_to_message.text or message.reply_to_message.caption or "").strip()
    if not text:
        await message.answer("Напиши <code>/mock текст</code> или ответь на сообщение.", parse_mode="HTML")
        return

    res = []
    upper = False
    for ch in text:
        if ch.isalpha():
            res.append(ch.upper() if upper else ch.lower())
            upper = not upper
        else:
            res.append(ch)
    await message.answer("".join(res))


@router.message(Command("count"))
async def cmd_count(message: Message):
    text = (message.text or "").replace("/count", "", 1).strip()
    if not text and message.reply_to_message:
        text = (message.reply_to_message.text or message.reply_to_message.caption or "").strip()
    if not text:
        await message.answer("Напиши <code>/count текст</code> или ответь на сообщение.", parse_mode="HTML")
        return

    words_count = len(text.split())
    chars_all = len(text)
    chars_no_spaces = len(text.replace(" ", ""))
    await message.answer(
        f"📊 <b>Статистика текста:</b>\n"
        f"• Слов: <b>{words_count}</b>\n"
        f"• Символов (с пробелами): <b>{chars_all}</b>\n"
        f"• Символов (без пробелов): <b>{chars_no_spaces}</b>",
        parse_mode="HTML",
    )
