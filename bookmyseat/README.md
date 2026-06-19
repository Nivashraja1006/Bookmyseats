# 🎬 BookMySeat — Django Movie Booking App

A full-featured movie ticket booking web application inspired by BookMyShow, built with Django 3.2.

---

## ✨ Features

1. **🎬 Movie Booking System** — Browse, filter, and book movie tickets
2. **🔍 Smart Filters** — Auto-submit genre & language filters + search
3. **🪑 Seat Reservation** — Interactive seat map with 5-minute hold & countdown timer
4. **💳 Payment Processing** — Razorpay integration (test mode ready)
5. **📧 Email Notifications** — Booking confirmations via Gmail SMTP
6. **👤 User Authentication** — Email/username login, register, profile management
7. **📊 Admin Dashboard** — Real-time analytics with Chart.js (revenue, bookings, genres)
8. **🎥 Movie Trailers** — YouTube video embedding on movie detail pages

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 3.2.19, Python |
| Database | SQLite (dev) / PostgreSQL (prod) |
| Payment | Razorpay |
| Email | Gmail SMTP |
| Frontend | HTML/CSS/JavaScript, jQuery |
| Icons | Font Awesome 6 |
| Charts | Chart.js 4 |
| Fonts | Bebas Neue, DM Sans |
| Server | Gunicorn |

---

## 🚀 Quick Start (Local Development)

### 1. Clone / Extract the project

```bash
cd bookmyseat
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate       # Linux / Mac
venv\Scripts\activate          # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
# Edit .env with your Razorpay keys and Gmail credentials
```

### 5. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Seed sample data (movies, theaters, shows)

```bash
python manage.py seed_data
```

This creates:
- 8 movies (5 now showing + 3 coming soon)
- 5 theaters across Chennai & Bangalore
- Shows for the next 7 days
- Superuser: `admin@bookmyseat.com` / `admin123`

### 7. Run the development server

```bash
python manage.py runserver
```

Open **http://127.0.0.1:8000** in your browser 🎉

---

## 🔑 Admin Access

- **URL:** http://127.0.0.1:8000/admin/
- **Email:** `admin@bookmyseat.com`
- **Password:** `admin123`

**Dashboard:** http://127.0.0.1:8000/dashboard/

---

## 💳 Razorpay Setup

1. Create a free account at [razorpay.com](https://razorpay.com)
2. Go to **Settings → API Keys**
3. Generate **Test Mode** keys
4. Add to `.env`:
   ```
   RAZORPAY_KEY_ID=rzp_test_xxxxxxxxxxxx
   RAZORPAY_KEY_SECRET=xxxxxxxxxxxxxxxxxxxxxxxx
   ```

> In test mode, use card number `4111 1111 1111 1111`, any future expiry, CVV `123`

---

## 📧 Gmail SMTP Setup

1. Enable **2-Factor Authentication** on your Google account
2. Go to **Google Account → Security → App Passwords**
3. Create an app password for "Mail"
4. Add to `.env`:
   ```
   EMAIL_HOST_USER=youremail@gmail.com
   EMAIL_HOST_PASSWORD=xxxx xxxx xxxx xxxx
   ```

---

## 🗂️ Project Structure

```
bookmyseat/
├── bookmyseat/          # Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── movies/              # Movies, theaters, shows
│   ├── models.py        # Movie, Genre, Language, Theater, Show, Seat
│   ├── views.py         # Home, movie list, movie detail
│   ├── dashboard_views.py  # Admin analytics
│   ├── urls.py
│   └── management/commands/seed_data.py
├── bookings/            # Booking flow & payments
│   ├── models.py        # Booking model
│   ├── views.py         # Seat selection, Razorpay, confirmation
│   ├── utils.py         # Email sending, seat generation
│   └── urls.py
├── users/               # Authentication & profiles
│   ├── models.py        # CustomUser
│   ├── views.py
│   ├── forms.py
│   └── urls.py
├── templates/           # All HTML templates
│   ├── base.html
│   ├── movies/
│   ├── bookings/
│   ├── users/
│   └── admin_dashboard/
├── static/
│   ├── css/main.css
│   └── js/main.js
├── manage.py
├── requirements.txt
└── .env.example
```

---

## 🧪 Running with PostgreSQL

Update `.env`:
```
DATABASE_URL=postgresql://postgres:password@localhost:5432/bookmyseat
```

Create the DB:
```bash
psql -U postgres -c "CREATE DATABASE bookmyseat;"
```

---

## 🌐 Deployment (Heroku / Railway)

```bash
# Set environment variables on your platform
heroku config:set SECRET_KEY=... RAZORPAY_KEY_ID=... DATABASE_URL=...
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py seed_data
```

---

## 📸 Screenshots

| Page | Description |
|------|-------------|
| Home | Hero section, Now Showing, Coming Soon |
| Movie Detail | Poster, trailer, show times by date |
| Seat Selection | Interactive seat map with real-time pricing |
| Payment | Razorpay checkout modal |
| Confirmation | Booking ID, ticket details |
| Dashboard | Revenue charts, top movies, recent bookings |

---

## 📝 Notes

- SQLite is used by default for easy local development
- Seat generation is automatic when a show is first visited
- Holds expire after 5 minutes (configurable in `settings.py` → `SEAT_HOLD_MINUTES`)
- Email sending falls back gracefully if SMTP is not configured
