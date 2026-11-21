from io import BytesIO
from aiogram import Bot, Router
from aiogram.filters import Command
from aiogram.types import BufferedInputFile, Message
from services.image_service import (
    grayscale_photo_bytes,
    invert_photo_bytes,
    render_meme_image,
    render_quote_image,
    resize_photo_bytes,
)
from services.sticker_service import has_ffmpeg, webm_to_mp4_bytes, webp_to_png_bytes

router = Router()


async def _download_replied_photo(message: Message, bot: Bot) -> bytes | None:
    replied = message.reply_to_message
    if not replied or not replied.photo:
        return None
    photo = replied.photo[-1]
    file = await bot.get_file(photo.file_id)
    buf = BytesIO()
    await bot.download_file(file.file_path, destination=buf)
    return buf.getvalue()


@router.message(Command("vid"))
async def cmd_vid(message: Message, bot: Bot):
    replied = message.reply_to_message
    if not replied or not replied.sticker:
        await message.answer("Ответь командой <code>/vid</code> на стикер.", parse_mode="HTML")
        return

    sticker = replied.sticker
    file = await bot.get_file(sticker.file_id)
    buf = BytesIO()
    await bot.download_file(file.file_path, destination=buf)
    raw_bytes = buf.getvalue()

    if not sticker.is_video and not sticker.is_animated:
        png_bytes = webp_to_png_bytes(raw_bytes)
        await message.answer_photo(
            BufferedInputFile(png_bytes, filename="sticker.png"),
            caption="Стикер в формате фото (.png)",
        )
        return

    if sticker.is_video:
        if not has_ffmpeg():
            await message.answer("Для видеостикеров нужен установленный <code>ffmpeg</code>.", parse_mode="HTML")
            return
        mp4_bytes = webm_to_mp4_bytes(raw_bytes)
        if not mp4_bytes:
            await message.answer("Не удалось сконвертировать видеостикер.")
            return
        await message.answer_video(
            BufferedInputFile(mp4_bytes, filename="sticker.mp4"),
            caption="Видеостикер в формате .mp4",
        )
        return

    await message.answer(
        "Анимированные стикеры (.tgs) в базовой версии не рендерятся — "
        "используй статичный стикер или видеостикер (.webm)."
    )


@router.message(Command("quote"))
async def cmd_quote(message: Message):
    replied = message.reply_to_message
    text = (replied.text or replied.caption or "").strip() if replied else ""
    if not text:
        await message.answer("Ответь командой <code>/quote</code> на текстовое сообщение.", parse_mode="HTML")
        return

    author = "Пользователь"
    if replied.from_user:
        author = replied.from_user.full_name or (replied.from_user.username or "Пользователь")

    quote_bytes = render_quote_image(author, text)
    await message.answer_photo(BufferedInputFile(quote_bytes, filename="quote.png"))


@router.message(Command("meme"))
async def cmd_meme(message: Message, bot: Bot):
    photo_bytes = await _download_replied_photo(message, bot)
    if not photo_bytes:
        await message.answer(
            "Ответь командой <code>/meme верхний текст | нижний текст</code> на фото.",
            parse_mode="HTML",
        )
        return

    raw_args = (message.text or "").replace("/meme", "", 1).strip()
    if "|" in raw_args:
        top_text, bottom_text = [part.strip() for part in raw_args.split("|", 1)]
    else:
        top_text, bottom_text = raw_args, ""

    meme_bytes = render_meme_image(photo_bytes, top_text, bottom_text)
    await message.answer_photo(BufferedInputFile(meme_bytes, filename="meme.jpg"))


@router.message(Command("invert"))
async def cmd_invert(message: Message, bot: Bot):
    photo_bytes = await _download_replied_photo(message, bot)
    if not photo_bytes:
        await message.answer("Ответь командой <code>/invert</code> на фото.", parse_mode="HTML")
        return
    await message.answer_photo(
        BufferedInputFile(invert_photo_bytes(photo_bytes), filename="inverted.jpg"),
        caption="Цвета инвертированы",
    )


@router.message(Command("grayscale"))
async def cmd_grayscale(message: Message, bot: Bot):
    photo_bytes = await _download_replied_photo(message, bot)
    if not photo_bytes:
        await message.answer("Ответь командой <code>/grayscale</code> на фото.", parse_mode="HTML")
        return
    await message.answer_photo(
        BufferedInputFile(grayscale_photo_bytes(photo_bytes), filename="gray.jpg"),
        caption="Чёрно-белый вариант",
    )


@router.message(Command("resize"))
async def cmd_resize(message: Message, bot: Bot):
    photo_bytes = await _download_replied_photo(message, bot)
    if not photo_bytes:
        await message.answer("Ответь командой <code>/resize 512x512</code> на фото.", parse_mode="HTML")
        return

    raw = (message.text or "").replace("/resize", "", 1).strip().lower().replace(" ", "")
    if "x" not in raw:
        await message.answer("Укажи размер в формате <code>/resize 512x512</code>.", parse_mode="HTML")
        return

    try:
        w_str, h_str = raw.split("x", 1)
        w, h = int(w_str), int(h_str)
    except ValueError:
        await message.answer("Ширина и высота должны быть числами, например <code>512x512</code>.", parse_mode="HTML")
        return

    if not (16 <= w <= 2048 and 16 <= h <= 2048):
        await message.answer("Размер должен быть от <code>16</code> до <code>2048</code> пикселей.", parse_mode="HTML")
        return

    resized_bytes = resize_photo_bytes(photo_bytes, w, h)
    await message.answer_photo(
        BufferedInputFile(resized_bytes, filename=f"resized_{w}x{h}.jpg"),
        caption=f"Новый размер: {w}x{h}",
    )


@router.message(Command("info"))
async def cmd_info(message: Message):
    target = message.reply_to_message or message
    if target.sticker:
        s = target.sticker
        await message.answer(
            f"<b>Стикер:</b>\n"
            f"• Пак: <code>{s.set_name or 'нет'}</code>\n"
            f"• Эмодзи: {s.emoji or '—'}\n"
            f"• Размер: {s.width}x{s.height}\n"
            f"• Видео: {s.is_video} | Анимация: {s.is_animated}",
            parse_mode="HTML",
        )
    elif target.photo:
        p = target.photo[-1]
        await message.answer(
            f"<b>Фото:</b>\n• Разрешение: {p.width}x{p.height}\n• Размер файла: {p.file_size or 0} байт",
            parse_mode="HTML",
        )
    else:
        await message.answer(
            f"<b>Сообщение:</b>\n• ID чата: <code>{target.chat.id}</code>\n• ID сообщения: <code>{target.message_id}</code>",
            parse_mode="HTML",
        )
