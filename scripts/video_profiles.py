"""Editable canvas presets shared by local video and cover helpers.

These are production starting points, not a promise that a platform's current
upload rules or interface safe zones will remain unchanged.
"""

from pathlib import Path

from PIL import ImageFont


PROFILES = {
    "wide": (1920, 1080),
    "vertical": (1080, 1920),
    "square": (1080, 1080),
    "portrait-feed": (1080, 1350),
}

COVER_PROFILES = {
    "wide": (1280, 720),
    "vertical": (1080, 1920),
    "square": (1080, 1080),
    "portrait-feed": (1080, 1350),
}


def dimensions(profile: str, width: int | None = None, height: int | None = None,
               *, cover: bool = False) -> tuple[int, int]:
    presets = COVER_PROFILES if cover else PROFILES
    if (width is None) != (height is None):
        raise ValueError("Pass both --width and --height, or neither")
    result = (width, height) if width is not None else presets[profile]
    if any(value < 64 or value % 2 for value in result):
        raise ValueError("Canvas dimensions must be even and at least 64 pixels")
    return result


def video_filter(width: int, height: int, mode: str, focus_x: float = 0.5,
                 focus_y: float = 0.5, fps: int = 30, rotation: str = "auto") -> str:
    if not 0 <= focus_x <= 1 or not 0 <= focus_y <= 1:
        raise ValueError("Focus values must be between 0 and 1")
    if fps < 1 or fps > 120:
        raise ValueError("FPS must be between 1 and 120")
    prefix = {"auto": "", "none": "", "cw": "transpose=clock,",
              "ccw": "transpose=cclock,", "180": "hflip,vflip,"}[rotation]
    if mode == "crop":
        return (
            f"{prefix}scale={width}:{height}:force_original_aspect_ratio=increase:force_divisible_by=2,"
            f"crop={width}:{height}:x='(in_w-out_w)*{focus_x}':y='(in_h-out_h)*{focus_y}',"
            f"fps={fps},format=yuv420p[v]"
        )
    if mode == "fit":
        return (
            f"{prefix}split=2[bg][fg];"
            f"[bg]scale={width}:{height}:force_original_aspect_ratio=increase:force_divisible_by=2,"
            f"crop={width}:{height},boxblur=30:2,eq=brightness=-0.12[back];"
            f"[fg]scale={width}:{height}:force_original_aspect_ratio=decrease:force_divisible_by=2[front];"
            f"[back][front]overlay=(W-w)/2:(H-h)/2,fps={fps},format=yuv420p[v]"
        )
    raise ValueError(f"Unknown framing mode: {mode}")


def font(bold: bool = False, size: int = 24) -> ImageFont.FreeTypeFont:
    candidates = [
        Path("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else
             "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
    ]
    for path in candidates:
        if path.is_file():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default(size=size)
