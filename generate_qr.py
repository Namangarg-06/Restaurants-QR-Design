"""
QR Code & Standee Front Page Generator for Olive Leaf Restaurant
Reads settings dynamically from config.js and generates high-res QR codes & standee graphics.
"""

import sys
import os
import re
import math
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
        "footerThanks": "Thank you for dining at Olive Leaf! ✨"
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

def draw_star(draw, cx, cy, size, fill_color):
    """Draw a 5-pointed geometric star"""
    points = []
    for i in range(10):
        r = size if i % 2 == 0 else size / 2.2
        angle = i * math.pi / 5 - math.pi / 2
        points.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    draw.polygon(points, fill=fill_color)

def draw_camera_icon(draw, cx, cy, size, stroke_color):
    """Draw a vector Instagram camera outline"""
    s = size
    draw.rounded_rectangle([cx - s, cy - s, cx + s, cy + s], radius=int(s * 0.3), outline=stroke_color, width=3)
    draw.ellipse([cx - s * 0.45, cy - s * 0.45, cx + s * 0.45, cy + s * 0.45], outline=stroke_color, width=3)
    draw.ellipse([cx + s * 0.45, cy - s * 0.65, cx + s * 0.65, cy - s * 0.45], fill=stroke_color)

def create_qr_codes(custom_url=None):
    cfg = load_config()
    target_url = custom_url if custom_url else cfg["landingPageUrl"]
    
    os.makedirs("output", exist_ok=True)
    print(f"[*] Generating QR Codes for URL: {target_url}")

    # 1. Standard Crisp High-Res Black & White QR Code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=20,
        border=3,
    )
    qr.add_data(target_url)
    qr.make(fit=True)

    img_standard = qr.make_image(fill_color="black", back_color="white").convert("RGBA")
    img_standard.save("qr_standard.png", "PNG")
    print("  [+] Saved qr_standard.png")

    # 2. Branded Luxury QR Code
    qr_luxury = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=20,
        border=3,
    )
    qr_luxury.add_data(target_url)
    qr_luxury.make(fit=True)

    img_luxury = qr_luxury.make_image(
        fill_color="#12271d",
        back_color="#fdfbf5"
    ).convert("RGBA")
    img_luxury.save("qr_olive_leaf_luxury.png", "PNG")
    print("  [+] Saved qr_olive_leaf_luxury.png")

    # 3. QR Code with Official Emblem in Center
    qr_badge = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=22,
        border=4,
    )
    qr_badge.add_data(target_url)
    qr_badge.make(fit=True)
    
    qr_img = qr_badge.make_image(
        fill_color="#09140e",
        back_color="#ffffff"
    ).convert("RGBA")

    qr_w, qr_h = qr_img.size
    badge_size = int(qr_w * 0.25)
    badge_x = (qr_w - badge_size) // 2
    badge_y = (qr_h - badge_size) // 2

    if os.path.exists("logo_emblem_square.png"):
        emblem_raw = Image.open("logo_emblem_square.png").convert("RGBA")
        emblem_resized = emblem_raw.resize((badge_size, badge_size), Image.Resampling.LANCZOS)
        
        mask = Image.new("L", (badge_size, badge_size), 0)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.rounded_rectangle([0, 0, badge_size, badge_size], radius=int(badge_size * 0.22), fill=255)

        badge_box = Image.new("RGBA", (badge_size, badge_size), (0, 0, 0, 0))
        badge_box.paste(emblem_resized, (0, 0), mask)

        draw_border = ImageDraw.Draw(badge_box)
        draw_border.rounded_rectangle([1, 1, badge_size - 1, badge_size - 1], radius=int(badge_size * 0.22), outline="#d4af37", width=5)

        qr_img.paste(badge_box, (badge_x, badge_y), badge_box)

    qr_img.save("qr_with_olive_badge.png", "PNG")
    qr_img.save("qr_code.png", "PNG")
    print("  [+] Saved qr_code.png (With official Olive emblem in center)")

    # 4. Generate Table Standee Card (Front Page)
    generate_standee_card(qr_img, cfg)

