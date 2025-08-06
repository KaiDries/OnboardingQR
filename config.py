"""
Configuration file for AnyKrowd Onboarding QR Generator
"""

# Application Information
APP_NAME = "AnyKrowd Onboarding QR Generator"
APP_VERSION = "1.0.0"
APP_AUTHOR = "AnyKrowd Development Team"

# QR Code Settings
QR_CODE_SIZE = 140  # Size in pixels for main QR codes
QR_CODE_BORDER = 6  # Border padding around QR codes
WHATSAPP_QR_SIZE = 80  # Size for WhatsApp QR codes

# PDF Layout Settings
PDF_WIDTH = 595.27  # A4 width in points
PDF_HEIGHT = 841.89  # A4 height in points
PDF_MARGIN = 70  # Standard margin

# Colors (Hex format)
COLORS = {
    'application_primary': '#1E3A8A',  # Blue for application template
    'guest_primary': '#6A1B9A',       # Purple for guest template
    'whatsapp_green': '#25D366',       # WhatsApp official green
    'text_primary': '#000000',         # Black for main text
    'text_secondary': '#666666',       # Gray for secondary text
    'text_muted': '#999999'            # Light gray for page numbers
}

# Font Settings
FONTS = {
    'title': ('Helvetica-Bold', 32),
    'subtitle': ('Helvetica-Bold', 20),
    'header': ('Helvetica-Bold', 18),
    'body': ('Helvetica', 14),
    'small': ('Helvetica', 12),
    'tiny': ('Helvetica', 10)
}

# Database Settings (defaults - override with environment variables)
DATABASE_DEFAULTS = {
    'host': 'localhost',
    'port': 3306,
    'charset': 'utf8mb4'
}

# File Settings
OUTPUT_DIRECTORY = "output"
TEMP_DIRECTORY = "temp"
IMPORT_FILE_NAME = "missing_users_import.csv"
TOPUP_MANUAL_IMAGE = "TOPUPMANUAL.png"

# Template Settings
TEMPLATES = {
    'application': {
        'name': 'Application Onboarding QR',
        'description': 'Voor kassa/terminal configuratie',
        'instructions_count': 7,
        'supports_topup': True
    },
    'guest': {
        'name': 'Guest User Onboarding QR', 
        'description': 'Voor gebruiker-specifieke configuratie',
        'instructions_count': 5,
        'dual_qr': True,
        'supports_topup': True
    }
}

# URL Format
QR_URL_FORMAT = "https://{domain}/?onboardingQrCode={qr_code}#/auth/signuphome"

# Error Messages
ERROR_MESSAGES = {
    'no_tenant': "Tenant niet gevonden. Controleer de slug en probeer opnieuw.",
    'no_qrs': "Geen onboarding QR codes gevonden voor deze tenant.",
    'database_error': "Database verbinding mislukt. Controleer je instellingen.",
    'pdf_generation_error': "Fout bij het genereren van PDF. Probeer opnieuw."
}

# Success Messages
SUCCESS_MESSAGES = {
    'tenant_found': "✓ Tenant gevonden en gevalideerd",
    'qrs_loaded': "✓ Onboarding QR codes geladen", 
    'pdf_generated': "✓ PDF succesvol gegenereerd",
    'whatsapp_added': "✓ WhatsApp QR code toegevoegd",
    'cache_cleared': "✓ Cache opgeschoond"
}
