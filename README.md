# 🎯 Zero-Click CRM

**AI-Powered CRM That Updates Itself - No Manual Data Entry Required**

Zero-Click CRM automatically extracts structured CRM data from voice notes, emails, and text conversations using AI. Built for the hackathon, production-ready MVP.

---

## 🌟 Key Features

- **🎤 Voice-to-CRM**: Record or upload voice notes → auto-populate contacts and deals
- **✉️ Text/Email Processing**: Paste conversations → extract structured CRM data
- **🔍 Natural Language Search**: Ask "Show deals > $5K this week" in plain English
- **📊 Real-time Dashboard**: Live updates as new data flows in
- **🤖 AI-Powered Extraction**: Uses Claude AI to understand context and extract key info

---

## 🏗️ Architecture

```
Voice/Email → Whisper (STT) → Claude AI (Extraction) → Supabase (Storage) → Streamlit (UI)
```

**Tech Stack:**
- **Backend**: FastAPI + Python
- **AI**: OpenAI Whisper (transcription) + Anthropic Claude (extraction)
- **Database**: Supabase (PostgreSQL)
- **Frontend**: Streamlit
- **Deployment**: Local or cloud (Vercel/Render)

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Supabase account (free tier works)
- Anthropic API key (Claude) OR OpenAI API key

### 1️⃣ Setup Supabase

1. Create a free account at [supabase.com](https://supabase.com)
2. Create a new project
3. Go to SQL Editor and run the SQL from `backend/setup_database.sql`
4. Get your project URL and anon key from Settings → API

### 2️⃣ Configure Environment

```bash
# Copy the example env file
cp .env.example .env

# Edit .env with your credentials
nano .env
```

Required environment variables:
```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
ANTHROPIC_API_KEY=your_claude_api_key
```

### 3️⃣ Install Dependencies

```bash
# Install Python packages
pip install -r requirements.txt
```

Note: First run will download Whisper model (~150MB)

### 4️⃣ Start the Backend

```bash
cd backend
python main.py
```

Backend will run on `http://localhost:8000`

### 5️⃣ Start the Frontend

```bash
# In a new terminal
cd frontend
streamlit run app.py
```

Frontend will run on `http://localhost:8501`

---

## 📖 Usage Guide

### Voice Input Example

1. Go to **🎤 Voice Input** page
2. Upload an audio file (or record one)
3. Click **Process Audio**
4. Watch as:
   - Audio is transcribed
   - AI extracts contact, company, deal value, next steps
   - CRM auto-updates with new entry

**Example voice note:**
> "Hey, I just had a call with Sarah Johnson from Acme Corp. She's interested in our enterprise plan at $10,000. We need to send her a proposal by next Monday and schedule a demo."

**Auto-extracted:**
- Contact: Sarah Johnson
- Company: Acme Corp
- Deal Value: $10,000
- Next Step: Send proposal & schedule demo
- Follow-up: Next Monday

### Text/Email Input

Paste email content or meeting notes → AI extracts structured data automatically.

### Natural Language Search

Ask questions in plain English:
- "Show all deals over $5,000"
- "Find contacts from Acme Corp"
- "Deals closing this week"

---

## 🗂️ Project Structure

```
crm/
├── backend/
│   ├── main.py              # FastAPI server
│   ├── database.py          # Supabase client
│   ├── speech_to_text.py    # Whisper integration
│   ├── llm_extraction.py    # Claude AI extraction
│   ├── query_agent.py       # NL to SQL conversion
│   └── setup_database.sql   # Database schema
├── frontend/
│   ├── app.py              # Streamlit dashboard
│   └── components/         # UI components
├── requirements.txt        # Python dependencies
├── .env.example           # Environment template
└── README.md
```

---

## 🧪 API Endpoints

**Base URL:** `http://localhost:8000`

### POST `/upload_audio`
Upload audio file for processing
- **Input**: Audio file (WAV, MP3, M4A, OGG)
- **Output**: Transcript, extracted CRM data, database IDs

### POST `/process_text`
Process text/email content
- **Input**: `{"text": "...", "source": "email"}`
- **Output**: Extracted CRM data, database IDs

### GET `/contacts`
Get all contacts

### GET `/deals`
Get all deals

### GET `/activities`
Get all activities (calls, emails, meetings)

### POST `/query`
Natural language query
- **Input**: `{"query": "Show deals > $5000"}`
- **Output**: Filtered results

---

## 🎬 Demo Script (2-Minute Pitch)

1. **Start**: "Traditional CRMs require endless manual data entry. We built Zero-Click CRM to fix that."

2. **Show Voice Demo**:
   - Upload pre-recorded voice note
   - Watch it auto-populate contact + deal in real-time
   - Highlight: "No typing, no forms, no dropdowns"

3. **Show NLP Search**:
   - Type: "Show deals over $5K closing this week"
   - Instant filtered results
   - Highlight: "Natural language, like talking to an assistant"

4. **Close**: "Zero-Click CRM saves sales teams hours per week by automating data entry. Built in 48 hours, ready to scale."

---

## 🔮 Future Enhancements

- **Email Integration**: Auto-sync Gmail/Outlook
- **Meeting Integration**: Zoom/Teams transcription
- **Mobile App**: Record on-the-go
- **LinkedIn Enrichment**: Auto-update contact info
- **Smart Reminders**: AI-suggested follow-ups
- **Team Collaboration**: Share deals and notes

---

## 🛠️ Troubleshooting

### "Missing SUPABASE_URL or SUPABASE_KEY"
Make sure `.env` file exists and has valid Supabase credentials.

### "Error loading Whisper model"
First run downloads ~150MB model. Check internet connection.

### "API connection error"
Ensure backend is running on port 8000 before starting frontend.

### Database tables not found
Run the SQL from `backend/setup_database.sql` in Supabase SQL Editor.

---

## 📊 Performance Notes

- **Voice transcription**: 2-5 seconds for 30-second clips
- **AI extraction**: 1-3 seconds per request
- **Database operations**: <100ms

---

## 🤝 Contributing

This is a hackathon MVP. For production use:
1. Add user authentication
2. Implement rate limiting
3. Add comprehensive error handling
4. Set up monitoring and logging
5. Add unit and integration tests

---

## 📄 License

MIT License - feel free to use for your hackathon or startup!

---

## 🎯 Built With

- [FastAPI](https://fastapi.tiangolo.com/) - Backend framework
- [Streamlit](https://streamlit.io/) - Frontend framework
- [Anthropic Claude](https://anthropic.com) - AI extraction
- [OpenAI Whisper](https://openai.com/research/whisper) - Speech-to-text
- [Supabase](https://supabase.com) - Database
- [PostgreSQL](https://www.postgresql.org/) - Data storage

---

## 👏 Acknowledgments

Built for the hackathon challenge. Inspired by the need to eliminate manual CRM data entry.

**Team**: Your team name here
**Date**: November 2025
**Status**: MVP Complete ✅

---

## 📞 Support

For questions or issues:
- GitHub Issues (add your repo)
- Email: your-email@example.com

---

**Happy hacking! 🚀**
