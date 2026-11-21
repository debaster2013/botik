from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message
from db import Database

router = Router()


@router.message(F.chat.type.in_({"group", "supergroup"}))
async def track_messages(message: Message, db: Database):
    if message.from_user and not message.from_user.is_bot:
        db.add_message(message.chat.id, message.from_user.id, message.from_user.username)


@router.message(Command("stats"))
async def cmd_stats(message: Message, db: Database):
    rows = db.get_top_users(message.chat.id, limit=10)
    if not rows:
        await message.answer("Пока нет статистики по этому чату.")
        return

    lines = ["<b>Топ активности в чате:</b>"]
    for idx, (username, count) in enumerate(rows, start=1):
        lines.append(f"{idx}. @{username} — <b>{count}</b> сообщ.")
    await message.answer("\n".join(lines), parse_mode="HTML")


@router.message(Command("mystats"))
async def cmd_mystats(message: Message, db: Database):
    if not message.from_user:
        return
    row = db.get_user_stats(message.chat.id, message.from_user.id)
    if not row:
        await message.answer("По тебе пока нет статистики в этом чате.")
        return
    username, count = row
    await message.answer(
        f"👤 <b>Статистика @{username}:</b>\n• Сообщений в чате: <b>{count}</b>",
        parse_mode="HTML",
    )
