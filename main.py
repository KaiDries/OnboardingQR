#!/usr/bin/env python3
"""
AnyKrowd Onboarding QR Code Generator
Version: 1.0.0
Author: AnyKrowd Development Team
Date: August 2025

This application generates QR codes for onboarding processes based on tenant data
from the AnyKrowd database. It supports two types of templates:
1. Application onboarding QR codes - For kassa/terminal configuration
2. Guest user onboarding QR codes - For user-specific configurations with dual QR codes

Features:
- MySQL database integration with AWS RDS
- PDF generation with professional layouts
- WhatsApp group QR code integration
- Smart user search and import file generation
- Email validation and cleaning
- Professional styling with corporate branding
- Comprehensive logging and error handling
"""

import sys
import json
import csv
import os
import shutil
import glob
import importlib
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path

# Import version information
try:
    from version import __version__, get_version_info
except ImportError:
    __version__ = "1.0.0"
    get_version_info = lambda: {"version": __version__}

# Import logging configuration
try:
    from logging_config import setup_logging, OperationLogger
except ImportError:
    # Fallback logging setup
    logging.basicConfig(level=logging.INFO)
    
    class OperationLogger:
        def __init__(self, operation: str, logger=None):
            self.operation = operation
        def __enter__(self):
            return self
        def __exit__(self, *args):
            pass

