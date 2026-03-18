from PIL import Image, ImageDraw, ImageFont
import datetime, json

# Load namnsdag + temadagar
with open("full.json", "r", encoding="utf-8") as f:
    DB = json.load(f)

MONTHS = [
    "", "januari", "februari", "mars", "april", "maj", "juni",
    "juli", "augusti", "september", "oktober", "november", "december"
]

WEEKDAYS = [
    "Måndag", "Tisdag", "Onsdag", "Torsdag",
    "Fredag", "Lördag", "Söndag"
]

# Load fonts
def load_font(size):
    try:
        return ImageFont.truetype("DejaVuSans.ttf", size)
    except:
        return ImageFont.load_default()

FONT_DATE = load_font(100)       # Datum + veckodag
FONT_TEMA = load_font(100)       # Temadag
FONT_NAMN = load_font(150)       # Namnsdag

def generate_image():
    # Today's date
    now = datetime.datetime.now()
    mm = f"{now.month:02d}"
    dd = f"{now.day:02d}"
    key = f"{mm}-{dd}"

    # Weekday logic
    if key == "02-29":
        weekday = "Skottdagen"
    else:
        weekday = WEEKDAYS[now.weekday()]

    date_text = f"{weekday} {int(dd)} {MONTHS[int(mm)]}"

    # Get JSON data
    item = DB.get(key, {"namnsdag": [], "temadag": []})
    namn_raw = ", ".join(item.get("namnsdag", []))
    namn_text = f"Namnsdag: {namn_raw}" if namn_raw else "Namnsdag: -"

    tema_raw = ", ".join(item.get("temadag", []))
    tema_text = f"Temadag: {tema_raw}" if tema_raw else ""

    # Create image
    img = Image.new("RGB", (1920, 1080), "#001133")  # Mörkblå bakgrund
    draw = ImageDraw.Draw(img)

    # Center positions (vertikalt)
    center_x = 1920 // 2

    # TEXT MÅTT
    _, _, w_date, h_date = draw.textbbox((0,0), date_text, font=FONT_DATE)

