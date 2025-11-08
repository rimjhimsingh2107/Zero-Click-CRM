"""
Database module for Supabase integration
Handles all CRM data operations
"""
import os
from typing import Optional, Dict, List, Any
from datetime import datetime
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

class DatabaseClient:
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_KEY")
        
        if not self.url or not self.key:
            raise ValueError("Missing SUPABASE_URL or SUPABASE_KEY in environment")
        
        self.client: Client = create_client(self.url, self.key)
    
    # ==================== CONTACTS ====================
    
    def find_or_create_contact(self, name: str, company: Optional[str] = None, 
                               email: Optional[str] = None, phone: Optional[str] = None) -> int:
        """Find existing contact or create new one"""
        # Try to find existing contact
        query = self.client.table('contacts').select('*').eq('name', name)
        if company:
            query = query.eq('company', company)
        
        result = query.execute()
        
        if result.data and len(result.data) > 0:
            return result.data[0]['id']
        
        # Create new contact
        contact_data = {
            'name': name,
            'company': company,
            'email': email,
            'phone': phone,
            'created_at': datetime.now().isoformat()
        }
        
        result = self.client.table('contacts').insert(contact_data).execute()
        return result.data[0]['id']
    
    def get_all_contacts(self) -> List[Dict[str, Any]]:
        """Retrieve all contacts"""
        result = self.client.table('contacts').select('*').order('created_at', desc=True).execute()
        return result.data
    
    def get_contact_by_id(self, contact_id: int) -> Optional[Dict[str, Any]]:
        """Get specific contact by ID"""
        result = self.client.table('contacts').select('*').eq('id', contact_id).execute()
        return result.data[0] if result.data else None
    
    # ==================== DEALS ====================
    
    def create_deal(self, contact_id: int, deal_value: Optional[float] = None,
                    stage: str = "initial", next_step: Optional[str] = None,
                    follow_up_date: Optional[str] = None, notes: Optional[str] = None) -> Dict[str, Any]:
        """Create a new deal"""
        deal_data = {
            'contact_id': contact_id,
            'deal_value': deal_value,
            'stage': stage,
            'next_step': next_step,
            'follow_up_date': follow_up_date,
            'notes': notes,
            'created_at': datetime.now().isoformat()
        }
        
        result = self.client.table('deals').insert(deal_data).execute()
        return result.data[0]
    
    def get_all_deals(self) -> List[Dict[str, Any]]:
        """Retrieve all deals with contact information"""
        result = self.client.table('deals').select('*, contacts(*)').order('created_at', desc=True).execute()
        return result.data
    
    def get_deals_by_contact(self, contact_id: int) -> List[Dict[str, Any]]:
        """Get all deals for a specific contact"""
        result = self.client.table('deals').select('*').eq('contact_id', contact_id).execute()
        return result.data
    
    def execute_raw_query(self, query: str) -> List[Dict[str, Any]]:
        """Execute raw SQL query (for AI-generated queries)"""
        # Note: Supabase doesn't support raw SQL directly via Python client
        # This is a simplified version - in production, use RPC functions
        return []
    
    # ==================== ACTIVITIES ====================
    
    def create_activity(self, activity_type: str, transcript: str, 
                        summary: Optional[str] = None, contact_id: Optional[int] = None) -> Dict[str, Any]:
        """Log an activity (email, call, meeting)"""
        activity_data = {
            'type': activity_type,
            'transcript': transcript,
            'summary': summary,
            'contact_id': contact_id,
            'timestamp': datetime.now().isoformat()
        }
        
        result = self.client.table('activities').insert(activity_data).execute()
        return result.data[0]
    
    def get_all_activities(self) -> List[Dict[str, Any]]:
        """Retrieve all activities"""
        result = self.client.table('activities').select('*, contacts(*)').order('timestamp', desc=True).execute()
        return result.data
    
    def get_activities_by_contact(self, contact_id: int) -> List[Dict[str, Any]]:
        """Get all activities for a specific contact"""
        result = self.client.table('activities').select('*').eq('contact_id', contact_id).execute()
        return result.data

# Global database instance
db = DatabaseClient()
