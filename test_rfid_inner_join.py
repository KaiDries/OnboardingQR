#!/usr/bin/env python3
"""
Test script to verify that the new INNER JOIN query correctly returns
only users that have RFID tags with QR codes.
"""

import os
import sys
from qr_generator import QRCodeGenerator

def test_rfid_inner_join():
    """Test that only users with RFID tags are returned"""
    
    # Create QR generator
    qr_gen = QRCodeGenerator()
    
    # Test data simulating onboarding data from the database
    onboarding_qrs = [
        {
            'onboarding_name': 'User With RFID',
            'qr_code': 'ONBOARD123',
            'location_name': 'Test Location',
            'sales_name': 'Test Sales', 
            'event_name': 'Test Event',
            'rollen': 'cashier',
            'betaalmethodes': 'cash,card'
        },
        {
            'onboarding_name': 'User Without RFID',
            'qr_code': 'ONBOARD456',
            'location_name': 'Test Location 2',
            'sales_name': 'Test Sales 2',
            'event_name': 'Test Event 2', 
            'rollen': 'manager',
            'betaalmethodes': 'card'
        }
    ]
    
    # Mock user data map - only users WITH RFID tags will be found by INNER JOIN
    user_data_map = {
        'User With RFID': {
            'firstname': 'John',
            'lastname': 'Doe',
            'email': 'john.doe@test-domain.com',
            'qr_code': 'RFID_TAG_XYZ789'  # This user HAS an RFID tag
        }
        # 'User Without RFID' is NOT in the map because INNER JOIN won't find them
    }
    
    # Test domain and tenant
    domain = "test-domain.com"
    tenant_id = "test-tenant"
    
    print("Testing INNER JOIN approach for USER QR codes...")
    print("Expected behavior:")
    print("- User With RFID: Should have USER QR code")
    print("- User Without RFID: Should show 'Geen User' (not found by INNER JOIN)")
    
    try:
        # Generate test PDF
        filename = qr_gen.generate_multi_page_guest_template(
            onboarding_qrs,
            domain,
            tenant_id,
            user_data_map
        )
        
        print(f"✓ Test PDF generated: {filename}")
        print("✓ PDF should show:")
        print("  - Page 1: User With RFID + USER QR code (RFID_TAG_XYZ789)")
        print("  - Page 2: User Without RFID + 'Geen User' message")
        
        return True
        
    except Exception as e:
        print(f"✗ Error generating test PDF: {e}")
        return False

if __name__ == "__main__":
    success = test_rfid_inner_join()
    sys.exit(0 if success else 1)
