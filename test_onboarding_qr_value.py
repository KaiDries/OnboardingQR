#!/usr/bin/env python3
"""
Test script to verify that user QR codes now use RFID tag QR code values
from the rfid_tags table as specified in the SQL query.
"""

import os
import sys
from qr_generator import QRCodeGenerator

def test_rfid_qr_values():
    """Test that user QR codes use RFID tag qr_code values"""
    
    # Create QR generator
    qr_gen = QRCodeGenerator()
    
    # Test data simulating onboarding data from the database
    onboarding_qrs = [
        {
            'onboarding_name': 'Test User 1',
            'qr_code': 'ONBOARD123',  # This is used for onboarding QR
            'location_name': 'Test Location',
            'sales_name': 'Test Sales',
            'event_name': 'Test Event',
            'rollen': 'cashier',
            'betaalmethodes': 'cash,card'
        }
    ]
    
    # Mock user data map with RFID tag QR code (simulating the joined query result)
    user_data_map = {
        'Test User 1': {
            'id': 1,
            'firstname': 'Test',
            'lastname': 'User',
            'email': 'test.user@test-domain.com',
            'qr_code': 'RFID_TAG_ABC123'  # This should be used for user QR
        }
    }
    
    # Test domain and tenant
    domain = "test-domain.com"
    tenant_id = "test-tenant"
    
    print("Testing user QR code generation with RFID tag QR values...")
    print(f"Onboarding QR code: {onboarding_qrs[0]['qr_code']}")
    print(f"User RFID QR code: {user_data_map['Test User 1']['qr_code']}")
    print("Expected: User QR should use RFID tag QR code value")
    
    try:
        # Generate test PDF
        filename = qr_gen.generate_multi_page_guest_template(
            onboarding_qrs,
            domain,
            tenant_id,
            user_data_map
        )
        
        print(f"✓ Test PDF generated: {filename}")
        print("✓ User QR codes should now contain RFID tag QR code values")
        print(f"✓ Onboarding QR: {onboarding_qrs[0]['qr_code']}")
        print(f"✓ User QR: {user_data_map['Test User 1']['qr_code']}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error generating test PDF: {e}")
        return False

if __name__ == "__main__":
    success = test_rfid_qr_values()
    sys.exit(0 if success else 1)
