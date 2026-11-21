from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from domains import (
    generate_domain_ideas,
    get_zone_info,
    is_valid_label,
    is_valid_zone,
    list_zones_text,
    parse_domain_input,
)

router = Router()


@router.message(Command("zones"))
async def cmd_zones(message: Message):
    await message.answer(list_zones_text(), parse_mode="HTML")


@router.message(Command("domain"))
async def cmd_domain(message: Message):
    raw = (message.text or "").replace("/domain", "", 1).strip()
    if not raw:
        await message.answer(
            "Пример: <code>/domain burmaldungeons.gg</code> или <code>/domain myproject</code>",
            parse_mode="HTML",
        )
        return

    label, zone = parse_domain_input(raw)
    if not is_valid_label(label):
        await message.answer(
            "Некорректное имя домена. Используй латиницу (<code>a-z</code>), цифры и дефис не на краях.",
            parse_mode="HTML",
        )
        return

    if zone:
        if not is_valid_zone(zone):
            await message.answer("Некорректная доменная зона.", parse_mode="HTML")
            return
        variants = generate_domain_ideas(label, limit=5)
        await message.answer(
            f"🌐 <b>Домен:</b> <code>{label}.{zone}</code>\n"
            f"📌 <b>Зона:</b> {get_zone_info(zone)}\n\n"
            f"<b>Другие варианты для «{label}»:</b>\n" + "\n".join(f"• <code>{v}</code>" for v in variants),
            parse_mode="HTML",
        )
    else:
        variants = generate_domain_ideas(label, limit=8)
        await message.answer(
            f"💡 <b>Варианты для «{label}»:</b>\n" + "\n".join(f"• <code>{v}</code>" for v in variants),
            parse_mode="HTML",
        )
