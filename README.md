# Find a Tender Monitor

A small Python pipeline that watches the UK Government's
[Find a Tender](https://www.find-tender.service.gov.uk/) service for new and updated procurement notices, stores them in a local SQLite database, and emails an alert when something changes.

## How it works

1. **Fetch** — `main.py` calls the Find a Tender OCDS Release Packages API for everything updated since the last successful sync.
2. **Validate** — each release is parsed into typed [Pydantic](https://docs.pydantic.dev/) models (`dantic.py`).
3. **Deduplicate** — a content hash of the key fields (title, status, value, end date) is compared against the stored copy so unchanged notices are skipped (`utility.py`).
4. **Store** — new and changed contracts are written to `contracts db` (`db.py`), and the sync watermark is advanced.
5. **Alert** — new or updated contracts trigger an HTML email built from `templates/template.html` and sent over Gmail SMTP (`jinja.py`).

`scheduler.py` wraps the pipeline in an APScheduler job so it runs on an interval.

## Project layout

| File | Purpose |
| --- | --- |
| `main.py` | Orchestrates a single pipeline run |
| `db.py` | Database schema and setup |
| `utility.py` | Hashing, upsert logic, and sync-time tracking |
| `dantic.py` | Pydantic models for the OCDS data |
| `jinja.py` | Renders and sends the alert email |
| `scheduler.py` | Runs the pipeline on a schedule |
| `templates/` | Jinja2 email templates |

## Setup

1. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Copy the environment template and fill in your details:

   ```bash
   cp .env.example .env
   ```

   You'll need a Gmail [App Password](https://myaccount.google.com/apppasswords)
   for `passkey` (account password doesnt work w smtp, requires app password)

4. Create the database:

   ```bash
   python db.py
   ```

## Usage

Run the pipeline once:

```bash
python main.py
```

Run it on a schedule (defaults to every 3 hours):

```bash
python scheduler.py
```
