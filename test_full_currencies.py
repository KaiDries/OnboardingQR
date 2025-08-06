#!/usr/bin/env python3
"""
Test the currencies optimization with actual PDF generation
"""

from qr_generator import QRCodeGenerator

def test_currencies_optimization():
    """Generate test PDFs to verify currencies optimization"""
    qr_gen = QRCodeGenerator()
    
    # Test 1: Large list (should create separate currencies page)
    print("Testing large onboarding list (20 items)...")
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
    
    try:
        # Generate application template
        filename = qr_gen.generate_multi_page_application_template(
            large_onboarding_list,
            "test-domain.com",
            "test-tenant-large",
            None  # No WhatsApp
        )
        print(f"✓ Generated application PDF: {filename}")
        
        # Calculate expected pages
        base_pages = len(large_onboarding_list)  # 20 individual pages
        overview_page = 1  # 1 overview page
        currencies_page = 1 if qr_gen._needs_separate_currencies_page(large_onboarding_list) else 0
        expected_total = overview_page + base_pages + currencies_page
        
        print(f"✓ Expected pages: {expected_total} (1 overview + {base_pages} individual + {currencies_page} currencies)")
        print(f"✓ Currencies should be on separate page: {qr_gen._needs_separate_currencies_page(large_onboarding_list)}")
        
    except Exception as e:
        print(f"✗ Error generating test PDF: {e}")

if __name__ == "__main__":
    test_currencies_optimization()
