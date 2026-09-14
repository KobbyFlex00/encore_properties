```markdown
# Encore Property Group Ltd — Web Platform

Production-ready web platform for **Encore Property Group Ltd**, a certified luxury real estate agency based in Accra, Ghana. The platform features an interactive luxury estate showcase, HTMX-powered property search, video-first social media listing links, automated reference code tracking, and direct client lead capture.

---

## 🌟 Live Deployment & Infrastructure

- **Production URL:** [https://encorepropertieslimited.com](https://encorepropertieslimited.com)
- **Alternative Subdomain:** [https://www.encorepropertieslimited.com](https://www.encorepropertieslimited.com)
- **Render Service:** `encore-properties.onrender.com`
- **Hosting / PaaS:** [Render](https://render.com)
- **Domain Registrar & DNS:** [Hostinger](https://hostinger.com)
- **SSL/TLS:** Automated certificate issuance via Let's Encrypt (Render Managed)

---

## 🏛️ Corporate & Regulatory Compliance

- **Company Registration:** CS214391021 (Incorporated under Companies Act, 2019 [Act 992])
- **Tax Identification Number (TIN):** C0061330159
- **Accreditation:**
  - **GREPA** (Ghana Real Estate Professionals Association) Certified Member
  - **NAR** (National Association of REALTORS®) International REALTOR®

---

## 🎨 Brand Identity & Palette

| Token | Hex Code | Visual Reference | Usage |
| :--- | :--- | :--- | :--- |
| **Lime Green** | `#22C55E` | ![#22C55E](https://via.placeholder.com/15/22C55E/000000?text=+) | Primary accent, status badges, active indicators, WhatsApp CTA |
| **Metallic Gold** | `#C5A059` | ![#C5A059](https://via.placeholder.com/15/C5A059/000000?text=+) | Brand typography, house logo elements, prices, phone CTA |
| **Pitch Dark** | `#0A0A0A` | ![#0A0A0A](https://via.placeholder.com/15/0A0A0A/000000?text=+) | Dark mode body background |
| **Card Surface** | `#141414` | ![#141414](https://via.placeholder.com/15/141414/000000?text=+) | Dark mode card background and filter containers |
| **Border Gray** | `#262626` | ![#262626](https://via.placeholder.com/15/262626/000000?text=+) | Subtle hairline borders |

---

## 🚀 Key Platform Features

- **Dynamic HTMX Search & Filter:** Instant listing search by keyword, category, location, and listing type (Sale, Rent, Short Stay, Land) with zero full-page reloads.
- **Hero Image Carousel:** Interactive luxury mansion slider with responsive touch navigation, manual slide indicators, and background auto-play powered by Alpine.js.
- **Automated Listing Identification:** Read-only auto-incrementing property reference codes (`EP-001`, `EP-002`, etc.) generated at the database model level.
- **Video-First Listing Strategy:** Mandatory social media link integration (TikTok, Instagram, YouTube) allowing users to jump straight into live video walkthroughs.
- **Lead Capture & Notifications:** Direct sales desk contact inquiries dispatched via Gmail SMTP directly to `encorepropertiesgrouplimited@gmail.com`.
- **Mobile-First UX:** Clean interface omitting redundant sticky navigation bars in favor of dedicated circular floating action buttons for WhatsApp and Direct Call.
- **Universal Multi-Platform Favicons:** Custom vector SVG logo rendered into `.ico`, `.png`, and `apple-touch-icon.png` formats with a dedicated `/favicon.ico` redirect route in Django.

---

## 🛠️ Technology Stack

- **Backend:** Python 3.11+, Django 5.x
- **Frontend Architecture:** Tailwind CSS (CDN), Alpine.js, HTMX, FontAwesome 6.5
- **Static File Handling:** WhiteNoise (configured for production compression and caching)
- **Image Processing:** Pillow (PIL)
- **Application Server:** Gunicorn
- **Database:** SQLite (Local Dev) / PostgreSQL (Production)

---

## 📂 Project Directory Structure

```text
encore_properties/
├── core/
│   ├── migrations/
│   ├── static/
│   │   ├── apple-touch-icon.png
│   │   ├── favicon-32x32.png
│   │   ├── favicon.ico
│   │   ├── favicon.png
│   │   └── favicon.svg
│   ├── templates/
│   │   ├── properties/
│   │   │   ├── partials/
│   │   │   │   └── property_grid.html
│   │   │   ├── property_detail.html
│   │   │   └── property_list.html
│   │   ├── about.html
│   │   ├── base.html
│   │   └── contact.html
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── encore_project/
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── requirements.txt
├── render.yaml (optional)
└── .gitignore

```

---

## 💻 Local Development Setup

### 1. Clone & Setup Virtual Environment

```powershell
# Clone the repository
git clone [https://github.com/](https://github.com/)<your-username>/encore_properties.git
cd encore_properties

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1   # On Windows PowerShell
# source venv/bin/activate    # On macOS/Linux

```

### 2. Install Dependencies

```bash
pip install -r requirements.txt

```

### 3. Configure Environment Variables (`.env`)

Create a `.env` file in the project root:

```ini
SECRET_KEY=django-insecure-your-local-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
EMAIL_HOST_USER=encorepropertiesgrouplimited@gmail.com
EMAIL_HOST_PASSWORD=your-google-app-password

```

### 4. Database Migrations & Superuser Setup

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

```

### 5. Generate Multi-Platform Favicon Suite

Run the automated Python generator to compile all required browser icon sizes:

```powershell
python -c @"
from PIL import Image, ImageDraw
import os

os.makedirs('core/static', exist_ok=True)
size = 512
img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

green = (34, 197, 94, 255)
gold = (197, 160, 89, 255)

draw.line([(80, 420), (80, 100)], fill=green, width=44)
draw.line([(80, 100), (420, 100)], fill=green, width=44)
draw.line([(140, 270), (270, 150), (400, 270)], fill=gold, width=38)
draw.line([(185, 260), (185, 400), (410, 400)], fill=gold, width=34)

w_size, gap = 24, 14
sx, sy = 245, 285
draw.rectangle([sx, sy, sx + w_size, sy + w_size], fill=gold)
draw.rectangle([sx + w_size + gap, sy, sx + 2*w_size + gap, sy + w_size], fill=gold)
draw.rectangle([sx, sy + w_size + gap, sx + w_size, sy + 2*w_size + gap], fill=gold)
draw.rectangle([sx + w_size + gap, sy + w_size + gap, sx + 2*w_size + gap, sy + 2*w_size + gap], fill=gold)

apple = Image.new('RGBA', (180, 180), (15, 15, 15, 255))
scaled = img.resize((145, 145), Image.Resampling.LANCZOS)
apple.paste(scaled, (18, 18), scaled)
apple.save('core/static/apple-touch-icon.png')

img.resize((96, 96), Image.Resampling.LANCZOS).save('core/static/favicon.png')
img.resize((32, 32), Image.Resampling.LANCZOS).save('core/static/favicon-32x32.png')
img.save('core/static/favicon.ico', format='ICO', sizes=[(16, 16), (32, 32), (48, 48)])
"@

```

### 6. Collect Static Assets & Run Server

```bash
python manage.py collectstatic --noinput
python manage.py runserver

```

Open `http://127.0.0.1:8000` in your web browser.

---

## 🌐 Production Deployment Configuration (Render)

### Service Settings

* **Environment:** Python 3
* **Build Command:**
```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate

```


* **Start Command:**
```bash
gunicorn encore_project.wsgi:application

```



### Required Environment Variables (Render Dashboard)

| Variable | Recommended Value |
| --- | --- |
| `PYTHON_VERSION` | `3.11.8` |
| `DEBUG` | `False` |
| `SECRET_KEY` | *(Cryptographically secure 50+ character string)* |
| `ALLOWED_HOSTS` | `.onrender.com,encorepropertieslimited.com,www.encorepropertieslimited.com` |
| `CSRF_TRUSTED_ORIGINS` | `https://encorepropertieslimited.com,https://www.encorepropertieslimited.com,https://*.onrender.com` |
| `EMAIL_HOST_USER` | `encorepropertiesgrouplimited@gmail.com` |
| `EMAIL_HOST_PASSWORD` | *(16-character Google App Password)* |

---

## 📡 Hostinger DNS Management Setup

To route live apex domain and subdomain traffic to Render:

| Type | Name / Host | Target / Value | TTL | Purpose |
| --- | --- | --- | --- | --- |
| **A** | `@` | `216.24.57.1` | `300` | Apex Domain Routing |
| **CNAME** | `www` | `encore-properties.onrender.com` | `300` | Subdomain Routing |

*Note: Remove any conflicting default Hostinger `AAAA` (IPv6) or parked domain records to ensure prompt Let's Encrypt SSL/TLS verification.*

---

## 📞 Official Corporate Contact

* **Main Lines:** 024 405 7147 / 059 918 7441 / 059 887 0757
* **Official WhatsApp:** +233 59 887 0757
* **Email:** encorepropertiesgrouplimited@gmail.com
* **Headquarters:** Accra, Greater Accra Region, Ghana
* **Socials:** [Instagram](https://www.instagram.com/encorepropertieslimited) | [TikTok](https://www.google.com/search?q=https://www.tiktok.com/%40encorepropertygroupltd) | [YouTube](https://youtube.com/@encorepropertiesltd) | [Facebook](https://www.google.com/search?q=https://www.facebook.com/profile.php%3Fid%3D100083054480577)

---

## 📄 License

Proprietary software owned by **Encore Property Group Ltd**. All rights reserved. Unauthorized reproduction, modification, distribution, or commercial exploitation is strictly prohibited under the laws of Ghana and international copyright conventions.

```

```
