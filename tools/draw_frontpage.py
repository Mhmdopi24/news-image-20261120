#!/usr/bin/env python3
"""Draw the front page for THE WORLD TODAY, Friday 20 November 2026.

One 1024x1024 PNG newspaper front page summing up the day's world news.
All artwork is flat vector-style drawing done here with Pillow; all text is
set with system serif/sans fonts. No external images are used.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 233)
INK = (17, 17, 17)
RED = (164, 31, 31)
MUTED = (90, 86, 76)
PANEL = (223, 231, 238)
NAVY = (31, 58, 95)
GOLD = (176, 141, 60)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, leading, fill=INK):
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def star_points(cx, cy, r_out, r_in, rot=-90):
    pts = []
    for i in range(10):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + i * 36)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def flag_us(d, x, y, w, h):
    stripe = h / 7
    for i in range(7):
        if i % 2 == 0:
            d.rectangle([x, y + i * stripe, x + w, y + (i + 1) * stripe], fill=(178, 34, 52))
    cw, ch = w * 0.42, stripe * 4
    d.rectangle([x, y, x + cw, y + ch], fill=(31, 58, 95))
    for r in range(3):
        for c in range(4):
            px = x + 8 + c * (cw - 14) / 3
            py = y + 7 + r * (ch - 12) / 2
            d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(255, 255, 255))


def flag_cn(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    d.polygon(star_points(x + w * 0.18, y + h * 0.28, h * 0.22, h * 0.09), fill=(255, 222, 0))
    for sx, sy in [(0.42, 0.12), (0.52, 0.24), (0.52, 0.42), (0.42, 0.52)]:
        d.polygon(star_points(x + w * sx, y + h * sy, h * 0.09, h * 0.037), fill=(255, 222, 0))


def flag_ru(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h / 3], fill=(255, 255, 255))
    d.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill=(0, 57, 166))
    d.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=(213, 0, 50))


def flag_at(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h / 3], fill=(237, 41, 36))
    d.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill=(255, 255, 255))
    d.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=(237, 41, 36))


def flag_nl(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h / 3], fill=(174, 28, 40))
    d.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill=(255, 255, 255))
    d.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=(33, 70, 139))


def draw_scales(d, x0, y0, x1, y1):
    """Scales of justice inside box (x0,y0)-(x1,y1)."""
    d.rectangle([x0, y0, x1, y1], fill=PANEL, outline=INK, width=2)
    cx = (x0 + x1) // 2
    top, bot = y0 + 26, y1 - 52
    d.ellipse([cx - 6, top - 6, cx + 6, top + 6], fill=GOLD)
    d.rectangle([cx - 4, top, cx + 4, bot], fill=NAVY)
    beam_y = top + 26
    d.rectangle([x0 + 34, beam_y - 4, x1 - 34, beam_y + 4], fill=NAVY)
    for side in (-1, 1):
        px = cx + side * (x1 - x0 - 68) // 2
        d.line([px, beam_y, px - 26, bot - 34], fill=NAVY, width=3)
        d.line([px, beam_y, px + 26, bot - 34], fill=NAVY, width=3)
        d.line([px, beam_y, px, bot - 34], fill=NAVY, width=3)
        d.pieslice([px - 30, bot - 38, px + 30, bot + 6], start=0, end=180, fill=GOLD, outline=NAVY, width=2)
    d.rectangle([cx - 52, bot, cx + 52, bot + 10], fill=NAVY)
    d.rectangle([cx - 70, bot + 10, cx + 70, bot + 18], fill=NAVY)
    d.text(((x0 + x1) / 2 - 108, y1 - 34), "The Peace Palace, The Hague",
           font=font(SERIF, 17), fill=MUTED)


def draw_cyclone(d, x0, y0, x1, y1):
    """Cyclone spiral with rain and a coastline, drawn to fit the box."""
    d.rectangle([x0, y0, x1, y1], fill=(214, 228, 238), outline=INK, width=2)
    cx, cy = x0 + 78, (y0 + y1) // 2
    rmax = min(34, (y1 - y0) // 2 - 6)
    for r, a0 in [(rmax, 200), (int(rmax * 0.75), 140),
                  (int(rmax * 0.5), 80), (int(rmax * 0.28), 20)]:
        d.arc([cx - r, cy - r, cx + r, cy + r], start=a0, end=a0 + 250,
              fill=NAVY, width=4)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=RED)
    for i in range(4):
        rx = x0 + 12 + i * 22
        d.line([rx, y0 + 8, rx - 8, y0 + 24], fill=(90, 120, 150), width=3)
    d.polygon([(x1 - 120, y1 - 6), (x1 - 66, y1 - 44), (x1 - 10, y1 - 6)],
              fill=(120, 150, 110))
    d.ellipse([x1 - 72, y1 - 50, x1 - 60, y1 - 38], fill=RED)
    d.text((x1 - 208, y0 + 8), "LANDFALL: MIDDAY", font=font(SANS_B, 15), fill=RED)


def draw_sunset(d, x0, y0, x1, y1):
    """Sunset skyline with 'VI', drawn to fit box (x0,y0)-(x1,y1)."""
    bands = [(255, 176, 66), (255, 140, 90), (235, 92, 110), (150, 80, 140)]
    bh = (y1 - y0) / len(bands)
    for i, col in enumerate(bands):
        d.rectangle([x0, y0 + i * bh, x1, y0 + (i + 1) * bh + 1], fill=col)
    d.ellipse([x0 + 14, y0 + 8, x0 + 44, y0 + 38], fill=(255, 236, 180))
    sky = y0 + (y1 - y0) * 0.60
    heights = [0.30, 0.45, 0.36, 0.52, 0.34, 0.46]
    bw = (x1 - x0) / len(heights)
    for i, hf in enumerate(heights):
        bx = x0 + i * bw
        d.rectangle([bx + 2, sky - (y1 - y0) * hf * 0.55, bx + bw - 2, y1],
                    fill=(30, 20, 50))
    px = x0 + 12
    d.line([px, y1, px - 8, y0 + 26], fill=(30, 20, 50), width=4)
    for a in (-50, -25, 0, 25, 50):
        ex = px - 8 + 20 * math.sin(math.radians(a))
        ey = y0 + 26 + 8 * math.cos(math.radians(a)) - 6
        d.line([px - 8, y0 + 26, ex, ey], fill=(30, 20, 50), width=3)
    d.text((x1 - 84, y0 + 16), "VI", font=font(SERIF_B, 44), fill=(255, 255, 255),
           stroke_width=2, stroke_fill=(30, 20, 50))


def draw_embassies(d, x0, y0, x1, y1):
    """Damaged embassy buildings with Austrian and Dutch flags."""
    d.rectangle([x0, y0, x1, y1], fill=(228, 226, 220), outline=INK, width=2)
    mid = y0 + (y1 - y0) * 0.45
    d.polygon([(x0 + 18, y1 - 6), (x0 + 18, mid + 12), (x0 + 66, mid - 6),
               (x0 + 114, mid + 12), (x0 + 114, y1 - 6)], fill=(120, 116, 108))
    d.rectangle([x0 + 150, mid + 4, x1 - 18, y1 - 6], fill=(96, 92, 84))
    for wx in range(3):
        d.rectangle([x0 + 160 + wx * 34, mid + 14, x0 + 176 + wx * 34, mid + 30],
                    fill=(248, 244, 233))
    bx, by = x0 + 66, mid - 6
    for a in range(0, 360, 45):
        ex = bx + 16 * math.cos(math.radians(a))
        ey = by + 16 * math.sin(math.radians(a))
        d.line([bx, by, ex, ey], fill=RED, width=3)
    d.line([x0 + 30, y0 + 6, x0 + 30, y0 + 26], fill=INK, width=3)
    d.line([x1 - 66, y0 + 6, x1 - 66, y0 + 26], fill=INK, width=3)
    flag_at(d, x0 + 30, y0 + 8, 30, 18)
    flag_nl(d, x1 - 66, y0 + 8, 30, 18)


def draw_court(d, x0, y0, x1, y1):
    """Courthouse with columns and a taegeuk roundel."""
    d.rectangle([x0, y0, x1, y1], fill=(232, 230, 224), outline=INK, width=2)
    d.polygon([(x0 + 14, y0 + 30), ((x0 + x1) // 2, y0 + 8), (x1 - 14, y0 + 30)],
              fill=NAVY)
    d.rectangle([x0 + 14, y0 + 30, x1 - 14, y0 + 36], fill=NAVY)
    for i in range(3):
        cx = x0 + 44 + i * ((x1 - x0 - 88) // 2)
        d.rectangle([cx - 8, y0 + 36, cx + 8, y1 - 16], fill=(250, 250, 248),
                    outline=INK, width=2)
    d.rectangle([x0 + 14, y1 - 16, x1 - 14, y1 - 10], fill=NAVY)
    cx, cy, r = (x0 + x1) // 2, y0 + 20, 9
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(205, 46, 58))
    d.pieslice([cx - r, cy - r, cx + r, cy + r], start=0, end=180, fill=(0, 66, 160))
    d.ellipse([cx - r, cy - 3, cx, cy + 3], fill=(0, 66, 160))
    d.ellipse([cx, cy - 3, cx + r, cy + 3], fill=(205, 46, 58))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # Border
    d.rectangle([14, 14, W - 15, H - 15], outline=INK, width=2)
    d.rectangle([20, 20, W - 21, H - 21], outline=INK, width=1)

    # Masthead (auto-fit to the page width)
    title = "THE WORLD TODAY"
    tsize = 88
    tf = font(SERIF_B, tsize)
    while d.textlength(title, font=tf) > 940 and tsize > 40:
        tsize -= 2
        tf = font(SERIF_B, tsize)
    d.text(((W - d.textlength(title, font=tf)) / 2, 30), title, font=tf, fill=INK)
    d.line([28, 134, W - 28, 134], fill=INK, width=2)
    d.line([28, 138, W - 28, 138], fill=INK, width=1)
    df = font(SANS_B, 22)
    d.text((28, 148), "FRIDAY, 20 NOVEMBER 2026", font=df, fill=INK)
    mid = "ONE DAY  •  ONE WORLD"
    mf = font(SANS, 17)
    d.text(((W - d.textlength(mid, font=mf)) / 2, 152), mid, font=mf, fill=MUTED)
    d.text((W - 28 - d.textlength("No. 324", font=df), 148), "No. 324", font=df, fill=INK)
    d.line([28, 182, W - 28, 182], fill=INK, width=4)
    d.line([28, 188, W - 28, 188], fill=INK, width=1)

    # ---- Lead story: ICJ / Myanmar (192-450) ----
    kf = font(SANS_B, 17)
    d.text((28, 200), "THE HAGUE  •  WORLD COURT", font=kf, fill=RED)
    hf = font(SERIF_B, 54)
    d.text((28, 228), "MYANMAR GUILTY", font=hf, fill=INK)
    d.text((28, 290), "OF GENOCIDE", font=hf, fill=INK)
    bf = font(SERIF, 19)
    y = para(d, 28, 360, "The UN's highest court finds Myanmar responsible "
             "for genocide against the Rohingya — a first in 80 years.",
             bf, 592, 25)
    para(d, 28, y + 6, "9–6 ruling on the 2017 crackdown; reparations ordered.",
         bf, 592, 25)
    draw_scales(d, 648, 200, 996, 442)

    d.line([28, 460, W - 28, 460], fill=INK, width=2)

    # ---- Row 2: two stories (470-700) ----
    y = 474
    d.text((28, y), "SHENZHEN  •  APEC SUMMIT", font=kf, fill=RED)
    d.text((524, y), "INDIA  •  CYCLONE AKVAN", font=kf, fill=RED)
    h2 = font(SERIF_B, 27)
    y2 = para(d, 28, y + 28, "TRUMP, XI AND PUTIN MEET FOR FIRST TIME",
              h2, 460, 32)
    para(d, 524, y + 28, "300,000 FLEE AS CYCLONE AKVAN NEARS",
         h2, 460, 32)
    sf = font(SERIF, 17)
    para(d, 28, y2 + 6, "Ninety minutes on nuclear risks, Ukraine and Iran — "
         "a pledge of more talks, but no breakthrough.",
         sf, 460, 21)
    para(d, 524, y2 + 6, "Severe storm nears the Andhra Pradesh and Odisha "
         "coasts; landfall due at midday, gusts of 110 km/h.",
         sf, 460, 21)
    fy = 622
    flag_us(d, 28, fy, 140, 66)
    flag_cn(d, 182, fy, 140, 66)
    flag_ru(d, 336, fy, 140, 66)
    d.text((28, fy + 70), "U.S.  •  CHINA  •  RUSSIA", font=font(SANS, 13), fill=MUTED)
    draw_cyclone(d, 524, 622, 996, 700)
    d.line([512, 474, 512, 700], fill=INK, width=1)

    d.line([28, 712, W - 28, 712], fill=INK, width=2)

    # ---- Row 3: three stories (722-930) ----
    cols = [(28, 338), (352, 662), (676, 996)]
    y = 724
    kickers = ["CULTURE  •  GAMES", "KYIV  •  WAR", "SEOUL  •  COURTS"]
    heads = ["GTA VI SMASHES LAUNCH RECORDS",
             "STRIKES DAMAGE EMBASSIES IN KYIV",
             "TOP COURT CLEARS EX-PM HAN"]
    bodies = ["An estimated 19m copies and $1.84bn in first-day sales; "
              "99 on Metacritic.",
              "Russian missiles hit Kyiv; Ukraine says it struck the "
              "Crimean Bridge.",
              "The Supreme Court clears the ex-PM over the martial-law "
              "case."]
    h3 = font(SERIF_B, 23)
    bf3 = font(SERIF, 15)
    for (x0, x1), k, htxt, btxt in zip(cols, kickers, heads, bodies):
        d.text((x0, y), k, font=kf, fill=RED)
        yy = para(d, x0, y + 26, htxt, h3, x1 - x0, 27)
        para(d, x0, yy + 4, btxt, bf3, x1 - x0, 19)
    for vx in (344, 668):
        d.line([vx, 724, vx, 930], fill=INK, width=1)
    draw_sunset(d, 28, 856, 338, 930)
    draw_embassies(d, 352, 856, 662, 930)
    draw_court(d, 676, 856, 996, 930)

    # ---- Footer (942-1004) ----
    d.line([28, 942, W - 28, 942], fill=INK, width=2)
    d.text((28, 952), "ALSO TODAY —", font=font(SANS_B, 16), fill=RED)
    ff = font(SERIF, 15)
    d.text((28, 976), "Fiji drought disaster declared  •  Anthropic valued at "
           "$1.5tn, reports say  •  Nicholls 113* as India face NZ",
           font=ff, fill=INK)

    img.save("entry.png", format="PNG", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
