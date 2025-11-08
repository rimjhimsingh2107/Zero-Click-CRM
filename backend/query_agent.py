"""
Query Agent module
Converts natural language queries to database operations
"""
import os
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

class QueryAgent:
    def __init__(self, provider: str = "anthropic"):
        """Initialize query agent with LLM"""
        self.provider = provider.lower()
        
        if self.provider == "anthropic":
            import anthropic
            self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            self.model = "claude-3-5-sonnet-20241022"
        elif self.provider == "openai":
            import openai
            self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            self.model = "gpt-4-turbo-preview"
    
    def natural_language_to_filter(self, query: str) -> Dict[str, Any]:
        """
        Convert natural language query to filter parameters
        
        Returns a dict with filter criteria that can be applied to data
        """
        prompt = f"""Convert this user query into structured filter parameters for a CRM database.

Database schema:
- contacts: id, name, company, email, phone, created_at
- deals: id, contact_id, deal_value, stage, next_step, follow_up_date, notes, created_at

Return ONLY a JSON object with these optional keys:
- table: "contacts" or "deals"
- company: string to match
- deal_value_min: minimum deal value
- deal_value_max: maximum deal value
- date_from: start date (YYYY-MM-DD)
- date_to: end date (YYYY-MM-DD)
- name_contains: partial name match
- stage: deal stage
- has_follow_up: boolean

Query: "{query}"

Return ONLY the JSON object."""

        try:
            if self.provider == "anthropic":
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=512,
                    messages=[{"role": "user", "content": prompt}]
                )
                content = response.content[0].text
            elif self.provider == "openai":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0
                )
                content = response.choices[0].message.content
            
            # Clean and parse JSON
            content = content.strip()
            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()
            
            import json
            filters = json.loads(content)
            return filters
            
        except Exception as e:
            print(f"Error converting query: {str(e)}")
            return {"table": "deals"}
    
    def apply_filters(self, data: List[Dict[str, Any]], filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Apply filter parameters to dataset"""
        from datetime import datetime
        
        filtered = data
        
        # Apply company filter
        if filters.get("company"):
            filtered = [d for d in filtered if d.get("company", "").lower() == filters["company"].lower()]
        
        # Apply deal value filters
        if filters.get("deal_value_min") is not None:
            filtered = [d for d in filtered if d.get("deal_value", 0) >= filters["deal_value_min"]]
        if filters.get("deal_value_max") is not None:
            filtered = [d for d in filtered if d.get("deal_value", 0) <= filters["deal_value_max"]]
        
        # Apply date filters
        if filters.get("date_from"):
            date_from = datetime.fromisoformat(filters["date_from"])
            filtered = [d for d in filtered 
                       if d.get("follow_up_date") and datetime.fromisoformat(d["follow_up_date"]) >= date_from]
        
        if filters.get("date_to"):
            date_to = datetime.fromisoformat(filters["date_to"])
            filtered = [d for d in filtered 
                       if d.get("follow_up_date") and datetime.fromisoformat(d["follow_up_date"]) <= date_to]
        
        # Apply name filter
        if filters.get("name_contains"):
            name = filters["name_contains"].lower()
            filtered = [d for d in filtered 
                       if name in d.get("name", "").lower() or 
                          (d.get("contacts") and name in d["contacts"].get("name", "").lower())]
        
        return filtered

# Global query agent
try:
    query_agent = QueryAgent(provider="anthropic")
except Exception:
    query_agent = QueryAgent(provider="openai")
