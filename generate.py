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

    center_x = 1920 // 2  # Centrerat horisontellt

    # TEXT MÅTT för centrerad layout
    _, _, w_date, h_date = draw.textbbox((0,0), date_text, font=FONT_DATE)
    _, _, w_namn, h_namn = draw.textbbox((0,0), namn_text, font=FONT_NAMN)

    if tema_text:
        _, _, w_tema, h_tema = draw.textbbox((0,0), tema_text, font=FONT_TEMA)
    else:
        w_tema, h_tema = 0, 0

    # Räkna ut totalhöjd för centrerad placering
    total_height = h_date + h_namn + h_tema + 120
    start_y = (1080 - total_height) // 2
    y = start_y

    # --- RITA CIRKEL ---
    circle_radius = 600
    circle_center = (center_x, 540)

    draw.ellipse(
        (
            circle_center[0] - circle_radius,
            circle_center[1] - circle_radius,
            circle_center[0] + circle_radius,
            circle_center[1] + circle_radius
        ),
        fill="#5FA8FF",    # Ljusblå
        outline="white",
        width=10
    )

    # --- RITA TEXT ---

    # Datum
    draw.text((center_x - w_date//2, y), date_text, fill="white", font=FONT_DATE)
    y += h_date + 40

    # Namnsdag
    draw.text((center_x - w_namn//2, y), namn_text, fill="white", font=FONT_NAMN)
    y += h_namn + 40

    # Temadag
    if tema_text:
        draw.text((center_x - w_tema//2, y), tema_text, fill="white", font=FONT_TEMA)

    # SPARA BILD
    img.save("namnsdag-2026.png")

if __name__ == "__main__":
    generate_image()
