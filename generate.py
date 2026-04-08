from PIL import Image, ImageDraw, ImageFont
import datetime, json, os

# =========================
# DATE (FRÅN WORKFLOW)
# =========================
run_date = os.environ.get("RUN_DATE")
if not run_date:
    raise RuntimeError("RUN_DATE not set")

now = datetime.datetime.strptime(run_date, "%Y-%m-%d")

# =========================
# LOAD DATA
# =========================
with open("full.json", "r", encoding="utf-8") as f:
    DB = json.load(f)

MONTHS = [
    "", "januari", "februari", "mars", "april", "maj", "juni",
    "juli", "augusti", "september", "oktober", "november", "december"
]

WEEKDAYS = [
    "Måndag", "Tisdag", "Onsdag",
    "Torsdag", "Fredag", "Lördag", "Söndag"
]

# =========================
# FONTS
# =========================
def load_font(size):
    return ImageFont.truetype("DejaVuSans.ttf", size)

def autoscale(draw, text, max_width, start):
    size = start
    while size > 30:
        font = load_font(size)
        if draw.textbbox((0, 0), text, font=font)[2] <= max_width:
            return font
        size -= 5
    return load_font(30)

# =========================
# IMAGE
# =========================
def generate_image():
    mm = f"{now.month:02d}"
    dd = f"{now.day:02d}"
    key = f"{mm}-{dd}"

    weekday = WEEKDAYS[now.weekday()]
    date_text = f"{weekday} {int(dd)} {MONTHS[int(mm)]}"

    item = DB.get(key, {"namnsdag": [], "temadag": []})

    namn = " & ".join(item.get("namnsdag", []))
    namn_text = f"Namnsdag: {namn}" if namn else "Namnsdag: -"

    tema = " & ".join(item.get("temadag", []))
    tema_text = f"Temadag: {tema}" if tema else ""

    img = Image.new("RGB", (1920, 1080), "#4169E1")
    draw = ImageDraw.Draw(img)
    cx = 960

    FONT_DATE = load_font(100)
    FONT_NAMN = autoscale(draw, namn_text, 1100, 150)
    FONT_TEMA = autoscale(draw, tema_text, 1100, 100) if tema_text else None

    _, _, wd, hd = draw.textbbox((0,0), date_text, font=FONT_DATE)
    _, _, wn, hn = draw.textbbox((0,0), namn_text, font=FONT_NAMN)
    ht = draw.textbbox((0,0), tema_text, font=FONT_TEMA)[3] if tema_text else 0

    total = hd + hn + ht + 120
    y = (1080 - total) // 2

    draw.ellipse((360, 120, 1560, 960), fill="#5FA8FF", outline="white", width=10)

    draw.text((cx - wd//2, y), date_text, fill="white", font=FONT_DATE)
    y += hd + 40
    draw.text((cx - wn//2, y), namn_text, fill="white", font=FONT_NAMN)
    y += hn + 40

    if tema_text:
        wt = draw.textbbox((0,0), tema_text, font=FONT_TEMA)[2]
        draw.text((cx - wt//2, y), tema_text, fill="white", font=FONT_TEMA)

    version = now.strftime("%Y%m%d")
    img.save(f"namnsdag-2026_v{version}.png")

if __name__ == "__main__":
    generate_image()
