# Friends Birthday Reminder

A Python script that creates recurring Google Calendar events for your friends' birthdays, with email and popup reminders.

## Setup

1. **Install dependencies** (requires Python >= 3.14 and [uv](https://docs.astral.sh/uv/)):
   ```bash
   uv sync
   ```

2. **Configure Google Calendar API**:
   - Create a project in the [Google Cloud Console](https://console.cloud.google.com/)
   - Enable the Google Calendar API
   - Create OAuth 2.0 credentials and download the client secrets file
   - Copy it to `config/credentials.json`:
     ```bash
     cp config/credentials.example.json config/credentials.json
     ```

3. **Prepare your data** using the example files as reference:
   ```bash
   cp data/birthdays.example.csv data/birthdays.csv
   cp data/attendees.example.csv data/attendees.csv
   ```

   `birthdays.csv` — one row per friend:
   | name | day | month | city | state |
   |------|-----|-------|------|-------|
   | Juan Perez | 15 | 3 | Lima | Lima |

   `attendees.csv` — people who receive the calendar invite:
   | name | email |
   |------|-------|
   | Juan Perez | juan@example.com |

## Usage

```bash
uv run src/app.py
```

On first run, a browser window will open for Google OAuth authorization. The token is saved to `config/token.json` for subsequent runs.
