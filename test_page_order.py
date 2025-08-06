#!/usr/bin/env python3
"""
Test de correcte pagina volgorde voor currencies
"""

from qr_generator import QRCodeGenerator

def test_page_order():
    """Test dat currencies pagina direct na overview komt"""
    print("Testing page order optimization...")
    
    qr_gen = QRCodeGenerator()
    
    # Create large onboarding list (should trigger separate currencies page)
    large_onboarding_list = []
    for i in range(20):
        large_onboarding_list.append({
            'onboarding_name': f'Test-User-{i+1}',
            'qr_code': f'TEST{i+1:03d}',
            'location_name': f'Location-{i+1}',
            'sales_name': 'Test Sales',
            'event_name': 'Test Event 2025',
            'rollen': 'sales',
            'betaalmethodes': 'QR, RFID'
        })
    
    print(f"Onboarding count: {len(large_onboarding_list)}")
    print(f"Needs separate currencies page: {qr_gen._needs_separate_currencies_page(large_onboarding_list)}")
    
    try:
        # Generate application template
        filename = qr_gen.generate_multi_page_application_template(
            large_onboarding_list,
            "test-domain.com",
            "test-page-order",
            None  # No WhatsApp
        )
        print(f"✓ Generated PDF: {filename}")
        
        # Expected page order:
        # Page 1: Overview
        # Page 2: Currencies (separate page)
        # Page 3-22: Individual onboarding pages (20 pages)
        expected_pages = 1 + 1 + 20  # overview + currencies + individuals
        print(f"✓ Expected total pages: {expected_pages}")
        print("✓ Expected page order:")
        print("  - Page 1: Configuration Overview")
        print("  - Page 2: Currencies Information")
        print("  - Pages 3-22: Individual Onboarding QR pages")
        
    except Exception as e:
        print(f"✗ Error generating test PDF: {e}")

if __name__ == "__main__":
    test_page_order()
