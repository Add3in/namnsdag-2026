from PIL import Image, ImageDraw, ImageFont
import datetime, json, os

# ===== Datum från workflow =====
run_date = os.environ.get("RUN_DATE")
now = datetime.datetime.strptime(run_date, "%Y-%m-%d")

# ===== Data =====
with open("full.json", "r", encoding="utf-8") as f:
    DB = json.load(f)

MONTHS = ["", "januari", "februari", "mars", "april", "maj", "juni",
          "juli", "augusti", "september", "oktober", "november", "december"]

WEEKDAYS = ["Måndag", "Tisdag", "Onsdag",
            "Torsdag", "Fredag", "Lördag", "Söndag"]

# ===== Fonts =====
def load_font(size):
    return ImageFont.truetype("DejaVuSans.ttf", size)

# ===== Bild =====
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

    # Cirkel
    draw.ellipse((360, 120, 1560, 960), fill="#5FA8FF", outline="white", width=10)

    font_date = load_font(100)
    font_name = load_font(70)

    # ✅ KORREKT MÄTNING AV TEXT
    w_date, h_date = draw.textbbox((0,0), date_text, font=font_date)[2:4]
    w_name, h_name = draw.textbbox((0,0), namn_text, font=font_name)[2:4]

    center_x = 960
    center_y = 540

    draw.text(
        (center_x - w_date//2, center_y - 80),
        date_text,
        fill="white",
        font=font_date
    )

    draw.text(
        (center_x - w_name//2, center_y + 20),
        namn_text,
        fill="white",
        font=font_name
    )

    version = now.strftime("%Y%m%d")
    img.save(f"namnsdag-2026_v{version}.png")

if __name__ == "__main__":
    generate_image()
