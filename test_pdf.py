#!/usr/bin/env python3
"""
Quick test to generate PDF with the fixes
"""

from qr_generator import QRCodeGenerator
from database import DatabaseConnection

def quick_pdf_test():
    """Generate a quick PDF to test the fixes"""
    print("=== Quick PDF Generation Test ===\n")
    
    # Mock data for testing
    onboarding_qrs = [
        {
            'onboarding_name': 'TOPUP',
            'location_name': 'TOPUP',
            'sales_name': 'MERCH',
            'event_name': 'HANGAR',
            'qr_code': 'test123',
            'rollen': 'top_up',
            'betaalmethodes': 'CARD, CASH'
        },
        {
            'onboarding_name': 'BAR A',
            'location_name': 'BAR 1',
            'sales_name': 'BAR',
            'event_name': 'HANGAR',
            'qr_code': 'test456',
            'rollen': 'sales',
            'betaalmethodes': 'CARD, RFID'
        }
    ]
    
    qr_gen = QRCodeGenerator()
    
    try:
        filename = qr_gen.generate_multi_page_application_template(
            onboarding_qrs,
            "summercamp-2025.com",
            "summercamp-2025",
            None
        )
        print(f"✓ Generated test PDF: {filename}")
        print("Check the PDF for:")
        print("1. TOPUP showing 'CARD, CASH' instead of 'Geen'")
        print("2. Centered table layout")
        print("3. Refund date visibility under event dates")
        
    except Exception as e:
        print(f"✗ Error generating PDF: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    quick_pdf_test()
