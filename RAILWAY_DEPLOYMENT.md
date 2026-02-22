# Railway Deployment Guide

Deploy your Tourism Bot on Railway in minutes.

## Quick Start

### 1. Prerequisites
- [Railway account](https://railway.app) (free tier: $5 credit/month)
- Telegram Bot Token from [@BotFather](https://t.me/botfather)
- Git repository (GitHub recommended)

### 2. Deploy Web Admin

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Deploy to Railway"
   git push origin main
   ```

2. **Create Railway Project**
   - Go to [railway.app](https://railway.app)
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway auto-detects Python and deploys

3. **Add Environment Variables**
   - Go to your service → Variables tab
   - Add:
     ```
     BOT_TOKEN=your_bot_token_here
     DATABASE_URL=sqlite+aiosqlite:///./db.sqlite3
     ADMIN_USERNAME=admin
     ADMIN_PASSWORD=your_secure_password
     SESSION_SECRET_KEY=generate_random_string_here
     PORT=8000
     ```

4. **Generate Domain**
   - Settings tab → Generate Domain
   - Access admin at: `https://your-app.railway.app/admin`

### 3. Deploy Telegram Bot Worker

1. **Add New Service**
   - In same project, click "New" → "GitHub Repo"
   - Select same repository
   - Name it "tourism-bot-worker"

2. **Configure Start Command**
   - Settings → Start Command: `python bot/main.py`

3. **Add Environment Variables**
   ```
   BOT_TOKEN=your_bot_token_here
   DATABASE_URL=sqlite+aiosqlite:///./db.sqlite3
   ```

## Database Options

### SQLite (Current - Simple)
- ✅ Easy setup, no configuration
- ⚠️ Data persists but limited to 1GB on Railway
- Good for small to medium usage

### PostgreSQL (Recommended for Production)

1. **Add PostgreSQL**
   - Click "New" → "Database" → "Add PostgreSQL"
   - Railway auto-creates DATABASE_URL

2. **Update Requirements**
   Add to `requirements.txt`:
   ```
   asyncpg==0.29.0
   psycopg2-binary==2.9.9
   ```

3. **Update DATABASE_URL**
   Replace in both services:
   ```
   postgresql+asyncpg://user:pass@host:port/db
   ```

## Environment Variables Reference

| Variable | Required | Description |
|----------|----------|-------------|
| BOT_TOKEN | Yes | Telegram bot token from BotFather |
| DATABASE_URL | Yes | Database connection string |
| ADMIN_USERNAME | Yes | Admin panel username |
| ADMIN_PASSWORD | Yes | Admin panel password |
| SESSION_SECRET_KEY | Yes | Random string for sessions |
| PORT | Auto | Railway sets automatically |

## Project Structure on Railway

```
Project: tourism-bot
├── Service 1: tourism-bot-admin (Web)
│   └── Start: python web/run_admin.py
└── Service 2: tourism-bot-worker (Worker)
    └── Start: python bot/main.py
```

## Post-Deployment

1. **Access Admin Panel**
   - URL: `https://your-app.railway.app/admin`
   - Login with ADMIN_USERNAME/ADMIN_PASSWORD

2. **Test Bot**
   - Open Telegram → Find your bot
   - Send `/start`

3. **Monitor Logs**
   - Railway Dashboard → Service → Deployments → View Logs

## Troubleshooting

**Bot not responding:**
- Check worker service logs
- Verify BOT_TOKEN is correct
- Ensure worker service is deployed

**Admin panel 502 error:**
- Check web service logs
- Verify PORT is not hardcoded
- Check if service is running

**Database errors:**
- Verify DATABASE_URL format
- Check database service is running
- Review migration logs

## Cost Optimization

Railway free tier includes:
- $5 credit/month
- ~500 hours of usage
- 1GB storage

Tips:
- Use 1 project for both services (shares resources)
- Monitor usage in dashboard
- Upgrade to Hobby plan ($5/month) if needed

## Advantages of Railway

✅ Automatic HTTPS
✅ Zero-config deployments
✅ Built-in PostgreSQL
✅ Easy environment variables
✅ Great free tier
✅ Simple pricing

## Support

- Railway Docs: [docs.railway.app](https://docs.railway.app)
- Railway Discord: [discord.gg/railway](https://discord.gg/railway)
- Project Docs: See `docs/` folder
