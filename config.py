# Application Information
APP_NAME = "AnyKrowd Onboarding QR Generator"
APP_VERSION = "1.0.0"
APP_AUTHOR = "AnyKrowd Development Team"

# Multi-language Support
SUPPORTED_LANGUAGES = {
    'nl': 'Nederlands',
    'en': 'English', 
    'fr': 'Français',
    'es': 'Español'
}

# Translations for templates
TRANSLATIONS = {
    'en': {
        'configuration_overview': 'CONFIGURATION OVERVIEW',
        'user_overview': 'USER OVERVIEW',
        'page': 'Page',
        'of': 'of',
        'user_configuration': 'USER CONFIGURATION',
        'currency_configuration': 'CURRENCY CONFIGURATION',
        'topup_manual': 'TOP-UP MANUAL',
        'whatsapp_group': 'WhatsApp Group Configuration',
        'has_whatsapp': 'Is there a WhatsApp group for this event? (y/n):',
        'enter_whatsapp': 'Enter the WhatsApp group link:',
        'whatsapp_set': 'WhatsApp group set:',
        'no_whatsapp': 'No WhatsApp group configured',
        'yes_options': ['y', 'yes'],
        'no_options': ['n', 'no']
    },
    'nl': {
        'configuration_overview': 'CONFIGURATIE OVERZICHT',
        'user_overview': 'GEBRUIKERS OVERZICHT',
        'page': 'Pagina',
        'of': 'van',
        'user_configuration': 'GEBRUIKER CONFIGURATIE',
        'currency_configuration': 'VALUTA CONFIGURATIE',
        'topup_manual': 'OPWAARDEREN HANDLEIDING',
        'whatsapp_group': 'WhatsApp Groep Configuratie',
        'has_whatsapp': 'Is er een WhatsApp groep voor dit event? (j/n):',
        'enter_whatsapp': 'Voer de WhatsApp groep link in:',
        'whatsapp_set': 'WhatsApp groep ingesteld:',
        'no_whatsapp': 'Geen WhatsApp groep geconfigureerd',
        'yes_options': ['j', 'ja'],
        'no_options': ['n', 'nee']
    },
    'fr': {
        'configuration_overview': 'APERÇU DE CONFIGURATION',
        'user_overview': 'APERÇU DES UTILISATEURS',
        'page': 'Page',
        'of': 'de',
        'user_configuration': 'CONFIGURATION UTILISATEUR',
        'currency_configuration': 'CONFIGURATION DE DEVISE',
        'topup_manual': 'MANUEL DE RECHARGE',
        'whatsapp_group': 'Configuration du Groupe WhatsApp',
        'has_whatsapp': 'Y a-t-il un groupe WhatsApp pour cet événement? (o/n):',
        'enter_whatsapp': 'Entrez le lien du groupe WhatsApp:',
        'whatsapp_set': 'Groupe WhatsApp configuré:',
        'no_whatsapp': 'Pas de groupe WhatsApp configuré',
        'yes_options': ['o', 'oui'],
        'no_options': ['n', 'non']
    },
    'es': {
        'configuration_overview': 'RESUMEN DE CONFIGURACIÓN',
        'user_overview': 'RESUMEN DE USUARIOS',
        'page': 'Página',
        'of': 'de',
        'user_configuration': 'CONFIGURACIÓN DE USUARIO',
        'currency_configuration': 'CONFIGURACIÓN DE MONEDA',
        'topup_manual': 'MANUAL DE RECARGA',
        'whatsapp_group': 'Configuración del Grupo WhatsApp',
        'has_whatsapp': '¿Hay un grupo de WhatsApp para este evento? (s/n):',
        'enter_whatsapp': 'Introduce el enlace del grupo WhatsApp:',
        'whatsapp_set': 'Grupo WhatsApp configurado:',
        'no_whatsapp': 'No hay grupo WhatsApp configurado',
        'yes_options': ['s', 'si', 'sí'],
        'no_options': ['n', 'no']
    }
}

# Error Messages
ERROR_MESSAGES = {
    'no_tenant': "Tenant niet gevonden. Controleer de slug en probeer opnieuw.",
    'no_qrs': "Geen onboarding QR codes gevonden voor deze tenant.",
    'database_error': "Database verbinding mislukt. Controleer je instellingen.",
    'pdf_generation_error': "Fout bij het genereren van PDF. Probeer opnieuw."
}

# Success Messages
SUCCESS_MESSAGES = {
    'tenant_found': " Tenant gevonden en gevalideerd",
    'qrs_loaded': " Onboarding QR codes geladen", 
    'pdf_generated': " PDF succesvol gegenereerd",
    'whatsapp_added': " WhatsApp QR code toegevoegd",
    'cache_cleared': " Cache opgeschoond"
}

# File Settings
IMPORT_FILE_NAME = "missing_users_import.csv"
