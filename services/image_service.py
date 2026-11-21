from io import BytesIO
from PIL import Image, ImageDraw, ImageOps
from services.fonts import load_font


def render_quote_image(author: str, text: str) -> bytes:
    width, height = 900, 420
    img = Image.new("RGB", (width, height), (24, 26, 33))
    draw = ImageDraw.Draw(img)

    draw.rounded_rectangle([24, 24, width - 24, height - 24], radius=24, fill=(34, 38, 48))
    draw.rectangle([56, 60, 66, height - 60], fill=(99, 102, 241))

    font_author = load_font(30)
    font_quote = load_font(34)

    draw.text((92, 62), author, font=font_author, fill=(165, 180, 252))

    words = text.split()
    lines, current = [], ""
    for w in words:
        trial = f"{current} {w}".strip()
        bbox = draw.textbbox((0, 0), trial, font=font_quote)
        if bbox[2] - bbox[0] <= width - 140:
            current = trial
        else:
            lines.append(current)
            current = w
    if current:
        lines.append(current)
    lines = lines[:5]

    y = 125
    for idx, line in enumerate(lines):
        formatted = f"«{line}»" if idx == 0 else line
        draw.text((92, y), formatted, font=font_quote, fill=(243, 244, 246))
        y += 46

    out = BytesIO()
    img.save(out, format="PNG")
    return out.getvalue()


def render_meme_image(photo_bytes: bytes, top_text: str, bottom_text: str) -> bytes:
    with Image.open(BytesIO(photo_bytes)) as img:
        canvas = img.convert("RGB")
        w, h = canvas.size
        draw = ImageDraw.Draw(canvas)
        font = load_font(max(24, w // 14))

        def draw_outlined(text: str, y_pos: int):
            if not text:
                return
            t = text.upper()
            bbox = draw.textbbox((0, 0), t, font=font)
            tw = bbox[2] - bbox[0]
            x_pos = max(12, (w - tw) // 2)
            for dx in (-2, 0, 2):
                for dy in (-2, 0, 2):
                    if dx or dy:
                        draw.text((x_pos + dx, y_pos + dy), t, font=font, fill=(0, 0, 0))
            draw.text((x_pos, y_pos), t, font=font, fill=(255, 255, 255))

        draw_outlined(top_text, 16)
        draw_outlined(bottom_text, max(16, h - int(w // 10) - 16))

        out = BytesIO()
        canvas.save(out, format="JPEG", quality=92)
        return out.getvalue()


def invert_photo_bytes(photo_bytes: bytes) -> bytes:
    with Image.open(BytesIO(photo_bytes)) as img:
        inverted = ImageOps.invert(img.convert("RGB"))
        out = BytesIO()
        inverted.save(out, format="JPEG", quality=92)
        return out.getvalue()


def grayscale_photo_bytes(photo_bytes: bytes) -> bytes:
    with Image.open(BytesIO(photo_bytes)) as img:
        gray = ImageOps.grayscale(img.convert("RGB")).convert("RGB")
        out = BytesIO()
        gray.save(out, format="JPEG", quality=92)
        return out.getvalue()


def resize_photo_bytes(photo_bytes: bytes, width: int, height: int) -> bytes:
    with Image.open(BytesIO(photo_bytes)) as img:
        resized = img.convert("RGB").resize((width, height), Image.Resampling.LANCZOS)
        out = BytesIO()
        resized.save(out, format="JPEG", quality=92)
        return out.getvalue()
