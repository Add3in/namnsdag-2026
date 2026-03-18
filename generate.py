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

# Font loader
def load_font(size):
    try:
        return ImageFont.truetype("DejaVuSans.ttf", size)
    except:
        return ImageFont.load_default()

# Auto-scale function for any text
def autoscale_text(draw, text, max_width, start_size):
    size = start_size
    while size > 30:  # Minsta tillåtna textstorlek
        font = load_font(size)
        w = draw.textbbox((0,0), text, font=font)[2]
        if w <= max_width:
            return font
        size -= 5
    return load_font(30)

def generate_image():
    now = datetime.datetime.now()
    mm = f"{now.month:02d}"
    dd = f"{now.day:02d}"
    key = f"{mm}-{dd}"

    # Weekday
    if key == "02-29":
        weekday = "Skottdagen"
    else:
        weekday = WEEKDAYS[now.weekday()]

    date_text = f"{weekday} {int(dd)} {MONTHS[int(mm)]}"

    # JSON-data
    item = DB.get(key, {"namnsdag": [], "temadag": []})
    namn_raw = ", ".join(item.get("namnsdag", []))
    namn_text = f"Namnsdag: {namn_raw}" if namn_raw else "Namnsdag: -"

    tema_raw = ", ".join(item.get("temadag", []))
    tema_text = f"Temadag: {tema_raw}" if tema_raw else ""

    # Create image
    img = Image.new("RGB", (1920, 1080), "#001133")  # Mörkblå bakgrund
    draw = ImageDraw.Draw(img)

    center_x = 1920 // 2

    # Datum-storlek är fast
    FONT_DATE = load_font(100)

    # Autoskalning så texten hamnar inne i cirkeln (1100 px bred)
    max_width = 1100

    FONT_NAMN = autoscale_text(draw, namn_text, max_width, 150)
    FONT_TEMA = autoscale_text(draw, tema_text, max_width, 100) if tema_text else None

    # Textmått
    _, _, w_date, h_date = draw.textbbox((0,0), date_text, font=FONT_DATE)
    _, _, w_namn, h_namn = draw.textbbox((0,0), namn_text, font=FONT_NAMN)

    if tema_text:
        _, _, w_tema, h_tema = draw.textbbox((0,0), tema_text, font=FONT_TEMA)
    else:
        w_tema, h_tema = 0, 0

    # Total höjd
    total_height = h_date + h_namn + h_tema + 120
    start_y = (1080 - total_height) // 2
    y = start_y

    # Cirkel
    circle_radius = 600
    circle_center = (center_x, 540)

    draw.ellipse(
        (
            circle_center[0] - circle_radius,
            circle_center[1] - circle_radius,
            circle_center[0] + circle_radius,
            circle_center[1] + circle_radius
        ),
        fill="#5FA8FF",
        outline="white",
        width=10
    )

    # Datum
    draw.text((center_x - w_date//2, y), date_text, fill="white", font=FONT_DATE)
    y += h_date + 40

    # Namnsdag
    draw.text((center_x - w_namn//2, y), namn_text, fill="white", font=FONT_NAMN)
    y += h_namn + 40

    # Temadag
    if tema_text:
        draw.text((center_x - w_tema//2, y), tema_text, fill="white", font=FONT_TEMA)

    img.save("namnsdag-2026.png")

if __name__ == "__main__":
    generate_image()
