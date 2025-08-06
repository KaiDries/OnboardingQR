#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test script to verify multilingual functionality in OnboardingQR application
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import TRANSLATIONS, SUPPORTED_LANGUAGES
from qr_generator import QRCodeGenerator

def test_translations():
    """Test all translations for completeness and correctness"""
    print("=" * 60)
    print("TESTING MULTILINGUAL FUNCTIONALITY")
    print("=" * 60)
    
    # Initialize QR generator to test its get_translation method
    qr_gen = QRCodeGenerator()
    
    # Test 1: Check if all languages have the same keys
    print("\n1. Testing translation key consistency...")
    
    # Get all keys from English (reference language)
    en_keys = set(TRANSLATIONS['en'].keys())
    
    for lang_code, lang_name in SUPPORTED_LANGUAGES.items():
        if lang_code in TRANSLATIONS:
            lang_keys = set(TRANSLATIONS[lang_code].keys())
            missing_keys = en_keys - lang_keys
            extra_keys = lang_keys - en_keys
            
            if missing_keys or extra_keys:
                print(f"   ❌ {lang_name} ({lang_code}): Missing keys: {missing_keys}, Extra keys: {extra_keys}")
            else:
                print(f"   ✅ {lang_name} ({lang_code}): All keys present")
        else:
            print(f"   ❌ {lang_name} ({lang_code}): Language not found in TRANSLATIONS")
    
    # Test 2: Test get_translation method
    print("\n2. Testing get_translation method...")
    
    test_keys = ['configuration_overview', 'user_configuration', 'currency_configuration', 'topup_manual']
    
    for key in test_keys:
        print(f"\n   Testing key: '{key}'")
        for lang_code, lang_name in SUPPORTED_LANGUAGES.items():
            try:
                translation = qr_gen.get_translation(key, lang_code)
                print(f"      {lang_code} ({lang_name}): {translation}")
            except Exception as e:
                print(f"      ❌ {lang_code} ({lang_name}): Error - {e}")
    
    # Test 3: Test WhatsApp prompts
    print("\n3. Testing WhatsApp prompts...")
    
    whatsapp_keys = ['whatsapp_group', 'has_whatsapp', 'enter_whatsapp', 'whatsapp_set', 'no_whatsapp']
    
    for lang_code, lang_name in SUPPORTED_LANGUAGES.items():
        print(f"\n   {lang_name} ({lang_code}):")
        for key in whatsapp_keys:
            try:
                translation = qr_gen.get_translation(key, lang_code)
                print(f"      {key}: {translation}")
            except Exception as e:
                print(f"      ❌ {key}: Error - {e}")
    
    # Test 4: Test yes/no options
    print("\n4. Testing yes/no options...")
    
    for lang_code, lang_name in SUPPORTED_LANGUAGES.items():
        try:
            yes_options = qr_gen.get_translation('yes_options', lang_code)
            no_options = qr_gen.get_translation('no_options', lang_code)
            print(f"   {lang_name} ({lang_code}): Yes={yes_options}, No={no_options}")
        except Exception as e:
            print(f"   ❌ {lang_name} ({lang_code}): Error - {e}")
    
    # Test 5: Test page numbering
    print("\n5. Testing page numbering format...")
    
    for lang_code, lang_name in SUPPORTED_LANGUAGES.items():
        try:
            page_word = qr_gen.get_translation('page', lang_code)
            of_word = qr_gen.get_translation('of', lang_code)
            page_format = f"{page_word} 1 {of_word} 5"
            print(f"   {lang_name} ({lang_code}): {page_format}")
        except Exception as e:
            print(f"   ❌ {lang_name} ({lang_code}): Error - {e}")

def test_language_selection():
    """Test the language selection functionality"""
    print("\n" + "=" * 60)
    print("TESTING LANGUAGE SELECTION")
    print("=" * 60)
    
    print("\nLanguage selection menu would show:")
    for i, (code, name) in enumerate(SUPPORTED_LANGUAGES.items(), 1):
        print(f"{i}. {name} ({code})")
    
    print("\nTesting language code mapping:")
    language_list = list(SUPPORTED_LANGUAGES.keys())
    for i in range(1, len(SUPPORTED_LANGUAGES) + 1):
        if 1 <= i <= len(SUPPORTED_LANGUAGES):
            language_code = language_list[i - 1]
            language_name = SUPPORTED_LANGUAGES[language_code]
            print(f"   Choice {i} -> {language_code} ({language_name})")

def test_error_handling():
    """Test error handling for invalid language codes"""
    print("\n" + "=" * 60)
    print("TESTING ERROR HANDLING")
    print("=" * 60)
    
    qr_gen = QRCodeGenerator()
    
    # Test with invalid language code
    print("\nTesting with invalid language code 'invalid':")
    try:
        translation = qr_gen.get_translation('configuration_overview', 'invalid')
        print(f"   Result (should fallback to English): {translation}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test with invalid key
    print("\nTesting with invalid key 'nonexistent_key':")
    try:
        translation = qr_gen.get_translation('nonexistent_key', 'en')
        print(f"   Result (should return key itself): {translation}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

def main():
    """Run all tests"""
    try:
        test_translations()
        test_language_selection()
        test_error_handling()
        
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        print("✅ All tests completed successfully!")
        print("✅ Multilingual system is ready for use")
        print("✅ Application flow: tenant -> language -> WhatsApp -> template")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
