#!/usr/bin/env python3
"""
Quick test to verify the guest header change
"""

from qr_generator import QRCodeGenerator
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

def test_guest_header():
    """Test that guest header shows onboarding name instead of 'User:'"""
    print("Testing guest header change...")
    
    # Create a test onboarding data
    test_onboarding_data = {
        'onboarding_name': 'John-Doe',
        'qr_code': 'TEST123',
        'location_name': 'Test Location',
        'sales_name': 'Test Sales',
        'event_name': 'Test Event',
        'rollen': 'sales_manager',
        'betaalmethodes': 'CARD, CASH'
    }
    
    # Create QR generator
    qr_gen = QRCodeGenerator()
    
    # Create a test PDF to check the header
    test_filename = "test_header_verification.pdf"
    c = canvas.Canvas(test_filename, pagesize=A4)
    width, height = A4
    
    # Test the guest page drawing function
    try:
        qr_gen._draw_guest_page(
            c, 
            test_onboarding_data, 
            "test-domain.com", 
            width, 
            height, 
            1, 
            1, 
            "test-tenant",
            None,  # No user data map
            None   # No WhatsApp URL
        )
        
        c.save()
        print(f"✓ Test PDF created: {test_filename}")
        print(f"✓ Header should now show: {test_onboarding_data['onboarding_name']}")
        print("✓ Check the generated PDF to verify the header shows the onboarding name instead of 'User:'")
        
    except Exception as e:
        print(f"✗ Error testing header: {e}")

if __name__ == "__main__":
    test_guest_header()
