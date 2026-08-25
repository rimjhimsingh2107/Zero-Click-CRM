# Zero-Click CRM

A CRM that fills itself in from voice notes, emails and meeting notes.

## Overview

Sales reps skip CRM data entry because it is tedious, and a CRM full of stale
records is worse than no CRM at all. This removes the typing step instead of
trying to make it more pleasant: you talk, forward an email, or paste notes,
and structured contacts, deals and activities appear.

Voice goes through Whisper for transcription. Claude handles the extraction,
which is the part a template cannot do — working out that "Sarah from Acme is
in for about 10k, proposal by Monday" means a contact, a company, a $10,000
deal and a Monday follow-up, without inventing fields that were never said.
Search runs the same idea backwards, turning "deals over $5k closing this
week" into SQL so nobody has to build a filter.

Capture

- Voice notes, transcribed locally
- Email threads and pasted meeting notes
- Contacts, deals and activities extracted automatically

Retrieval

- Plain-English search across the database
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
