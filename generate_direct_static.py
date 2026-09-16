"""
Generate Direct Static QR Codes for Google Reviews and Instagram,
plus Dual-QR Standee.
"""

import qrcode
from PIL import Image, ImageDraw, ImageFont

GOOGLE_URL = "https://share.google/CAuKpe2Po706mPhkI"
INSTAGRAM_URL = "https://www.instagram.com/oliveleafindore?stkn=MXduZGk2ZzU3emZjdw=="

def generate_direct_static_qrs():
    print("[*] Generating 100% Direct Static QR Codes (No hosting needed)...")

    # 1. Google Review Direct Static QR
    qr_g = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=16,
        border=3,
    )
    qr_g.add_data(GOOGLE_URL)
    qr_g.make(fit=True)
    img_google = qr_g.make_image(fill_color="#12271d", back_color="#ffffff").convert("RGBA")
    img_google.save("qr_google_direct.png", "PNG")
    print("  [+] Saved qr_google_direct.png (Direct to Google Reviews)")

    # 2. Instagram Direct Static QR
    qr_i = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=16,
        border=3,
    )
    qr_i.add_data(INSTAGRAM_URL)
    qr_i.make(fit=True)
    img_insta = qr_i.make_image(fill_color="#12271d", back_color="#ffffff").convert("RGBA")
    img_insta.save("qr_instagram_direct.png", "PNG")
    print("  [+] Saved qr_instagram_direct.png (Direct to Instagram)")

    # 3. Generate Combined Dual-QR Table Standee
    generate_dual_standee_card(img_google, img_insta)

def generate_dual_standee_card(img_google, img_insta):
    w, h = 1400, 1800
    standee = Image.new("RGB", (w, h), "#0c1812")
    draw = ImageDraw.Draw(standee)

    # Borders
    draw.rectangle([40, 40, w - 40, h - 40], outline="#d4af37", width=4)
    draw.rectangle([52, 52, w - 52, h - 52], outline="#f7e092", width=1)

    try:
        title_font = ImageFont.truetype("times.ttf", 82)
        sub_font = ImageFont.truetype("arial.ttf", 32)
        box_title_font = ImageFont.truetype("arialbd.ttf", 36)
        box_sub_font = ImageFont.truetype("arial.ttf", 26)
        footer_font = ImageFont.truetype("arial.ttf", 28)
    except Exception:
        title_font = ImageFont.load_default()
        sub_font = ImageFont.load_default()
        box_title_font = ImageFont.load_default()
        box_sub_font = ImageFont.load_default()
        footer_font = ImageFont.load_default()

    # Brand Title
    title = "OLIVE LEAF"
    tb = draw.textbbox((0, 0), title, font=title_font)
    draw.text(((w - (tb[2] - tb[0])) // 2, 140), title, fill="#f7e092", font=title_font)

    sub = "RESTAURANT & CAFE * INDORE"
    sb = draw.textbbox((0, 0), sub, font=sub_font)
    draw.text(((w - (sb[2] - sb[0])) // 2, 250), sub, fill="#c9d8d0", font=sub_font)

    tag = "PURE VEGETARIAN * FINE DINING"
    tag_b = draw.textbbox((0, 0), tag, font=box_sub_font)
    draw.text(((w - (tag_b[2] - tag_b[0])) // 2, 310), tag, fill="#d4af37", font=box_sub_font)

    # Dual Columns for Google and Instagram
    card_w, card_h = 550, 820
    y_pos = 430

    # Column 1: Google Review Card (Left)
    x_g = 110
    draw.rounded_rectangle([x_g, y_pos, x_g + card_w, y_pos + card_h], radius=24, fill="#142c20", outline="#d4af37", width=2)
    
    g_title = "RATE US 5-STARS"
    gt_b = draw.textbbox((0, 0), g_title, font=box_title_font)
    draw.text((x_g + (card_w - (gt_b[2] - gt_b[0])) // 2, y_pos + 40), g_title, fill="#ffffff", font=box_title_font)
    
    g_sub = "Google Reviews"
    gs_b = draw.textbbox((0, 0), g_sub, font=box_sub_font)
    draw.text((x_g + (card_w - (gs_b[2] - gs_b[0])) // 2, y_pos + 95), g_sub, fill="#f7e092", font=box_sub_font)

    # Google QR box
    qr_box_size = 440
    qr_x_g = x_g + (card_w - qr_box_size) // 2
    draw.rounded_rectangle([qr_x_g, y_pos + 160, qr_x_g + qr_box_size, y_pos + 160 + qr_box_size], radius=16, fill="#ffffff")
    qr_g_resized = img_google.resize((400, 400), Image.Resampling.LANCZOS)
    standee.paste(qr_g_resized, (qr_x_g + 20, y_pos + 180), qr_g_resized)

    g_btn = "⭐ Scan For Review"
    gbtn_b = draw.textbbox((0, 0), g_btn, font=box_sub_font)
    draw.text((x_g + (card_w - (gbtn_b[2] - gbtn_b[0])) // 2, y_pos + 720), g_btn, fill="#ffffff", font=box_sub_font)

    # Column 2: Instagram Card (Right)
    x_i = 740
    draw.rounded_rectangle([x_i, y_pos, x_i + card_w, y_pos + card_h], radius=24, fill="#142c20", outline="#d4af37", width=2)

    i_title = "FOLLOW US"
    it_b = draw.textbbox((0, 0), i_title, font=box_title_font)
    draw.text((x_i + (card_w - (it_b[2] - it_b[0])) // 2, y_pos + 40), i_title, fill="#ffffff", font=box_title_font)

    i_sub = "@oliveleafindore"
    is_b = draw.textbbox((0, 0), i_sub, font=box_sub_font)
    draw.text((x_i + (card_w - (is_b[2] - is_b[0])) // 2, y_pos + 95), i_sub, fill="#f7e092", font=box_sub_font)

    # Instagram QR box
    qr_x_i = x_i + (card_w - qr_box_size) // 2
    draw.rounded_rectangle([qr_x_i, y_pos + 160, qr_x_i + qr_box_size, y_pos + 160 + qr_box_size], radius=16, fill="#ffffff")
    qr_i_resized = img_insta.resize((400, 400), Image.Resampling.LANCZOS)
    standee.paste(qr_i_resized, (qr_x_i + 20, y_pos + 180), qr_i_resized)

    i_btn = "📸 Scan For Instagram"
    ibtn_b = draw.textbbox((0, 0), i_btn, font=box_sub_font)
    draw.text((x_i + (card_w - (ibtn_b[2] - ibtn_b[0])) // 2, y_pos + 720), i_btn, fill="#ffffff", font=box_sub_font)

    # Footer
    thanks = "Thank You For Visiting Olive Leaf!"
    th_b = draw.textbbox((0, 0), thanks, font=box_title_font)
    draw.text(((w - (th_b[2] - th_b[0])) // 2, 1420), thanks, fill="#f7e092", font=box_title_font)

    loc = "Ground Floor, Skye Corporate Park, Scheme 78, Vijay Nagar, Indore"
    loc_b = draw.textbbox((0, 0), loc, font=footer_font)
    draw.text(((w - (loc_b[2] - loc_b[0])) // 2, 1500), loc, fill="#8ca398", font=footer_font)

    standee.save("standee_dual_direct_static.png", "PNG", dpi=(300, 300))
    print("  [+] Saved standee_dual_direct_static.png (Direct Dual Static QR Standee)")

if __name__ == "__main__":
    generate_direct_static_qrs()
