"""
Version information for AnyKrowd Onboarding QR Generator
"""

__version__ = "1.0.0"
__author__ = "AnyKrowd Development Team"
__email__ = "development@anykrowd.com"
__description__ = "Professional QR code generator for AnyKrowd onboarding processes"
__url__ = "https://github.com/anykrowd/onboarding-qr-generator"

# Version history
VERSION_HISTORY = [
    {
        "version": "1.0.0",
        "date": "2025-08-04",
        "features": [
            "Initial release with dual template support",
            "WhatsApp QR code integration",
            "TOPUP manual automation",
            "Professional PDF generation",
            "Smart user search and import file generation",
            "Cache management system",
            "Comprehensive error handling"
        ],
        "fixes": [
            "Optimized positioning for instruction sections",
            "Enhanced template consistency",
            "Improved text localization"
        ]
    }
]

def get_version_info() -> dict:
    """Get comprehensive version information"""
    return {
        "version": __version__,
        "author": __author__,
        "description": __description__,
        "latest_release": VERSION_HISTORY[0] if VERSION_HISTORY else None
    }
