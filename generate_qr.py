"""
QR Code & Standee Front Page Generator for Olive Leaf Restaurant
Clean QR code without center logo, and clean standee without action lines below QR.
"""

import sys
import os
import re
import qrcode
from PIL import Image, ImageDraw, ImageFont

def load_config():
    config = {
        "landingPageUrl": "https://namangarg-06.github.io/oliveleaf/",
        "restaurantName": "Olive Leaf",
        "tagline": "PURE VEGETARIAN • FINE DINING",
        "phoneNumber": "9993896969",
        "phoneButtonText": "Call / Reservation: 9993896969",
        "address": "Shop 9, 10 Ground Floor, Skye Corporate Park, Scheme No. 78, Vijay Nagar, Indore",
        "instagramUsername": "@oliveleafindore",
        "footerThanks": "Thank you for dining at Olive Leaf!"
    }
    if os.path.exists("config.js"):
        try:
            with open("config.js", "r", encoding="utf-8") as f:
                content = f.read()
            for key in config.keys():
                m = re.search(rf'{key}\s*:\s*["\']([^"\']+)["\']', content)
                if m:
                    config[key] = m.group(1)
        except Exception as e:
            print("Notice: Could not parse config.js, using defaults:", e)
    return config

def create_qr_codes(custom_url=None):
    cfg = load_config()
    target_url = custom_url if custom_url else cfg["landingPageUrl"]
    
    os.makedirs("output", exist_ok=True)
    print(f"[*] Generating QR Codes for URL: {target_url}")

    # 1. Clean Crisp Black & White QR Code (No Center Logo)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=20,
        border=3,
    )
    qr.add_data(target_url)
    qr.make(fit=True)

    img_standard = qr.make_image(fill_color="black", back_color="white").convert("RGBA")
    img_standard.save("qr_standard.png", "PNG")
    print("  [+] Saved qr_standard.png")

    # 2. Branded Luxury Green QR Code (Clean, No Logo in Center)
    qr_luxury = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=20,
        border=3,
    )
    qr_luxury.add_data(target_url)
    qr_luxury.make(fit=True)

    img_luxury = qr_luxury.make_image(
        fill_color="#10251a",
        back_color="#ffffff"
    ).convert("RGBA")
    img_luxury.save("qr_olive_leaf_luxury.png", "PNG")
    img_luxury.save("qr_code.png", "PNG")
    print("  [+] Saved qr_code.png (Clean QR Code without center logo)")

    # 3. Generate Table Standee Card (Front Page)
    generate_standee_card(img_luxury, cfg)

