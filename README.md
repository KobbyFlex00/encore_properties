# Encore Property Group Ltd — Web Platform

Modern, responsive web platform for a certified luxury real estate agency in Ghana. The platform features an interactive luxury estate showcase, instant property filtering via HTMX, video-first social media listing links, automated listing reference codes, and direct customer inquiry capture.

---

## 🌟 Deployment & Architecture

* **Primary Domain:** `https://encorepropertieslimited.com`
* **Subdomain:** `https://www.encorepropertieslimited.com`
* **Infrastructure:** Cloud Platform as a Service (PaaS) with automatic SSL/TLS termination
* **Routing:** Managed DNS with apex redirect and custom subdomain routing

---

## 🏛️ Regulatory & Industry Accreditation

* **Industry Affiliations:**

  * **GREPA** (Ghana Real Estate Professionals Association) Certified Member
  * **NAR** (National Association of REALTORS®) International REALTOR®
* **Incorporation:** Registered and incorporated under the Companies Act, 2019 (Act 992) in Accra, Ghana.

---

## 🎨 Brand Design Tokens

| Token             | Hex Code  | Usage                                                  |
| :---------------- | :-------- | :----------------------------------------------------- |
| **Vibrant Green** | `#22C55E` | Primary brand accents, status tags, WhatsApp CTA       |
| **Metallic Gold** | `#C5A059` | Brand typography, logos, pricing indicators, phone CTA |
| **Pitch Dark**    | `#0A0A0A` | Dark mode background surface                           |
| **Card Surface**  | `#141414` | Card containers, interactive UI backgrounds            |
| **Subtle Border** | `#262626` | UI separation lines and card borders                   |

---

## 🚀 Key Platform Features

* **Instant Search & Filtering:** HTMX-driven catalog filtering by keyword, listing category, location, and deal type (Sale, Rent, Short Stay, Land) with zero full-page reloads.
* **Hero Image Carousel:** Responsive, auto-playing luxury estate carousel with touch support, manual indicator navigation, and Alpine.js state management.
* **Automated Listing References:** Read-only, auto-incrementing reference codes (`EP-001`, `EP-002`, etc.) handled at the model layer.
* **Video-First Listing Strategy:** Integrated links to social walkthroughs (Instagram, TikTok, YouTube) directly from property preview cards.
* **Inquiry Notification System:** Direct customer inquiry dispatch via Django email backends.
* **Optimized Mobile Interface:** Clean, focused viewport that prioritizes listing visibility and floating contact buttons for one-touch communications.
* **Universal Multi-Format Favicon Suite:** Native support for `.ico`, `.png`, and `apple-touch-icon.png` with direct `/favicon.ico` route resolution in Django.

---

## 🛠️ Technology Stack

* **Backend:** Python 3.11+, Django 5.x
* **Frontend Architecture:** Tailwind CSS, Alpine.js, HTMX, FontAwesome 6.5
* **Static Assets:** WhiteNoise (configured for production compression and caching)
* **Image Processing:** Pillow (PIL)
* **WSGI Server:** Gunicorn
* **Database:** SQLite (Development) / PostgreSQL (Production)

---

## 📂 Project Structure

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
└── .gitignore
```

---

## 💻 Local Development Setup

### 1. Clone & Environment Preparation

```bash
# Clone the repository
git clone https://github.com/<organization>/<repository>.git
cd encore_properties

# Create and activate virtual environment
python -m venv venv

# Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Linux / macOS
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Local Environment Variables (`.env`)

Create a `.env` file in the project root:

```ini
DEBUG=True
SECRET_KEY=django-insecure-development-placeholder-key
ALLOWED_HOSTS=localhost,127.0.0.1
EMAIL_HOST_USER=admin@example.com
EMAIL_HOST_PASSWORD=samplepassword
```

> **Security Note:** Never commit production `.env` files, passwords, API keys, or secret tokens to GitHub.

### 4. Database Migrations & Administration Setup

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 5. Generate Multi-Platform Favicon Suite

