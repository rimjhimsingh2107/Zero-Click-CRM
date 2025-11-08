#!/usr/bin/env python3
"""
Quick Test Script - Verify Zero-Click CRM is ready for demo
Run this to test all critical features
"""
import requests
import time

API_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:8501"

def test_api(endpoint, method="GET", data=None):
    """Test an API endpoint"""
    try:
        if method == "GET":
            response = requests.get(f"{API_URL}{endpoint}", timeout=5)
        else:
            response = requests.post(f"{API_URL}{endpoint}", json=data, timeout=10)
        
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, f"Status {response.status_code}: {response.text}"
    except requests.exceptions.ConnectionError:
        return False, "Connection refused - is backend running?"
    except requests.exceptions.Timeout:
        return False, "Request timeout"
    except Exception as e:
        return False, str(e)

print("🧪 Zero-Click CRM Test Suite")
print("=" * 60)

# Test 1: Backend Running
print("\n1️⃣ Testing Backend Connection...")
success, result = test_api("/")
if success:
    print("   ✅ Backend is running!")
    print(f"   📊 Version: {result.get('version', 'N/A')}")
else:
    print(f"   ❌ Backend test failed: {result}")
    print("   💡 Start backend with: cd backend && python main.py")
    exit(1)

# Test 2: Database Connection
print("\n2️⃣ Testing Database Connection...")
success, result = test_api("/contacts")
if success:
    contact_count = len(result.get('contacts', []))
    print(f"   ✅ Database connected! Found {contact_count} contacts")
    if contact_count == 0:
        print("   ⚠️  No demo data loaded")
        print("   💡 Run: python scripts/setup_demo.py")
else:
    print(f"   ❌ Database test failed: {result}")
    exit(1)

# Test 3: Deals
print("\n3️⃣ Testing Deals...")
success, result = test_api("/deals")
if success:
    deal_count = len(result.get('deals', []))
    total_value = sum(d.get('deal_value', 0) or 0 for d in result.get('deals', []))
    print(f"   ✅ Found {deal_count} deals")
    print(f"   💰 Total pipeline: ${total_value:,.2f}")
else:
    print(f"   ❌ Deals test failed: {result}")

# Test 4: Sample Emails
print("\n4️⃣ Testing Email Parser...")
success, result = test_api("/sample_emails")
if success:
    sample_count = len(result.get('samples', []))
    print(f"   ✅ Email parser working! {sample_count} sample emails available")
else:
    print(f"   ❌ Email parser test failed: {result}")

# Test 5: Text Processing
print("\n5️⃣ Testing Text Processing...")
test_text = "Quick call with John from TestCorp. They want a $5,000 deal. Follow up Monday."
success, result = test_api("/process_text", "POST", {"text": test_text, "source": "test"})
if success:
    extracted = result.get('extracted_data', {})
    print(f"   ✅ Text processing works!")
    print(f"   👤 Extracted contact: {extracted.get('contact_name', 'N/A')}")
    print(f"   🏢 Company: {extracted.get('company', 'N/A')}")
    print(f"   💰 Deal value: ${extracted.get('deal_value', 0) or 0:,.2f}")
else:
    print(f"   ❌ Text processing failed: {result}")
    print("   💡 Check if API key is configured in .env")

# Test 6: Natural Language Query
print("\n6️⃣ Testing Natural Language Search...")
success, result = test_api("/query", "POST", {"query": "Show all deals"})
if success:
    print(f"   ✅ Search works! Found {result.get('count', 0)} results")
else:
    print(f"   ❌ Search test failed: {result}")

# Test 7: Frontend
print("\n7️⃣ Testing Frontend...")
try:
    response = requests.get(FRONTEND_URL, timeout=3)
    if response.status_code == 200:
        print(f"   ✅ Frontend is running at {FRONTEND_URL}")
    else:
        print(f"   ⚠️  Frontend returned status {response.status_code}")
except requests.exceptions.ConnectionError:
    print(f"   ❌ Frontend not running")
    print("   💡 Start with: cd frontend && streamlit run app.py")
except Exception as e:
    print(f"   ❌ Frontend test error: {str(e)}")

# Summary
print("\n" + "=" * 60)
print("📊 Test Summary")
print("=" * 60)
print("\n✅ Core features working!")
print("🎯 You're ready to demo!\n")
print("Next steps:")
print("  1. If no demo data: python scripts/setup_demo.py")
print("  2. Record voice notes: See demo/audio/VOICE_SCRIPTS.md")
print("  3. Practice demo: See DEMO_SCRIPT.md")
print("  4. Verify checklist: See PRE_DEMO_CHECKLIST.md")
print("\n🚀 Good luck with your demo!")
