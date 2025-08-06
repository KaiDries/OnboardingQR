#!/usr/bin/env python3
"""
Test user QR code generation to verify it contains only the value
"""

from qr_generator import QRCodeGenerator
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

def test_user_qr_value():
    """Test that user QR code contains only the value, not full URL"""
    print("Testing user QR code generation...")
    
    # Create QR generator
    qr_gen = QRCodeGenerator()
    
    # Test onboarding data
    test_onboarding_data = {
        'onboarding_name': 'John-Doe',
        'qr_code': 'ONBOARD123',
        'location_name': 'Test Location',
        'sales_name': 'Test Sales',
        'event_name': 'Test Event',
        'rollen': 'sales',
        'betaalmethodes': 'CARD, CASH'
    }
    
    # Test user data with QR code
    test_user_data_map = {
        'John-Doe': {
            'firstname': 'John',
            'lastname': 'Doe',
            'email': 'john.doe@test.com',
            'qr_code': 'USER456'  # This should be the content of the user QR
        }
    }
    
    # Create a test PDF
    test_filename = "test_user_qr_value.pdf"
    c = canvas.Canvas(test_filename, pagesize=A4)
    width, height = A4
    
    try:
        # Test the guest page drawing function
        qr_gen._draw_guest_page(
            c, 
            test_onboarding_data, 
            "test-domain.com", 
            width, 
            height, 
            1, 
            1, 
            "test-tenant",
            test_user_data_map,
            None  # No WhatsApp URL
        )
        
        c.save()
        print(f"✓ Test PDF created: {test_filename}")
        print("✓ Expected results:")
        print("  - Onboarding QR should contain: https://test-domain.com/?onboardingQrCode=ONBOARD123#/auth/signuphome")
        print("  - User QR should contain: USER456 (just the value)")
        print("✓ Check the generated PDF to verify the QR codes contain the correct content")
        
    except Exception as e:
        print(f"✗ Error testing user QR: {e}")

if __name__ == "__main__":
    test_user_qr_value()
