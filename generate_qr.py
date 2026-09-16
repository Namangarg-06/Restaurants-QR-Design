"""
QR Code Generator for Olive Leaf Restaurant
Generates high-resolution, print-ready QR codes and branded standee graphics.
"""

import sys
import os
import qrcode
from PIL import Image, ImageDraw, ImageFont

# Default target URL (Hosted GitHub Pages or custom domain)
# You can change this URL or pass it as a command line argument: python generate_qr.py "YOUR_URL"
DEFAULT_URL = "https://namangarg-06.github.io/oliveleaf/"

def create_qr_codes(target_url=DEFAULT_URL):
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
    print("  [+] Saved qr_standard.png (High-Res 300+ DPI)")

    # 2. Branded Olive Green & Rich Gold QR Code
    # Brand Colors:
    # Olive Dark: (13, 26, 20)
    # Gold: (212, 175, 55)
    qr_luxury = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=20,
        border=3,
    )
    qr_luxury.add_data(target_url)
    qr_luxury.make(fit=True)

    img_luxury = qr_luxury.make_image(
        fill_color="#12271d",  # Deep Olive Forest
        back_color="#fdfbf5"   # Warm Cream
    ).convert("RGBA")
    img_luxury.save("qr_olive_leaf_luxury.png", "PNG")
    print("  [+] Saved qr_olive_leaf_luxury.png")

    # 3. QR Code with Center Emblem / Badge
    # Generate QR with high error correction to allow center icon
    qr_badge = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=22,
        border=4,
    )
    qr_badge.add_data(target_url)
    qr_badge.make(fit=True)
    
    qr_img = qr_badge.make_image(
        fill_color="#0e2017",
        back_color="#ffffff"
    ).convert("RGBA")

    # Draw center circle badge with 'OL' monogram & leaf
    qr_w, qr_h = qr_img.size
    badge_size = int(qr_w * 0.24)
    badge_x = (qr_w - badge_size) // 2
    badge_y = (qr_h - badge_size) // 2

    # Create badge image
    badge = Image.new("RGBA", (badge_size, badge_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(badge)
    
    # White background circle with gold border
    draw.ellipse([2, 2, badge_size - 2, badge_size - 2], fill="#12271d", outline="#d4af37", width=int(badge_size * 0.07))
    
    # Draw simple elegant leaf / monogram in center
    # Draw 'OL' text
    try:
        font = ImageFont.truetype("arial.ttf", int(badge_size * 0.38))
    except Exception:
        font = ImageFont.load_default()

    # Draw letters OL in gold
    text = "OL"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    draw.text(
        ((badge_size - text_w) // 2, (badge_size - text_h) // 2 - 2),
        text,
        fill="#f7e092",
        font=font
    )

    # Paste badge onto QR code
    qr_img.paste(badge, (badge_x, badge_y), badge)
    qr_img.save("qr_with_olive_badge.png", "PNG")
    print("  [+] Saved qr_with_olive_badge.png")

    # Also copy main qr to root as qr_code.png
    qr_img.save("qr_code.png", "PNG")
    print("  [+] Saved qr_code.png (Default for standee)")

    # 4. Generate Table Standee Card (Printable Graphic)
    generate_standee_card(qr_img)

def generate_standee_card(qr_img):
    """Creates a high-resolution printable table standee (1200 x 1800 px)"""
    w, h = 1200, 1800
    standee = Image.new("RGB", (w, h), "#0d1b14")
    draw = ImageDraw.Draw(standee)

    # Outer decorative gold border
    border_margin = 45
    draw.rectangle(
        [border_margin, border_margin, w - border_margin, h - border_margin],
        outline="#d4af37",
        width=4
    )
    draw.rectangle(
        [border_margin + 12, border_margin + 12, w - border_margin - 12, h - border_margin - 12],
        outline="#f7e092",
        width=1
    )

    # Fonts
    try:
        title_font = ImageFont.truetype("times.ttf", 76)
        sub_font = ImageFont.truetype("arial.ttf", 32)
        instruction_font = ImageFont.truetype("arialbd.ttf", 46)
        desc_font = ImageFont.truetype("arial.ttf", 28)
        footer_font = ImageFont.truetype("arial.ttf", 26)
    except Exception:
        title_font = ImageFont.load_default()
        sub_font = ImageFont.load_default()
        instruction_font = ImageFont.load_default()
        desc_font = ImageFont.load_default()
        footer_font = ImageFont.load_default()

    # 1. Header: OLIVE LEAF
    title_text = "OLIVE LEAF"
    tb = draw.textbbox((0, 0), title_text, font=title_font)
    draw.text(((w - (tb[2] - tb[0])) // 2, 160), title_text, fill="#f7e092", font=title_font)

    # Subtitle
    sub_text = "RESTAURANT & CAFE"
    sb = draw.textbbox((0, 0), sub_text, font=sub_font)
    draw.text(((w - (sb[2] - sb[0])) // 2, 260), sub_text, fill="#c9d8d0", font=sub_font)

    # Tagline badge
    tag_text = "PURE VEGETARIAN  *  FINE DINING"
    tb2 = draw.textbbox((0, 0), tag_text, font=desc_font)
    draw.text(((w - (tb2[2] - tb2[0])) // 2, 320), tag_text, fill="#d4af37", font=desc_font)

    # 2. Instruction Banner
    inst_text = "SCAN TO CONNECT"
    ib = draw.textbbox((0, 0), inst_text, font=instruction_font)
    draw.text(((w - (ib[2] - ib[0])) // 2, 420), inst_text, fill="#ffffff", font=instruction_font)

    inst_sub = "Review on Google  *  Follow on Instagram"
    isb = draw.textbbox((0, 0), inst_sub, font=desc_font)
    draw.text(((w - (isb[2] - isb[0])) // 2, 485), inst_sub, fill="#f7e092", font=desc_font)

    # 3. QR Code in White Rounded Card
    qr_card_size = 660
    qr_card_x = (w - qr_card_size) // 2
    qr_card_y = 570
    
    # White background card
    draw.rounded_rectangle(
        [qr_card_x, qr_card_y, qr_card_x + qr_card_size, qr_card_y + qr_card_size],
        radius=30,
        fill="#ffffff",
        outline="#d4af37",
        width=5
    )

    # Resize QR to fit nicely inside white card
    qr_display_size = 580
    qr_resized = qr_img.resize((qr_display_size, qr_display_size), Image.Resampling.LANCZOS)
    qr_pos_x = qr_card_x + (qr_card_size - qr_display_size) // 2
    qr_pos_y = qr_card_y + (qr_card_size - qr_display_size) // 2
    standee.paste(qr_resized, (qr_pos_x, qr_pos_y), qr_resized)

    # 4. Action Highlights Below QR
    act1 = "⭐ Google Review (5-Stars)"
    ab1 = draw.textbbox((0, 0), act1, font=desc_font)
    draw.text(((w - (ab1[2] - ab1[0])) // 2, 1310), act1, fill="#ffffff", font=desc_font)

    act2 = "📸 Follow @oliveleafindore"
    ab2 = draw.textbbox((0, 0), act2, font=desc_font)
    draw.text(((w - (ab2[2] - ab2[0])) // 2, 1370), act2, fill="#f7e092", font=desc_font)

    # 5. Footer: Location & Thank you
    loc_text = "Ground Floor, Skye Corporate Park, Vijay Nagar, Indore"
    lb = draw.textbbox((0, 0), loc_text, font=footer_font)
    draw.text(((w - (lb[2] - lb[0])) // 2, 1580), loc_text, fill="#8ca398", font=footer_font)

    thanks_text = "Thank You for Dining With Us!"
    thb = draw.textbbox((0, 0), thanks_text, font=desc_font)
    draw.text(((w - (thb[2] - thb[0])) // 2, 1640), thanks_text, fill="#d4af37", font=desc_font)

    standee.save("table_standee_printable.png", "PNG", dpi=(300, 300))
    print("  [+] Saved table_standee_printable.png (Ready to Print on A4/Standee)")

if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_URL
    create_qr_codes(url)
