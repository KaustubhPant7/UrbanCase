# MyStore — Django Branding & Products Site

A minimal, clean Django project for a product-showcase store with Google login, COD ordering, and WhatsApp/Instagram integration.

---

## Stack

| Layer | Choice |
|---|---|
| Framework | Django 4.2 |
| Auth | django-allauth (Google OAuth) |
| DB | SQLite (dev) / PostgreSQL (prod) |
| Styling | Bootstrap 5 + Bootstrap Icons |
| Static files | WhiteNoise |

---

## Project Structure

```
config/          # settings, urls, wsgi
core/            # homepage, banners, social links
products/        # Category + Product models
orders/          # Order model + COD form
users/           # auth (django-allauth handles it)
templates/       # all HTML templates
static/css/      # main.css
```

---

## Quick Start

```bash
# 1. Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Copy env file and fill in values
cp .env.example .env

# 4. Run migrations
python manage.py migrate

# 5. Create a superuser (for admin)
python manage.py createsuperuser

# 6. Start dev server
python manage.py runserver
```

Visit `http://127.0.0.1:8000`

---

## Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project → APIs & Services → Credentials
3. Create **OAuth 2.0 Client ID** (Web application)
4. Add authorized redirect URI:  
   `http://127.0.0.1:8000/accounts/google/login/callback/`
5. Copy **Client ID** and **Client Secret** into `.env`
6. In Django Admin → Sites → change domain to `127.0.0.1:8000`
7. In Django Admin → Social Applications → Add Google app with your credentials

---

## Admin Panel

`/admin/` — manage:
- **Categories** — add/edit product categories
- **Products** — name, price, image, stock, featured flag
- **Orders** — view orders, update status (Pending → Confirmed → Delivered)
- **Banners** — homepage hero images
- **Social Links** — Instagram URL + WhatsApp number

---

## WhatsApp Ordering Flow

1. User views a product
2. Clicks **"Order via WhatsApp"** → opens WhatsApp with pre-filled message
3. Admin confirms and optionally records the order in admin

OR use the built-in **COD form** (Order Now button) which saves to the database.

---

## Models Summary

```
Category       → name, slug, description
Product        → name, price, discount_price, image, stock, is_featured, tagline, category
Order          → product, user, qty, customer_name/phone/address, status (COD)
Banner         → title, subtitle, image, button CTA
SocialLink     → instagram_url, whatsapp_number
```
