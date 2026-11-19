#!/usr/bin/env python3
"""THE WORLD — front page for Thursday 19 November 2026.

Deterministic: fixed fonts, no randomness, no timestamps. Running it twice
writes byte-identical PNGs. Output: 1024x1024 PNG, well under 1 MiB.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 28
PAPER = (251, 248, 241)
INK = (26, 26, 26)
GRAY = (90, 86, 78)
RED = (139, 26, 26)
RULE = (180, 172, 158)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

SERIF_I = SERIF_I if os.path.exists(SERIF_I) else SERIF


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_center(draw, y, text, fnt, fill=INK):
    x = (W - draw.textlength(text, font=fnt)) / 2
    draw.text((x, y), text, font=fnt, fill=fill)
    return y + fnt.size


def rule(draw, x0, x1, y, width=1, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- stories
LEAD = {
    "kicker": "SHENZHEN SUMMIT",
    "headline": "TRUMP, XI AND PUTIN MEET IN SHENZHEN",
    "subhead": (
        "The three leaders hold a rare trilateral, pledging talks on trade, "
        "energy and Ukraine — but leave the hardest questions open."
    ),
    "body": (
        "SHENZHEN — Presidents Donald Trump, Xi Jinping and Vladimir Putin "
        "met here on Thursday for the first three-way summit of their "
        "presidencies. The leaders announced working groups on trade, "
        "energy security and a path to end the war in Ukraine."
    ),
}

# 35 self-contained headlines, 5 per region, 7 regions.
REGIONS = [
    ("NORTH AMERICA", [
        "US House passes budget deal after late-night vote",
        "Fed holds rates, signals one cut in December",
        "Canada unveils Arctic defence plan",
        "Mexico City metro line reopens after quake checks",
        "California wildfire crews gain ground",
    ]),
    ("SOUTH AMERICA", [
        "Brazil's Congress approves Amazon fund",
        "Argentina inflation falls to two-year low",
        "Chile copper output hits record",
        "Colombia peace talks resume in Havana",
        "Peru opens new Pacific port terminal",
    ]),
    ("EUROPE", [
        "EU agrees joint defence procurement",
        "UK economy grows faster than forecast",
        "France launches high-speed rail link",
        "Germany's coalition backs energy package",
        "Ukraine grain exports reach wartime high",
    ]),
    ("MIDDLE EAST", [
        "Gaza ceasefire monitors deploy",
        "Saudi Arabia opens Red Sea resort",
        "Israel and Lebanon agree border talks",
        "UAE launches AI research hub",
        "Iraq oil exports steady after pipeline fix",
    ]),
    ("AFRICA", [
        "Nigeria's naira steadies after reforms",
        "Kenya opens Africa's largest wind farm",
        "South Africa power cuts ease",
        "Egypt's Suez Canal traffic rebounds",
        "Ethiopia signs Grand Dam power deal",
    ]),
    ("ASIA-PACIFIC", [
        "Japan's Nikkei hits record high",
        "India launches lunar lander mission",
        "Australia signs Pacific climate pact",
        "South Korea chip exports surge",
        "Indonesia opens new capital district",
    ]),
    ("OCEANIA", [
        "New Zealand votes in local elections",
        "Fiji coral project shows regrowth",
        "Papua New Guinea quake aid arrives",
        "Samoa hosts Pacific leaders' summit",
        "Australia's Great Barrier Reef survey",
    ]),
]


def draw_skyline(draw, x0, y0, x1, y1):
    """Simple Shenzhen skyline: dark towers, a pale sun, three banners."""
    draw.rectangle([x0, y0, x1, y1], fill=(232, 226, 210))
    draw.rectangle([x0, y0, x1, y1], outline=RULE, width=1)
    cx, cy, r = x0 + 48, y0 + 40, 24
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(214, 164, 92))
    base = y1 - 8
    towers = [
        (0.02, 0.10, 0.62), (0.13, 0.09, 0.78), (0.24, 0.11, 0.55),
        (0.37, 0.10, 0.88), (0.49, 0.12, 0.70), (0.63, 0.10, 0.80),
        (0.75, 0.11, 0.60), (0.88, 0.09, 0.72),
    ]
    span = x1 - x0
    for fx, fw, fh in towers:
        tx0 = x0 + int(fx * span)
        tx1 = tx0 + int(fw * span)
        ty0 = base - int(fh * (y1 - y0 - 16))
        draw.rectangle([tx0, ty0, tx1, base], fill=(58, 58, 60))
        for wy in range(ty0 + 8, base - 6, 14):
            for wx in range(tx0 + 5, tx1 - 5, 12):
                if (wx + wy) % 28 < 10:
                    draw.rectangle([wx, wy, wx + 3, wy + 4], fill=(232, 226, 210))
    bw, bh = 24, 52
    bx = x0 + 12
    by = y1 - bh - 4
    # US
    draw.rectangle([bx, by, bx + bw, by + bh], fill=(255, 255, 255), outline=INK)
    for i in range(7):
        draw.rectangle([bx, by + i * 7, bx + bw, by + i * 7 + 3],
                       fill=(178, 34, 34) if i % 2 == 0 else (255, 255, 255))
    draw.rectangle([bx, by, bx + 11, by + 21], fill=(30, 60, 120))
    # China
    bx += bw + 9
    draw.rectangle([bx, by, bx + bw, by + bh], fill=(222, 41, 16), outline=INK)
    draw.ellipse([bx + 4, by + 5, bx + 10, by + 11], fill=(255, 222, 0))
    draw.ellipse([bx + 13, by + 9, bx + 17, by + 13], fill=(255, 222, 0))
    draw.ellipse([bx + 12, by + 18, bx + 16, by + 22], fill=(255, 222, 0))
    # Russia
    bx += bw + 9
    draw.rectangle([bx, by, bx + bw, by + bh], fill=(255, 255, 255), outline=INK)
    draw.rectangle([bx, by + 17, bx + bw, by + 34], fill=(0, 57, 166))
    draw.rectangle([bx, by + 34, bx + bw, by + bh], fill=(213, 0, 50))
    cap = font(SANS, 10)
    draw.text((x0 + 6, y1 + 5), "Shenzhen, Thursday — the summit skyline.",
              font=cap, fill=GRAY)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead
    y = 26
    mast = font(SERIF_B, 68)
    draw_center(d, y, "THE WORLD", mast)
    y += 84
    rule(d, MARGIN, W - MARGIN, y, width=2, fill=INK)
    y += 5
    rule(d, MARGIN, W - MARGIN, y, width=1, fill=INK)
    y += 11
    dateline = font(SANS_B, 14)
    draw_center(d, y, "THURSDAY, 19 NOVEMBER 2026  •  35 STORIES  •  7 REGIONS",
                dateline)
    y += 24
    rule(d, MARGIN, W - MARGIN, y, width=1, fill=RULE)

    # ---- lead story
    y += 12
    kick = font(SANS_B, 15)
    d.text((MARGIN, y), LEAD["kicker"], font=kick, fill=RED)
    y += 24
    head = font(SERIF_B, 38)
    for line in wrap(d, LEAD["headline"], head, W - 2 * MARGIN):
        d.text((MARGIN, y), line, font=head, fill=INK)
        y += 46
    y += 2
    sub = font(SERIF_I, 17)
    for line in wrap(d, LEAD["subhead"], sub, W - 2 * MARGIN):
        d.text((MARGIN, y), line, font=sub, fill=(60, 58, 52))
        y += 22
    y += 6
    # body text (left) + skyline (right)
    body_top = y
    body_w = 560
    body = font(SERIF, 13)
    for line in wrap(d, LEAD["body"], body, body_w):
        d.text((MARGIN, y), line, font=body, fill=INK)
        y += 18
    img_w = W - MARGIN - (MARGIN + body_w + 24)
    draw_skyline(d, MARGIN + body_w + 24, body_top,
                 MARGIN + body_w + 24 + img_w, body_top + 118)
    y = max(y, body_top + 118 + 20)
    rule(d, MARGIN, W - MARGIN, y, width=1, fill=RULE)

    # ---- region grid: 2 columns (left 4 regions, right 3), headlines only
    y += 12
    col_w = (W - 2 * MARGIN - 24) // 2
    left_x, right_x = MARGIN, MARGIN + col_w + 24

    def region_block(x, top, name, stories):
        yy = top
        hdr = font(SANS_B, 14)
        d.text((x, yy), name, font=hdr, fill=RED)
        yy += 20
        rule(d, x, x + col_w, yy, width=1, fill=INK)
        yy += 7
        tf = font(SANS_B, 12)
        for title in stories:
            for line in wrap(d, title, tf, col_w):
                d.text((x, yy), line, font=tf, fill=INK)
                yy += 15
            yy += 3
        return yy

    ly = y
    for name, stories in REGIONS[:4]:
        ly = region_block(left_x, ly, name, stories)
        ly += 8
    ry = y
    for name, stories in REGIONS[4:]:
        ry = region_block(right_x, ry, name, stories)
        ry += 8
    # day-in-numbers box under the right column
    by = ry + 4
    box_h = 116
    d.rectangle([right_x, by, right_x + col_w, by + box_h],
                fill=(240, 234, 222), outline=RULE)
    d.text((right_x + 12, by + 10), "THE DAY IN NUMBERS",
           font=font(SANS_B, 13), fill=RED)
    nums = [
        "3  leaders at one table in Shenzhen",
        "35  stories from 7 regions",
        "5m  tonnes of grain shipped from Ukraine",
        "310 MW  from Kenya's new wind farm",
    ]
    ny = by + 32
    for n in nums:
        d.text((right_x + 12, ny), n, font=font(SANS, 12), fill=INK)
        ny += 19

    # ---- footer
    fy = H - 32
    rule(d, MARGIN, W - MARGIN, fy, width=1, fill=RULE)
    draw_center(d, fy + 8,
                "THE WORLD  •  Thursday 19 November 2026  •  theworld.news",
                font(SANS, 12), fill=GRAY)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
