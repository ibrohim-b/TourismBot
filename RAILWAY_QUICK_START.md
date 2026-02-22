# Railway Quick Setup

## One-Click Deploy (Easiest)

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template)

## Manual Setup (5 minutes)

### Step 1: Deploy Admin Panel

```bash
# Push to GitHub
git add .
git commit -m "Deploy to Railway"
git push
```

1. Go to [railway.app](https://railway.app/new)
2. Click "Deploy from GitHub repo"
3. Select your repo
4. Add variables:
   - `BOT_TOKEN` = Your bot token
   - `ADMIN_USERNAME` = admin
   - `ADMIN_PASSWORD` = your_password
   - `SESSION_SECRET_KEY` = random_string
5. Generate domain in Settings

### Step 2: Deploy Bot Worker

1. Same project → "New Service"
2. Select same repo
3. Settings → Start Command: `python start_bot.py`
4. Add variables:
   - `BOT_TOKEN` = Same token
   - `DATABASE_URL` = sqlite+aiosqlite:///./db.sqlite3

Done! 🎉

## Access

- Admin: `https://your-app.railway.app/admin`
- Bot: Search in Telegram

## Need PostgreSQL?

In your project:
1. "New" → "Database" → "PostgreSQL"
2. Railway auto-sets DATABASE_URL
3. Redeploy both services

See [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md) for details.
