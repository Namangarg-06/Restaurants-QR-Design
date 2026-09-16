"""
QR Code & Standee Front Page Generator for Olive Leaf Restaurant
- Pure solid black QR code
- Official Google & Instagram badges
- Elegant Italic Gold 'Thank You For Dining With Us 🌿'
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
        "footerThanks": "Thank You For Dining With Us 🌿"
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
    print(f"[*] Generating Solid Black QR Code for URL: {target_url}")

    # Pure Solid Black QR Code (No Center Logo, Maximum Contrast)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=20,
        border=3,
    )
    qr.add_data(target_url)
    qr.make(fit=True)

    # 100% Solid Black on White
    qr_black = qr.make_image(fill_color="black", back_color="white").convert("RGBA")
    qr_black.save("qr_standard.png", "PNG")
    qr_black.save("qr_code.png", "PNG")
    print("  [+] Saved qr_code.png (100% Solid Pure Black)")

    # Generate Standee with Solid Black QR
    generate_standee_card(qr_black, cfg)

def draw_gold_leaf(draw, cx, cy, size, fill_color):
    """Draw a luxury olive leaf branch in gold"""
    # Main leaf
    draw.polygon([
        (cx - size * 0.7, cy + size * 0.5),
        (cx - size * 0.2, cy - size * 0.3),
        (cx + size * 0.9, cy - size * 0.8),
        (cx + size * 0.4, cy + size * 0.1)
    ], fill=fill_color)
    # Smaller side leaf
    draw.polygon([
        (cx - size * 0.4, cy + size * 0.7),
        (cx - size * 0.7, cy + size * 0.2),
        (cx - size * 0.1, cy - size * 0.1),
        (cx + size * 0.1, cy + size * 0.3)
    ], fill=fill_color)
    # Stem
    draw.line([(cx - size * 0.9, cy + size * 0.85), (cx + size * 0.3, cy - size * 0.2)], fill=fill_color, width=2)

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
        sub_font = ImageFont.truetype("arial.ttf", 28)
        badge_font = ImageFont.truetype("arialbd.ttf", 26)
        footer_font = ImageFont.truetype("arial.ttf", 27)
        # Elegant Italic font for Thank You
        thanks_font = ImageFont.truetype("georgiai.ttf", 40)
    except Exception:
        instruction_font = ImageFont.load_default()
        sub_font = ImageFont.load_default()
        badge_font = ImageFont.load_default()
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
        cy = 125
        draw.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=20, fill="#ffffff", outline="#d4af37", width=3)
        standee.paste(logo_resized, (cx + card_pad, cy + card_pad), logo_resized)

    # Tagline Badge
    tag_text = cfg.get("tagline", "PURE VEGETARIAN • FINE DINING").replace("*", "•")
    tb2 = draw.textbbox((0, 0), tag_text, font=sub_font)
    draw.text(((w - (tb2[2] - tb2[0])) // 2, 365), tag_text, fill="#f7e092", font=sub_font)

    # 2. Instruction Title (More breathing room)
    inst_text = "SCAN TO CONNECT"
    ib = draw.textbbox((0, 0), inst_text, font=instruction_font)
    draw.text(((w - (ib[2] - ib[0])) // 2, 435), inst_text, fill="#ffffff", font=instruction_font)

    # 3. Google Logo & Instagram Logo Pill Badges (Generous top & bottom space)
    g_badge_w, g_badge_h = 400, 62
    i_badge_w, i_badge_h = 430, 62
    gap = 26
    total_badges_w = g_badge_w + i_badge_w + gap
    start_badges_x = (w - total_badges_w) // 2
    badges_y = 515

    # Badge 1: Google
    draw.rounded_rectangle(
        [start_badges_x, badges_y, start_badges_x + g_badge_w, badges_y + g_badge_h],
        radius=31, fill="#0f251a", outline="#d4af37", width=2
    )
    if os.path.exists("google_icon.png"):
        g_ico = Image.open("google_icon.png").convert("RGBA").resize((40, 40), Image.Resampling.LANCZOS)
        standee.paste(g_ico, (start_badges_x + 16, badges_y + 11), g_ico)
    g_text = "Rate Us on Google"
    draw.text((start_badges_x + 72, badges_y + 16), g_text, fill="#ffffff", font=badge_font)

    # Badge 2: Instagram
    insta_x = start_badges_x + g_badge_w + gap
    draw.rounded_rectangle(
        [insta_x, badges_y, insta_x + i_badge_w, badges_y + i_badge_h],
        radius=31, fill="#0f251a", outline="#d4af37", width=2
    )
    if os.path.exists("instagram_icon.png"):
        i_ico = Image.open("instagram_icon.png").convert("RGBA").resize((40, 40), Image.Resampling.LANCZOS)
        standee.paste(i_ico, (insta_x + 16, badges_y + 11), i_ico)
    i_text = "Follow Us on Instagram"
    draw.text((insta_x + 72, badges_y + 16), i_text, fill="#ffffff", font=badge_font)

    # 4. Main Solid Black QR Code Card (50px spacing below badges)
    qr_card_size = 710
    qr_card_x = (w - qr_card_size) // 2
    qr_card_y = 630
    
    draw.rounded_rectangle(
        [qr_card_x, qr_card_y, qr_card_x + qr_card_size, qr_card_y + qr_card_size],
        radius=30,
        fill="#ffffff",
        outline="#d4af37",
        width=5
    )

    qr_display_size = 630
    qr_resized = qr_img.resize((qr_display_size, qr_display_size), Image.Resampling.LANCZOS)
    qr_pos_x = qr_card_x + (qr_card_size - qr_display_size) // 2
    qr_pos_y = qr_card_y + (qr_card_size - qr_display_size) // 2
    standee.paste(qr_resized, (qr_pos_x, qr_pos_y), qr_resized)

    # 5. Footer: Location & Contact
    line1 = "Shop 9, 10 Ground Floor, Skye Corporate Park"
    l1_b = draw.textbbox((0, 0), line1, font=footer_font)
    draw.text(((w - (l1_b[2] - l1_b[0])) // 2, 1445), line1, fill="#8ca398", font=footer_font)

    line2 = "Scheme No. 78, Vijay Nagar, Indore - 452010"
    l2_b = draw.textbbox((0, 0), line2, font=footer_font)
    draw.text(((w - (l2_b[2] - l2_b[0])) // 2, 1490), line2, fill="#8ca398", font=footer_font)

    phone_text = cfg.get("phoneButtonText", "Call / Reservation: 9993896969")
    pb = draw.textbbox((0, 0), phone_text, font=footer_font)
    draw.text(((w - (pb[2] - pb[0])) // 2, 1538), phone_text, fill="#c9d8d0", font=footer_font)

    # 6. Elegant Italic Gold 'Thank You For Dining With Us 🌿'
    thanks_text = "Thank You For Dining With Us"
    thb = draw.textbbox((0, 0), thanks_text, font=thanks_font)
    text_width = thb[2] - thb[0]
    
    leaf_gap = 20
    leaf_size = 28
    total_thanks_width = text_width + leaf_gap + leaf_size
    thanks_start_x = (w - total_thanks_width) // 2
    thanks_y = 1625

    draw.text((thanks_start_x, thanks_y), thanks_text, fill="#f7e092", font=thanks_font)
    draw_gold_leaf(draw, thanks_start_x + text_width + leaf_gap + 10, thanks_y + 20, leaf_size, "#d4af37")

    # Save outputs
    standee.save("table_standee_printable.png", "PNG", dpi=(300, 300))
    standee.save("front_page_standee.png", "PNG", dpi=(300, 300))
    print("  [+] Saved table_standee_printable.png & front_page_standee.png with Solid Black QR, Logos & Italic Gold Thank You!")

if __name__ == "__main__":
    url_arg = sys.argv[1] if len(sys.argv) > 1 else None
    create_qr_codes(url_arg)