Run the following Python command to build standard web and mobile icons:

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

draw.rectangle(
    [sx, sy, sx + w_size, sy + w_size],
    fill=gold
)

draw.rectangle(
    [sx + w_size + gap, sy, sx + 2*w_size + gap, sy + w_size],
    fill=gold
)

draw.rectangle(
    [sx, sy + w_size + gap, sx + w_size, sy + 2*w_size + gap],
    fill=gold
)

draw.rectangle(
    [
        sx + w_size + gap,
        sy + w_size + gap,
        sx + 2*w_size + gap,
        sy + 2*w_size + gap
    ],
    fill=gold
)

apple = Image.new('RGBA', (180, 180), (15, 15, 15, 255))

scaled = img.resize(
    (145, 145),
    Image.Resampling.LANCZOS
)

apple.paste(scaled, (18, 18), scaled)

apple.save(
    'core/static/apple-touch-icon.png'
)

img.resize(
    (96, 96),
    Image.Resampling.LANCZOS
).save(
    'core/static/favicon.png'
)

img.resize(
    (32, 32),
    Image.Resampling.LANCZOS
).save(
    'core/static/favicon-32x32.png'
)

img.save(
    'core/static/favicon.ico',
    format='ICO',
    sizes=[
        (16, 16),
        (32, 32),
        (48, 48)
    ]
)
"@
```

### 6. Collect Static Assets & Run Server

```bash
python manage.py collectstatic --noinput
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000
```

to preview the local environment.

---

## 🌐 Production Deployment Configuration

### Build & Execution Commands

**Build Command:**

```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
```

**Start Command:**

```bash
gunicorn encore_project.wsgi:application
```

### Production Environment Variables

| Variable               | Description                    | Example / Recommended                               |
| :--------------------- | :----------------------------- | :-------------------------------------------------- |
| `PYTHON_VERSION`       | Runtime engine version         | `3.11.8`                                            |
| `DEBUG`                | Application environment state  | `False`                                             |
| `SECRET_KEY`           | Cryptographic signing key      | `<generate-secure-random-token>`                    |
| `ALLOWED_HOSTS`        | Permitted server domains       | `.provider.com,yourdomain.com,www.yourdomain.com`   |
| `CSRF_TRUSTED_ORIGINS` | Trusted origins for form POSTs | `https://yourdomain.com,https://www.yourdomain.com` |
| `EMAIL_HOST_USER`      | Transactional email account    | `<service-inbox>@example.com`                       |
| `EMAIL_HOST_PASSWORD`  | App-specific service token     | `<app-password>`                                    |

> **Production Security:** Use a strong, randomly generated `SECRET_KEY`, disable `DEBUG`, and store sensitive environment variables in your hosting provider's secret/environment configuration rather than in source control.

---

## 📡 DNS Configuration Template

When connecting a custom domain registrar to your cloud host:

| Record Type   | Host  | Value / Target                   | TTL   | Purpose                  |
| :------------ | :---- | :------------------------------- | :---- | :----------------------- |
| **A / ALIAS** | `@`   | `<assigned-platform-ip-or-host>` | `300` | Apex root domain routing |
| **CNAME**     | `www` | `<assigned-platform-hostname>`   | `300` | Subdomain routing        |

> Ensure unused `AAAA` (IPv6) or parking records from the domain registrar are removed where necessary so automated SSL verification and domain routing can complete successfully.

---

## 📜 License

Proprietary software owned by **Encore Property Group Ltd**. All rights reserved.

Unauthorized reproduction, modification, distribution, or commercial exploitation is strictly prohibited under applicable copyright and commercial software laws.

---

## 👨‍💻 Development

Built with:

**Django · Python · Tailwind CSS · Alpine.js · HTMX · PostgreSQL · Gunicorn**

---

## 📞 Contact

**Encore Property Group Ltd**

**Website:** https://encorepropertieslimited.com

**Production Domain:** `encorepropertieslimited.com`
