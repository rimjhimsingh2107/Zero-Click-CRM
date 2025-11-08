"""
Supabase Database Setup Script
Run this to create the necessary tables in your Supabase database
"""

SETUP_SQL = """
-- Create contacts table
CREATE TABLE IF NOT EXISTS contacts (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    company VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create deals table
CREATE TABLE IF NOT EXISTS deals (
    id BIGSERIAL PRIMARY KEY,
    contact_id BIGINT REFERENCES contacts(id) ON DELETE CASCADE,
    deal_value DECIMAL(12, 2),
    stage VARCHAR(100) DEFAULT 'initial',
    next_step TEXT,
    follow_up_date DATE,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create activities table
CREATE TABLE IF NOT EXISTS activities (
    id BIGSERIAL PRIMARY KEY,
    type VARCHAR(50) NOT NULL,
    transcript TEXT,
    summary TEXT,
    contact_id BIGINT REFERENCES contacts(id) ON DELETE SET NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_contacts_name ON contacts(name);
CREATE INDEX IF NOT EXISTS idx_contacts_company ON contacts(company);
CREATE INDEX IF NOT EXISTS idx_deals_contact_id ON deals(contact_id);
CREATE INDEX IF NOT EXISTS idx_deals_follow_up_date ON deals(follow_up_date);
CREATE INDEX IF NOT EXISTS idx_activities_contact_id ON activities(contact_id);
CREATE INDEX IF NOT EXISTS idx_activities_timestamp ON activities(timestamp);

-- Enable Row Level Security (RLS)
ALTER TABLE contacts ENABLE ROW LEVEL SECURITY;
ALTER TABLE deals ENABLE ROW LEVEL SECURITY;
ALTER TABLE activities ENABLE ROW LEVEL SECURITY;

-- Create policies (for development, allow all operations)
-- In production, you should restrict these based on user authentication

DROP POLICY IF EXISTS "Enable read access for all users" ON contacts;
CREATE POLICY "Enable read access for all users" ON contacts FOR SELECT USING (true);

DROP POLICY IF EXISTS "Enable insert for all users" ON contacts;
CREATE POLICY "Enable insert for all users" ON contacts FOR INSERT WITH CHECK (true);

DROP POLICY IF EXISTS "Enable update for all users" ON contacts;
CREATE POLICY "Enable update for all users" ON contacts FOR UPDATE USING (true);

DROP POLICY IF EXISTS "Enable read access for all users" ON deals;
CREATE POLICY "Enable read access for all users" ON deals FOR SELECT USING (true);

DROP POLICY IF EXISTS "Enable insert for all users" ON deals;
CREATE POLICY "Enable insert for all users" ON deals FOR INSERT WITH CHECK (true);

DROP POLICY IF EXISTS "Enable update for all users" ON deals;
CREATE POLICY "Enable update for all users" ON deals FOR UPDATE USING (true);

DROP POLICY IF EXISTS "Enable read access for all users" ON activities;
CREATE POLICY "Enable read access for all users" ON activities FOR SELECT USING (true);

DROP POLICY IF EXISTS "Enable insert for all users" ON activities;
CREATE POLICY "Enable insert for all users" ON activities FOR INSERT WITH CHECK (true);

DROP POLICY IF EXISTS "Enable update for all users" ON activities;
CREATE POLICY "Enable update for all users" ON activities FOR UPDATE USING (true);
"""

print("=== Supabase Database Setup SQL ===")
print("\nCopy the SQL below and run it in your Supabase SQL Editor:")
print("\n" + "="*50)
print(SETUP_SQL)
print("="*50)
print("\nSteps:")
print("1. Go to your Supabase project dashboard")
print("2. Navigate to SQL Editor")
print("3. Create a new query")
print("4. Paste the SQL above")
print("5. Click 'Run'")
