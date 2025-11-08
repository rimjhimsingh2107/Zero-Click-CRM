"""
Email Integration Module
Parses email content and extracts relevant information
"""
import re
from typing import Dict, Any, Optional
from datetime import datetime


class EmailParser:
    """Simple email parser for extracting structured data from email text"""
    
    @staticmethod
    def parse_email(email_text: str) -> Dict[str, Any]:
        """
        Parse email text and extract key components
        
        Args:
            email_text: Raw email content or formatted email string
            
        Returns:
            Dictionary with parsed email components:
            - from_name: Sender name
            - from_email: Sender email
            - to_email: Recipient email  
            - subject: Email subject
            - body: Email body text
            - date: Email date if available
        """
        parsed = {
            "from_name": None,
            "from_email": None,
            "to_email": None,
            "subject": None,
            "body": None,
            "date": None
        }
        
        # Try to parse structured email format
        lines = email_text.split('\n')
        body_lines = []
        in_body = False
        
        for line in lines:
            line = line.strip()
            
            # Parse From field
            if line.lower().startswith('from:'):
                from_match = re.search(r'from:\s*(.+?)(?:\s*<(.+?)>)?$', line, re.IGNORECASE)
                if from_match:
                    parsed["from_name"] = from_match.group(1).strip()
                    if from_match.group(2):
                        parsed["from_email"] = from_match.group(2).strip()
            
            # Parse To field
            elif line.lower().startswith('to:'):
                to_match = re.search(r'to:\s*<?(.+?)>?$', line, re.IGNORECASE)
                if to_match:
                    parsed["to_email"] = to_match.group(1).strip()
            
            # Parse Subject field
            elif line.lower().startswith('subject:'):
                parsed["subject"] = line[8:].strip()
            
            # Parse Date field
            elif line.lower().startswith('date:'):
                parsed["date"] = line[5:].strip()
            
            # Empty line typically separates headers from body
            elif not line and not in_body:
                in_body = True
            
            # Collect body lines
            elif in_body:
                body_lines.append(line)
        
        # If no structured format detected, treat entire text as body
        if not parsed["subject"] and not parsed["from_email"]:
            parsed["body"] = email_text.strip()
        else:
            parsed["body"] = '\n'.join(body_lines).strip()
        
        return parsed
    
    @staticmethod
    def extract_email_addresses(text: str) -> list:
        """Extract all email addresses from text"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return re.findall(email_pattern, text)
    
    @staticmethod
    def extract_phone_numbers(text: str) -> list:
        """Extract phone numbers from text"""
        # Common phone formats
        phone_patterns = [
            r'\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',  # +1-555-123-4567
            r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',  # (555) 123-4567
            r'\d{3}[-.\s]\d{3}[-.\s]\d{4}',  # 555-123-4567
        ]
        
        phones = []
        for pattern in phone_patterns:
            phones.extend(re.findall(pattern, text))
        return list(set(phones))  # Remove duplicates
    
    @staticmethod
    def extract_currency_amounts(text: str) -> list:
        """Extract dollar amounts from text"""
        # Matches: $5,000 or $5000 or 5k or 5K
        patterns = [
            r'\$\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',  # $5,000.00
            r'(\d+)\s*k\b',  # 5k (thousands)
            r'\$\s*(\d+)',  # $5000
        ]
        
        amounts = []
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                # Convert to float
                if isinstance(match, str):
                    # Remove commas
                    clean = match.replace(',', '')
                    try:
                        value = float(clean)
                        # If it's a 'k' notation, multiply by 1000
                        if 'k' in text[text.find(clean):text.find(clean)+len(clean)+2].lower():
                            value *= 1000
                        amounts.append(value)
                    except ValueError:
                        pass
        
        return amounts
    
    @staticmethod
    def create_sample_emails() -> list:
        """
        Generate sample emails for demo purposes
        """
        samples = [
            {
                "from": "Sarah Johnson <sarah.johnson@acmecorp.com>",
                "subject": "Re: Enterprise Plan Inquiry",
                "body": """Hi there,

Thanks for the quick response! After discussing with our team, we're very interested in moving forward with the enterprise plan at $10,000 annually.

We have about 25 sales reps who would need access, and the advanced reporting features you mentioned are exactly what we need.

Our budget has been approved, but I need to present this to our VP of Sales next Monday. Could you send over a detailed proposal with implementation timeline?

Looking forward to working together!

Best regards,
Sarah Johnson
Director of Sales Operations
Acme Corp
Phone: +1-555-0101"""
            },
            {
                "from": "Michael Chen <mchen@techstart.io>",
                "subject": "CRM Demo Request",
                "body": """Hello,

I'm the founder of TechStart Inc, an early-stage startup in the fintech space. We're looking for a CRM solution that can scale with us.

I saw your pricing starts at around $5K which fits our budget. Before we commit, I'd love to see a live demo of the platform, especially:
- Contact management
- Deal pipeline tracking  
- Mobile app capabilities

Are you available for a 30-minute demo this Wednesday afternoon?

Thanks,
Michael Chen
Founder & CEO, TechStart Inc
mchen@techstart.io"""
            },
            {
                "from": "Emily Rodriguez <emily.r@globalsol.com>",
                "subject": "Contract Review - Final Steps",
                "body": """Hi team,

We're in the final stages of review for the $15,000 annual contract. Our legal team has gone through the terms and we're ready to proceed.

Just need to finalize a few details:
1. Data migration support for our existing 50+ user accounts
2. Custom integration with Salesforce
3. On-site training for our sales team

If we can confirm these items by end of week, we can sign and start implementation next month.

Best,
Emily Rodriguez  
VP of Sales, Global Solutions
emily.r@globalsol.com
+1-555-0103"""
            }
        ]
        
        return samples


# Global parser instance
email_parser = EmailParser()


if __name__ == "__main__":
    # Test the parser
    sample = """From: John Doe <john@example.com>
To: sales@company.com
Subject: Interested in your product

Hi there,

I'm interested in your CRM solution for my company. We have about 20 sales reps and are looking to spend around $8,000 annually.

Can you call me at 555-123-4567 to discuss?

Thanks,
John"""
    
    parsed = email_parser.parse_email(sample)
    print("Parsed Email:")
    for key, value in parsed.items():
        print(f"  {key}: {value}")
    
    print("\nExtracted emails:", email_parser.extract_email_addresses(sample))
    print("Extracted phones:", email_parser.extract_phone_numbers(sample))
    print("Extracted amounts:", email_parser.extract_currency_amounts(sample))
