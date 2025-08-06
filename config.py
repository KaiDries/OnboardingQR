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
        'no_options': ['n', 'no'],
        # PDF Template Translations
        'cash_configuration': 'CASH CONFIGURATION',
        'device_configuration': 'Device Configuration',
        'installation_instructions': 'Installation Instructions',
        'event': 'Event',
        'location': 'Location',
        'sales': 'Sales',
        'roles': 'Roles',
        'payment_methods': 'Payment methods',
        'no_roles_specified': 'No roles specified',
        'step1': '1 - Open StaffX MC',
        'step2': '2 - Click on ONBOARDING QR',
        'step3': '3 - Use camera - and point to the QR code above',
        'step4': '4 - Login with ClientX-QR',
        'step5': '5 - Open the event application on your smartphone',
        'step6': '6 - Open the Payment QR',
        'step7': '7 - Scan with the cash register device - the QR code on your phone',
        'whatsapp_support': 'Having problems - contact us via WhatsApp',
        'whatsapp_support_detail': 'and send us a video or photo of the problem'
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
        'no_options': ['n', 'nee'],
        # PDF Template Translations
        'cash_configuration': 'KASSA CONFIGURATIE',
        'device_configuration': 'Toestel Configuratie',
        'installation_instructions': 'Installatie Instructies',
        'event': 'Evenement',
        'location': 'Locatie',
        'sales': 'Sales',
        'roles': 'Rollen',
        'payment_methods': 'Betaalmethodes',
        'no_roles_specified': 'Geen rollen gespecifieerd',
        'step1': '1 - Open StaffX MC',
        'step2': '2 - Klik op ONBOARDING QR',
        'step3': '3 - Use camera - en richt je op de bovenstaande QR code',
        'step4': '4 - Login met ClientX-QR',
        'step5': '5 - Open de applicatie van het evenement op jouw smartphone',
        'step6': '6 - Open de Payment QR',
        'step7': '7 - Scan met het kassa toestel - de QR code op jouw gsm',
        'whatsapp_support': 'Heb je problemen - contacteer ons via WhatsApp',
        'whatsapp_support_detail': 'en stuur ons een video of foto van het probleem'
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
        'no_options': ['n', 'non'],
        # PDF Template Translations
        'cash_configuration': 'CONFIGURATION CAISSE',
        'device_configuration': 'Configuration de l\'Appareil',
        'installation_instructions': 'Instructions d\'Installation',
        'event': 'Événement',
        'location': 'Lieu',
        'sales': 'Ventes',
        'roles': 'Rôles',
        'payment_methods': 'Méthodes de paiement',
        'no_roles_specified': 'Aucun rôle spécifié',
        'step1': '1 - Ouvrir StaffX MC',
        'step2': '2 - Cliquer sur ONBOARDING QR',
        'step3': '3 - Utiliser la caméra - et pointer vers le QR code ci-dessus',
        'step4': '4 - Se connecter avec ClientX-QR',
        'step5': '5 - Ouvrir l\'application de l\'événement sur votre smartphone',
        'step6': '6 - Ouvrir le QR de Paiement',
        'step7': '7 - Scanner avec l\'appareil de caisse - le QR code sur votre téléphone',
        'whatsapp_support': 'Vous avez des problèmes - contactez-nous via WhatsApp',
        'whatsapp_support_detail': 'et envoyez-nous une vidéo ou photo du problème'
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
        'no_options': ['n', 'no'],
        # PDF Template Translations
        'cash_configuration': 'CONFIGURACIÓN DE CAJA',
        'device_configuration': 'Configuración del Dispositivo',
        'installation_instructions': 'Instrucciones de Instalación',
        'event': 'Evento',
        'location': 'Ubicación',
        'sales': 'Ventas',
        'roles': 'Roles',
        'payment_methods': 'Métodos de pago',
        'no_roles_specified': 'No se especificaron roles',
        'step1': '1 - Abrir StaffX MC',
        'step2': '2 - Hacer clic en ONBOARDING QR',
        'step3': '3 - Usar cámara - y apuntar al código QR de arriba',
        'step4': '4 - Iniciar sesión con ClientX-QR',
        'step5': '5 - Abrir la aplicación del evento en tu smartphone',
        'step6': '6 - Abrir el QR de Pago',
        'step7': '7 - Escanear con el dispositivo de caja - el código QR en tu teléfono',
        'whatsapp_support': 'Tienes problemas - contáctanos vía WhatsApp',
        'whatsapp_support_detail': 'y envíanos un video o foto del problema'
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
