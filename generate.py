from PIL import Image, ImageDraw, ImageFont
import datetime, json, os

# =================================
# DATE (from GitHub workflow)
# =================================
run_date = os.environ.get("RUN_DATE")
if not run_date:
    raise RuntimeError("RUN_DATE not set")

now = datetime.datetime.strptime(run_date, "%Y-%m-%d")

# =================================
# LOAD DATA
# =================================
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

def load_font(size):
    return ImageFont.truetype("DejaVuSans.ttf", size)

def autoscale(draw, text, max_width, start):
    size = start
    while size > 30:
        font = load_font(size)
        if draw.textbbox((0,0), text, font=font)[2] <= max_width:
            return font
        size -= 5
    return load_font(30)

def generate_image():
    mm = f"{now.month:02d}"
    dd = f"{now.day:02d}"
    key = f"{mm}-{dd}"

    date_text = f"{WEEKDAYS[now.weekday()]} {int(dd)} {MONTHS[int(mm)]}"
    item = DB.get(key, {"namnsdag": [], "temadag": []})

    namn = " & ".join(item.get("namnsdag", []))
    namn_text = f"Namnsdag: {namn}"

    img = Image.new("RGB", (1920, 1080), "#4169E1")
    draw = ImageDraw.Draw(img)
    cx = 960

    FONT_DATE = load_font(100)
    FONT_NAME = autoscale(draw, namn_text, 1100, 150)

    height_total = 320
    y = (1080 - height_total) // 2

    draw.ellipse((360, 120, 1560, 960), fill="#5FA8FF", outline="white", width=10)

    w = draw.textbbox((0,0), date_text, font=FONT_DATE)[2]
    draw.text((cx - w//2, y), date_text, fill="white", font=FONT_DATE)

    y += 150
    w = draw.textbbox((0,0), namn_text, font=FONT_NAME)[2]
    draw.text((cx - w//2, y), namn_text, fill="white", font=FONT_NAME)

    version = now.strftime("%Y%m%d")
    img.save(f"namnsdag-2026_v{version}.png")

if __name__ == "__main__":
    generate_image()
