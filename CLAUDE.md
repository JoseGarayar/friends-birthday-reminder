# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Python script that reads friend birthday data from a CSV file and creates recurring yearly Google Calendar events with email/popup reminders. Attendees are managed in a separate CSV file.

## Setup & Run

```bash
# Install dependencies (requires Python >=3.14 and uv)
uv sync

# Copy example files and fill in real data
cp config/credentials.example.json config/credentials.json
cp config/token.example.json config/token.json
cp data/birthdays.example.csv data/birthdays.csv
cp data/attendees.example.csv data/attendees.csv

# Run the script
uv run src/app.py
```

On first run, it opens a browser for Google OAuth and saves the token for subsequent runs.

## Architecture

Single-file app in `src/app.py` with the following functions:
- `get_credentials()` — Handles Google OAuth flow (load/refresh/save token)
- `build_event(friend, emails)` — Builds a Google Calendar event dict for a single friend
- `create_events()` — Orchestrator: gets credentials, reads data, creates calendar events
- `read_birthdays()` — Reads `data/birthdays.csv` (columns: `name,day,month,city,state`)
- `read_attendees()` — Reads `data/attendees.csv` (columns: `name,email`)

## Project Structure

- `src/` — Application code
- `config/` — Google OAuth credentials and token (gitignored, except `*.example.*`)
- `data/` — CSV data files (gitignored, except `*.example.*`)

## Key Details

- Calendar events use timezone `America/Lima` and Spanish-language text
- Events recur yearly (`RRULE:FREQ=YEARLY`)
