#!/usr/bin/env python3
"""Build the news-image-20261123 front page (1024x1024 PNG).

Deterministic: fixed text, fixed geometry, no network, no randomness,
no timestamps. Run: python3 build_image.py  ->  entry.png
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (17, 17, 17)
RED = (176, 30, 30)
NAVY = (18, 53, 91)
TEAL = (14, 107, 107)
GREEN = (30, 122, 52)
GREY = (90, 86, 76)

FD = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = "DejaVuSerif-Bold.ttf"
SANS_B = "DejaVuSans-Bold.ttf"
SANS = "DejaVuSans.ttf"


def font(name, size):
    return ImageFont.truetype(FD + name, size)


def wrap(draw, text, fnt, width):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def centre(draw, y, text, fnt, fill, x0=0, x1=W):
    w = draw.textlength(text, font=fnt)
    draw.text(((x0 + x1 - w) / 2, y), text, font=fnt, fill=fill)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    m = 30

    # ---- masthead ----
    d.rectangle([0, 0, W, 118], fill=INK)
    centre(d, 8, "THE WORLD", font(SERIF_B, 62), (247, 243, 232))
    centre(d, 82, "MONDAY  23  NOVEMBER  2026", font(SANS_B, 24), (232, 196, 90))
    d.line([m, 132, W - m, 132], fill=INK, width=3)
    centre(d, 140, "ONE DAY  \u2022  ONE PAGE  \u2022  THE DAY IN FULL",
           font(SANS_B, 17), GREY)

    # ---- LEAD: COP31 ----
    y = 176
    d.text((m, y), "COP31 COLLAPSES", font=font(SERIF_B, 62), fill=RED)
    d.text((m, y + 66), "NO CLIMATE DEAL", font=font(SERIF_B, 58), fill=INK)
    lead = ("The longest UN climate talks in history end in Antalya, "
            "Turkey, with no agreement on phasing out fossil fuels "
            "or on adaptation finance.")
    yy = y + 140
    for line in wrap(d, lead, font(SANS, 25), 600):
        d.text((m, yy), line, font=font(SANS, 25), fill=INK)
        yy += 32

    # lead visual: cracked globe panel (right)
    px0, py0, px1, py1 = 668, 176, W - m, 424
    d.rectangle([px0, py0, px1, py1], fill=NAVY)
    d.ellipse([px0 + 62, py0 + 18, px0 + 238, py0 + 194], fill=(46, 130, 180))
    d.ellipse([px0 + 92, py0 + 48, px0 + 150, py0 + 96], fill=(72, 160, 90))
    d.ellipse([px0 + 150, py0 + 110, px0 + 208, py0 + 164], fill=(72, 160, 90))
    d.line([px0 + 150, py0 + 18, px0 + 132, py0 + 80, px0 + 168, py0 + 120,
            px0 + 140, py0 + 194], fill=(247, 243, 232), width=5)
    centre(d, py1 - 38, "THE PLANET WAITS", font(SANS_B, 20),
           (247, 243, 232), px0, px1)

    d.line([m, 440, W - m, 440], fill=INK, width=2)

    # ---- SECOND: Ukraine drones ----
    y = 456
    d.rectangle([m, y, W - m, y + 118], fill=(20, 20, 20))
    d.text((m + 16, y + 10), "UKRAINE DRONES SINK RUSSIAN",
           font=font(SANS_B, 34), fill=(247, 243, 232))
    d.text((m + 16, y + 50), "WARSHIP OFF LIBYA",
           font=font(SANS_B, 34), fill=(232, 196, 90))
    d.text((m + 16, y + 88),
           "Zelensky confirms sea-drone strike at Benghazi  \u2022  Kyiv hit: 15 killed",
           font=font(SANS, 19), fill=(200, 200, 200))

    # ---- THIRD: Nvidia ----
    y = 592
    d.rectangle([m, y, W - m, y + 96], fill=(232, 246, 232))
    d.rectangle([m, y, m + 8, y + 96], fill=GREEN)
    d.text((m + 22, y + 8), "HUANG IS BACK AT NVIDIA",
           font=font(SANS_B, 36), fill=INK)
    d.text((m + 22, y + 52),
           "Shares soar 31% as CEO returns after 11 days  \u2022  Nasdaq +6%",
           font=font(SANS, 22), fill=INK)
    cx, cy = 880, y + 78
    d.line([(cx - 110, cy), (cx - 70, cy - 26), (cx - 30, cy - 14),
            (cx + 10, cy - 44), (cx + 50, cy - 58)], fill=GREEN, width=6)
    d.polygon([(cx + 50, cy - 58), (cx + 28, cy - 52), (cx + 50, cy - 34)],
              fill=GREEN)

    # ---- GRID: six more stories ----
    stories = [
        ("INDONESIA", RED, "Factory fire kills 24",
         "Blaze at sweets factory; dozens still missing."),
        ("KYIV", NAVY, "Strikes kill 15",
         "Russian bombardment hits the Kyiv region."),
        ("MERCURY", TEAL, "BepiColombo arrives",
         "Spacecraft enter orbit after an 8-year trip."),
        ("MATHS", (110, 60, 140), "AI proves Riemann",
         "Anthropic says AI helped crack the great puzzle."),
        ("FBI", (120, 40, 40), "Police database hacked",
         "FBI probes breach of crime records system."),
        ("MARKETS", GREEN, "Bitcoin rebounds",
         "BTC back to $61,000; CrowdStrike buys Zscaler, $44bn."),
    ]
    gx, gy = m, 706
    cw, ch, gap = 310, 92, 14
    for i, (tag, col, head, sub) in enumerate(stories):
        x = gx + (i % 3) * (cw + gap)
        yy = gy + (i // 3) * (ch + gap)
        d.rectangle([x, yy, x + cw, yy + ch], fill=(255, 255, 255),
                    outline=(200, 194, 178), width=2)
        d.rectangle([x, yy, x + cw, yy + 26], fill=col)
        d.text((x + 8, yy + 4), tag, font=font(SANS_B, 16), fill=(255, 255, 255))
        d.text((x + 8, yy + 32), head, font=font(SANS_B, 19), fill=INK)
        for j, line in enumerate(wrap(d, sub, font(SANS, 15), cw - 16)):
            d.text((x + 8, yy + 56 + j * 18), line, font=font(SANS, 15),
                   fill=GREY)

    # ---- footer ----
    fy = 920
    d.line([m, fy, W - m, fy], fill=INK, width=2)
    centre(d, fy + 12, "23 NOVEMBER 2026", font(SERIF_B, 30), INK)
    centre(d, fy + 52,
           "COP31 fails  \u2022  War at sea off Libya  \u2022  Huang returns  \u2022  Fire in Indonesia",
           font(SANS, 19), GREY)
    centre(d, fy + 80, "THE WORLD  \u2022  MONDAY 23 NOVEMBER 2026",
           font(SANS_B, 15), GREY)

    img.save("entry.png", "PNG", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
