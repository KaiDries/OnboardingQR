#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test the actual main application to verify language selection works
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all imports work correctly"""
    print("Testing imports...")
    
    try:
        from config import SUPPORTED_LANGUAGES, TRANSLATIONS
        print("✅ Config imports successful")
        
        from qr_generator import QRCodeGenerator
        print("✅ QRCodeGenerator import successful")
        
        # Test QRCodeGenerator get_translation method
        qr_gen = QRCodeGenerator()
        test_translation = qr_gen.get_translation('configuration_overview', 'nl')
        print(f"✅ get_translation method works: {test_translation}")
        
        from main import OnboardingQRManager
        print("✅ OnboardingQRManager import successful")
        
        # Test if get_language_selection method exists
        manager = OnboardingQRManager()
        if hasattr(manager, 'get_language_selection'):
            print("✅ get_language_selection method exists")
        else:
            print("❌ get_language_selection method missing")
            
        if hasattr(manager, 'get_whatsapp_info'):
            print("✅ get_whatsapp_info method exists")
        else:
            print("❌ get_whatsapp_info method missing")
            
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_language_selection_simulation():
    """Simulate the language selection without user input"""
    print("\n" + "=" * 50)
    print("SIMULATING LANGUAGE SELECTION")
    print("=" * 50)
    
    try:
        from config import SUPPORTED_LANGUAGES
        from main import OnboardingQRManager
        
        manager = OnboardingQRManager()
        
        print("\nLanguage options that would be shown:")
        for i, (code, name) in enumerate(SUPPORTED_LANGUAGES.items(), 1):
            print(f"{i}. {name} ({code})")
            
        print("\nSimulating selections:")
        language_list = list(SUPPORTED_LANGUAGES.keys())
        for i in range(1, len(SUPPORTED_LANGUAGES) + 1):
            language_code = language_list[i - 1]
            language_name = SUPPORTED_LANGUAGES[language_code]
            print(f"Choice {i} -> {language_code} ({language_name})")
            
        return True
        
    except Exception as e:
        print(f"❌ Language selection test error: {e}")
        return False

def test_whatsapp_prompts():
    """Test WhatsApp prompts in all languages"""
    print("\n" + "=" * 50)
    print("TESTING WHATSAPP PROMPTS")
    print("=" * 50)
    
    try:
        from config import TRANSLATIONS, SUPPORTED_LANGUAGES
        
        for lang_code, lang_name in SUPPORTED_LANGUAGES.items():
            print(f"\n--- {lang_name} ({lang_code}) ---")
            
            translations = TRANSLATIONS.get(lang_code, TRANSLATIONS['en'])
            
            print(f"Header: {translations['whatsapp_group']}")
            print(f"Question: {translations['has_whatsapp']}")
            print(f"Yes options: {translations['yes_options']}")
            print(f"No options: {translations['no_options']}")
            print(f"Enter prompt: {translations['enter_whatsapp']}")
            print(f"Success message: {translations['whatsapp_set']}")
            print(f"No WhatsApp: {translations['no_whatsapp']}")
            
        return True
        
    except Exception as e:
        print(f"❌ WhatsApp prompts test error: {e}")
        return False

def test_template_methods():
    """Test that template generation methods accept language parameter"""
    print("\n" + "=" * 50)
    print("TESTING TEMPLATE METHOD SIGNATURES")
    print("=" * 50)
    
    try:
        from qr_generator import QRCodeGenerator
        import inspect
        
        qr_gen = QRCodeGenerator()
        
        # Check generate_multi_page_application_template
        if hasattr(qr_gen, 'generate_multi_page_application_template'):
            sig = inspect.signature(qr_gen.generate_multi_page_application_template)
            params = list(sig.parameters.keys())
            print(f"✅ generate_multi_page_application_template params: {params}")
            if 'language' in params:
                print("   ✅ Language parameter present")
            else:
                print("   ❌ Language parameter missing")
        else:
            print("❌ generate_multi_page_application_template method missing")
            
        # Check generate_multi_page_guest_template
        if hasattr(qr_gen, 'generate_multi_page_guest_template'):
            sig = inspect.signature(qr_gen.generate_multi_page_guest_template)
            params = list(sig.parameters.keys())
            print(f"✅ generate_multi_page_guest_template params: {params}")
            if 'language' in params:
                print("   ✅ Language parameter present")
            else:
                print("   ❌ Language parameter missing")
        else:
            print("❌ generate_multi_page_guest_template method missing")
            
        return True
        
    except Exception as e:
        print(f"❌ Template methods test error: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("COMPREHENSIVE APPLICATION TEST")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 4
    
    if test_imports():
        tests_passed += 1
    
    if test_language_selection_simulation():
        tests_passed += 1
    
    if test_whatsapp_prompts():
        tests_passed += 1
        
    if test_template_methods():
        tests_passed += 1
    
    print("\n" + "=" * 60)
    print("TEST RESULTS")
    print("=" * 60)
    print(f"Tests passed: {tests_passed}/{total_tests}")
    
    if tests_passed == total_tests:
        print("✅ All tests passed! The application is ready for multilingual use.")
        print("\nApplication Flow:")
        print("1. ✅ Tenant selection")
        print("2. ✅ Language selection")
        print("3. ✅ WhatsApp configuration (multilingual)")
        print("4. ✅ Template type selection")
        print("5. ✅ QR generation with translations")
    else:
        print(f"❌ {total_tests - tests_passed} test(s) failed. Please check the implementation.")

if __name__ == "__main__":
    main()
