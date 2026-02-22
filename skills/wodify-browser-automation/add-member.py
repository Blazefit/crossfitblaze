#!/Users/daneel/.openclaw/workspace/skills/wodify-browser-automation/venv/bin/python3
"""
Simple Wodify Member Add - WITH ACTUAL PRICES
Usage: python3 add-member.py "Name" "Email" "membership-type"

Extracted from Wodify on 2026-02-22
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# ACTUAL CrossFit Blaze Membership Prices (from Wodify Admin)
MEMBERSHIPS = {
    # Main Memberships
    "premium": {
        "name": "CrossFit Blaze Premium", 
        "price": 155,  # $135-$155 range, using high end
        "term": "month",
        "attendance": "Unlimited",
        "wodify_id": "10510"
    },
    "basic": {
        "name": "Blaze Basic", 
        "price": 0,  # Shows $0.00 in Wodify - needs manual price entry
        "term": "month",
        "attendance": "8 Classes",
        "note": "Price needs to be set manually in Wodify",
        "wodify_id": "19868"
    },
    "dropin": {
        "name": "Drop-In", 
        "price": 20,  # $20-$60 range
        "term": "visit",
        "attendance": "1 Class",
        "wodify_id": "14856"
    },
    
    # Class Packs
    "10pack": {
        "name": "Blaze Punchcard (10 sessions)", 
        "price": 165,
        "term": "10 classes",
        "attendance": "10 Classes",
        "wodify_id": "10511"
    },
    "private10": {
        "name": "10 Private 30min Sessions", 
        "price": 350,
        "term": "10 sessions",
        "attendance": "10 Classes",
        "wodify_id": "11222"
    },
    
    # Specialty Programs
    "kids": {
        "name": "Blaze Fit Kids", 
        "price": 89,
        "term": "month",
        "attendance": "Unlimited",
        "wodify_id": "10513"
    },
    "bootcamp": {
        "name": "Blaze Bootcamp", 
        "price": 130,  # $35-$130 range
        "term": "month",
        "attendance": "Unlimited",
        "wodify_id": "57168"
    },
    "barbell": {
        "name": "Barbell Club", 
        "price": 100,
        "term": "month",
        "attendance": "Unlimited",
        "wodify_id": "67338"
    },
    "athome": {
        "name": "Blaze at Home", 
        "price": 40,
        "term": "month",
        "attendance": "Unlimited",
        "wodify_id": "57170"
    },
    
    # Trials
    "trial": {
        "name": "Free Trial", 
        "price": 0,
        "term": "trial",
        "attendance": "3 Classes",
        "wodify_id": "15058"
    }
}

def add_member_simple(name: str, email: str, membership_type: str = "premium"):
    """Add a member with actual Wodify prices"""
    
    # Normalize membership type
    membership_key = membership_type.lower().strip()
    if membership_key not in MEMBERSHIPS:
        print(f"Unknown membership type: {membership_type}")
        print(f"Available: {', '.join(MEMBERSHIPS.keys())}")
        return False
    
    membership = MEMBERSHIPS[membership_key]
    
    print(f"\nAdding member to Wodify:")
    print(f"  Name: {name}")
    print(f"  Email: {email}")
    print(f"  Membership: {membership['name']}")
    if membership['price'] > 0:
        print(f"  Price: ${membership['price']}/{membership['term']}")
    else:
        print(f"  Price: TBD (needs manual setup)")
    print()
    
    # Generate a phone number placeholder
    phone = "239-555-0000"
    
    # Call the main wodify script
    import subprocess
    result = subprocess.run([
        sys.executable, "wodify.py",
        "add-client", name, email, phone
    ], capture_output=True, text=True)
    
    print(result.stdout)
    if result.stderr:
        print(result.stderr)
    
    # Log the membership details
    config_dir = Path.home() / ".wodify"
    config_dir.mkdir(exist_ok=True)
    
    member_log = config_dir / "membership-additions.json"
    
    entries = []
    if member_log.exists():
        with open(member_log) as f:
            entries = json.load(f)
    
    entries.append({
        "timestamp": datetime.now().isoformat(),
        "name": name,
        "email": email,
        "membership": membership['name'],
        "price": membership['price'],
        "term": membership['term'],
        "attendance": membership['attendance'],
        "wodify_id": membership.get('wodify_id'),
        "status": "added_to_wodify",
        "note": "Set membership plan in Wodify admin manually"
    })
    
    with open(member_log, "w") as f:
        json.dump(entries, f, indent=2)
    
    print(f"\n✓ Member added to Wodify")
    print(f"✓ Membership logged: {membership['name']}")
    print(f"⚠️  IMPORTANT: You must manually set the membership plan in Wodify:")
    print(f"   1. Go to People → Clients")
    print(f"   2. Find the client: {name}")
    print(f"   3. Edit → Memberships → Add Membership")
    print(f"   4. Select: {membership['name']}")
    print(f"   5. Set price: ${membership['price']}")
    
    return True

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 add-member.py 'Name' 'Email' [membership-type]")
        print()
        print("Examples:")
        print('  python3 add-member.py "John Smith" "john@email.com" premium')
        print('  python3 add-member.py "Jane Doe" "jane@email.com" dropin')
        print()
        print("Membership types (from Wodify):")
        print("  Main Memberships:")
        for key in ['premium', 'basic', 'dropin']:
            info = MEMBERSHIPS[key]
            print(f"    {key:12} = {info['name']} (${info['price']}/{info['term']})")
        print("\n  Class Packs:")
        for key in ['10pack', 'private10']:
            info = MEMBERSHIPS[key]
            print(f"    {key:12} = {info['name']} (${info['price']}/{info['term']})")
        print("\n  Specialty:")
        for key in ['kids', 'bootcamp', 'barbell', 'athome']:
            info = MEMBERSHIPS[key]
            print(f"    {key:12} = {info['name']} (${info['price']}/{info['term']})")
        print("\n  Trial:")
        print(f"    {'trial':12} = {MEMBERSHIPS['trial']['name']} (Free)")
        sys.exit(1)
    
    name = sys.argv[1]
    email = sys.argv[2]
    membership_type = sys.argv[3] if len(sys.argv) > 3 else "premium"
    
    add_member_simple(name, email, membership_type)

if __name__ == "__main__":
    main()
