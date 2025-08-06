#!/usr/bin/env python3
"""
Test script for TOPUP payment methods fix
"""

from database import DatabaseConnection

def test_topup_payment_methods():
    """Test if TOPUP shows correct payment methods"""
    print("=== Testing TOPUP Payment Methods ===\n")
    
    db = DatabaseConnection()
    
    # Test connection
    if not db.connect("tenant-summercamp-2025"):
        print("✗ Could not connect to tenant database")
        return
    
    print("✓ Connected to tenant database")
    
    # Get onboarding QRs
    onboarding_qrs = db.get_onboarding_qrs("summercamp-2025")
    
    if not onboarding_qrs:
        print("✗ No onboarding QRs found")
        return
    
    print(f"✓ Found {len(onboarding_qrs)} onboarding QRs")
    print("\nChecking payment methods for each onboarding:")
    
    for qr in onboarding_qrs:
        name = qr.get('onboarding_name', 'Unknown')
        roles = qr.get('rollen', 'Geen') or 'Geen'
        payment = qr.get('betaalmethodes', 'Geen') or 'Geen'
        
        print(f"\n{name}:")
        print(f"  Roles: {roles}")
        print(f"  Payment: {payment}")
        
        # Special check for TOPUP
        if 'TOPUP' in name.upper() or 'top_up' in roles:
            if payment == 'Geen' or payment == '':
                print(f"  ⚠ ISSUE: TOPUP should have payment methods but shows: '{payment}'")
            else:
                print(f"  ✓ TOPUP has payment methods: {payment}")
    
    db.disconnect()
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    test_topup_payment_methods()
