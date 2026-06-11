# 🤖 Telegram Group Management Bot

A full-featured, async Telegram group management bot built with **python-telegram-bot v21+**, **SQLAlchemy 2 ORM**, and support for both **PostgreSQL** and **SQLite**.

---

## ✨ Features

| Category | Commands / Capabilities |
|---|---|
| 🔨 **Moderation** | `/ban`, `/tban`, `/unban`, `/kick`, `/mute`, `/tmute`, `/unmute` |
| ⚠️ **Warnings** | `/warn`, `/unwarn`, `/resetwarns`, `/warns` — auto-ban at limit |
| 🛡 **Anti-Spam** | Anti-flood, anti-link, anti-invite — auto-mute flooder |
| 🔤 **Word Filter** | `/addfilter`, `/removefilter`, `/filters` — per-word action |
| 📒 **Notes** | `/note`, `/get`, `/delnote`, `/notes`, `#notename` shorthand |
| ⚙️ **Custom Commands** | `/addcmd`, `/delcmd`, `/cmds` |
| 👋 **Welcome / Goodbye** | `/setwelcome`, `/setgoodbye`, template variables |
| ✅ **Verification** | Button-click human verification, restrict until verified |
| 🔐 **Locks** | `/lock`, `/unlock`, `/locks` — 12 media types |
| 📊 **Statistics** | `/stats`, `/mystats` — message tracking per user |
| ⚙️ **Settings Panel** | `/settings` — inline toggle panel for all features |
| 📝 **Logging** | Every action logged to DB + optional Telegram channel |
| 🗄 **Database** | PostgreSQL (async) + SQLite fallback via SQLAlchemy ORM |
| 🐳 **Docker** | `Dockerfile` + `docker-compose.yml` with Postgres service |
| 🌐 **Replit** | `.replit` + `replit.nix` for one-click deployment |

---

## 🚀 Quick Start

### 1. Clone & configure

```bash
git clone <your-repo>
cd tgbot
cp .env.example .env
# Edit .env and set BOT_TOKEN and OWNER_ID
```

### 2. Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run

```bash
python main.py
```

The bot will auto-create all database tables on first launch.

---

## ⚙️ Configuration (`.env`)

