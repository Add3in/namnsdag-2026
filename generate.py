from PIL import Image, ImageDraw, ImageFont
import datetime, json

# Load namnsdag + temadagar
with open("full.json", "r", encoding="utf-8") as f:
    DB = json.load(f)

MONTHS = [
    "", "januari", "februari", "mars", "april", "maj", "juni",
    "juli", "augusti", "september", "oktober", "november", "december"
]

WEEKDAYS = ["Måndag","Tisdag","Onsdag","Torsdag","Fredag","Lördag","Söndag"]

# Font fallback
def load_font(size):
    try:
        return ImageFont.truetype("DejaVuSans.ttf", size)
    except:
        return ImageFont.load_default()

FONT_DATE = load_font(64)
FONT_NAME = load_font(48)
FONT_TEMA = load_font(32)

def generate_image():
    now = datetime.datetime.now()
    mm = f"{now.month:02d}"
    dd = f"{now.day:02d}"
    key = f"{mm}-{dd}"

    # Feb 29 special
    if key == "02-29":
        weekday = "Skottdagen"
    else:
        weekday = WEEKDAYS[now.weekday()]

    date_text = f"{weekday} {int(dd)} {MONTHS[int(mm)]}"

    item = DB.get(key, {"namnsdag": [], "temadag": []})

    namn = ", ".join(item.get("namnsdag", []))
    namn_text = f"Namnsdag: {namn}" if namn else "Namnsdag: -"

    tema = ", ".join(item.get("temadag", []))
    tema_text = f"Temadag: {tema}" if tema else ""

    img = Image.new("RGB", (1920,1080), "#003366")
    draw = ImageDraw.Draw(img)

    # Date
    w = draw.textbbox((0,0), date_text, font=FONT_DATE)[2]
    draw.text(((1920-w)/2, 150), date_text, fill="white", font=FONT_DATE)

    # Namnsdag
    w = draw.textbbox((0,0), namn_text, font=FONT_NAME)[2]
    draw.text(((1920-w)/2, 300), namn_text, fill="white", font=FONT_NAME)

    # Temadag
    if tema_text:
        w = draw.textbbox((0,0), tema_text, font=FONT_TEMA)[2]
        draw.text(((1920-w)/2, 450), tema_text, fill="white", font=FONT_TEMA)

    img.save("namnsdag-2026.png")

if __name__ == "__main__":
    generate_image()
