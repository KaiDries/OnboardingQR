#!/usr/bin/env python3
"""
Debug currencies page logic
"""

def test_currencies_threshold():
    """Test the currencies page threshold with actual count from screenshot"""
    from qr_generator import QRCodeGenerator
    
    qr_gen = QRCodeGenerator()
    
    # Count from screenshot: approximately 19 onboardings
    onboarding_count = 19
    test_list = [{"onboarding_name": f"Test-{i}"} for i in range(onboarding_count)]
    
    needs_separate = qr_gen._needs_separate_currencies_page(test_list)
    print(f"Onboarding count: {onboarding_count}")
    print(f"Threshold: 15")
    print(f"Needs separate currencies page: {needs_separate}")
    print(f"Expected: True (since {onboarding_count} > 15)")
    
    if needs_separate:
        print("✓ Logic is correct - should create separate currencies page")
    else:
        print("✗ Logic error - should create separate currencies page")

if __name__ == "__main__":
    test_currencies_threshold()
