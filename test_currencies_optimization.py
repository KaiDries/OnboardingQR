#!/usr/bin/env python3
"""
Test the currencies page optimization
"""

from qr_generator import QRCodeGenerator

def test_currencies_optimization():
    """Test that currencies page optimization works correctly"""
    print("Testing currencies page optimization...")
    
    qr_gen = QRCodeGenerator()
    
    # Test 1: Small list (should include currencies on overview page)
    small_list = [{"onboarding_name": f"Test-{i}"} for i in range(5)]
    needs_separate = qr_gen._needs_separate_currencies_page(small_list)
    print(f"Small list (5 items): Needs separate page = {needs_separate} (should be False)")
    
    # Test 2: Medium list (should include currencies on overview page)
    medium_list = [{"onboarding_name": f"Test-{i}"} for i in range(15)]
    needs_separate = qr_gen._needs_separate_currencies_page(medium_list)
    print(f"Medium list (15 items): Needs separate page = {needs_separate} (should be False)")
    
    # Test 3: Large list (should create separate currencies page)
    large_list = [{"onboarding_name": f"Test-{i}"} for i in range(20)]
    needs_separate = qr_gen._needs_separate_currencies_page(large_list)
    print(f"Large list (20 items): Needs separate page = {needs_separate} (should be True)")
    
    # Test 4: Very large list (should create separate currencies page)
    xl_list = [{"onboarding_name": f"Test-{i}"} for i in range(30)]
    needs_separate = qr_gen._needs_separate_currencies_page(xl_list)
    print(f"XL list (30 items): Needs separate page = {needs_separate} (should be True)")
    
    print("✓ Currencies optimization test completed")

if __name__ == "__main__":
    test_currencies_optimization()