def generate_standee_card(qr_img, cfg):
    w, h = 1200, 1800
    standee = Image.new("RGB", (w, h), "#08130d")
    draw = ImageDraw.Draw(standee)

    # Luxury Gold Double Border
    border_margin = 45
    draw.rectangle([border_margin, border_margin, w - border_margin, h - border_margin], outline="#d4af37", width=4)
    draw.rectangle([border_margin + 12, border_margin + 12, w - border_margin - 12, h - border_margin - 12], outline="#f7e092", width=2)

    try:
        instruction_font = ImageFont.truetype("arialbd.ttf", 46)
        sub_font = ImageFont.truetype("arial.ttf", 30)
        action_font = ImageFont.truetype("arial.ttf", 32)
        footer_font = ImageFont.truetype("arial.ttf", 26)
        thanks_font = ImageFont.truetype("arial.ttf", 32)
    except Exception:
        instruction_font = ImageFont.load_default()
        sub_font = ImageFont.load_default()
        action_font = ImageFont.load_default()
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
    inst_text = "SCAN TO CONNECT"
    ib = draw.textbbox((0, 0), inst_text, font=instruction_font)
    draw.text(((w - (ib[2] - ib[0])) // 2, 460), inst_text, fill="#ffffff", font=instruction_font)

    inst_sub = f"Review on Google  *  Follow {cfg.get('instagramUsername', '@oliveleafindore')}"
    isb = draw.textbbox((0, 0), inst_sub, font=sub_font)
    draw.text(((w - (isb[2] - isb[0])) // 2, 520), inst_sub, fill="#f7e092", font=sub_font)

    # 3. Main QR Code in White Rounded Card
    qr_card_size = 650
    qr_card_x = (w - qr_card_size) // 2
    qr_card_y = 590
    
    draw.rounded_rectangle(
        [qr_card_x, qr_card_y, qr_card_x + qr_card_size, qr_card_y + qr_card_size],
        radius=30,
        fill="#ffffff",
        outline="#d4af37",
        width=5
    )

    qr_display_size = 570
    qr_resized = qr_img.resize((qr_display_size, qr_display_size), Image.Resampling.LANCZOS)
    qr_pos_x = qr_card_x + (qr_card_size - qr_display_size) // 2
    qr_pos_y = qr_card_y + (qr_card_size - qr_display_size) // 2
    standee.paste(qr_resized, (qr_pos_x, qr_pos_y), qr_resized)

    # 4. Action Highlights Below QR (Vector Star and Camera, No Broken Boxes!)
    # Row 1: Google Review
    act1_text = "Google Review (5-Stars)"
    ab1 = draw.textbbox((0, 0), act1_text, font=action_font)
    total_w1 = (ab1[2] - ab1[0]) + 40
    start_x1 = (w - total_w1) // 2
    draw_star(draw, start_x1 + 14, 1315, 16, "#ffc107")
    draw.text((start_x1 + 40, 1300), act1_text, fill="#ffffff", font=action_font)

    # Row 2: Instagram
    act2_text = f"Follow {cfg.get('instagramUsername', '@oliveleafindore')}"
    ab2 = draw.textbbox((0, 0), act2_text, font=action_font)
    total_w2 = (ab2[2] - ab2[0]) + 40
    start_x2 = (w - total_w2) // 2
    draw_camera_icon(draw, start_x2 + 14, 1378, 13, "#f7e092")
    draw.text((start_x2 + 40, 1362), act2_text, fill="#f7e092", font=action_font)

    # 5. Footer: Location & Contact (2-Line clean address, No Truncation!)
    line1 = "Shop 9, 10 Ground Floor, Skye Corporate Park"
    l1_b = draw.textbbox((0, 0), line1, font=footer_font)
    draw.text(((w - (l1_b[2] - l1_b[0])) // 2, 1520), line1, fill="#8ca398", font=footer_font)

    line2 = "Scheme No. 78, Vijay Nagar, Indore - 452010"
    l2_b = draw.textbbox((0, 0), line2, font=footer_font)
    draw.text(((w - (l2_b[2] - l2_b[0])) // 2, 1560), line2, fill="#8ca398", font=footer_font)

    phone_text = cfg.get("phoneButtonText", "Call / Reservation: 9993896969")
    pb = draw.textbbox((0, 0), phone_text, font=footer_font)
    draw.text(((w - (pb[2] - pb[0])) // 2, 1605), phone_text, fill="#c9d8d0", font=footer_font)

    # Clean thanks text (no broken unicode sparkle)
    thanks_text = "Thank you for dining at Olive Leaf!"
    thb = draw.textbbox((0, 0), thanks_text, font=thanks_font)
    draw.text(((w - (thb[2] - thb[0])) // 2, 1660), thanks_text, fill="#d4af37", font=thanks_font)

    # Save as both files
    standee.save("table_standee_printable.png", "PNG", dpi=(300, 300))
    standee.save("front_page_standee.png", "PNG", dpi=(300, 300))
    print("  [+] Saved table_standee_printable.png & front_page_standee.png (Pixel-Perfect Front Page!)")

if __name__ == "__main__":
    url_arg = sys.argv[1] if len(sys.argv) > 1 else None
    create_qr_codes(url_arg)
