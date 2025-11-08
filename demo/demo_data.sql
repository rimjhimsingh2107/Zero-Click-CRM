-- Zero-Click CRM Demo Data
-- Run this in Supabase SQL Editor to populate with sample data

-- Clear existing demo data (optional)
-- DELETE FROM activities;
-- DELETE FROM deals;
-- DELETE FROM contacts;

-- Insert sample contacts
INSERT INTO contacts (name, company, email, phone, created_at) VALUES
('Sarah Johnson', 'Acme Corp', 'sarah.johnson@acmecorp.com', '+1-555-0101', NOW() - INTERVAL '5 days'),
('Michael Chen', 'TechStart Inc', 'mchen@techstart.io', '+1-555-0102', NOW() - INTERVAL '4 days'),
('Emily Rodriguez', 'Global Solutions', 'emily.r@globalsol.com', '+1-555-0103', NOW() - INTERVAL '3 days'),
('David Kim', 'Innovation Labs', 'david@innovlabs.com', '+1-555-0104', NOW() - INTERVAL '2 days'),
('Jessica Martinez', 'FutureTech', 'jmartinez@futuretech.com', '+1-555-0105', NOW() - INTERVAL '1 day'),
('Robert Taylor', 'CloudNine Systems', 'rtaylor@cloudnine.io', '+1-555-0106', NOW() - INTERVAL '6 hours'),
('Amanda Wilson', 'DataFlow Inc', 'awilson@dataflow.com', '+1-555-0107', NOW() - INTERVAL '3 hours');

-- Insert sample deals (use contact IDs from above)
-- Note: Adjust contact_id values based on your actual inserted IDs
INSERT INTO deals (contact_id, deal_value, stage, next_step, follow_up_date, notes, created_at)
SELECT 
    c.id,
    CASE 
        WHEN c.name = 'Sarah Johnson' THEN 10000.00
        WHEN c.name = 'Michael Chen' THEN 5000.00
        WHEN c.name = 'Emily Rodriguez' THEN 15000.00
        WHEN c.name = 'David Kim' THEN 8500.00
        WHEN c.name = 'Jessica Martinez' THEN 12000.00
        WHEN c.name = 'Robert Taylor' THEN 7500.00
        ELSE 6000.00
    END as deal_value,
    CASE 
        WHEN c.name IN ('Sarah Johnson', 'Michael Chen') THEN 'proposal'
        WHEN c.name IN ('Emily Rodriguez', 'David Kim') THEN 'negotiation'
        ELSE 'initial'
    END as stage,
    CASE 
        WHEN c.name = 'Sarah Johnson' THEN 'Send enterprise plan proposal'
        WHEN c.name = 'Michael Chen' THEN 'Schedule product demo'
        WHEN c.name = 'Emily Rodriguez' THEN 'Final contract review'
        WHEN c.name = 'David Kim' THEN 'Pricing discussion'
        WHEN c.name = 'Jessica Martinez' THEN 'Technical requirements gathering'
        ELSE 'Initial discovery call'
    END as next_step,
    CASE 
        WHEN c.name = 'Sarah Johnson' THEN CURRENT_DATE + 2
        WHEN c.name = 'Michael Chen' THEN CURRENT_DATE + 3
        WHEN c.name = 'Emily Rodriguez' THEN CURRENT_DATE + 1
        WHEN c.name = 'David Kim' THEN CURRENT_DATE + 5
        WHEN c.name = 'Jessica Martinez' THEN CURRENT_DATE + 4
        ELSE CURRENT_DATE + 7
    END as follow_up_date,
    CASE 
        WHEN c.name = 'Sarah Johnson' THEN 'Very interested in enterprise features. Budget approved.'
        WHEN c.name = 'Michael Chen' THEN 'Startup founder, looking for scalable solution. Price-sensitive.'
        WHEN c.name = 'Emily Rodriguez' THEN 'Large enterprise client. Multiple stakeholders involved.'
        WHEN c.name = 'David Kim' THEN 'R&D team needs advanced features. Ready to commit.'
        ELSE 'Initial contact, needs more information.'
    END as notes,
    NOW() - INTERVAL '1 day' * (7 - ROW_NUMBER() OVER()) as created_at
FROM contacts c
WHERE c.name IN ('Sarah Johnson', 'Michael Chen', 'Emily Rodriguez', 'David Kim', 'Jessica Martinez', 'Robert Taylor', 'Amanda Wilson');

-- Insert sample activities
INSERT INTO activities (type, transcript, summary, contact_id, timestamp)
SELECT 
    CASE 
        WHEN c.name IN ('Sarah Johnson', 'Michael Chen') THEN 'call'
        WHEN c.name IN ('Emily Rodriguez') THEN 'meeting'
        ELSE 'email'
    END as type,
    CASE 
        WHEN c.name = 'Sarah Johnson' THEN 'Had a great call with Sarah from Acme Corp. She expressed strong interest in our enterprise plan at $10,000. They need advanced reporting features and multi-user support. Budget is approved, just needs to present to stakeholders. Follow up next Monday with detailed proposal.'
        WHEN c.name = 'Michael Chen' THEN 'Spoke with Michael from TechStart Inc. Early-stage startup looking for affordable CRM solution. Interested in $5K annual plan but wants to see a live demo first. Schedule demo for Wednesday.'
        WHEN c.name = 'Emily Rodriguez' THEN 'Meeting with Emily from Global Solutions went well. Large enterprise deal worth $15K. They have 50+ sales reps who need the system. In final contract review stage. Legal team involved. Close by end of week.'
        WHEN c.name = 'David Kim' THEN 'Email exchange with David from Innovation Labs. Their R&D team needs our analytics features. Deal value around $8,500. Discussing pricing options. He wants to understand our data security measures.'
        ELSE 'Initial contact made. Need to qualify opportunity further.'
    END as transcript,
    CASE 
        WHEN c.name = 'Sarah Johnson' THEN 'Enterprise deal, $10K, budget approved, needs proposal'
        WHEN c.name = 'Michael Chen' THEN 'Startup, $5K, price-sensitive, demo requested'
        WHEN c.name = 'Emily Rodriguez' THEN 'Large enterprise, $15K, in contract review'
        WHEN c.name = 'David Kim' THEN 'R&D team, $8.5K, discussing security and pricing'
        ELSE 'Initial contact, qualification needed'
    END as summary,
    c.id as contact_id,
    NOW() - INTERVAL '1 day' * (7 - ROW_NUMBER() OVER()) as timestamp
FROM contacts c
WHERE c.name IN ('Sarah Johnson', 'Michael Chen', 'Emily Rodriguez', 'David Kim', 'Jessica Martinez')
ORDER BY c.created_at;

-- Verify data was inserted
SELECT 'Contacts inserted:', COUNT(*) FROM contacts;
SELECT 'Deals inserted:', COUNT(*) FROM deals;
SELECT 'Activities inserted:', COUNT(*) FROM activities;

-- Show pipeline summary
SELECT 
    COUNT(*) as total_deals,
    SUM(deal_value) as pipeline_value,
    AVG(deal_value) as avg_deal_size,
    COUNT(DISTINCT contact_id) as unique_contacts
FROM deals;
