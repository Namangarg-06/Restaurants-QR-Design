# 🌿 Olive Leaf Restaurant - Dual Link QR Code & Landing Page

Ye project **Olive Leaf Restaurant & Cafe (Vijay Nagar, Indore)** ke liye design kiya gaya hai jisme customer ek hi QR code scan karke dono options access kar sakta hai:
1. ⭐ **Google Review (5-Star Rating)**: `https://share.google/CAuKpe2Po706mPhkI`
2. 📸 **Instagram Profile**: `https://www.instagram.com/oliveleafindore`

---

## 📁 Files Overview (Aapke Folder me kya-kya hai)

1. **`index.html`**
   - Premium luxury mobile-responsive landing page.
   - Olive green + Champagne Gold theme with olive branch luxury emblem.
   - 2 clickable direct cards: Google Reviews & Instagram.
   - 1-tap call & location badge (Skye Corporate Park, Indore).

2. **`standee.html`**
   - Printable Table Tent / Standee web card.
   - Browser me open karke **Ctrl + P** press karke directly print ya PDF save kar sakte hain (A4 ya 4x6 / 5x7 inches acrylic standees ke liye).

3. **`generate_qr.py`**
   - Python script jisse aap kabhi bhi naye URL ya resolution ke sath QR code generate kar sakte hain.
   - Run command: `python generate_qr.py "Aapka_Web_Link"`

4. **Generated QR Code Images (High-Resolution 300 DPI)**:
   - `qr_code.png` / `qr_with_olive_badge.png`: Premium QR code jiske center me Olive Leaf ka emblem hai.
   - `qr_olive_leaf_luxury.png`: Olive green aur gold luxury QR code.
   - `qr_standard.png`: Crisp black & white standard QR code.
   - `table_standee_printable.png`: Ready-to-print restaurant table card.

---

## 🌐 1 Minute Me Live Kaise Karein (Free Hosting)

Kisi bhi phone ke camera se QR scan hone par page khulne ke liye, page ka ek public web link hona zaroori hota hai. Iske liye 2 sabse aasan tareeqe hain:

### Tareeqa 1: GitHub Pages (100% Free & Permanent) - Recommended
Aapka GitHub username: `namangarg-06`
1. GitHub par jaakar naya repository banayein: naam rakhein `oliveleaf`.
2. Ye saari files us repo me push kar dein (ya GitHub Desktop se publish kar dein).
3. Repo ki **Settings -> Pages** me jakar `Branch: main` select karke Save karein.
4. Aapka page turant live ho jayega is link par:
   👉 **`https://namangarg-06.github.io/oliveleaf/`**
5. Default QR code isi link ke liye generate kiya gaya hai!

### Tareeqa 2: Netlify Drop (10 Seconds, Zero Setup)
1. Browser me kholein: [app.netlify.com/drop](https://app.netlify.com/drop)
2. Is poore `QR Code` folder ko drag karke wahan chhod dein.
3. Netlify aapko turant ek live free URL de dega (jaise `oliveleaf.netlify.app`).
4. Phir agar aapko QR code update karna ho toh terminal me run karein:
   ```bash
   python generate_qr.py "https://aapka-link.netlify.app"
   ```

---

## 🖼️ Logo Kaise Badlein?

Agar aapke paas restaurant ka original image logo hai:
- Bas apni image file ko is folder me copy karein aur uska naam **`logo.png`** rakh dein.
- Page apne aap us image logo ko display karne lagega!
