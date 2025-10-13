# Fickle Ferrets API 🦦

Share words of affirmation with fickle ferrets and see if you spark joy! A FastAPI demo showing async webhook patterns with background processing and SQLite persistence.

## 🚀 Quick Start

```bash
# Install dependencies (requires uv: https://docs.astral.sh/uv/)
uv sync

# Start the server (database auto-creates on first run)
uv run python -m app.main

# View current champion phrase
curl http://localhost:8000/champion

# Send an affirmation (uses champion phrase automatically)
curl -X POST http://localhost:8000/affirmation

# View history in browser
open http://localhost:8000/affirmations/history
```

**API Docs**: http://localhost:8000/docs

## What it is

Fickle Ferrets is the hottest app that sends affirmations to our talented, but fickle ferrets, and gets a response back as to whether these words sparked joy in the ferrets or not. The app uses a "champion phrase" system - there's always a current champion affirmation stored in the database that gets sent to the ferrets.

## 📋 How It Works

1. **POST /affirmation** → Sends champion phrase to ferrets, returns immediately with affirmation ID (202 Accepted)
2. **Background**: Shares the champion phrase with ferrets via external API, waits 0-1 seconds
3. **Webhook callback**: Ferrets' reaction posted to `/webhook/ferret-reaction`
4. **Database**: Everything logged to `fickle_ferrets.db` (SQLite), including the champion phrase
5. **GET /affirmations/history** → View all past affirmations and reactions
6. **GET /champion** → View the current champion phrase

**Flow Diagram:**
```
POST /affirmation → Create DB record → Return 202 Accepted
    ↓ (background)
Call external API → Wait 0-1s → POST to webhook → Update DB
```

## 🔌 Key Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/affirmation` | Send champion phrase to ferrets, get ID back immediately (no body required) |
| `GET` | `/champion` | **View current champion phrase** |
| `GET` | `/affirmations/history?limit=50` | View all stored affirmations & results |
| `GET` | `/health` | Health check |
| `GET` | `/` | Welcome message |

### Example: View Champion Phrase

```bash
curl http://localhost:8000/champion
```

**Response:**
```json
{
  "phrase": "Whoosa good ferret!",
  "updated_at": "2025-10-11T12:00:00.000"
}
```

### Example: Send Affirmation

```bash
curl -X POST http://localhost:8000/affirmation
```

**Response:**
```json
{
  "affirmation_id": "a1b2c3d4-...",
  "message": "Your words have been shared with the ferrets! They're contemplating... 🦦"
}
```

*Note: The affirmation endpoint automatically uses the current champion phrase from the database - no request body needed!*

### Example: View History

```bash
curl http://localhost:8000/affirmations/history
```

**Response:**
```json
[
  {
    "affirmation_id": "a1b2c3d4-...",
    "words_of_affirmation": "You are amazing!",
    "joy_sparked": true,
    "created_at": "2025-10-11T12:34:56.789",
    "callback_received_at": "2025-10-11T12:35:01.234"
  }
]
```

## 🗄️ Database

**SQLite database** (`fickle_ferrets.db`) auto-creates on startup and stores:
- Current champion phrase (seeds with default on first run)
- All affirmations sent
- Ferret reactions (joy sparked or not)
- Timestamps for creation and callback

**View data:** Use the `/affirmations/history` or `/champion` endpoints (see above)

**Reset database:**
```bash
rm fickle_ferrets.db  # Will recreate on next startup with default champion phrase
```

## 📁 Project Structure

```
app/
├── main.py              # FastAPI app + DB initialization
├── api/routes.py        # All endpoints
├── schemas/models.py    # Pydantic models
├── services/ferret_service.py  # Business logic + DB operations
└── db/
    ├── base.py          # SQLAlchemy base
    ├── models.py        # DB models
    └── session.py       # DB session
```

## 🎨 Features

- ✅ **Async webhook pattern** with FastAPI BackgroundTasks
- ✅ **SQLite persistence** with SQLAlchemy 2.0
- ✅ **CLI tool** (`post_affirm` command)
- ✅ **Modular architecture** (api, schemas, services, db)
- ✅ **Type hints** throughout (Python 3.13+)
- ✅ **Interactive API docs** (Swagger UI)

## 🛠️ Development

**Install uv** (if needed):
```bash
# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Run server with auto-reload:**
```bash
uv run python -m app.main
```

**View logs in console:**
```
[DATABASE] 🗄️  Initializing SQLite database...
[DATABASE] 🏆 Champion phrase loaded: 'Whoosa good ferret!'
[AFFIRMATION] 🦦 New affirmation received! ID: a1b2c3d4-...
[AFFIRMATION] 📝 Using champion phrase: 'Whoosa good ferret!'
[FERRETS] 🤔 Ferrets are contemplating... (0.78 seconds)
[WEBHOOK] 🦦 Ferret Response: ✨ JOY SPARKED!
[DATABASE] 💾 Updated affirmation result: a1b2c3d4-... (joy=True)
```

## 📝 Notes

- Created for interview case study demonstrating FastAPI best practices
- Integrates with external Spark Joy API: `https://spark-joy.local-services.workers.dev/spark`
- All data persisted locally in SQLite (portable, can backup)
- Database file gitignored

---

**Why Fickle Ferrets?** Because simulating a real transaction was boring. 🦦
