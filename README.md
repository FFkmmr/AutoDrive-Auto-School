# AutoDrive Auto School

A multilingual Django web application for an auto school — handles bookings, contact forms, and email notifications via Mailgun.

**Stack:** Python 3.11 · Django 5.2 · PostgreSQL · WhiteNoise · Gunicorn · Railway

---

## Local Development

### Prerequisites

- Python 3.11+
- Git

### Setup

```bash
# 1. Clone the repo
git clone https://github.com/FFkmmr/AutoDrive-Auto-School.git
cd AutoDrive-Auto-School

# 2. Create and activate a virtual environment
python -m venv venv

# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create your local env file
cp .env.example .env
# Edit .env and fill in your values (SECRET_KEY is required)

# 5. Apply migrations
python autoschool/manage.py migrate

# 6. Start the dev server
python autoschool/manage.py runserver
```

The app will be available at `http://127.0.0.1:8000`.

> **Note:** Set `DEBUG=1` in your `.env` for local development. Static files are served automatically in debug mode — no `collectstatic` needed.

---

## Docker (Local)

```bash
# Build the image
docker build -t autodrive .

# Run with your env file
docker run -p 8000:8000 --env-file .env autodrive
```

The app will be available at `http://localhost:8000`.

---

## Deploy to Railway

### 1. Push to GitHub

Make sure your code is pushed to GitHub.

### 2. Create a Railway project

1. Go to [railway.app](https://railway.app) and create a new project.
2. Select **Deploy from GitHub repo** and connect your repository.
3. Railway will detect the `Dockerfile` automatically.

### 3. Add a PostgreSQL database

In your Railway project, click **New** → **Database** → **PostgreSQL**. Railway will automatically inject `DATABASE_URL` into your service's environment.

### 4. Set environment variables

In the Railway service settings, add the following variables:

| Variable | Description |
|---|---|
| `SECRET_KEY` | Django secret key (generate a strong random string) |
| `DEBUG` | Set to `0` for production |
| `ALLOWED_HOSTS` | Your Railway domain, e.g. `myapp.up.railway.app` |
| `DATABASE_URL` | Injected automatically by Railway PostgreSQL |
| `MAILGUN_API_KEY` | Your Mailgun API key |
| `MAILGUN_DOMAIN` | Your Mailgun sending domain |
| `MAILGUN_FROM` | Sender address, e.g. `AutoDrive <no-reply@yourdomain.com>` |
| `MAILGUN_TO` | Recipient address(es) for form submissions |

### 5. Deploy

Railway will build the Docker image and deploy automatically on every push to your connected branch.

After the first deploy, run the initial migration via the Railway shell or a one-off command:

```bash
python autoschool/manage.py migrate
```

---

## Environment Variables Reference

Copy `.env.example` to `.env` and fill in all required values:

```
SECRET_KEY=          # Required — Django secret key
DEBUG=1              # 1 for local dev, 0 for production
DATABASE_URL=        # Optional locally (defaults to SQLite); required in production

MAILGUN_API_KEY=     # Mailgun private API key
MAILGUN_DOMAIN=      # Mailgun sending domain
MAILGUN_FROM=        # Sender display name + address
MAILGUN_TO=          # Recipient(s) for contact/booking forms
```

---

## Project Structure

```
AutoDrive-Auto-School/
├── autoschool/               # Django project root
│   ├── autoschool/           # Project config (settings, urls, wsgi)
│   ├── main/                 # Core app (home, about, booking, contact)
│   ├── mailgun/              # Email handling app
│   ├── templates/            # HTML templates
│   ├── static/               # CSS, JS, images
│   ├── locale/               # Translations (ru, ro, en)
│   └── manage.py
├── requirements.txt
├── Dockerfile
├── railway.toml
└── .env.example
```

## Languages

The site supports **Russian**, **Romanian**, and **English** via Django's i18n framework.
