from PIL import Image, ImageDraw, ImageFont
import datetime, json
import pytz   # För svensk tid

# ✅ Svensk tidszon
TZ = pytz.timezone("Europe/Stockholm")

# ✅ Ladda JSON-databasen
with open("full.json", "r", encoding="utf-8") as f:
    DB = json.load(f)

MONTHS = ["", "januari", "februari", "mars", "april", "maj", "juni",
          "juli", "augusti", "september", "oktober", "november", "december"]

WEEKDAYS = ["Måndag", "Tisdag", "Onsdag", "Torsdag",
            "Fredag", "Lördag", "Söndag"]

def load_font(size):
    return ImageFont.truetype("DejaVuSans.ttf", size)

def autoscale_text(draw, text, max_width, start_size):
    size = start_size
    while size > 30:
        font = load_font(size)
        w = draw.textbbox((0, 0), text, font=font)[2]
        if w <= max_width:
            return font
        size -= 5
    return load_font(30)

def generate_image():
    # ✅ Svensk tid
    now = datetime.datetime.now(TZ)

    mm = f"{now.month:02d}"
    dd = f"{now.day:02d}"
    key = f"{mm}-{dd}"

    weekday = "Skottdagen" if key == "02-29" else WEEKDAYS[now.weekday()]
    date_text = f"{weekday} {int(dd)} {MONTHS[int(mm)]}"

    item = DB.get(key, {"namnsdag": [], "temadag": []})

    namn_raw = " & ".join(item.get("namnsdag", []))
    namn_text = f"Namnsdag: {namn_raw}" if namn_raw else "Namnsdag: -"

    tema_raw = " & ".join(item.get("temadag", []))
    tema_text = f"Temadag: {tema_raw}" if tema_raw else ""

    img = Image.new("RGB", (1920, 1080), "#4169E1")
    draw = ImageDraw.Draw(img)
    center_x = 1920 // 2

    FONT_DATE = load_font(100)
    FONT_NAMN = autoscale_text(draw, namn_text, 1100, 150)
    FONT_TEMA = autoscale_text(draw, tema_text, 1100, 100) if tema_text else None

    _, _, w_date, h_date = draw.textbbox((0,0), date_text, font=FONT_DATE)
    _, _, w_namn, h_namn = draw.textbbox((0,0), namn_text, font=FONT_NAMN)

    w_tema, h_tema = 0, 0
    if tema_text:
        _, _, w_tema, h_tema = draw.textbbox((0,0), tema_text, font=FONT_TEMA)

    total_height = h_date + h_namn + h_tema + 120
    y = (1080 - total_height) // 2

    circle_radius = 600
    circle_center = (center_x, 540)

    draw.ellipse(
        (circle_center[0]-circle_radius, circle_center[1]-circle_radius,
         circle_center[0]+circle_radius, circle_center[1]+circle_radius),
        fill="#5FA8FF",
        outline="white",
        width=10
    )

    draw.text((center_x - w_date//2, y), date_text, fill="white", font=FONT_DATE)
    y += h_date + 40
    draw.text((center_x - w_namn//2, y), namn_text, fill="white", font=FONT_NAMN)
    y += h_namn + 40

    if tema_text:
        draw.text((center_x - w_tema//2, y), tema_text, fill="white", font=FONT_TEMA)

    # ✅ Spara version + fallback
    version = now.strftime("%Y%m%d")

    img.save(f"namnsdag-2026_v{version}.png")
    img.save("namnsdag-2026.png")

if __name__ == "__main__":
    generate_image()
