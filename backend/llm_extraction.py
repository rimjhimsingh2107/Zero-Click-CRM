"""
LLM extraction module
Uses Claude/Gemini/GPT to extract structured CRM data from text
"""
import os
import json
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

class LLMExtractor:
    def __init__(self, provider: str = "anthropic"):
        """
        Initialize LLM client
        Supports: anthropic, openai, google
        """
        self.provider = provider.lower()
        
        if self.provider == "anthropic":
            import anthropic
            self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            self.model = "claude-3-5-sonnet-20241022"
        elif self.provider == "openai":
            import openai
            self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            self.model = "gpt-4-turbo-preview"
        elif self.provider == "google":
            import google.generativeai as genai
            genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
            self.client = genai.GenerativeModel('gemini-pro')
            self.model = "gemini-pro"
        else:
            raise ValueError(f"Unsupported provider: {provider}")
    
    def extract_crm_data(self, text: str) -> Dict[str, Any]:
        """
        Extract structured CRM data from text
        
        Returns:
            {
                "contact_name": str,
                "company": str,
                "email": str (optional),
                "phone": str (optional),
                "deal_value": float (optional),
                "next_step": str (optional),
                "follow_up_date": str (optional, YYYY-MM-DD),
                "notes": str (optional)
            }
        """
        prompt = f"""You are an AI CRM assistant. Extract structured data from the following text.

Return ONLY a valid JSON object with these keys (use null for missing values):
- contact_name (string): Person's name
- company (string): Company name
- email (string): Email address if mentioned
- phone (string): Phone number if mentioned
- deal_value (number): Dollar amount of deal (just the number, no $ or commas)
- next_step (string): What needs to happen next
- follow_up_date (string): Date in YYYY-MM-DD format
- notes (string): Any additional relevant information

Text to analyze:
"{text}"

Return ONLY the JSON object, no other text."""

        try:
            if self.provider == "anthropic":
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=1024,
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
            
            elif self.provider == "google":
                response = self.client.generate_content(prompt)
                content = response.text
            
            # Parse JSON response
            # Remove markdown code blocks if present
            content = content.strip()
            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()
            
            data = json.loads(content)
            return data
            
        except Exception as e:
            print(f"Error extracting CRM data: {str(e)}")
            # Return empty structure on error
            return {
                "contact_name": None,
                "company": None,
                "email": None,
                "phone": None,
                "deal_value": None,
                "next_step": None,
                "follow_up_date": None,
                "notes": text
            }
    
    def generate_summary(self, text: str, max_words: int = 50) -> str:
        """Generate a brief summary of the conversation"""
        prompt = f"Summarize this conversation in {max_words} words or less:\n\n{text}"
        
        try:
            if self.provider == "anthropic":
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=256,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.content[0].text
            elif self.provider == "openai":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3
                )
                return response.choices[0].message.content
            elif self.provider == "google":
                response = self.client.generate_content(prompt)
                return response.text
        except Exception as e:
            print(f"Error generating summary: {str(e)}")
            return text[:100] + "..." if len(text) > 100 else text

# Global extractor instance (default to Anthropic/Claude)
try:
    llm_extractor = LLMExtractor(provider="anthropic")
except Exception:
    # Fallback to OpenAI if Anthropic not configured
    try:
        llm_extractor = LLMExtractor(provider="openai")
    except Exception:
        # Final fallback to Google if available
        llm_extractor = LLMExtractor(provider="google")