def generate_standee_card(qr_img, cfg):
    w, h = 1200, 1800
    standee = Image.new("RGB", (w, h), "#08130d")
    draw = ImageDraw.Draw(standee)

    # Luxury Gold Double Border
    border_margin = 45
    draw.rectangle([border_margin, border_margin, w - border_margin, h - border_margin], outline="#d4af37", width=4)
    draw.rectangle([border_margin + 12, border_margin + 12, w - border_margin - 12, h - border_margin - 12], outline="#f7e092", width=2)

    try:
        instruction_font = ImageFont.truetype("arialbd.ttf", 48)
        sub_font = ImageFont.truetype("arial.ttf", 30)
        footer_font = ImageFont.truetype("arial.ttf", 27)
        thanks_font = ImageFont.truetype("arial.ttf", 34)
    except Exception:
        instruction_font = ImageFont.load_default()
        sub_font = ImageFont.load_default()
        footer_font = ImageFont.load_default()
        thanks_font = ImageFont.load_default()

    # 1. Header: Official Logo Card
    if os.path.exists("logo.png"):
        logo = Image.open("logo.png").convert("RGBA")
        logo_w = 420
        logo_h = int(logo_w * (logo.height / logo.width))
        logo_resized = logo.resize((logo_w, logo_h), Image.Resampling.LANCZOS)
        
        card_pad = 18
        cw = logo_w + card_pad * 2
        ch = logo_h + card_pad * 2
        cx = (w - cw) // 2
        cy = 135
        draw.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=20, fill="#ffffff", outline="#d4af37", width=3)
        standee.paste(logo_resized, (cx + card_pad, cy + card_pad), logo_resized)

    # Tagline Badge
    tag_text = cfg.get("tagline", "PURE VEGETARIAN • FINE DINING").replace("*", "•")
    tb2 = draw.textbbox((0, 0), tag_text, font=sub_font)
    draw.text(((w - (tb2[2] - tb2[0])) // 2, 385), tag_text, fill="#f7e092", font=sub_font)

    # 2. Instruction Banner
    inst_text = cfg.get("standeeHeading", "SCAN TO CONNECT")
    ib = draw.textbbox((0, 0), inst_text, font=instruction_font)
    draw.text(((w - (ib[2] - ib[0])) // 2, 460), inst_text, fill="#ffffff", font=instruction_font)

    inst_sub = cfg.get("standeeSubheading", "Share Your Experience  •  Follow Our Journey")
    isb = draw.textbbox((0, 0), inst_sub, font=sub_font)
    draw.text(((w - (isb[2] - isb[0])) // 2, 525), inst_sub, fill="#f7e092", font=sub_font)

    # 3. Main QR Code in White Rounded Card (Balanced size & position)
    qr_card_size = 680
    qr_card_x = (w - qr_card_size) // 2
    qr_card_y = 600
    
    draw.rounded_rectangle(
        [qr_card_x, qr_card_y, qr_card_x + qr_card_size, qr_card_y + qr_card_size],
        radius=30,
        fill="#ffffff",
        outline="#d4af37",
        width=5
    )

    qr_display_size = 600
    qr_resized = qr_img.resize((qr_display_size, qr_display_size), Image.Resampling.LANCZOS)
    qr_pos_x = qr_card_x + (qr_card_size - qr_display_size) // 2
    qr_pos_y = qr_card_y + (qr_card_size - qr_display_size) // 2
    standee.paste(qr_resized, (qr_pos_x, qr_pos_y), qr_resized)

    # (Note: Google Review and Instagram action lines removed as requested!)

    # 4. Footer: Location & Contact
    line1 = "Shop 9, 10 Ground Floor, Skye Corporate Park"
    l1_b = draw.textbbox((0, 0), line1, font=footer_font)
    draw.text(((w - (l1_b[2] - l1_b[0])) // 2, 1430), line1, fill="#8ca398", font=footer_font)

    line2 = "Scheme No. 78, Vijay Nagar, Indore - 452010"
    l2_b = draw.textbbox((0, 0), line2, font=footer_font)
    draw.text(((w - (l2_b[2] - l2_b[0])) // 2, 1475), line2, fill="#8ca398", font=footer_font)

    phone_text = cfg.get("phoneButtonText", "Call / Reservation: 9993896969")
    pb = draw.textbbox((0, 0), phone_text, font=footer_font)
    draw.text(((w - (pb[2] - pb[0])) // 2, 1525), phone_text, fill="#c9d8d0", font=footer_font)

    # Clean thanks text
    thanks_text = "Thank you for dining at Olive Leaf!"
    thb = draw.textbbox((0, 0), thanks_text, font=thanks_font)
    draw.text(((w - (thb[2] - thb[0])) // 2, 1615), thanks_text, fill="#d4af37", font=thanks_font)

    # Save outputs
    standee.save("table_standee_printable.png", "PNG", dpi=(300, 300))
    standee.save("front_page_standee.png", "PNG", dpi=(300, 300))
    print("  [+] Saved table_standee_printable.png & front_page_standee.png (Clean Standee without subtext)")

if __name__ == "__main__":
    url_arg = sys.argv[1] if len(sys.argv) > 1 else None
    create_qr_codes(url_arg)
