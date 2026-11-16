"""Create deterministic 512x512 RGB PNG: a tiny launch ship bursting from a portal."""
from __future__ import annotations

import struct
import zlib
from pathlib import Path

W = H = 512
BG = (7, 10, 30)


def png_chunk(kind: bytes, payload: bytes) -> bytes:
    return struct.pack(">I", len(payload)) + kind + payload + struct.pack(">I", zlib.crc32(kind + payload) & 0xFFFFFFFF)


def put(px: bytearray, x: int, y: int, color: tuple[int, int, int]) -> None:
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        px[i : i + 3] = bytes(color)


def rect(px: bytearray, x0: int, y0: int, x1: int, y1: int, color: tuple[int, int, int]) -> None:
    for y in range(max(0, y0), min(H, y1 + 1)):
        start = (y * W + max(0, x0)) * 3
        end = (y * W + min(W - 1, x1) + 1) * 3
        px[start:end] = bytes(color) * (end - start) // 3


def line(px: bytearray, x0: int, y0: int, x1: int, y1: int, color: tuple[int, int, int], width: int = 1) -> None:
    dx, dy = abs(x1 - x0), abs(y1 - y0)
    sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
    err = dx - dy
    while True:
        for oy in range(-width // 2, width // 2 + 1):
            for ox in range(-width // 2, width // 2 + 1):
                put(px, x0 + ox, y0 + oy, color)
        if x0 == x1 and y0 == y1:
            return
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy


def circle(px: bytearray, cx: int, cy: int, r: int, color: tuple[int, int, int]) -> None:
    rr = r * r
    for y in range(cy - r, cy + r + 1):
        for x in range(cx - r, cx + r + 1):
            if (x - cx) ** 2 + (y - cy) ** 2 <= rr:
                put(px, x, y, color)


def main() -> None:
    px = bytearray(bytes(BG) * (W * H))
    # Halo bands: bold concentric launch portal.
    circle(px, 256, 325, 158, (18, 22, 73))
    circle(px, 256, 325, 132, (38, 24, 110))
    circle(px, 256, 325, 105, (255, 39, 149))
    circle(px, 256, 325, 82, (20, 20, 68))
    circle(px, 256, 325, 61, (9, 12, 38))

    # Deterministic starfield / speed streaks.
    stars = [(38, 62, 3), (91, 142, 2), (148, 48, 2), (205, 101, 3), (300, 58, 2), (388, 129, 3), (465, 72, 2), (438, 204, 3), (64, 248, 2), (115, 198, 2), (352, 174, 2), (477, 300, 2)]
    for x, y, r in stars:
        circle(px, x, y, r, (255, 239, 142))
    for x, y, length in [(32, 176, 43), (408, 98, 50), (62, 364, 34), (431, 385, 55), (104, 94, 24), (374, 252, 32)]:
        line(px, x, y, x + length, y - length // 3, (75, 180, 255), 3)

    # Rocket flame behind ship.
    line(px, 256, 267, 256, 424, (255, 242, 116), 23)
    line(px, 256, 288, 256, 405, (255, 116, 35), 13)
    line(px, 256, 305, 256, 387, (255, 248, 207), 6)
    for x, y, dx in [(220, 340, -25), (292, 352, 30), (233, 398, -18), (280, 418, 20)]:
        line(px, x, y, x + dx, y + 42, (255, 61, 171), 5)

    # Rocket body: readable silhouette, window, fins, nose.
    line(px, 256, 112, 256, 289, (241, 248, 255), 64)
    line(px, 256, 112, 256, 289, (255, 255, 255), 52)
    for y, half in [(112, 0), (120, 18), (135, 30), (151, 39)]:
        line(px, 256, y, 256, y + 1, (255, 255, 255), max(2, half * 2 + 2))
    line(px, 256, 205, 256, 287, (255, 58, 160), 8)
    line(px, 256, 154, 256, 197, (25, 53, 116), 34)
    circle(px, 256, 154, 20, (64, 213, 255))
    circle(px, 250, 148, 7, (208, 251, 255))
    line(px, 222, 244, 181, 285, (255, 255, 255), 18)
    line(px, 290, 244, 331, 285, (255, 255, 255), 18)
    line(px, 222, 244, 181, 285, (255, 52, 151), 7)
    line(px, 290, 244, 331, 285, (255, 52, 151), 7)

    # Pixel sparks at portal edge.
    for x, y in [(137, 302), (164, 382), (342, 289), (363, 354), (187, 427), (320, 436), (105, 328), (402, 321)]:
        line(px, x - 8, y, x + 8, y, (255, 232, 93), 3)
        line(px, x, y - 8, x, y + 8, (255, 232, 93), 3)

    raw = b"".join(b"\x00" + px[y * W * 3 : (y + 1) * W * 3] for y in range(H))
    data = b"\x89PNG\r\n\x1a\n" + png_chunk(b"IHDR", struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)) + png_chunk(b"IDAT", zlib.compress(raw, 9)) + png_chunk(b"IEND", b"")
    Path(__file__).with_name("entry.png").write_bytes(data)


if __name__ == "__main__":
    main()
