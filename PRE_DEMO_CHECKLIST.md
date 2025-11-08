# 🚀 Zero-Click CRM - Pre-Demo Checklist

## ✅ Setup Checklist (Do This BEFORE Demo Day!)

### 1. Environment Setup
- [ ] `.env` file created with all required keys:
  - [ ] `SUPABASE_URL` configured
  - [ ] `SUPABASE_KEY` configured  
  - [ ] `ANTHROPIC_API_KEY` or `OPENAI_API_KEY` configured
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] Whisper model downloaded (happens on first run)

### 2. Database Setup
- [ ] Supabase project created
- [ ] Database tables created (run `backend/setup_database.sql` in Supabase SQL Editor)
- [ ] Row Level Security policies enabled
- [ ] Test connection works (`python -c "from backend.database import db; print(db.get_all_contacts())"`)

### 3. Demo Data
- [ ] Demo data loaded using ONE of these methods:
  - [ ] **Option A**: Run SQL script (`demo/demo_data.sql`) in Supabase
  - [ ] **Option B**: Run Python script (`python scripts/setup_demo.py`)
- [ ] Verify data appears in dashboard (should see 3+ contacts with deals)

### 4. Voice Notes (Critical!)
- [ ] Record OR download sample voice notes:
  - [ ] `sample_enterprise.wav` - Sarah Johnson / $10K deal
  - [ ] `sample_startup.wav` - Michael Chen / $5K deal  
  - [ ] `sample_enterprise_closing.wav` - Emily Rodriguez / $15K deal
- [ ] Voice scripts available at `demo/audio/VOICE_SCRIPTS.md`
- [ ] Test one voice note upload works end-to-end

### 5. Services Running
- [ ] Backend running on port 8000
  - Test: `curl http://localhost:8000` should return API info
- [ ] Frontend running on port 8501
  - Test: Open `http://localhost:8501` in browser
- [ ] Both services responding (no errors in console)

### 6. Feature Testing
- [ ] **Voice Input**: Upload audio file → see transcript and extracted data
- [ ] **Text Input**: Paste sample email → see CRM data extracted
- [ ] **Dashboard**: Shows contacts, deals, pipeline value
- [ ] **Smart Search**: Try "Show all deals over $5000" → returns results
- [ ] **Analytics**: Shows metrics and upcoming follow-ups

### 7. Demo Preparation
- [ ] Read `DEMO_SCRIPT.md` completely
- [ ] Practice demo 2-3 times (time yourself!)
- [ ] Prepare answers to common questions (see DEMO_SCRIPT.md)
- [ ] Test on actual presentation laptop/screen
- [ ] Close unnecessary browser tabs
- [ ] Disable notifications during demo

### 8. Backup Plan
- [ ] Screenshots of working features saved
- [ ] OR screen recording of full demo flow
- [ ] Printed slide deck as fallback
- [ ] Know how to switch to backup if live demo fails

---

## 🎯 5-Minute Quick Start (Day of Demo)

```bash
# Terminal 1 - Start Backend
cd backend
python main.py

# Terminal 2 - Start Frontend
cd frontend
streamlit run app.py

# Terminal 3 - Verify
curl http://localhost:8000  # Should see API response
open http://localhost:8501   # Should open dashboard
```

---

## 🧪 Test Script (Run Before Demo)

Run through this complete flow to verify everything works:

1. **Open Dashboard**
   - [ ] See demo contacts and deals loaded
   - [ ] Pipeline value shows total (should be $30K+ with demo data)

2. **Upload Voice Note**
   - [ ] Go to Voice Input page
   - [ ] Upload `sample_enterprise.wav`
   - [ ] Click Process Audio
   - [ ] Verify transcript appears
   - [ ] Verify Sarah Johnson contact created
   - [ ] Verify $10,000 deal appears

3. **Process Sample Email**
   - [ ] Go to Text Input page
   - [ ] Click "Sample Emails" tab
   - [ ] Process first sample email
   - [ ] Verify data extracted correctly

4. **Natural Language Search**
   - [ ] Go to Smart Search page
   - [ ] Type: "Show all deals over $5000"
   - [ ] Verify filtered results appear

5. **Return to Dashboard**
   - [ ] See new entries from voice note
   - [ ] Pipeline value increased
   - [ ] Recent activities logged

**If all 5 steps work → You're ready to demo! 🎉**

---

## 🚨 Common Issues & Fixes

### Issue: "Missing SUPABASE_URL or SUPABASE_KEY"
**Fix**: Check `.env` file exists and has correct keys from Supabase dashboard

### Issue: "Error loading Whisper model"
**Fix**: First run downloads ~150MB model. Check internet connection and wait

### Issue: "API connection error" in frontend
**Fix**: Ensure backend is running on port 8000 before starting frontend

### Issue: "Table not found" errors
**Fix**: Run `backend/setup_database.sql` in Supabase SQL Editor

### Issue: Voice transcription very slow
**Fix**: Whisper "base" model is loaded. First transcription may be slow (~5-10s)

### Issue: No demo data visible
**Fix**: Run `python scripts/setup_demo.py` or load `demo/demo_data.sql` manually

### Issue: LLM extraction fails
**Fix**: Check API key is valid for Anthropic/OpenAI in `.env` file

---

## 📊 Demo Day Checklist

**30 minutes before:**
- [ ] Services running and tested
- [ ] Demo data loaded
- [ ] Voice files ready
- [ ] Browser ready (single tab)
- [ ] Demo script handy

**10 minutes before:**
- [ ] Close everything except browser
- [ ] Disable notifications
- [ ] Test audio/screen sharing (if virtual)
- [ ] Have backup plan ready

**Right before demo:**
- [ ] Refresh dashboard (F5)
- [ ] Take deep breath
- [ ] Remember: Show confidence!

---

## 🎯 Success Criteria

Your demo is successful if:
- ✅ Voice-to-CRM flow works smoothly
- ✅ Data appears in dashboard automatically
- ✅ Natural language search demonstrates value
- ✅ Audience says "wow" or asks "when can we use this?"
- ✅ You get follow-up questions/meetings

---

## 💡 Pro Tips

1. **Start with impact**: "We solve a $10K/year problem per sales rep"
2. **Let the tech speak**: Don't over-explain, show the magic
3. **Have energy**: Your enthusiasm is contagious
4. **Know your fallback**: If something breaks, pivot smoothly
5. **End strong**: "This works. Ready to scale. Let's talk next steps."

---

## 📞 Emergency Contacts

If you need help during setup:
- Check `README.md` for troubleshooting
- Review `DEMO_SCRIPT.md` for demo flow
- Test on a fresh browser if issues occur

---

**You've got this! The tech works, the demo is killer, and you're going to crush it! 🚀**

*Last updated: For November 2025 Hackathon*