class OnboardingQRManager:
    """Main application manager for QR code generation"""
    
    def __init__(self):
        # Initialize logging
        self.logger = setup_logging() if 'setup_logging' in globals() else logging.getLogger(__name__)
        
        # Import modules dynamically after cache clearing
        self.db = None
        self.qr_gen = None
        self.tenant_data: Optional[Dict[str, Any]] = None
        
        # Import constants
        from config import APP_NAME, SUCCESS_MESSAGES, ERROR_MESSAGES, IMPORT_FILE_NAME
        self.APP_NAME = APP_NAME
        self.SUCCESS_MESSAGES = SUCCESS_MESSAGES
        self.ERROR_MESSAGES = ERROR_MESSAGES
        self.IMPORT_FILE_NAME = IMPORT_FILE_NAME
        
        self.logger.info(f"Initialized {self.APP_NAME} v{__version__}")
    
    def initialize_modules(self):
        """Initialize database and QR generator modules after cache clearing"""
        if self.db is None:
            from database import DatabaseConnection
            self.db = DatabaseConnection()
        if self.qr_gen is None:
            from qr_generator import QRCodeGenerator
            self.qr_gen = QRCodeGenerator()
    
    def clear_python_cache(self) -> None:
        """Clear Python cache files to ensure fresh imports after code changes"""
        try:
            with OperationLogger("Cache clearing", self.logger):
                # Clear __pycache__ directories
                cache_dirs = glob.glob("**/__pycache__", recursive=True)
                for cache_dir in cache_dirs:
                    if os.path.exists(cache_dir):
                        shutil.rmtree(cache_dir)
                
                # Clear .pyc files
                pyc_files = glob.glob("**/*.pyc", recursive=True)
                for pyc_file in pyc_files:
                    if os.path.exists(pyc_file):
                        os.remove(pyc_file)
                
                # Clear relevant modules from sys.modules
                modules_to_clear = [name for name in sys.modules.keys() 
                                  if any(module in name for module in ['qr_generator', 'database', 'utils', 'config'])]
                
                for module_name in modules_to_clear:
                    if module_name in sys.modules:
                        del sys.modules[module_name]
                
                # Force reimport of key modules
                if 'qr_generator' in sys.modules:
                    importlib.reload(sys.modules['qr_generator'])
                if 'database' in sys.modules:
                    importlib.reload(sys.modules['database'])
                
                self.logger.info("Python cache cleared and modules reloaded")
                print("✓ Python cache cleared and modules reloaded")
                
        except Exception as e:
            self.logger.warning(f"Cache clearing encountered an issue: {e}")
            print(f"Warning: Cache clearing encountered an issue: {e}")
            print("This won't affect functionality, continuing...")
    
    def start_process(self) -> None:
        """Main process flow with comprehensive error handling"""
        print(f"=== {self.APP_NAME} v{__version__} ===\n")
        self.logger.info("Starting onboarding QR generation process")
        
        try:
            with OperationLogger("Full QR generation process", self.logger):
                # Clear cache FIRST to ensure fresh code
                self.clear_python_cache()
                
                # Initialize modules after cache clearing
                self.initialize_modules()
                
                # Test database connectivity before proceeding
                print("Testing database connectivity...")
                if not self.db.test_network_connectivity():
                    print("\n⚠ DATABASE CONNECTIVITY ISSUE DETECTED")
                    print("The application may not function properly due to network issues.")
                    print("Possible solutions:")
                    print("1. Check your internet connection")
                    print("2. Ensure VPN is connected (if required)")
                    print("3. Check if AWS RDS is accessible from your location")
                    print("4. Contact your network administrator")
                    
                    continue_anyway = input("\nDo you want to continue anyway? (y/n): ").strip().lower()
                    if continue_anyway not in ['y', 'yes', 'j', 'ja']:
                        print("Operation cancelled due to connectivity issues")
                        return
                    else:
                        print("⚠ Continuing with limited functionality...")
                
                # Step 1: Get tenant slug
                slug = input("Enter the tenant slug: ").strip()
                if not slug:
                    self.logger.error("No tenant slug provided")
                    print("Error: Tenant slug is required")
                    return
                
                # Step 2: Find tenant
                if not self.find_tenant(slug):
                    return
                
                # Step 3: Select language
                language = self.get_language_selection()
                
                # Step 4: Ask for WhatsApp group
                whatsapp_url = self.get_whatsapp_info(language)
                
                # Step 5: Get onboarding QRs
                onboarding_qrs = self.get_onboarding_data()
                if not onboarding_qrs:
                    self.logger.warning("No onboarding QRs found for tenant")
                    print(self.ERROR_MESSAGES['no_qrs'])
                    return
                
                # Step 6: Display onboarding options
                self.display_onboarding_options(onboarding_qrs)
                
                # Step 7: Choose template type
                self.choose_template_type(onboarding_qrs, whatsapp_url, language)
                
        except KeyboardInterrupt:
            self.logger.info("Process interrupted by user")
            print("\n\nProcess interrupted by user")
        except Exception as e:
            self.logger.error(f"Unexpected error in main process: {e}", exc_info=True)
            print(f"\nUnexpected error: {e}")
        finally:
            if self.db:
                self.db.disconnect()
                self.logger.info("Database connection closed")
    
    def find_tenant(self, slug: str) -> bool:
        """Find and validate tenant with fallback options"""
        print(f"Searching for tenant with slug: {slug}")
        
        tenant = self.db.find_tenant_by_slug(slug)
        
        if tenant:
            self.tenant_data = tenant
            print(f"✓ Domain found: {tenant['domain']}")
            print(f"✓ Tenant ID: {tenant['tenant_id']}")
            
            # Create tenant variable format
            from utils import get_tenant_variable_name
            tenant_var = get_tenant_variable_name(tenant['tenant_id'])
            print(f"✓ Tenant variable: {tenant_var}")
            
            return True
        
        # No exact match found - show partial matches and options
        print(f"⚠ No exact match found for slug '{slug}'")
        
        # Search for partial matches
        partial_matches = self.db.find_partial_tenants(slug)
        
        if partial_matches:
            print(f"\nFound {len(partial_matches)} similar tenant(s):")
            for i, match in enumerate(partial_matches[:10], 1):  # Show max 10 matches
                print(f"{i}. {match['tenant_id']} -> {match['domain']}")
            
            print("\nOptions:")
            for i, match in enumerate(partial_matches[:10], 1):
                print(f"{i}. Use '{match['tenant_id']}'")
            print("9. Manual tenant setup")
            print("0. Cancel")
            
            while True:
                try:
                    choice = input(f"\nSelect option (1-{min(len(partial_matches), 10)}, 9, or 0): ").strip()
                    
                    if choice == "0":
                        print("Operation cancelled")
                        self.db.disconnect()
                        return False
                    elif choice == "9":
                        return self.manual_tenant_setup()
                    else:
                        choice_num = int(choice)
                        if 1 <= choice_num <= min(len(partial_matches), 10):
                            selected_tenant = partial_matches[choice_num - 1]
                            self.tenant_data = selected_tenant
                            print(f"✓ Selected tenant: {selected_tenant['tenant_id']} -> {selected_tenant['domain']}")
                            
                            # Create tenant variable format
                            from utils import get_tenant_variable_name
                            tenant_var = get_tenant_variable_name(selected_tenant['tenant_id'])
                            print(f"✓ Tenant variable: {tenant_var}")
                            
                            return True
                        else:
                            print(f"Please enter a number between 1 and {min(len(partial_matches), 10)}, 9, or 0")
                except ValueError:
                    print("Please enter a valid number")
        else:
            print(f"No similar tenants found for '{slug}'")
            print("\nOptions:")
            print("9. Manual tenant setup")
            print("0. Cancel")
            
            while True:
                choice = input("\nSelect option (9 or 0): ").strip()
                if choice == "0":
                    print("Operation cancelled")
                    self.db.disconnect()
                    return False
                elif choice == "9":
                    return self.manual_tenant_setup()
                else:
                    print("Please enter 9 or 0")
    
    def manual_tenant_setup(self) -> bool:
        """Allow manual tenant setup when slug is not found"""
        print("\n=== Manual Tenant Setup ===")
        print("Please provide the tenant information manually:")
        
        while True:
            tenant_id = input("Enter tenant ID: ").strip()
            if tenant_id:
                break
            print("Tenant ID is required")
        
        while True:
            domain = input("Enter domain (e.g., summercamp-2025.com): ").strip()
            if domain:
                # If domain doesn't contain a dot, suggest adding .com
                if '.' not in domain:
                    suggested_domain = f"{domain}.com"
                    use_suggestion = input(f"Domain '{domain}' seems incomplete. Use '{suggested_domain}' instead? (y/n): ").strip().lower()
                    if use_suggestion in ['y', 'yes', 'j', 'ja']:
                        domain = suggested_domain
                break
            print("Domain is required")
        
        # Create manual tenant data
        self.tenant_data = {
            'tenant_id': tenant_id,
            'domain': domain
        }
        
        print(f"✓ Manual tenant setup complete:")
        print(f"✓ Tenant ID: {tenant_id}")
        print(f"✓ Domain: {domain}")
        
        # Create tenant variable format
        from utils import get_tenant_variable_name
        tenant_var = get_tenant_variable_name(tenant_id)
        print(f"✓ Tenant variable: {tenant_var}")
        
        # Verify that the tenant database exists
        tenant_db = f"tenant-{tenant_id}"
        if not self.db.connect(tenant_db):
            print(f"⚠ Warning: Could not connect to tenant database '{tenant_db}'")
            print("This may cause issues when retrieving onboarding QRs")
            
            continue_anyway = input("Continue anyway? (y/n): ").strip().lower()
            if continue_anyway not in ['y', 'yes', 'j', 'ja']:
                print("Operation cancelled")
                self.db.disconnect()
                return False
        else:
            print(f"✓ Tenant database '{tenant_db}' is accessible")
        
        return True
    
    def get_language_selection(self) -> str:
        """Ask for language selection"""
        from config import SUPPORTED_LANGUAGES
        
        print(f"\n=== Language Selection ===")
        print("Available languages:")
        
        # Display available languages
        for i, (code, name) in enumerate(SUPPORTED_LANGUAGES.items(), 1):
            print(f"{i}. {name} ({code})")
        
        while True:
            try:
                choice = int(input("\nSelect language (1-" + str(len(SUPPORTED_LANGUAGES)) + "): "))
                if 1 <= choice <= len(SUPPORTED_LANGUAGES):
                    # Convert choice to language code
                    language_code = list(SUPPORTED_LANGUAGES.keys())[choice - 1]
                    language_name = SUPPORTED_LANGUAGES[language_code]
                    print(f"✓ Selected language: {language_name}")
                    return language_code
                print(f"Please enter a number between 1 and {len(SUPPORTED_LANGUAGES)}")
            except ValueError:
                print("Please enter a valid number")
    
    def get_whatsapp_info(self, language: str = 'en') -> Optional[str]:
        """Ask for WhatsApp group information"""
        from config import TRANSLATIONS
        
        translations = TRANSLATIONS.get(language, TRANSLATIONS['en'])
        
        print(f"\n=== {translations['whatsapp_group']} ===")
        
        while True:
            has_whatsapp = input(f"{translations['has_whatsapp']} ").strip().lower()
            yes_options = [opt.lower() for opt in translations['yes_options']]
            no_options = [opt.lower() for opt in translations['no_options']]
            
            if has_whatsapp in yes_options:
                whatsapp_url = input(f"{translations['enter_whatsapp']} ").strip()
                if whatsapp_url:
                    print(f"✓ {translations['whatsapp_set']} {whatsapp_url}")
                    return whatsapp_url
                else:
                    print("Geen WhatsApp link opgegeven")
                    return None
            elif has_whatsapp in no_options:
                print(f"✓ {translations['no_whatsapp']}")
                return None
            else:
                valid_options = translations['yes_options'] + translations['no_options']
                print(f"Please enter one of: {', '.join(valid_options)}")
    


    def get_onboarding_data(self) -> List[Dict[str, Any]]:
        """Retrieve onboarding QR data for tenant"""
        print(f"\nRetrieving onboarding QRs for tenant {self.tenant_data['tenant_id']}...")
        
        onboarding_qrs = self.db.get_onboarding_qrs(self.tenant_data['tenant_id'])
        
        if onboarding_qrs:
            print(f"✓ Found {len(onboarding_qrs)} onboarding QR(s)")
        
        return onboarding_qrs
    
    def display_onboarding_options(self, onboarding_qrs: List[Dict[str, Any]]):
        """Display available onboarding options"""
        print("\n=== Available Onboarding QRs ===")
        for i, qr in enumerate(onboarding_qrs, 1):
            print(f"{i}. {qr['onboarding_name']}")
            if qr['location_name']:
                print(f"   Location: {qr['location_name']}")
            if qr['sales_name']:
                print(f"   Sales: {qr['sales_name']}")
            if qr['event_name']:
                print(f"   Event: {qr['event_name']}")
            if qr.get('rollen'):
                print(f"   Rollen: {qr['rollen']}")
            if qr.get('betaalmethodes'):
                print(f"   Betaalmethodes: {qr['betaalmethodes']}")
            print(f"   QR Code: {qr['qr_code']}")
            print()
    
    def choose_template_type(self, onboarding_qrs: List[Dict[str, Any]], whatsapp_url: Optional[str] = None, language: str = 'en'):
        """Kies template type en genereer QR codes"""
        print("=== Template Opties ===")
        print("1. Applicatie Onboarding QR")
        print("2. Gast Gebruiker Onboarding QR")
        
        while True:
            try:
                choice = int(input("\nSelecteer template type (1 of 2): "))
                if choice in [1, 2]:
                    break
                print("Voer 1 of 2 in")
            except ValueError:
                print("Voer een geldig nummer in")
        
        if choice == 1:
            self.generate_application_qrs(onboarding_qrs, whatsapp_url, language)
        else:
            self.generate_guest_qrs(onboarding_qrs, whatsapp_url, language)
    
    def generate_application_qrs(self, onboarding_qrs: List[Dict[str, Any]], whatsapp_url: Optional[str] = None, language: str = 'en'):
        """Genereer applicatie onboarding QR codes"""
        print("\nGenereren van Applicatie Onboarding QR codes...")
        
        try:
            # Generate single multi-page PDF
            filename = self.qr_gen.generate_multi_page_application_template(
                onboarding_qrs, 
                self.tenant_data['domain'],
                self.tenant_data['tenant_id'],
                whatsapp_url,
                language=language
            )
            print(f"✓ Multi-page PDF gegenereerd: {filename}")
            print(f"✓ Bevat {len(onboarding_qrs)} onboarding QR pagina's")
            if whatsapp_url:
                print(f"✓ WhatsApp QR code toegevoegd")
            
        except Exception as e:
            print(f"✗ Fout bij genereren multi-page QR PDF: {e}")
        
        self.db.disconnect()
    
    def generate_guest_qrs(self, onboarding_qrs: List[Dict[str, Any]], whatsapp_url: Optional[str] = None, language: str = 'en'):
        """Genereer gast gebruiker onboarding QR codes"""
        print("\nGenereren van Gast Gebruiker Onboarding QR codes...")
        print("Zoeken naar gebruikersgegevens op basis van onboarding namen...")
        
        user_data_map = {}
        import_data = []
        
        for qr_data in onboarding_qrs:
            # Parse onboarding_name using utility function
            from utils import parse_onboarding_name, generate_expected_email
            firstname, lastname = parse_onboarding_name(qr_data['onboarding_name'])
            
            # Generate expected email using utility function
            expected_email = generate_expected_email(firstname, lastname, self.tenant_data['domain'])
            
            # Search for users with the expected email pattern
            users = self.db.find_user_by_onboarding_name(expected_email.split('@')[0], self.tenant_data['tenant_id'])
            
            if users:
                # Use only the FIRST user found - één user per onboarding QR
                selected_user = users[0]
                print(f"✓ Gebruiker gevonden voor {qr_data['onboarding_name']}: {selected_user.get('firstname', '')} {selected_user.get('lastname', '')} ({selected_user.get('email', expected_email)})")
                user_data_map[qr_data['onboarding_name']] = selected_user
            else:
                print(f"⚠ Geen gebruiker gevonden voor {qr_data['onboarding_name']} (verwachte email: {expected_email})")
                # Add to import file for manual processing
                import_data.append({
                    'firstname': firstname,
                    'lastname': lastname,
                    'email': expected_email
                })
        
        # Generate multi-page PDF
        try:
            filename = self.qr_gen.generate_multi_page_guest_template(
                onboarding_qrs,
                self.tenant_data['domain'],
                self.tenant_data['tenant_id'],
                user_data_map,
                whatsapp_url,
                language
            )
            print(f"✓ Multi-page gast PDF gegenereerd: {filename}")
            print(f"✓ Bevat {len(onboarding_qrs)} gast QR pagina's")
            if whatsapp_url:
                print(f"✓ WhatsApp QR code toegevoegd")
            
        except Exception as e:
            print(f"✗ Fout bij genereren multi-page gast QR PDF: {e}")
        
        # Create import file if needed
        if import_data:
            self.create_import_file(import_data)
            print(f"⚠ Import bestand aangemaakt voor {len(import_data)} ontbrekende gebruikers")
            print("Vul de gebruikersgegevens in en start het proces opnieuw zodra het klaar is")
        
        self.db.disconnect()
    
    def create_import_file(self, import_data: List[Dict[str, Any]]):
        """Create CSV import file for missing user data"""
        from utils import ensure_directory_exists
        ensure_directory_exists("output")
        filename = self.IMPORT_FILE_NAME
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['firstname', 'lastname', 'email']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for row in import_data:
                # Only write the required fields
                filtered_row = {
                    'firstname': row.get('firstname', ''),
                    'lastname': row.get('lastname', ''),
                    'email': row.get('email', '')
                }
                writer.writerow(filtered_row)
        
        print(f"✓ Created import file: {filename}")
        print("Please fill in the missing user information and save the file")

def main():
    """Main entry point with comprehensive error handling and version info"""
    try:
        # Print version information
        version_info = get_version_info()
        print(f"AnyKrowd Onboarding QR Generator v{version_info['version']}")
        print(f"Developed by: {version_info.get('author', 'AnyKrowd Development Team')}")
        print("-" * 60)
        
        # Initialize and run the manager
        manager = OnboardingQRManager()
        manager.start_process()
        
    except KeyboardInterrupt:
        print("\n\nProcess interrupted by user")
        sys.exit(0)
    except ImportError as e:
        print(f"\nMissing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"\nCritical error: {e}")
        print("Please check your configuration and try again")
        sys.exit(1)

if __name__ == "__main__":
    main()



