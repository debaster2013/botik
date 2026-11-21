import os
import shutil
import subprocess
import tempfile
from io import BytesIO
from pathlib import Path
from PIL import Image


def get_ffmpeg_bin() -> str | None:
    if Path("ffmpeg.exe").exists():
        return str(Path("ffmpeg.exe").resolve())
    return shutil.which("ffmpeg")


def has_ffmpeg() -> bool:
    return get_ffmpeg_bin() is not None


def webp_to_png_bytes(raw_bytes: bytes) -> bytes:
    with Image.open(BytesIO(raw_bytes)) as img:
        rgba = img.convert("RGBA")
        bg = Image.new("RGBA", rgba.size, (30, 30, 36, 255))
        composed = Image.alpha_composite(bg, rgba).convert("RGB")
        out = BytesIO()
        composed.save(out, format="PNG")
        return out.getvalue()


def webm_to_mp4_bytes(raw_bytes: bytes) -> bytes | None:
    ffmpeg_bin = get_ffmpeg_bin()
    if not ffmpeg_bin:
        return None

    with tempfile.TemporaryDirectory() as tmpdir:
        in_path = os.path.join(tmpdir, "in.webm")
        out_path = os.path.join(tmpdir, "out.mp4")
        with open(in_path, "wb") as f:
            f.write(raw_bytes)

        proc = subprocess.run(
            [
                ffmpeg_bin,
                "-y",
                "-i",
                in_path,
                "-c:v",
                "libx264",
                "-pix_fmt",
                "yuv420p",
                "-movflags",
                "+faststart",
                out_path,
            ],
            capture_output=True,
            text=True,
        )
        if proc.returncode != 0 or not os.path.exists(out_path):
            return None

        with open(out_path, "rb") as f:
            return f.read()
