#!/usr/bin/env python3
"""
Quick Demo Setup Script
Loads sample data and prepares the CRM for demo
"""
import os
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

try:
    from database import db
    from dotenv import load_dotenv
    
    load_dotenv()
    
    print("🎯 Zero-Click CRM Demo Setup")
    print("=" * 50)
    
    # Check database connection
    print("\n1. Checking database connection...")
    try:
        contacts = db.get_all_contacts()
        print(f"   ✅ Connected! Found {len(contacts)} existing contacts")
    except Exception as e:
        print(f"   ❌ Database connection failed: {str(e)}")
        print("\n   Please check your .env file has:")
        print("   - SUPABASE_URL")
        print("   - SUPABASE_KEY")
        sys.exit(1)
    
    print("\n2. Loading demo data...")
    print("   📝 Creating sample contacts...")
    
    # Create demo contacts with deals
    demo_data = [
        {
            "contact": {"name": "Sarah Johnson", "company": "Acme Corp", "email": "sarah.johnson@acmecorp.com", "phone": "+1-555-0101"},
            "deal": {"value": 10000, "next_step": "Send enterprise plan proposal", "days_out": 2, "notes": "Very interested in enterprise features. Budget approved."}
        },
        {
            "contact": {"name": "Michael Chen", "company": "TechStart Inc", "email": "mchen@techstart.io", "phone": "+1-555-0102"},
            "deal": {"value": 5000, "next_step": "Schedule product demo", "days_out": 3, "notes": "Startup founder, looking for scalable solution."}
        },
        {
            "contact": {"name": "Emily Rodriguez", "company": "Global Solutions", "email": "emily.r@globalsol.com", "phone": "+1-555-0103"},
            "deal": {"value": 15000, "next_step": "Final contract review", "days_out": 1, "notes": "Large enterprise client. Multiple stakeholders."}
        },
    ]
    
    created = 0
    for item in demo_data:
        try:
            contact_id = db.find_or_create_contact(**item["contact"])
            
            # Create deal
            follow_up = (datetime.now() + timedelta(days=item["deal"]["days_out"])).date().isoformat()
            db.create_deal(
                contact_id=contact_id,
                deal_value=item["deal"]["value"],
                next_step=item["deal"]["next_step"],
                follow_up_date=follow_up,
                notes=item["deal"]["notes"]
            )
            
            print(f"   ✅ Created: {item['contact']['name']} - ${item['deal']['value']}")
            created += 1
        except Exception as e:
            print(f"   ❌ Error creating {item['contact']['name']}: {str(e)}")
    
    print(f"\n✅ Demo setup complete!")
    print(f"   📊 Created {created} contacts with deals")
    print(f"\n🚀 You're ready to demo!")
    print(f"   - Backend: http://localhost:8000")
    print(f"   - Frontend: http://localhost:8501")
    
except ImportError as e:
    print(f"❌ Error: Could not import required modules")
    print(f"   {str(e)}")
    print(f"\n   Make sure you're running from the project root:")
    print(f"   python scripts/setup_demo.py")
    sys.exit(1)