| Variable | Required | Description |
|---|---|---|
| `BOT_TOKEN` | ✅ | From [@BotFather](https://t.me/BotFather) |
| `OWNER_ID` | ✅ | Your Telegram user ID |
| `DATABASE_URL` | — | Default: `sqlite+aiosqlite:///./tgbot.db` |
| `SUDO_USERS` | — | Comma-separated extra admin IDs |
| `LOG_CHANNEL_ID` | — | Channel/group ID for action logs |
| `WARN_LIMIT` | — | Warnings before auto-ban (default: 3) |
| `FLOOD_MAX_MESSAGES` | — | Messages per window before flood (default: 10) |
| `FLOOD_WINDOW_SECONDS` | — | Flood window in seconds (default: 10) |
| `WELCOME_MESSAGE` | — | Default welcome template |
| `GOODBYE_MESSAGE` | — | Default goodbye template |
| `WEBHOOK_URL` | — | Set to enable webhook mode |
| `WEBHOOK_PORT` | — | Webhook port (default: 8443) |

### Welcome variables

`{mention}`, `{name}`, `{username}`, `{chat}`, `{id}`

---

## 🐳 Docker Deployment

### With SQLite (simplest)

```bash
cp .env.example .env
# Set BOT_TOKEN and OWNER_ID in .env
docker build -t tgbot .
docker run --env-file .env -v $(pwd)/data:/app tgbot
```

### With PostgreSQL (recommended for production)

```bash
cp .env.example .env
# Add these to .env:
# DATABASE_URL=postgresql+asyncpg://botuser:botpassword@postgres:5432/tgbot
# POSTGRES_USER=botuser
# POSTGRES_PASSWORD=botpassword
# POSTGRES_DB=tgbot

docker-compose up -d
```

---

## 🌐 Replit Deployment

1. Create a new **Python** Repl
2. Upload all files or connect your GitHub repo
3. In **Secrets** (padlock icon), add:
   - `BOT_TOKEN` = your token
   - `OWNER_ID` = your user ID
   - `DATABASE_URL` = `sqlite+aiosqlite:///./tgbot.db` (or your Postgres URL)
4. Click **Run**

For the bot to stay alive on Replit Free, use a service like [UptimeRobot](https://uptimerobot.com) to ping your Repl URL every 5 minutes. Set `WEBHOOK_URL` to your Repl's public URL if using webhooks.

---

## 🗄 Database

The bot uses **SQLAlchemy 2 async ORM** and auto-creates tables on start.

### Switch to PostgreSQL

```
DATABASE_URL=postgresql+asyncpg://user:password@host:5432/dbname
```

### Run Alembic migrations (optional, for schema changes)

```bash
alembic revision --autogenerate -m "describe change"
alembic upgrade head
```

---

## 📁 Project Structure

```
tgbot/
├── main.py                     # Entry point
├── requirements.txt
├── .env.example
├── Dockerfile
├── docker-compose.yml
├── alembic.ini
├── alembic/
│   ├── env.py
│   └── script.py.mako
└── bot/
    ├── config.py               # Settings from .env
    ├── handlers/
    │   ├── __init__.py         # register_all()
    │   ├── start.py            # /start, /help
    │   ├── moderation.py       # ban/kick/mute/warn
    │   ├── antispam.py         # flood/link/invite/filter
    │   ├── welcome.py          # welcome/goodbye/verify
    │   ├── notes.py            # notes + custom commands
    │   ├── filters.py          # word filter management
    │   ├── locks.py            # media locks
    │   ├── stats.py            # statistics
    │   └── settings_panel.py   # inline settings
    ├── middlewares/
    │   └── flood.py            # sliding-window flood control
    ├── models/
    │   ├── base.py             # ORM models
    │   └── db.py               # engine, session, init_db
    └── utils/
        ├── helpers.py          # shared utilities
        ├── logger.py           # action logging
        └── settings.py         # chat settings CRUD
```

---

## 🔒 Bot Permissions Required

In BotFather, disable **privacy mode** (`/setprivacy → Disable`) so the bot can read all messages. The bot also needs these admin rights in your group:

- Delete messages
- Ban users
- Restrict members
- Read messages (privacy mode off)

---

## 📜 Commands Reference

```
/start          — Info and help menu
/help           — Categorised help

/ban            — Ban a user
/tban           — Temporarily ban (e.g. /tban @user 2h spam)
/unban          — Unban
/kick           — Kick (ban + unban)
/mute           — Mute
/tmute          — Temporarily mute
/unmute         — Unmute
/warn           — Warn (auto-ban at limit)
/unwarn         — Remove one warning
/resetwarns     — Reset all warnings
/warns          — Show warnings

/lock <type>    — Lock media type
/unlock <type>  — Unlock media type
/locks          — Show all lock statuses

/addfilter <word> [action]  — Add word filter
/removefilter <word>        — Remove filter
/filters                    — List filters

/note <name> <content>  — Save a note
/get <name>             — Retrieve a note
/delnote <name>         — Delete a note
/notes                  — List all notes

/addcmd <cmd> <response>  — Add custom command
/delcmd <cmd>             — Delete custom command
/cmds                     — List custom commands

/setwelcome <msg>   — Set welcome message
/setgoodbye <msg>   — Set goodbye message
/welcome            — Toggle welcome on/off

/stats      — Group message statistics
/mystats    — Your personal stats

/settings   — Inline settings panel (admins only)
```

---

## 🤝 Contributing

Pull requests are welcome. For major changes, open an issue first.

## 📄 License

MIT
