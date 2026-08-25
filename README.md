# Zero-Click CRM

A CRM that fills itself in from voice notes, emails and meeting notes.

## Overview

Sales reps skip CRM data entry because it is tedious, and a CRM full of stale
records is worse than no CRM at all. This removes the typing step instead of
trying to make it more pleasant: you talk, forward an email, or paste notes,
and structured contacts, deals and activities appear.

## How extraction works

```
voice note ──▶ Whisper ──▶ transcript ─┐
                                       ├──▶ Claude ──▶ {contact, deal, activity} ──▶ Postgres
email / notes ─────────────────────────┘
```

Transcription runs locally through Whisper. Extraction is the part a template
or a regex cannot do: "Sarah from Acme is in for about 10k, proposal by
Monday" has to become a contact, a company, a $10,000 deal value and a Monday
follow-up, with the amount normalised out of "about 10k" and the date resolved
against the note's own timestamp. Fields that were never mentioned are left
null rather than guessed, which matters more than filling them — a confidently
invented deal value is worse than a blank one.

Records are written across three related tables rather than one flat row, so
the same contact mentioned in several calls accumulates activities instead of
duplicating.

Search runs the same idea backwards. Rather than exposing filter builders,
`query_agent.py` turns a plain-English question into SQL against that schema,
so "deals over $5k closing this week" resolves to a value predicate and a date
range without anyone touching a form.

Capture

- Voice notes, transcribed locally
- Email threads and pasted meeting notes
- Contacts, deals and activities extracted automatically

Retrieval

- Plain-English search compiled to SQL
- Dashboard that updates as new records land

## Tech Stack

Backend

- FastAPI
- Python

AI

- Whisper for speech to text
- Claude for extraction and natural-language querying

Data

- Supabase
- PostgreSQL

Frontend

- Streamlit
