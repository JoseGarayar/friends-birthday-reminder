# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Python script that reads friend birthday data from an Excel spreadsheet (`DrinkTim.xlsx`) and creates recurring yearly Google Calendar events with email/popup reminders for each friend.

## Setup & Run

```bash
# Install dependencies (requires Python >=3.14)
pip install -e .
# Or with requirements.txt
pip install -r requirements.txt

# Run the script
python src/app.py
```

Requires `credentials.json` (Google OAuth client secrets) in the project root. On first run, it opens a browser for OAuth and saves `token.json` for subsequent runs.

## Architecture

Single-file app in `src/app.py` with two functions:
- `read_excel()` — Parses `DrinkTim.xlsx` (sheet "Hoja1"), extracting name, birth day/month, city, state, and email from specific column positions (columns: 2=month, 3=day, 4=name, 5=email, 6=city, 7=state)
- `create_events()` — Handles Google OAuth, then creates a calendar event per friend with yearly recurrence and reminders

## Key Details

- Calendar events use timezone `America/Lima` and Spanish-language text
- Events recur yearly (`RRULE:FREQ=YEARLY`)
- Sensitive files (`credentials.json`, `token.json`, `DrinkTim.xlsx`) are gitignored