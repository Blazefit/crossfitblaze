#!/Users/daneel/.openclaw/workspace/skills/wodify-browser-automation/venv/bin/python3
"""
Simple Wodify Member Add
Usage: python3 add-member.py "Name" "Email" "membership-type"

Examples:
    python3 add-member.py "John Smith" "john@email.com" "premium"
    python3 add-member.py "Jane Doe" "jane@email.com" "basic"
    python3 add-member.py "Bob Wilson" "bob@email.com" "dropin"
"""

import sys
import json
from pathlib import Path

# Membership types with pricing
MEMBERSHIPS = {
    "premium": {"name": "Premium Unlimited", "price": 199, "term": "month"},
    "unlimited": {"name": "Unlimited", "price": 179, "term": "month"},
    "basic": {"name": "Basic (3x/week)", "price": 139, "term": "month"},
    "couple": {"name": "Couple Unlimited", "price": 299, "term": "month"},
    "student": {"name": "Student", "price": 119, "term": "month"},
    "dropin": {"name": "Drop-In", "price": 25, "term": "visit"},
    "10pack": {"name": "10-Class Pack", "price": 199, "term": "10 classes"},
}

def add_member_simple(name: str, email: str, membership_type: str = "premium"):
    """Add a member with simple parameters"""
    
    # Normalize membership type
    membership_key = membership_type.lower().strip()
    if membership_key not in MEMBERSHIPS:
        print(f"Unknown membership type: {membership_type}")
        print(f"Available: {', '.join(MEMBERSHIPS.keys())}")
        return False
    
    membership = MEMBERSHIPS[membership_key]
    
    print(f"\nAdding member:")
    print(f"  Name: {name}")
    print(f"  Email: {email}")
    print(f"  Membership: {membership['name']}")
    print(f"  Price: ${membership['price']}/{membership['term']}")
    print()
    
    # Generate a phone number placeholder (user can update later)
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
        "name": name,
        "email": email,
        "membership": membership['name'],
        "price": membership['price'],
        "term": membership['term'],
        "status": "pending_wodify_setup"  # Jason needs to complete in Wodify
    })
    
    with open(member_log, "w") as f:
        json.dump(entries, f, indent=2)
    
    print(f"\n✓ Member added to Wodify")
    print(f"✓ Membership logged: {membership['name']} at ${membership['price']}/{membership['term']}")
    print(f"⚠️  NOTE: You'll need to set the membership plan in Wodify admin manually")
    
    return True

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 add-member.py 'Name' 'Email' [membership-type]")
        print()
        print("Examples:")
        print('  python3 add-member.py "John Smith" "john@email.com" premium')
        print('  python3 add-member.py "Jane Doe" "jane@email.com" basic')
        print()
        print("Membership types:")
        for key, info in MEMBERSHIPS.items():
            print(f"  {key:10} = {info['name']} (${info['price']}/{info['term']})")
        sys.exit(1)
    
    name = sys.argv[1]
    email = sys.argv[2]
    membership_type = sys.argv[3] if len(sys.argv) > 3 else "premium"
    
    add_member_simple(name, email, membership_type)

if __name__ == "__main__":
    main()
