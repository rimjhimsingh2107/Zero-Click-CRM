"""
FastAPI Backend for Zero-Click CRM
Handles audio uploads, transcription, and CRM data extraction
"""
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import os
import tempfile
from datetime import datetime

# Import our modules
from database import db
from speech_to_text import stt
from llm_extraction import llm_extractor
from query_agent import query_agent
from email_parser import email_parser

app = FastAPI(title="Zero-Click CRM API", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== Models ====================

class TextInput(BaseModel):
    text: str
    source: str = "manual"  # email, text, manual

class QueryInput(BaseModel):
    query: str

class EmailInput(BaseModel):
    email_text: str

# ==================== Routes ====================

@app.get("/")
async def root():
    return {
        "message": "Zero-Click CRM API",
        "version": "1.0.0",
        "endpoints": {
            "upload_audio": "/upload_audio",
            "process_text": "/process_text",
            "contacts": "/contacts",
            "deals": "/deals",
            "activities": "/activities",
            "query": "/query",
            "process_email": "/process_email",
            "sample_emails": "/sample_emails"
        }
    }

@app.post("/upload_audio")
async def upload_audio(file: UploadFile = File(...)):
    """
    Upload audio file, transcribe it, and extract CRM data
    """
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_path = tmp_file.name
        
        # Transcribe audio
        print(f"Transcribing audio file: {file.filename}")
        transcription = stt.transcribe_audio(tmp_path)
        transcript_text = transcription["text"]
        
        # Extract CRM data using LLM
        print(f"Extracting CRM data from transcript...")
        crm_data = llm_extractor.extract_crm_data(transcript_text)
        
        # Generate summary
        summary = llm_extractor.generate_summary(transcript_text)
        
        # Save to database
        print(f"Saving to database...")
        
        # Create or find contact
        contact_id = None
        if crm_data.get("contact_name"):
            contact_id = db.find_or_create_contact(
                name=crm_data["contact_name"],
                company=crm_data.get("company"),
                email=crm_data.get("email"),
                phone=crm_data.get("phone")
            )
        
        # Log activity
        activity = db.create_activity(
            activity_type="call",
            transcript=transcript_text,
            summary=summary,
            contact_id=contact_id
        )
        
        # Create deal if relevant
        deal = None
        if contact_id and (crm_data.get("deal_value") or crm_data.get("next_step")):
            deal = db.create_deal(
                contact_id=contact_id,
                deal_value=crm_data.get("deal_value"),
                next_step=crm_data.get("next_step"),
                follow_up_date=crm_data.get("follow_up_date"),
                notes=crm_data.get("notes")
            )
        
        # Clean up temp file
        os.unlink(tmp_path)
        
        return {
            "success": True,
            "transcript": transcript_text,
            "summary": summary,
            "extracted_data": crm_data,
            "contact_id": contact_id,
            "activity_id": activity["id"],
            "deal_id": deal["id"] if deal else None
        }
        
    except Exception as e:
        print(f"Error processing audio: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process_text")
async def process_text(input_data: TextInput):
    """
    Process raw text (from email, manual entry, etc.) and extract CRM data
    """
    try:
        text = input_data.text
        source = input_data.source
        
        # Extract CRM data
        crm_data = llm_extractor.extract_crm_data(text)
        summary = llm_extractor.generate_summary(text)
        
        # Save to database
        contact_id = None
        if crm_data.get("contact_name"):
            contact_id = db.find_or_create_contact(
                name=crm_data["contact_name"],
                company=crm_data.get("company"),
                email=crm_data.get("email"),
                phone=crm_data.get("phone")
            )
        
        # Log activity
        activity = db.create_activity(
            activity_type=source,
            transcript=text,
            summary=summary,
            contact_id=contact_id
        )
        
        # Create deal if relevant
        deal = None
        if contact_id and (crm_data.get("deal_value") or crm_data.get("next_step")):
            deal = db.create_deal(
                contact_id=contact_id,
                deal_value=crm_data.get("deal_value"),
                next_step=crm_data.get("next_step"),
                follow_up_date=crm_data.get("follow_up_date"),
                notes=crm_data.get("notes")
            )
        
        return {
            "success": True,
            "summary": summary,
            "extracted_data": crm_data,
            "contact_id": contact_id,
            "activity_id": activity["id"],
            "deal_id": deal["id"] if deal else None
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/contacts")
async def get_contacts():
    """Get all contacts"""
    try:
        contacts = db.get_all_contacts()
        return {"contacts": contacts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/deals")
async def get_deals():
    """Get all deals"""
    try:
        deals = db.get_all_deals()
        return {"deals": deals}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/activities")
async def get_activities():
    """Get all activities"""
    try:
        activities = db.get_all_activities()
        return {"activities": activities}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process_email")
async def process_email(email_input: EmailInput):
    """
    Process email content and extract CRM data
    """
    try:
        email_text = email_input.email_text
        
        # Parse email structure
        parsed_email = email_parser.parse_email(email_text)
        
        # Use body for CRM extraction (or full text if no body)
        text_to_analyze = parsed_email.get("body") or email_text
        
        # Extract CRM data
        crm_data = llm_extractor.extract_crm_data(text_to_analyze)
        summary = llm_extractor.generate_summary(text_to_analyze)
        
        # Override email if found in parsed data
        if parsed_email.get("from_email") and not crm_data.get("email"):
            crm_data["email"] = parsed_email["from_email"]
        
        # Override contact name if found
        if parsed_email.get("from_name") and not crm_data.get("contact_name"):
            crm_data["contact_name"] = parsed_email["from_name"]
        
        # Save to database
        contact_id = None
        if crm_data.get("contact_name"):
            contact_id = db.find_or_create_contact(
                name=crm_data["contact_name"],
                company=crm_data.get("company"),
                email=crm_data.get("email"),
                phone=crm_data.get("phone")
            )
        
        # Log activity
        activity = db.create_activity(
            activity_type="email",
            transcript=text_to_analyze,
            summary=summary,
            contact_id=contact_id
        )
        
        # Create deal if relevant
        deal = None
        if contact_id and (crm_data.get("deal_value") or crm_data.get("next_step")):
            deal = db.create_deal(
                contact_id=contact_id,
                deal_value=crm_data.get("deal_value"),
                next_step=crm_data.get("next_step"),
                follow_up_date=crm_data.get("follow_up_date"),
                notes=crm_data.get("notes")
            )
        
        return {
            "success": True,
            "parsed_email": parsed_email,
            "summary": summary,
            "extracted_data": crm_data,
            "contact_id": contact_id,
            "activity_id": activity["id"],
            "deal_id": deal["id"] if deal else None
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/sample_emails")
async def get_sample_emails():
    """Get sample emails for demo purposes"""
    try:
        samples = email_parser.create_sample_emails()
        return {"samples": samples}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query")
async def natural_language_query(query_input: QueryInput):
    """
    Execute natural language query on CRM data
    Example: "Show all deals > $5000 next week"
    """
    try:
        query = query_input.query
        
        # Convert query to filters
        filters = query_agent.natural_language_to_filter(query)
        
        # Get appropriate data
        if filters.get("table") == "contacts":
            data = db.get_all_contacts()
        else:
            data = db.get_all_deals()
        
        # Apply filters
        filtered_data = query_agent.apply_filters(data, filters)
        
        return {
            "query": query,
            "filters_applied": filters,
            "results": filtered_data,
            "count": len(filtered_data)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("BACKEND_PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
