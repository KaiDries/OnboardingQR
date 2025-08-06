import qrcode
from PIL import Image, ImageDraw, ImageFont
import os
from typing import Dict, Any, List
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
import io
from datetime import datetime

class QRCodeGenerator:
    def __init__(self):
        self.qr_size = 200
        self.template_dir = "templates"
        
    def get_translation(self, key: str, language: str = 'en') -> str:
        """Get translation for a key in the specified language"""
        from config import TRANSLATIONS
        
        # Use the specified language or fall back to English if not available
        translations = TRANSLATIONS.get(language, TRANSLATIONS['en'])
        
        # Return the translation for the key or the key itself if not found
        return translations.get(key, key)
    
    def _map_to_central_tenant_id(self, tenant_id: str) -> str:
        """Map tenant ID from local database format to central database format"""
        # Known mappings between tenant database names and central database IDs
        tenant_mappings = {
            "summercamp-2025": "summercamp",
            # Add more mappings as needed
        }
        
        return tenant_mappings.get(tenant_id, tenant_id)
        
    def generate_qr_url(self, domain: str, qr_code: str) -> str:
        """Generate the QR URL based on domain and QR code"""
        return f"https://{domain}/?onboardingQrCode={qr_code}#/auth/signuphome"
    
    def create_qr_code(self, url: str, size: int = None) -> Image.Image:
        """Create QR code image from URL"""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        
        qr_img = qr.make_image(fill_color="black", back_color="white")
        
        if size:
            qr_img = qr_img.resize((size, size), Image.Resampling.LANCZOS)
        
        return qr_img
    
    def generate_multi_page_application_template(self, onboarding_list: List[Dict[str, Any]], domain: str, tenant_name: str, whatsapp_url: str = None, language: str = 'en') -> str:
        """Generate a single multi-page PDF for all application onboarding QR codes"""
        filename = f"onboarding_app_{tenant_name}_all.pdf"
        c = canvas.Canvas(filename, pagesize=A4)
        width, height = A4
        
        page_count = 0
        total_pages = self._calculate_total_pages(onboarding_list) + 1  # +1 for configuration overview only
        
        # Page 1: Configuration Overview (table format) - ALLEEN deze pagina
        page_count += 1
        self._draw_configuration_overview_page(c, onboarding_list, tenant_name, domain, width, height, page_count, total_pages, "APPLICATION", None, language)
        
        # Page 2: Add separate currencies page if needed (directly after overview)
        if self._needs_separate_currencies_page(onboarding_list):
            page_count += 1
            c.showPage()  # Start new page for currencies
            self._draw_currencies_page(c, tenant_name, domain, width, height, page_count, total_pages, "APPLICATION", language)
        
        for onboarding_data in onboarding_list or []:
            page_count += 1
            c.showPage()  # Start new page
            
            # Draw main onboarding page
            self._draw_application_page(c, onboarding_data, domain, width, height, page_count, total_pages, tenant_name, whatsapp_url, language)
            
            # Check if TOPUP role is present and add manual page
            if self._has_topup_role(onboarding_data):
                page_count += 1
                c.showPage()  # Start new page for TOPUP manual
                self._draw_topup_manual_page(c, onboarding_data, width, height, page_count, total_pages, tenant_name, language)
        
        c.save()
        return filename
    
    def _calculate_total_pages(self, onboarding_list: List[Dict[str, Any]]) -> int:
        """Calculate total number of pages including TOPUP manual pages and currencies page"""
        if not onboarding_list:
            return 0
            
        total = len(onboarding_list)  # Base pages
        
        # Add extra pages for TOPUP roles
        for onboarding_data in onboarding_list:
            if self._has_topup_role(onboarding_data):
                total += 1
        
        # Add extra page for currencies if needed
        if self._needs_separate_currencies_page(onboarding_list):
            total += 1
        
        return total
    
    def _has_topup_role(self, onboarding_data: Dict[str, Any]) -> bool:
        """Check if onboarding data contains TOPUP role"""
        roles = onboarding_data.get('rollen', '')
        if roles:
            # Check if TOPUP or TOP_UP is in the roles string (case insensitive)
            roles_lower = roles.lower()
            return 'topup' in roles_lower or 'top_up' in roles_lower or 'top-up' in roles_lower
        return False
    
    def _draw_application_page(self, canvas_obj, onboarding_data: Dict[str, Any], domain: str, width: float, height: float, page_num: int, total_pages: int, tenant_name: str = None, whatsapp_url: str = None, language: str = 'en'):
        """Draw a single application onboarding page with clean, simple layout"""
        qr_url = self.generate_qr_url(domain, onboarding_data['qr_code'])
        qr_img = self.create_qr_code(qr_url, 200)
        
        # Header section with background
        canvas_obj.setFillColor("#1B4F72")
        canvas_obj.rect(0, height - 120, width, 120, fill=1)
        
        # Main title
        canvas_obj.setFillColor("#FFFFFF")
        canvas_obj.setFont("Helvetica-Bold", 32)
        canvas_obj.drawCentredString(width/2, height - 40, "KASSA CONFIGURATIE")
        
        # Onboarding QR name
        canvas_obj.setFont("Helvetica-Bold", 18)
        canvas_obj.drawCentredString(width/2, height - 65, f"{onboarding_data['onboarding_name']}")
        
        # Reset to black for main content
        canvas_obj.setFillColor("#000000")
        
        # Step 1 section
        y_pos = height - 120  # Adjusted up since we removed page number
        y_pos -= 30
        canvas_obj.setFont("Helvetica-Bold", 20)
        canvas_obj.setFillColor("#1B4F72")
        canvas_obj.drawCentredString(width/2, y_pos, 'Toestel Configuratie')
        
        # Underline for Toestel Configuratie
        canvas_obj.setStrokeColor("#1B4F72")
        canvas_obj.setLineWidth(2)
        canvas_obj.line(width/2 - 80, y_pos - 5, width/2 + 80, y_pos - 5)
        
        # QR Code (left side)
        qr_temp_path = f"temp_qr_{page_num}.png"
        qr_img.save(qr_temp_path)
        
        qr_x = 50
        qr_y = y_pos - 250
        canvas_obj.drawImage(qr_temp_path, qr_x, qr_y, 200, 200)
        
        # QR code border
        canvas_obj.setStrokeColor("#1B4F72")
        canvas_obj.setLineWidth(4)
        canvas_obj.rect(qr_x - 10, qr_y - 10, 220, 220, fill=0)
        
        # GECENTREERDE EVENT INFORMATIE (right side of QR) - GECENTREERD OP QR MIDDLE
        info_x = 280
        qr_middle_y = qr_y + 100  # Middle of the 200px QR code
        info_y = qr_middle_y + 50  # Start above the middle and work down
        
        # Just plain text, no formatting
        canvas_obj.setFillColor("#000000")
        canvas_obj.setFont("Helvetica-Bold", 12)
        
        if onboarding_data['event_name']:
            canvas_obj.drawString(info_x, info_y, f"Evenement: {onboarding_data['event_name']}")
            info_y -= 25
        
        if onboarding_data['location_name']:
            canvas_obj.drawString(info_x, info_y, f"Locatie: {onboarding_data['location_name']}")
            info_y -= 25
        
        if onboarding_data['sales_name']:
            canvas_obj.drawString(info_x, info_y, f"Sales: {onboarding_data['sales_name']}")
            info_y -= 25
        
        # Display roles from database or fallback text
        roles_text = onboarding_data.get('rollen') or "Geen rollen gespecifieerd"
        canvas_obj.drawString(info_x, info_y, f"Rollen: {roles_text}")
        info_y -= 25
        
        # Display payment methods if sales role is present AND not top_up role
        roles_text = onboarding_data.get('rollen', '').lower()
        if onboarding_data.get('betaalmethodes') and 'top_up' not in roles_text:
            canvas_obj.drawString(info_x, info_y, f"Betaalmethodes: {onboarding_data['betaalmethodes']}")
            info_y -= 25
        
        # Step 2 section - adjusted position for payment methods
        step2_y = qr_y - 90  # Moved down to accommodate payment methods
        canvas_obj.setFont("Helvetica-Bold", 20)
        canvas_obj.setFillColor("#1B4F72")
        canvas_obj.drawCentredString(width/2, step2_y, "Installatie Instructies")
        
        # Underline for Installatie Instructies
        canvas_obj.setStrokeColor("#1B4F72")
        canvas_obj.setLineWidth(2)
        canvas_obj.line(width/2 - 90, step2_y - 5, width/2 + 90, step2_y - 5)
        
        canvas_obj.setFillColor("#000000")
        step2_y -= 50
        
        # Instructions without box - clean text display
        canvas_obj.setFillColor("#000000")
        canvas_obj.setFont("Helvetica", 14)
        
        # New 7-step instructions with better spacing
        canvas_obj.drawString(70, step2_y, "1 - Open Staffx MC")
        step2_y -= 25
        canvas_obj.drawString(70, step2_y, "2 - Klik op ONBOARDING QR")
        step2_y -= 25
        canvas_obj.drawString(70, step2_y, "3 - Use camera - en richt je op de bovenstaande QR code")
        step2_y -= 25
        canvas_obj.drawString(70, step2_y, "4 - Login met ClientX-QR")
        step2_y -= 25
        canvas_obj.drawString(70, step2_y, "5 - Open de applicatie van het evenement op jouw smartphone")
        step2_y -= 25
        canvas_obj.drawString(70, step2_y, "6 - Open de Payment QR")
        step2_y -= 25
        canvas_obj.drawString(70, step2_y, "7 - Scan met het kassa toestel - de QR code op jouw gsm")
        
        # Support text - alleen tonen als WhatsApp URL beschikbaar is
        if whatsapp_url:
            canvas_obj.setFont("Helvetica-Bold", 12)
            canvas_obj.setFillColor("#1B4F72")
            canvas_obj.drawCentredString(width/2, 70, "Heb je problemen - contacteer ons via WhatsApp")
            canvas_obj.setFont("Helvetica", 11)
            canvas_obj.drawCentredString(width/2, 55, "en stuur ons een video of foto van het probleem")
        
        # WhatsApp QR code rechts onderaan (als opgegeven)
        if whatsapp_url:
            whatsapp_qr_size = 80  # Kleinere QR code voor WhatsApp
            whatsapp_x = width - whatsapp_qr_size - 30  # 30pt van rechter rand voor meer ruimte
            whatsapp_y = 50  # Net boven footer
            
            # Generate WhatsApp QR code
            whatsapp_qr = qrcode.QRCode(version=1, box_size=10, border=4)
            whatsapp_qr.add_data(whatsapp_url)
            whatsapp_qr.make(fit=True)
            whatsapp_qr_img = whatsapp_qr.make_image(fill_color="black", back_color="white")
            
            # Save temporary WhatsApp QR file
            whatsapp_temp_path = "temp_whatsapp_qr.png"
            whatsapp_qr_img.save(whatsapp_temp_path)
            
            # Draw groene achtergrond kader (zoals in voorbeeld)
            kader_padding = 8
            kader_x = whatsapp_x - kader_padding
            kader_y = whatsapp_y - kader_padding
            kader_size = whatsapp_qr_size + (kader_padding * 2)
            
            # Groene achtergrond kader met afgeronde hoeken effect
            canvas_obj.setFillColor("#25D366")  # WhatsApp groen
            canvas_obj.setStrokeColor("#25D366")
            canvas_obj.setLineWidth(3)
            canvas_obj.roundRect(kader_x, kader_y, kader_size, kader_size, 8, fill=1, stroke=1)
            
            # Witte binnenrand
            inner_padding = 3
            inner_x = kader_x + inner_padding
            inner_y = kader_y + inner_padding
            inner_size = kader_size - (inner_padding * 2)
            canvas_obj.setFillColor("white")
            canvas_obj.setStrokeColor("white")
            canvas_obj.roundRect(inner_x, inner_y, inner_size, inner_size, 5, fill=1, stroke=1)
            
            # Draw WhatsApp QR code
            canvas_obj.drawImage(whatsapp_temp_path, whatsapp_x, whatsapp_y, whatsapp_qr_size, whatsapp_qr_size)
            
            # Add WhatsApp label onder de QR code (groen kader)
            label_y = kader_y - 20
            label_width = kader_size
            label_height = 15
            
            # Groene label achtergrond
            canvas_obj.setFillColor("#25D366")
            canvas_obj.setStrokeColor("#25D366")
            canvas_obj.roundRect(kader_x, label_y, label_width, label_height, 5, fill=1, stroke=1)
            
            # Witte tekst op groene achtergrond
            canvas_obj.setFont("Helvetica-Bold", 9)
            canvas_obj.setFillColor("white")
            canvas_obj.drawCentredString(kader_x + label_width/2, label_y + 3, "Scan met camera")
            
            # Clean up WhatsApp QR file
            if os.path.exists(whatsapp_temp_path):
                os.remove(whatsapp_temp_path)
        
        # NIEUWE FOOTER - anyKrowd NV met timestamp en CLIENT - GECENTREERD
        canvas_obj.setFont("Helvetica", 10)
        canvas_obj.setFillColor("#666666")
        current_time = datetime.now().strftime("%d/%m/%Y %H:%M")
        client_info = f"CLIENT: {tenant_name}" if tenant_name else ""
        footer_text = f"anyKrowd NV - gegenereerd op: {current_time} - {client_info}"
        canvas_obj.drawCentredString(width/2, 30, footer_text)
        
        # Pagina informatie links onderaan
        canvas_obj.setFont("Helvetica", 9)
        canvas_obj.setFillColor("#999999")
        canvas_obj.drawString(20, 15, f"Pagina {page_num} van {total_pages}")
        
        # Clean up temp QR file
        if os.path.exists(qr_temp_path):
            os.remove(qr_temp_path)
    
    def generate_multi_page_guest_template(self, onboarding_list: List[Dict[str, Any]], domain: str, tenant_name: str, user_data_map: Dict[str, Dict[str, Any]] = None, whatsapp_url: str = None, language: str = 'en') -> str:
        """Generate a single multi-page PDF for all guest user onboarding QR codes"""
        # Ensure onboarding_list is not None
        if onboarding_list is None:
            onboarding_list = []
        
        filename = f"onboarding_guest_{tenant_name}_all.pdf"
        c = canvas.Canvas(filename, pagesize=A4)
        width, height = A4
        
        page_count = 0
        total_pages = self._calculate_total_pages_guest(onboarding_list) + 1  # +1 for configuration overview only
        
        # Page 1: Configuration Overview (table format)
        page_count += 1
        self._draw_configuration_overview_page(c, onboarding_list, tenant_name, domain, width, height, page_count, total_pages, "GUEST", user_data_map, language)
        
        # Page 2: Add separate currencies page if needed (directly after overview)
        if self._needs_separate_currencies_page(onboarding_list):
            page_count += 1
            c.showPage()  # Start new page for currencies
            self._draw_currencies_page(c, tenant_name, domain, width, height, page_count, total_pages, "GUEST", language)
        
        for onboarding_data in onboarding_list or []:
            page_count += 1
            c.showPage()
            
            # Draw main guest page
            self._draw_guest_page(c, onboarding_data, domain, width, height, page_count, total_pages, tenant_name, user_data_map, whatsapp_url, language)
            
            # Check if TOPUP role is present and add manual page
            if self._has_topup_role(onboarding_data):
                page_count += 1
                c.showPage()  # Start new page for TOPUP manual
                self._draw_topup_manual_page_guest(c, onboarding_data, width, height, page_count, total_pages, tenant_name)
        
        c.save()
        return filename
    
    def _calculate_total_pages_guest(self, onboarding_list: List[Dict[str, Any]]) -> int:
        """Calculate total number of pages for guest template including TOPUP manual pages and currencies page"""
        if not onboarding_list:
            return 0
            
        total = len(onboarding_list)  # Base pages
        
        # Add extra pages for TOPUP roles
        for onboarding_data in onboarding_list:
            if self._has_topup_role(onboarding_data):
                total += 1
        
        # Add extra page for currencies if needed
        if self._needs_separate_currencies_page(onboarding_list):
            total += 1
        
        return total
    
    def _needs_separate_currencies_page(self, onboarding_list: List[Dict[str, Any]]) -> bool:
        """Check if we need a separate page for currencies based on number of onboardings"""
        if not onboarding_list:
            return False
        
        # If more than 15 onboardings, put currencies on separate page
        # This leaves enough space for proper layout
        return len(onboarding_list) > 15
    
    def _draw_guest_page(self, canvas_obj, onboarding_data: Dict[str, Any], domain: str, width: float, height: float, page_num: int, total_pages: int, tenant_name: str = None, user_data_map: Dict[str, Dict[str, Any]] = None, whatsapp_url: str = None, language: str = 'en'):
        """Draw a single guest onboarding page with same layout as application but 2 QR codes"""
        qr_url = self.generate_qr_url(domain, onboarding_data['qr_code'])
        qr_img = self.create_qr_code(qr_url, 140)  # Smaller QR code
        
        # Get user data if available
        user_data = user_data_map.get(onboarding_data['onboarding_name']) if user_data_map else None
        user_email = user_data.get('email', '') if user_data else ''
        
        # Create User QR code - users from database always have RFID tag QR codes
        if user_data and user_data.get('qr_code'):
            user_qr_img = self.create_qr_code(user_data.get('qr_code'), 140)  # User's RFID tag QR code
        else:
            # This should not happen with the INNER JOIN query, but keep as safety fallback
            user_qr_img = None
        
        # Header section with background (using guest purple color)
        canvas_obj.setFillColor("#6A1B9A")  # Purple background for guest
        canvas_obj.rect(0, height - 120, width, 120, fill=1)
        
        # Main title - changed to KASSA CONFIGURATIE
        canvas_obj.setFillColor("#FFFFFF")
        canvas_obj.setFont("Helvetica-Bold", 32)
        canvas_obj.drawCentredString(width/2, height - 40, "KASSA CONFIGURATIE")
        
        # Show onboarding name instead of "User:"
        canvas_obj.setFont("Helvetica-Bold", 18)
        canvas_obj.drawCentredString(width/2, height - 65, onboarding_data['onboarding_name'])
        
        # Reset to black for main content
        canvas_obj.setFillColor("#000000")
        
        # Section divider
        y_pos = height - 120
        canvas_obj.setStrokeColor("#6A1B9A")
        canvas_obj.setLineWidth(3)
        canvas_obj.line(50, y_pos, width - 50, y_pos)
        
        # Step 1 section
        y_pos -= 30
        canvas_obj.setFont("Helvetica-Bold", 20)
        canvas_obj.setFillColor("#6A1B9A")
        canvas_obj.drawCentredString(width/2, y_pos, "Toestel Configuratie")
        
        # Underline for Toestel Configuratie
        canvas_obj.setStrokeColor("#6A1B9A")
        canvas_obj.setLineWidth(2)
        canvas_obj.line(width/2 - 80, y_pos - 5, width/2 + 80, y_pos - 5)
        
        # QR Codes (left: Onboarding QR, right: User QR) - optimized positioning
        qr_temp_path = f"temp_guest_qr_{page_num}.png"
        qr_img.save(qr_temp_path)
        
        # Calculate perfect positioning for balanced layout
        qr_size = 140
        border_padding = 6
        total_qr_width = qr_size + (border_padding * 2)
        
        # Left QR code (Onboarding QR) - perfectly positioned
        qr_left_x = 70  # More space from left edge
        qr_y = y_pos - 190  # Adjusted height for better spacing
        canvas_obj.drawImage(qr_temp_path, qr_left_x, qr_y, qr_size, qr_size)
        
        # Left QR code border - clean and consistent
        canvas_obj.setStrokeColor("#6A1B9A")
        canvas_obj.setLineWidth(2)
        canvas_obj.rect(qr_left_x - border_padding, qr_y - border_padding, 
                       qr_size + (border_padding * 2), qr_size + (border_padding * 2), fill=0)
        
        # Left QR label
        canvas_obj.setFont("Helvetica-Bold", 11)
        canvas_obj.setFillColor("#6A1B9A")
        canvas_obj.drawCentredString(qr_left_x + (qr_size/2), qr_y - 20, "ONBOARDING QR")
        
        # Right QR code (User QR) - only if available
        qr_right_x = width - qr_size - 70  # Same margin as left
        if user_qr_img:
            user_qr_temp_path = f"temp_user_qr_{page_num}.png"
            user_qr_img.save(user_qr_temp_path)
            canvas_obj.drawImage(user_qr_temp_path, qr_right_x, qr_y, qr_size, qr_size)
            
            # Right QR code border - identical to left
            canvas_obj.setStrokeColor("#6A1B9A")
            canvas_obj.setLineWidth(2)
            canvas_obj.rect(qr_right_x - border_padding, qr_y - border_padding, 
                           qr_size + (border_padding * 2), qr_size + (border_padding * 2), fill=0)
            
            # Right QR label
            canvas_obj.setFont("Helvetica-Bold", 11)
            canvas_obj.setFillColor("#6A1B9A")
            canvas_obj.drawCentredString(qr_right_x + (qr_size/2), qr_y - 20, "USER QR")
        else:
            # No user QR available - show placeholder
            canvas_obj.setStrokeColor("#CCCCCC")
            canvas_obj.setLineWidth(2)
            canvas_obj.rect(qr_right_x - border_padding, qr_y - border_padding, 
                           qr_size + (border_padding * 2), qr_size + (border_padding * 2), fill=0)
            
            # Placeholder text
            canvas_obj.setFont("Helvetica", 10)
            canvas_obj.setFillColor("#999999")
            canvas_obj.drawCentredString(qr_right_x + (qr_size/2), qr_y + (qr_size/2), "Geen USER QR")
            canvas_obj.drawCentredString(qr_right_x + (qr_size/2), qr_y + (qr_size/2) - 15, "beschikbaar")
        
        # GECENTREERDE EVENT INFORMATIE - perfectly centered between QR codes
        # Calculate center position between the two QR codes
        left_qr_end = qr_left_x + qr_size + border_padding
        right_qr_start = qr_right_x - border_padding
        center_space_width = right_qr_start - left_qr_end
        info_center_x = left_qr_end + (center_space_width / 2)
        
        # Start from top of QR codes and work down
        info_y = qr_y + qr_size - 10  # Start near top of QR codes
        
        # Event information - centered and well-structured with improved formatting
        canvas_obj.setFillColor("#000000")
        
        # Event with improved centered formatting
        if onboarding_data['event_name']:
            # Bold label
            canvas_obj.setFont("Helvetica-Bold", 13)
            canvas_obj.drawCentredString(info_center_x, info_y, "Event:")
            info_y -= 18
            # Answer on new line
            canvas_obj.setFont("Helvetica", 12)
            canvas_obj.drawCentredString(info_center_x, info_y, f"{onboarding_data['event_name']}")
            info_y -= 28  # Extra spacing between sections
        
        if onboarding_data['location_name']:
            # Bold label
            canvas_obj.setFont("Helvetica-Bold", 13)
            canvas_obj.drawCentredString(info_center_x, info_y, "Locatie:")
            info_y -= 18
            # Answer on new line
            canvas_obj.setFont("Helvetica", 12)
            canvas_obj.drawCentredString(info_center_x, info_y, f"{onboarding_data['location_name']}")
            info_y -= 28  # Extra spacing between sections
        
        if onboarding_data['sales_name']:
            # Bold label
            canvas_obj.setFont("Helvetica-Bold", 13)
            canvas_obj.drawCentredString(info_center_x, info_y, "Menu:")
            info_y -= 18
            # Answer on new line
            canvas_obj.setFont("Helvetica", 12)
            canvas_obj.drawCentredString(info_center_x, info_y, f"{onboarding_data['sales_name']}")
            info_y -= 28  # Extra spacing between sections
        
        # Display roles from database or fallback text
        roles_text = onboarding_data.get('rollen') or "Geen rollen gespecifieerd"
        # Bold label
        canvas_obj.setFont("Helvetica-Bold", 13)
        canvas_obj.drawCentredString(info_center_x, info_y, "Rollen:")
        info_y -= 18
        # Answer on new line
        canvas_obj.setFont("Helvetica", 12)
        canvas_obj.drawCentredString(info_center_x, info_y, f"{roles_text}")
        info_y -= 28  # Extra spacing between sections
        
        # Display payment methods if sales role is present AND not top_up role
        roles_text_lower = onboarding_data.get('rollen', '').lower()
        if onboarding_data.get('betaalmethodes') and 'top_up' not in roles_text_lower:
            # Bold label
            canvas_obj.setFont("Helvetica-Bold", 13)
            canvas_obj.drawCentredString(info_center_x, info_y, "Betaalmethodes:")
            info_y -= 18
            # Answer on new line
            canvas_obj.setFont("Helvetica", 11)  # Slightly smaller for payment methods
            canvas_obj.drawCentredString(info_center_x, info_y, f"{onboarding_data['betaalmethodes']}")
            info_y -= 28  # Extra spacing between sections
        
        # Step 2 section - Installatie Instructies (positioned dynamically below information)
        # Calculate position based on where the information ended
        calculated_step2_y = info_y - 20  # Position below the last information item with some spacing
        
        # Ensure minimum distance below QR codes 
        # QR codes are at qr_y = y_pos - 190, with size 140
        qr_bottom = (y_pos - 190) - 140  # Bottom of QR codes
        minimum_step2_y = qr_bottom - 40  # Minimum position with 40pt padding below QR codes
        
        # Use the lower position (further down the page) of the two
        step2_y = min(calculated_step2_y, minimum_step2_y)
        
        canvas_obj.setFont("Helvetica-Bold", 20)
        canvas_obj.setFillColor("#6A1B9A")
        canvas_obj.drawCentredString(width/2, step2_y, "Installatie Instructies")
        
        # Underline for Installatie Instructies
        canvas_obj.setStrokeColor("#6A1B9A")
        canvas_obj.setLineWidth(2)
        canvas_obj.line(width/2 - 90, step2_y - 5, width/2 + 90, step2_y - 5)
        
        canvas_obj.setFillColor("#000000")
        step2_y -= 35
        
        # Instructions with consistent formatting and spacing
        canvas_obj.setFillColor("#000000")
        canvas_obj.setFont("Helvetica", 14)
        instruction_line_height = 24  # Consistent line spacing
        
        # 5-step instructions with perfect alignment
        instructions = [
            "1 - Open Staffx MC (indien nog niet geopend)",
            "2 - Klik op ONBOARDING QR",
            "3 - Use camera - en scan de ONBOARDING QR",
            "4 - Login met ClientX-QR",
            "5 - Use camera - en scan de USER QR"
        ]
        
        for instruction in instructions:
            canvas_obj.drawString(70, step2_y, instruction)
            step2_y -= instruction_line_height
        
        step2_y -= 10  # Extra space before tip
        
        # Tip section with better formatting
        canvas_obj.setFont("Helvetica-Bold", 13)
        canvas_obj.setFillColor("#6A1B9A")
        canvas_obj.drawString(70, step2_y, "Tip:")
        canvas_obj.setFont("Helvetica", 12)
        canvas_obj.setFillColor("#000000")
        step2_y -= 22
        canvas_obj.drawString(70, step2_y, "Als je een van de 2 QR codes moet scannen - leg je hand even op de")
        step2_y -= 18
        canvas_obj.drawString(70, step2_y, "andere QR om problemen te vermijden.")
        
        # Support text - alleen tonen als WhatsApp URL beschikbaar is
        if whatsapp_url:
            canvas_obj.setFont("Helvetica-Bold", 12)
            canvas_obj.setFillColor("#6A1B9A")  # Guest template kleur
            canvas_obj.drawCentredString(width/2, 70, "Heb je problemen - contacteer ons via WhatsApp")
            canvas_obj.setFont("Helvetica", 11)
            canvas_obj.drawCentredString(width/2, 55, "en stuur ons een video of foto van het probleem")
        
        # User email address - gecentreerd boven de footer
        if user_email:
            canvas_obj.setFont("Helvetica-Bold", 12)
            canvas_obj.setFillColor("#6A1B9A")
            canvas_obj.drawCentredString(width/2, 45, f"User: {user_email}")
        
        # Pagina informatie links onderaan in footer
        canvas_obj.setFont("Helvetica", 9)
        canvas_obj.setFillColor("#999999")
        canvas_obj.drawString(20, 15, f"Pagina {page_num} van {total_pages}")
        
        # NIEUWE FOOTER VOOR GUEST - anyKrowd NV met timestamp en CLIENT - GECENTREERD
        canvas_obj.setFont("Helvetica", 10)
        canvas_obj.setFillColor("#666666")
        current_time = datetime.now().strftime("%d/%m/%Y %H:%M")
        client_info = f"CLIENT: {tenant_name}" if tenant_name else ""
        guest_footer_text = f"anyKrowd NV - gegenereerd op: {current_time} - {client_info}"
        canvas_obj.drawCentredString(width/2, 30, guest_footer_text)
        
        # WhatsApp QR code rechts onderaan (als opgegeven)
        if whatsapp_url:
            whatsapp_qr_size = 80  # Kleinere QR code voor WhatsApp
            whatsapp_x = width - whatsapp_qr_size - 30  # 30pt van rechter rand voor meer ruimte
            whatsapp_y = 50  # Net boven footer
            
            # Generate WhatsApp QR code
            whatsapp_qr = qrcode.QRCode(version=1, box_size=10, border=4)
            whatsapp_qr.add_data(whatsapp_url)
            whatsapp_qr.make(fit=True)
            whatsapp_qr_img = whatsapp_qr.make_image(fill_color="black", back_color="white")
            
            # Save temporary WhatsApp QR file
            whatsapp_temp_path = f"temp_whatsapp_guest_qr_{page_num}.png"
            whatsapp_qr_img.save(whatsapp_temp_path)
            
            # Draw groene achtergrond kader (zoals in voorbeeld)
            kader_padding = 8
            kader_x = whatsapp_x - kader_padding
            kader_y = whatsapp_y - kader_padding
            kader_size = whatsapp_qr_size + (kader_padding * 2)
            
            # Groene achtergrond kader met afgeronde hoeken effect
            canvas_obj.setFillColor("#25D366")  # WhatsApp groen
            canvas_obj.setStrokeColor("#25D366")
            canvas_obj.setLineWidth(3)
            canvas_obj.roundRect(kader_x, kader_y, kader_size, kader_size, 8, fill=1, stroke=1)
            
            # Witte binnenrand
            inner_padding = 3
            inner_x = kader_x + inner_padding
            inner_y = kader_y + inner_padding
            inner_size = kader_size - (inner_padding * 2)
            canvas_obj.setFillColor("white")
            canvas_obj.setStrokeColor("white")
            canvas_obj.roundRect(inner_x, inner_y, inner_size, inner_size, 5, fill=1, stroke=1)
            
            # Draw WhatsApp QR code
            canvas_obj.drawImage(whatsapp_temp_path, whatsapp_x, whatsapp_y, whatsapp_qr_size, whatsapp_qr_size)
            
            # Add WhatsApp label onder de QR code (groen kader)
            label_y = kader_y - 20
            label_width = kader_size
            label_height = 15
            
            # Groene label achtergrond
            canvas_obj.setFillColor("#25D366")
            canvas_obj.setStrokeColor("#25D366")
            canvas_obj.roundRect(kader_x, label_y, label_width, label_height, 5, fill=1, stroke=1)
            
            # Witte tekst op groene achtergrond
            canvas_obj.setFont("Helvetica-Bold", 9)
            canvas_obj.setFillColor("white")
            canvas_obj.drawCentredString(kader_x + label_width/2, label_y + 3, "Scan met camera")
            
            # Clean up WhatsApp QR file
            if os.path.exists(whatsapp_temp_path):
                os.remove(whatsapp_temp_path)
        
        # Clean up temp QR files
        if os.path.exists(qr_temp_path):
            os.remove(qr_temp_path)
        # Only remove user QR temp file if it was created
        if user_qr_img:
            user_qr_temp_path = f"temp_user_qr_{page_num}.png"
            if os.path.exists(user_qr_temp_path):
                os.remove(user_qr_temp_path)
    
    def _draw_topup_manual_page(self, canvas_obj, onboarding_data: Dict[str, Any], width: float, height: float, page_num: int, total_pages: int, tenant_name: str = None, language: str = 'en'):
        """Draw TOPUP manual page with optimized layout for better readability"""
        
        # Header section with background - same style as application pages
        canvas_obj.setFillColor("#1B4F72")  # Blue background for application template
        canvas_obj.rect(0, height - 120, width, 120, fill=1)
        
        # Main title
        canvas_obj.setFillColor("#FFFFFF")
        canvas_obj.setFont("Helvetica-Bold", 28)  # Slightly smaller for better proportion
        canvas_obj.drawCentredString(width/2, height - 35, "TOPUP HANDLEIDING")
        
        # Subtitle with onboarding name
        canvas_obj.setFont("Helvetica-Bold", 16)
        canvas_obj.drawCentredString(width/2, height - 60, f"{onboarding_data['onboarding_name']}")
        
        # Reset to black for main content
        canvas_obj.setFillColor("#000000")
        
        # Section divider
        y_pos = height - 120
        canvas_obj.setStrokeColor("#1B4F72")
        canvas_obj.setLineWidth(2)  # Thinner line
        canvas_obj.line(30, y_pos, width - 30, y_pos)  # Wider line
        
        # Try to load and display the topup manual image
        topup_image_path = "TOPUPMANUAL.png"
        
        try:
            if os.path.exists(topup_image_path):
                # Optimized image positioning for better page coverage
                margin = 40  # Smaller margins for more space
                available_width = width - (margin * 2)
                available_height = height - 200  # More space for image (120 header + 80 footer)
                
                # Load image to get dimensions
                from PIL import Image
                img = Image.open(topup_image_path)
                img_width, img_height = img.size
                
                # Calculate scaling with better utilization of space
                scale_w = available_width / img_width
                scale_h = available_height / img_height
                scale = min(scale_w, scale_h)  # Allow scaling up for better visibility
                
                # Ensure minimum and maximum scaling for readability
                scale = max(scale, 0.6)  # Minimum scale for readability
                scale = min(scale, 1.8)  # Maximum scale to prevent pixelation
                
                new_width = img_width * scale
                new_height = img_height * scale
                
                # Perfect centering with optimal positioning
                image_x = (width - new_width) / 2
                image_y = y_pos - 30 - new_height  # Start just below divider line
                
                # Ensure image doesn't go below footer area
                min_y = 120  # Leave space for footer
                if image_y < min_y:
                    # Recalculate if image is too tall
                    available_height = y_pos - 30 - min_y
                    scale_h = available_height / img_height
                    scale = min(scale_w, scale_h)
                    new_width = img_width * scale
                    new_height = img_height * scale
                    image_x = (width - new_width) / 2
                    image_y = y_pos - 30 - new_height
                
                # Draw subtle background for the image (optional enhancement)
                bg_padding = 10
                canvas_obj.setFillColor("#F8F9FA")  # Very light gray background
                canvas_obj.setStrokeColor("#E9ECEF")  # Light border
                canvas_obj.setLineWidth(1)
                canvas_obj.rect(image_x - bg_padding, image_y - bg_padding, 
                               new_width + (bg_padding * 2), new_height + (bg_padding * 2), 
                               fill=1, stroke=1)
                
                # Draw the image
                canvas_obj.drawImage(topup_image_path, image_x, image_y, new_width, new_height)
                
                # Calculate QR code position to center between image and footer
                footer_top = 60  # Footer starts at 60px from bottom (space for text + padding)
                available_space = image_y - footer_top  # Space between image bottom and footer top
                qr_y_position = image_y - (available_space / 2)  # Center in available space
                self._draw_youtube_qr_code(canvas_obj, width, qr_y_position, "#1B4F72")
                
            else:
                # Enhanced fallback if image is not found
                canvas_obj.setFont("Helvetica-Bold", 24)
                canvas_obj.setFillColor("#CC0000")
                canvas_obj.drawCentredString(width/2, height/2 + 50, "⚠ TOPUP HANDLEIDING ⚠")
                
                canvas_obj.setFont("Helvetica", 16)
                canvas_obj.setFillColor("#000000")
                canvas_obj.drawCentredString(width/2, height/2, f"Afbeelding niet gevonden: {topup_image_path}")
                canvas_obj.drawCentredString(width/2, height/2 - 25, "Controleer of het bestand in de juiste map staat")
                canvas_obj.drawCentredString(width/2, height/2 - 50, "Contacteer de IT afdeling voor ondersteuning")
                
                # Add troubleshooting box
                box_width = 400
                box_height = 120
                box_x = (width - box_width) / 2
                box_y = height/2 - 150
                
                canvas_obj.setStrokeColor("#CC0000")
                canvas_obj.setLineWidth(2)
                canvas_obj.rect(box_x, box_y, box_width, box_height, fill=0)
                
                canvas_obj.setFont("Helvetica-Bold", 12)
                canvas_obj.setFillColor("#CC0000")
                canvas_obj.drawCentredString(width/2, box_y + 90, "TROUBLESHOOTING:")
                canvas_obj.setFont("Helvetica", 10)
                canvas_obj.setFillColor("#000000")
                canvas_obj.drawCentredString(width/2, box_y + 70, "1. Controleer of TOPUPMANUAL.png aanwezig is")
                canvas_obj.drawCentredString(width/2, box_y + 55, "2. Zorg voor juiste bestandsrechten")
                canvas_obj.drawCentredString(width/2, box_y + 40, "3. Herstart de applicatie")
                canvas_obj.drawCentredString(width/2, box_y + 25, "4. Contacteer IT support")
                
        except Exception as e:
            # Enhanced error handling with more detail
            canvas_obj.setFont("Helvetica-Bold", 20)
            canvas_obj.setFillColor("#CC0000")
            canvas_obj.drawCentredString(width/2, height/2 + 80, "🚫 FOUT BIJ LADEN TOPUP HANDLEIDING 🚫")
            
            canvas_obj.setFont("Helvetica", 12)
            canvas_obj.setFillColor("#000000")
            canvas_obj.drawCentredString(width/2, height/2 + 40, f"Technische fout: {str(e)[:60]}...")
            canvas_obj.drawCentredString(width/2, height/2 + 20, "De handleiding kon niet worden geladen")
            canvas_obj.drawCentredString(width/2, height/2, "Contacteer onmiddellijk de IT afdeling")
            
            # Error details box
            canvas_obj.setStrokeColor("#FF6B6B")
            canvas_obj.setFillColor("#FFE6E6")
            canvas_obj.rect(50, height/2 - 80, width - 100, 60, fill=1, stroke=1)
            canvas_obj.setFont("Helvetica", 10)
            canvas_obj.setFillColor("#CC0000")
            canvas_obj.drawCentredString(width/2, height/2 - 50, "ERROR DETAILS:")
            canvas_obj.drawCentredString(width/2, height/2 - 65, f"Bestand: {topup_image_path}")
        
        # Standard footer - consistent with other templates
        canvas_obj.setFont("Helvetica", 10)
        canvas_obj.setFillColor("#666666")
        current_time = datetime.now().strftime("%d/%m/%Y %H:%M")
        client_info = f"CLIENT: {tenant_name}" if tenant_name else ""
        footer_text = f"anyKrowd NV - gegenereerd op: {current_time} - {client_info}"
        canvas_obj.drawCentredString(width/2, 30, footer_text)
        
        # Pagina informatie links onderaan
        canvas_obj.setFont("Helvetica", 9)
        canvas_obj.setFillColor("#999999")
        canvas_obj.drawString(20, 15, f"Pagina {page_num} van {total_pages}")
    
    def _draw_topup_manual_page_guest(self, canvas_obj, onboarding_data: Dict[str, Any], width: float, height: float, page_num: int, total_pages: int, tenant_name: str = None):
        """Draw TOPUP manual page for guest template with optimized layout for better readability"""
        
        # Header section with background - guest purple color
        canvas_obj.setFillColor("#6A1B9A")  # Purple background for guest template
        canvas_obj.rect(0, height - 120, width, 120, fill=1)
        
        # Main title
        canvas_obj.setFillColor("#FFFFFF")
        canvas_obj.setFont("Helvetica-Bold", 28)  # Slightly smaller for better proportion
        canvas_obj.drawCentredString(width/2, height - 35, "TOPUP HANDLEIDING")
        
        # Subtitle with onboarding name
        canvas_obj.setFont("Helvetica-Bold", 16)
        canvas_obj.drawCentredString(width/2, height - 60, f"{onboarding_data['onboarding_name']}")
        
        # Reset to black for main content
        canvas_obj.setFillColor("#000000")
        
        # Section divider
        y_pos = height - 120
        canvas_obj.setStrokeColor("#6A1B9A")
        canvas_obj.setLineWidth(2)  # Thinner line
        canvas_obj.line(30, y_pos, width - 30, y_pos)  # Wider line
        
        # Try to load and display the topup manual image
        topup_image_path = "TOPUPMANUAL.png"
        
        try:
            if os.path.exists(topup_image_path):
                # Optimized image positioning for better page coverage
                margin = 40  # Smaller margins for more space
                available_width = width - (margin * 2)
                available_height = height - 200  # More space for image (120 header + 80 footer)
                
                # Load image to get dimensions
                from PIL import Image
                img = Image.open(topup_image_path)
                img_width, img_height = img.size
                
                # Calculate scaling with better utilization of space
                scale_w = available_width / img_width
                scale_h = available_height / img_height
                scale = min(scale_w, scale_h)  # Allow scaling up for better visibility
                
                # Ensure minimum and maximum scaling for readability
                scale = max(scale, 0.6)  # Minimum scale for readability
                scale = min(scale, 1.8)  # Maximum scale to prevent pixelation
                
                new_width = img_width * scale
                new_height = img_height * scale
                
                # Perfect centering with optimal positioning
                image_x = (width - new_width) / 2
                image_y = y_pos - 30 - new_height  # Start just below divider line
                
                # Ensure image doesn't go below footer area
                min_y = 120  # Leave space for footer
                if image_y < min_y:
                    # Recalculate if image is too tall
                    available_height = y_pos - 30 - min_y
                    scale_h = available_height / img_height
                    scale = min(scale_w, scale_h)
                    new_width = img_width * scale
                    new_height = img_height * scale
                    image_x = (width - new_width) / 2
                    image_y = y_pos - 30 - new_height
                
                # Draw subtle background for the image (optional enhancement)
                bg_padding = 10
                canvas_obj.setFillColor("#F8F9FA")  # Very light gray background
                canvas_obj.setStrokeColor("#E9ECEF")  # Light border
                canvas_obj.setLineWidth(1)
                canvas_obj.rect(image_x - bg_padding, image_y - bg_padding, 
                               new_width + (bg_padding * 2), new_height + (bg_padding * 2), 
                               fill=1, stroke=1)
                
                # Draw the image
                canvas_obj.drawImage(topup_image_path, image_x, image_y, new_width, new_height)
                
                # Calculate QR code position to center between image and footer
                footer_top = 60  # Footer starts at 60px from bottom (space for text + padding)
                available_space = image_y - footer_top  # Space between image bottom and footer top
                qr_y_position = image_y - (available_space / 2)  # Center in available space
                self._draw_youtube_qr_code(canvas_obj, width, qr_y_position, "#6A1B9A")
                
            else:
                # Enhanced fallback if image is not found
                canvas_obj.setFont("Helvetica-Bold", 24)
                canvas_obj.setFillColor("#CC0000")
                canvas_obj.drawCentredString(width/2, height/2 + 50, "⚠ TOPUP HANDLEIDING ⚠")
                
                canvas_obj.setFont("Helvetica", 16)
                canvas_obj.setFillColor("#000000")
                canvas_obj.drawCentredString(width/2, height/2, f"Afbeelding niet gevonden: {topup_image_path}")
                canvas_obj.drawCentredString(width/2, height/2 - 25, "Controleer of het bestand in de juiste map staat")
                canvas_obj.drawCentredString(width/2, height/2 - 50, "Contacteer de IT afdeling voor ondersteuning")
                
                # Add troubleshooting box
                box_width = 400
                box_height = 120
                box_x = (width - box_width) / 2
                box_y = height/2 - 150
                
                canvas_obj.setStrokeColor("#CC0000")
                canvas_obj.setLineWidth(2)
                canvas_obj.rect(box_x, box_y, box_width, box_height, fill=0)
                
                canvas_obj.setFont("Helvetica-Bold", 12)
                canvas_obj.setFillColor("#CC0000")
                canvas_obj.drawCentredString(width/2, box_y + 90, "TROUBLESHOOTING:")
                canvas_obj.setFont("Helvetica", 10)
                canvas_obj.setFillColor("#000000")
                canvas_obj.drawCentredString(width/2, box_y + 70, "1. Controleer of TOPUPMANUAL.png aanwezig is")
                canvas_obj.drawCentredString(width/2, box_y + 55, "2. Zorg voor juiste bestandsrechten")
                canvas_obj.drawCentredString(width/2, box_y + 40, "3. Herstart de applicatie")
                canvas_obj.drawCentredString(width/2, box_y + 25, "4. Contacteer IT support")
                
        except Exception as e:
            # Enhanced error handling with more detail
            canvas_obj.setFont("Helvetica-Bold", 20)
            canvas_obj.setFillColor("#CC0000")
            canvas_obj.drawCentredString(width/2, height/2 + 80, "🚫 FOUT BIJ LADEN TOPUP HANDLEIDING 🚫")
            
            canvas_obj.setFont("Helvetica", 12)
            canvas_obj.setFillColor("#000000")
            canvas_obj.drawCentredString(width/2, height/2 + 40, f"Technische fout: {str(e)[:60]}...")
            canvas_obj.drawCentredString(width/2, height/2 + 20, "De handleiding kon niet worden geladen")
            canvas_obj.drawCentredString(width/2, height/2, "Contacteer onmiddellijk de IT afdeling")
            
            # Error details box
            canvas_obj.setStrokeColor("#FF6B6B")
            canvas_obj.setFillColor("#FFE6E6")
            canvas_obj.rect(50, height/2 - 80, width - 100, 60, fill=1, stroke=1)
            canvas_obj.setFont("Helvetica", 10)
            canvas_obj.setFillColor("#CC0000")
            canvas_obj.drawCentredString(width/2, height/2 - 50, "ERROR DETAILS:")
            canvas_obj.drawCentredString(width/2, height/2 - 65, f"Bestand: {topup_image_path}")
        
        # Standard footer - consistent with other templates  
        canvas_obj.setFont("Helvetica", 10)
        canvas_obj.setFillColor("#666666")
        current_time = datetime.now().strftime("%d/%m/%Y %H:%M")
        client_info = f"CLIENT: {tenant_name}" if tenant_name else ""
        footer_text = f"anyKrowd NV - gegenereerd op: {current_time} - {client_info}"
        canvas_obj.drawCentredString(width/2, 30, footer_text)
        
        # Pagina informatie links onderaan
        canvas_obj.setFont("Helvetica", 9)
        canvas_obj.setFillColor("#999999")
        canvas_obj.drawString(20, 15, f"Pagina {page_num} van {total_pages}")
    
    def _draw_youtube_qr_code(self, canvas_obj, width: float, y_position: float, brand_color: str):
        """Draw YouTube QR code with red bar containing 'Bekijk Online' text for TOPUP manual"""
        youtube_url = "https://youtu.be/S1DzBHeu9Rg"
        
        try:
            # Generate YouTube QR code
            youtube_qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=8,
                border=3,
            )
            youtube_qr.add_data(youtube_url)
            youtube_qr.make(fit=True)
            youtube_qr_img = youtube_qr.make_image(fill_color="black", back_color="white")
            
            # QR code dimensions - centered both horizontally and vertically around y_position
            qr_size = 120
            qr_x = (width - qr_size) / 2  # Center the QR code horizontally
            # Center QR code vertically around the given y_position
            # Total QR height including red bar = 120 (QR) + 35 (spacing) + 30 (bar) = 185
            total_qr_height = 185
            qr_y = y_position + (total_qr_height / 2) - qr_size  # Center around y_position
            
            # Save temporary YouTube QR file
            youtube_temp_path = "temp_youtube_qr.png"
            youtube_qr_img.save(youtube_temp_path)
            
            # Draw white background for QR code
            bg_padding = 8
            canvas_obj.setFillColor("white")
            canvas_obj.setStrokeColor("#DDDDDD")
            canvas_obj.setLineWidth(1)
            canvas_obj.rect(qr_x - bg_padding, qr_y - bg_padding, 
                           qr_size + (bg_padding * 2), qr_size + (bg_padding * 2), 
                           fill=1, stroke=1)
            
            # Draw YouTube QR code
            canvas_obj.drawImage(youtube_temp_path, qr_x, qr_y, qr_size, qr_size)
            
            # RED BAR with "Bekijk Online" below QR code
            bar_y = qr_y - bg_padding - 35  # Position below QR code
            bar_width = qr_size + (bg_padding * 2)  # Same width as QR background
            bar_height = 30
            bar_x = qr_x - bg_padding
            
            # Draw red background bar (YouTube red)
            canvas_obj.setFillColor("#FF0000")  # YouTube red
            canvas_obj.setStrokeColor("#CC0000")  # Darker red border
            canvas_obj.setLineWidth(1)
            canvas_obj.rect(bar_x, bar_y, bar_width, bar_height, fill=1, stroke=1)
            
            # White "Bekijk Online" text in red bar
            canvas_obj.setFont("Helvetica-Bold", 14)
            canvas_obj.setFillColor("white")
            canvas_obj.drawCentredString(bar_x + bar_width/2, bar_y + 8, "Bekijk Online")
            
            # Subtitle below red bar
            canvas_obj.setFont("Helvetica", 11)
            canvas_obj.setFillColor("#666666")
            canvas_obj.drawCentredString(bar_x + bar_width/2, bar_y - 18, "Scan voor video uitleg")
            
            # Clean up temp file
            if os.path.exists(youtube_temp_path):
                os.remove(youtube_temp_path)
                
        except Exception as e:
            # Fallback if YouTube QR generation fails
            canvas_obj.setFont("Helvetica-Bold", 14)
            canvas_obj.setFillColor("#FF0000")
            canvas_obj.drawCentredString(width/2, y_position, "🎥 Bekijk Online")
            canvas_obj.setFont("Helvetica", 11)
            canvas_obj.setFillColor("#666666")
            canvas_obj.drawCentredString(width/2, y_position - 20, "Video niet beschikbaar")
    
    def _draw_qr_code_small(self, canvas_obj, url: str, x: float, y: float, size: float):
        """Draw a small QR code for overview pages"""
        try:
            # Generate QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=3,
                border=1,
            )
            qr.add_data(url)
            qr.make(fit=True)
            
            # Create QR code image
            qr_img = qr.make_image(fill_color="black", back_color="white")
            
            # Convert to PIL if needed
            if hasattr(qr_img, 'convert'):
                qr_img = qr_img.convert('RGB')
            
            # Create temporary file for the QR image
            import tempfile
            import os
            
            temp_dir = tempfile.gettempdir()
            temp_qr_path = os.path.join(temp_dir, f"temp_qr_{hash(url) % 100000}.png")
            
            try:
                qr_img.save(temp_qr_path, format='PNG')
                
                # Draw QR code on canvas
                canvas_obj.drawImage(temp_qr_path, x, y, width=size, height=size, preserveAspectRatio=True)
                
            finally:
                # Clean up temp file
                if os.path.exists(temp_qr_path):
                    try:
                        os.remove(temp_qr_path)
                    except:
                        pass
                        
        except Exception as e:
            # Fallback: draw a simple rectangle with text
            canvas_obj.setStrokeColor("#000000")
            canvas_obj.setFillColor("#FFFFFF")
            canvas_obj.rect(x, y, size, size, fill=1, stroke=1)
            
            canvas_obj.setFillColor("#000000")
            canvas_obj.setFont("Helvetica", 6)
            canvas_obj.drawCentredString(x + size/2, y + size/2 - 3, "QR")
            canvas_obj.drawCentredString(x + size/2, y + size/2 + 3, "CODE")
            print(f"Error generating YouTube QR: {e}")

    def _draw_configuration_overview_page(self, canvas_obj, onboarding_list: List[Dict[str, Any]], tenant_name: str, domain: str, width: float, height: float, page_num: int, total_pages: int, template_type: str, user_data_map: Dict[str, Dict[str, Any]] = None, language: str = 'en'):
        """Draw a compact configuration overview page showing all onboarding QRs on one page"""
        
        # Header section with background - extra compact header
        color = "#1B4F72" if template_type == "APPLICATION" else "#6A1B9A"
        canvas_obj.setFillColor(color)
        canvas_obj.rect(0, height - 70, width, 70, fill=1)  # Nog kleiner: 70px header
        
        # Main title - compact
        canvas_obj.setFillColor("#FFFFFF")
        canvas_obj.setFont("Helvetica-Bold", 18)
        canvas_obj.drawCentredString(width/2, height - 30, "CONFIGURATIE OVERZICHT")
        
        # Client name and template type on one line
        canvas_obj.setFont("Helvetica-Bold", 12)
        template_text = "KASSA SETUP" if template_type == "APPLICATION" else ""
        if template_text:
            canvas_obj.drawCentredString(width/2, height - 50, f"CLIENT: {tenant_name.upper()} | {template_text}")
        else:
            canvas_obj.drawCentredString(width/2, height - 50, f"CLIENT: {tenant_name.upper()}")
        
        # Reset to black for main content
        canvas_obj.setFillColor("#000000")
        
        # Start content lager voor betere event zichtbaarheid
        y_pos = height - 90
        
        # Event information section - lager en EXTRA prominent
        if onboarding_list:
            event_name = onboarding_list[0].get('event_name', 'Niet gespecificeerd')
            config_count = len(onboarding_list) if onboarding_list else 0
            
            # Meer ruimte voor event sectie
            y_pos -= 30
            
            # Event naam EXTRA GROOT en prominenter
            canvas_obj.setFont("Helvetica-Bold", 26)  # Nog groter: 26pt
            canvas_obj.setFillColor(color)
            canvas_obj.drawCentredString(width/2, y_pos, f"EVENT: {event_name}")
            
            # Event times - veel meer zichtbaar
            try:
                from database import DatabaseConnection
                db = DatabaseConnection()
                tenant_id = tenant_name[7:] if tenant_name.startswith('tenant-') else tenant_name
                event_details = db.get_event_details(event_name, tenant_id)
                
                if event_details:
                    start_time = event_details.get('start_datetime')
                    end_time = event_details.get('end_datetime')
                    
                    y_pos -= 35  # Meer ruimte tussen event naam en tijden
                    canvas_obj.setFont("Helvetica-Bold", 16)  # Grotere font voor tijden
                    canvas_obj.setFillColor("#000000")
                    
                    time_info = ""
                    if start_time:
                        try:
                            if isinstance(start_time, str):
                                start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
                                start_formatted = start_dt.strftime("%d/%m/%Y %H:%M")
                            else:
                                start_formatted = start_time.strftime("%d/%m/%Y %H:%M")
                            time_info += f"Start: {start_formatted}"
                        except:
                            time_info += f"Start: {start_time}"
                    
                    if end_time:
                        try:
                            if isinstance(end_time, str):
                                end_dt = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
                                end_formatted = end_dt.strftime("%d/%m/%Y %H:%M")
                            else:
                                end_formatted = end_time.strftime("%d/%m/%Y %H:%M")
                            if time_info:
                                time_info += f"  |  Einde: {end_formatted}"
                            else:
                                time_info += f"Einde: {end_formatted}"
                        except:
                            if time_info:
                                time_info += f"  |  Einde: {end_time}"
                            else:
                                time_info += f"Einde: {end_time}"
                    
                    if time_info:
                        canvas_obj.drawCentredString(width/2, y_pos, time_info)
                
                # Check refund settings and display if enabled
                try:
                    from database import DatabaseConnection
                    refund_db = DatabaseConnection()
                    
                    # Map tenant ID correctly for central database lookup
                    # Handle different tenant ID formats between tenant DBs and central DB
                    central_tenant_id = self._map_to_central_tenant_id(tenant_id)
                    
                    # Try to get refund settings with error handling
                    refund_settings = refund_db.get_refund_settings(central_tenant_id)
                    
                    if refund_settings:  # Only proceed if we got data
                        refund_enabled = refund_settings.get('REFUND SCHEDULER ENABLED', '[ ]')
                        
                        if refund_enabled == '[X]':  # Only show if enabled
                            refund_start = refund_settings.get('REFUND START DATETIME', '')
                            refund_end = refund_settings.get('REFUND END DATETIME', '')
                            
                            if refund_start or refund_end:
                                y_pos -= 30  # Meer ruimte voor refund informatie
                                canvas_obj.setFont("Helvetica-Bold", 14)  # Grotere font voor refund info
                                canvas_obj.setFillColor("#CC6600")  # Orange color for refund info
                                
                                refund_info = ""
                                if refund_start:
                                    refund_info += f"Refund Start: {refund_start}"
                                if refund_end:
                                    if refund_info:
                                        refund_info += f"  |  Refund Einde: {refund_end}"
                                    else:
                                        refund_info += f"Refund Einde: {refund_end}"
                                
                                if refund_info:
                                    canvas_obj.drawCentredString(width/2, y_pos, refund_info)
                                    # Extra ruimte na refund info
                                    y_pos -= 10
                    
                    refund_db.disconnect()
                
                except Exception as e:
                    print(f"⚠ Could not fetch refund settings: {e}")
                
                db.disconnect()
            except Exception as e:
                print(f"Could not fetch event details: {e}")
            
            # Aantal configuraties EXTRA prominent en lager
            y_pos -= 40  # Meer ruimte voor totaal configuraties
            canvas_obj.setFont("Helvetica-Bold", 18)  # Grotere font voor totaal
            canvas_obj.setFillColor(color)
            canvas_obj.drawCentredString(width/2, y_pos, f"TOTAAL CONFIGURATIES: {config_count}")
        
        # Table section - Gecentreerde tabel met flexibele kolommen
        y_pos -= 50  # Meer ruimte tussen event info en tabel
        canvas_obj.setFillColor("#000000")
        canvas_obj.setFont("Helvetica-Bold", 10)
        
        # Dynamische kolombreedtes afhankelijk van template type
        if template_type == "GUEST":
            # Guest template - bredere tabel (520px) gecentreerd
            table_width = 520
            table_start_x = (width - table_width) / 2
            
            col1_x = table_start_x       # Name (80px)
            col2_x = table_start_x + 80  # User (80px)
            col3_x = table_start_x + 160 # Roles (90px)
            col4_x = table_start_x + 250 # Payment (80px)
            col5_x = table_start_x + 330 # Location (90px)
            col6_x = table_start_x + 420 # Status (100px)
            
            canvas_obj.drawString(col1_x, y_pos, "NAAM")
            canvas_obj.drawString(col2_x, y_pos, "GEBRUIKER")
            canvas_obj.drawString(col3_x, y_pos, "ROLLEN")
            canvas_obj.drawString(col4_x, y_pos, "BETALING")
            canvas_obj.drawString(col5_x, y_pos, "LOCATIE")
            canvas_obj.drawString(col6_x, y_pos, "STATUS")
        else:
            # Application template - smallere tabel (450px) gecentreerd
            table_width = 450
            table_start_x = (width - table_width) / 2
            
            col1_x = table_start_x       # Name (100px)
            col2_x = table_start_x + 100 # Roles (100px)
            col3_x = table_start_x + 200 # Payment (100px)
            col4_x = table_start_x + 300 # Location (80px)
            col5_x = table_start_x + 380 # Status (70px)
            
            canvas_obj.drawString(col1_x, y_pos, "NAAM")
            canvas_obj.drawString(col2_x, y_pos, "ROLLEN")
            canvas_obj.drawString(col3_x, y_pos, "BETALING")
            canvas_obj.drawString(col4_x, y_pos, "LOCATIE")
            canvas_obj.drawString(col5_x, y_pos, "STATUS")
        
        # Header underline - gecentreerd op tabel
        canvas_obj.setStrokeColor("#CCCCCC")
        canvas_obj.setLineWidth(1)
        canvas_obj.line(table_start_x, y_pos - 5, table_start_x + table_width, y_pos - 5)
        
        y_pos -= 20
        canvas_obj.setFont("Helvetica", 9)  # Smaller font for more rows
        
        # List all onboarding QRs - met betaalmethodes voor beide templates
        items_per_page = 25  # Minder items voor meer overzichtelijkheid
        for i, onboarding_data in enumerate(onboarding_list or []):
            if y_pos < 80:  # Stop if we run out of space
                break
                
            # Name - truncate if too long
            name = onboarding_data.get('onboarding_name', 'Unknown')
            if not name:
                name = 'Unknown'
            if len(name) > 12:
                name = name[:9] + "..."
            canvas_obj.drawString(col1_x, y_pos, name)
            
            if template_type == "GUEST":
                # User info - compact
                if user_data_map and onboarding_data.get('onboarding_name') in user_data_map:
                    user_data = user_data_map[onboarding_data['onboarding_name']]
                    user_email = user_data.get('email', 'Geen email') or 'Geen email'
                    # Show only first part of email for space
                    if '@' in user_email:
                        user_display = user_email.split('@')[0]
                    else:
                        user_display = user_email
                    if len(user_display) > 10:
                        user_display = user_display[:7] + "..."
                    canvas_obj.drawString(col2_x, y_pos, user_display)
                    
                    # Status indicator
                    canvas_obj.setFillColor("#008000")  # Green
                    canvas_obj.drawString(col6_x, y_pos, "✓ OK")
                    canvas_obj.setFillColor("#000000")
                else:
                    canvas_obj.drawString(col2_x, y_pos, "Geen user")
                    canvas_obj.setFillColor("#FF6600")  # Orange
                    canvas_obj.drawString(col6_x, y_pos, "⚠ Missing")
                    canvas_obj.setFillColor("#000000")
                
                # Roles - compact maar leesbaar
                roles = onboarding_data.get('rollen', 'Geen') or 'Geen'
                if len(roles) > 15:
                    roles = roles[:12] + "..."
                canvas_obj.drawString(col3_x, y_pos, roles)
                
                # Payment methods - Verbeterde verwerking
                payment = onboarding_data.get('betaalmethodes', '') or ''
                if not payment or payment.strip() == '':
                    payment = 'Geen'
                if len(payment) > 12:
                    payment = payment[:9] + "..."
                canvas_obj.drawString(col4_x, y_pos, payment)
                
                # Location - compact
                location = onboarding_data.get('location_name', 'Geen') or 'Geen'
                if len(location) > 10:
                    location = location[:7] + "..."
                canvas_obj.drawString(col5_x, y_pos, location)
                
            else:
                # Application template columns
                # Roles - compact maar leesbaar
                roles = onboarding_data.get('rollen', 'Geen') or 'Geen'
                if len(roles) > 15:
                    roles = roles[:12] + "..."
                canvas_obj.drawString(col2_x, y_pos, roles)
                
                # Payment methods - Verbeterde verwerking
                payment = onboarding_data.get('betaalmethodes', '') or ''
                if not payment or payment.strip() == '':
                    payment = 'Geen'
                if len(payment) > 12:
                    payment = payment[:9] + "..."
                canvas_obj.drawString(col3_x, y_pos, payment)
                
                # Location
                location = onboarding_data.get('location_name', 'Geen') or 'Geen'
                if len(location) > 10:
                    location = location[:7] + "..."
                canvas_obj.drawString(col4_x, y_pos, location)
                
                # Status - check for TOPUP
                if self._has_topup_role(onboarding_data):
                    canvas_obj.setFillColor("#0066CC")  # Blue
                    canvas_obj.drawString(col5_x, y_pos, "TOPUP")
                    canvas_obj.setFillColor("#000000")
                else:
                    canvas_obj.setFillColor("#008000")  # Green
                    canvas_obj.drawString(col5_x, y_pos, "✓ OK")
                    canvas_obj.setFillColor("#000000")
            
            y_pos -= 18  # Meer ruimte tussen regels voor leesbaarheid
        
        # Add note if there are more items than can fit
        if onboarding_list and len(onboarding_list) > items_per_page:
            canvas_obj.setFont("Helvetica-Oblique", 9)
            canvas_obj.setFillColor("#666666")
            canvas_obj.drawCentredString(width/2, y_pos - 10, f"... en nog {len(onboarding_list) - items_per_page} configuraties (zie individuele pagina's)")
        
        # Add currencies information section or reference to separate page
        if self._needs_separate_currencies_page(onboarding_list):
            # Add reference to separate currencies page
            y_pos -= 30
            canvas_obj.setFont("Helvetica-Bold", 14)
            canvas_obj.setFillColor(color)
            canvas_obj.drawCentredString(width/2, y_pos, "Currencies Information")
            y_pos -= 20
            canvas_obj.setFont("Helvetica-Oblique", 12)
            canvas_obj.setFillColor("#666666")
            canvas_obj.drawCentredString(width/2, y_pos, "→ Zie aparte currencies pagina voor details ←")
        else:
            # Include currencies directly on this page
            self._draw_currencies_section(canvas_obj, tenant_name, width, y_pos - 40, color)
        
        # Instruction for QR codes - updated to reflect new page order
        canvas_obj.setFont("Helvetica-Oblique", 11)
        canvas_obj.setFillColor(color)
        instruction_y = 70
        if self._needs_separate_currencies_page(onboarding_list):
            canvas_obj.drawCentredString(width/2, instruction_y, "→ Zie pagina 2 voor currencies info, daarna QR codes voor configuratie ←")
        else:
            canvas_obj.drawCentredString(width/2, instruction_y, "→ Scan de QR codes op de volgende pagina's voor configuratie ←")
        
        # Footer with page info
        canvas_obj.setFont("Helvetica", 9)
        canvas_obj.setFillColor("#999999")
        canvas_obj.drawString(20, 15, f"Pagina {page_num} van {total_pages}")
        
        # Footer with generation info
        canvas_obj.setFont("Helvetica", 9)
        canvas_obj.setFillColor("#666666")
        current_time = datetime.now().strftime("%d/%m/%Y %H:%M")
        footer_text = f"anyKrowd NV - {current_time} - CLIENT: {tenant_name}"
        canvas_obj.drawCentredString(width/2, 30, footer_text)
    
    def _draw_currencies_section(self, canvas_obj, tenant_name: str, width: float, start_y: float, color: str):
        """Draw currencies information table"""
        try:
            # Get currencies data
            from database import DatabaseConnection
            db = DatabaseConnection()
            tenant_id = tenant_name[7:] if tenant_name.startswith('tenant-') else tenant_name
            
            # Ensure connection to tenant database with retry logic
            if not db.connect(f"tenant-{tenant_id}", retry_attempts=2):
                print(f"⚠ Could not connect to tenant database for currencies - skipping currencies section")
                # Draw placeholder text instead
                y_pos = start_y
                canvas_obj.setFont("Helvetica-Bold", 14)
                canvas_obj.setFillColor(color)
                canvas_obj.drawCentredString(width/2, y_pos, "Currencies Information")
                y_pos -= 25
                canvas_obj.setFont("Helvetica", 10)
                canvas_obj.setFillColor("#666666")
                canvas_obj.drawCentredString(width/2, y_pos, "⚠ Database connection unavailable - currencies information could not be retrieved")
                return
                
            currencies = db.get_currencies(tenant_id)
            
            if not currencies:
                db.disconnect()
                # Draw "no currencies" message
                y_pos = start_y
                canvas_obj.setFont("Helvetica-Bold", 14)
                canvas_obj.setFillColor(color)
                canvas_obj.drawCentredString(width/2, y_pos, "Currencies Information")
                y_pos -= 25
                canvas_obj.setFont("Helvetica", 10)
                canvas_obj.setFillColor("#666666")
                canvas_obj.drawCentredString(width/2, y_pos, "No currencies configured for this tenant")
                return
            
            y_pos = start_y
            
            # Section title - gecentreerd
            canvas_obj.setFont("Helvetica-Bold", 14)
            canvas_obj.setFillColor(color)
            canvas_obj.drawCentredString(width/2, y_pos, "Currencies Information")
            y_pos -= 25
            
            # Table headers - gecentreerd op pagina
            canvas_obj.setFont("Helvetica-Bold", 9)
            canvas_obj.setFillColor("#000000")
            
            # Column positions - gecentreerd op pagina (breedte van ~400px)
            table_start_x = (width - 400) / 2  # Centreer de tabel
            col1_x = table_start_x      # Currency Name
            col2_x = table_start_x + 80   # Exchange Rate  
            col3_x = table_start_x + 160  # Burning Weight
            col4_x = table_start_x + 240  # Staff Order
            col5_x = table_start_x + 320  # Client Order
            
            canvas_obj.drawString(col1_x, y_pos, "Currency Name")
            canvas_obj.drawString(col2_x, y_pos, "Exchange Rate")
            canvas_obj.drawString(col3_x, y_pos, "Burning Weight")
            canvas_obj.drawString(col4_x, y_pos, "Staff Order")
            canvas_obj.drawString(col5_x, y_pos, "Client Order")
            
            # Header underline - gecentreerd
            canvas_obj.setStrokeColor("#CCCCCC")
            canvas_obj.setLineWidth(1)
            canvas_obj.line(table_start_x, y_pos - 5, table_start_x + 400, y_pos - 5)
            
            y_pos -= 15
            canvas_obj.setFont("Helvetica", 8)
            
            # Sort currencies by burning weight
            sorted_currencies = sorted(currencies, key=lambda c: float(c.get('burning_weight', 0)) if c.get('burning_weight') is not None else 0)
            
            # Display currencies (max 7 to fit on page)
            for i, currency in enumerate(sorted_currencies[:7]):
                if y_pos < 120:  # Stop if we run out of space
                    break
                    
                # Currency name
                name = currency.get('name', '')
                if len(name) > 20:
                    name = name[:17] + "..."
                canvas_obj.drawString(col1_x, y_pos, name)
                
                # Exchange rate
                rate = currency.get('exchange_rate', currency.get('rate', 0))
                canvas_obj.drawString(col2_x, y_pos, f"{rate:.2f}")
                
                # Burning weight
                weight = currency.get('burning_weight', 0)
                canvas_obj.drawString(col3_x, y_pos, str(weight))
                
                # Staff order
                staff_order = currency.get('staffx_order', currency.get('staff_order', 0))
                canvas_obj.drawString(col4_x, y_pos, str(staff_order))
                
                # Client order
                client_order = currency.get('clientx_order', currency.get('client_order', 0))
                canvas_obj.drawString(col5_x, y_pos, str(client_order))
                
                y_pos -= 12
            
            # Legend - gecentreerd
            y_pos -= 5
            canvas_obj.setFont("Helvetica-Oblique", 7)
            canvas_obj.setFillColor("#666666")
            canvas_obj.drawCentredString(width/2, y_pos, "Exchange Rate: De waarde van 1 token. Indien ≥1: meegenomen in revenue. Bij 0: meestal gratis coin (crew, etc).")
            
            db.disconnect()
            
        except Exception as e:
            print(f"Could not fetch currencies data: {e}")
    
    def _draw_currencies_page(self, canvas_obj, tenant_name: str, domain: str, width: float, height: float, page_num: int, total_pages: int, template_type: str, language: str = 'en'):
        """Draw a dedicated currencies page when there are too many onboardings"""
        
        # Header section with background
        color = "#1B4F72" if template_type == "APPLICATION" else "#6A1B9A"
        canvas_obj.setFillColor(color)
        canvas_obj.rect(0, height - 120, width, 120, fill=1)
        
        # Main title
        canvas_obj.setFillColor("#FFFFFF")
        canvas_obj.setFont("Helvetica-Bold", 32)
        canvas_obj.drawCentredString(width/2, height - 40, "CURRENCIES INFORMATION")
        
        # Client name
        canvas_obj.setFont("Helvetica-Bold", 18)
        canvas_obj.drawCentredString(width/2, height - 70, f"CLIENT: {tenant_name.upper()}")
        
        # Reset to black for main content
        canvas_obj.setFillColor("#000000")
        
        # Draw currencies section with more space
        self._draw_currencies_section(canvas_obj, tenant_name, width, height - 150, color)
        
        # Footer with page info
        canvas_obj.setFont("Helvetica", 9)
        canvas_obj.setFillColor("#999999")
        canvas_obj.drawString(20, 15, f"Pagina {page_num} van {total_pages}")
        
        # Footer with generation info
        canvas_obj.setFont("Helvetica", 9)
        canvas_obj.setFillColor("#666666")
        current_time = datetime.now().strftime("%d/%m/%Y %H:%M")
        footer_text = f"anyKrowd NV - {current_time} - CLIENT: {tenant_name}"
        canvas_obj.drawCentredString(width/2, 30, footer_text)
    
    def _draw_qr_visual_overview_page(self, canvas_obj, onboarding_list: List[Dict[str, Any]], tenant_name: str, domain: str, width: float, height: float, page_num: int, total_pages: int, template_type: str, user_data_map: Dict[str, Dict[str, Any]] = None):
        """Draw a visual QR code overview page with QR codes side by side"""
        
        # Header section with background
        color = "#1B4F72" if template_type == "APPLICATION" else "#6A1B9A"
        canvas_obj.setFillColor(color)
        canvas_obj.rect(0, height - 140, width, 140, fill=1)
        
        # Main title - larger and better centered
        canvas_obj.setFillColor("#FFFFFF")
        canvas_obj.setFont("Helvetica-Bold", 32)
        canvas_obj.drawCentredString(width/2, height - 45, "QR CODE OVERZICHT")
        
        # Client name - better spacing
        canvas_obj.setFont("Helvetica-Bold", 20)
        canvas_obj.drawCentredString(width/2, height - 75, f"CLIENT: {tenant_name.upper()}")
        
        # Template type - smaller and better positioned
        canvas_obj.setFont("Helvetica", 16)
        template_text = "KASSA TOESTEL QR CODES" if template_type == "APPLICATION" else "GEBRUIKER QR CODES"
        canvas_obj.drawCentredString(width/2, height - 105, template_text)
        
        # Reset to black for main content
        canvas_obj.setFillColor("#000000")
        
        # Start content below header
        y_pos = height - 160
        
        # List format: each onboarding with name above and QR codes side by side below
        qr_size = 120  # Size of each QR code
        onboarding_spacing = 160  # Space between each onboarding entry
        margin_left = 80  # Left margin
        
        for i, onboarding_data in enumerate(onboarding_list or []):
            if y_pos < 150:  # Stop if we run out of space
                break
            
            # Draw onboarding name above QR codes
            canvas_obj.setFont("Helvetica-Bold", 16)
            canvas_obj.setFillColor("#000000")
            
            # Truncate name if too long
            name = onboarding_data['onboarding_name']
            if len(name) > 35:
                name = name[:32] + "..."
            
            canvas_obj.drawString(margin_left, y_pos, name)
            y_pos -= 25
            
            # Position QR codes side by side
            onboarding_qr_x = margin_left
            user_qr_x = margin_left + qr_size + 60  # Space between QR codes
            qr_y = y_pos - qr_size
            
            # Draw Onboarding QR code (left)
            onboarding_url = f"https://{domain}/?onboardingQrCode={onboarding_data['qr_code']}#/auth/signuphome"
            self._draw_qr_code_small(canvas_obj, onboarding_url, onboarding_qr_x, qr_y, qr_size)
            
            # Label for onboarding QR
            canvas_obj.setFont("Helvetica-Bold", 12)
            canvas_obj.setFillColor(color)
            canvas_obj.drawCentredString(onboarding_qr_x + qr_size/2, qr_y - 15, "ONBOARDING QR")
            
            # Draw User QR code (right) if available
            if template_type == "GUEST" and user_data_map and onboarding_data['onboarding_name'] in user_data_map:
                user_data = user_data_map[onboarding_data['onboarding_name']]
                # Users from INNER JOIN query always have RFID tag QR codes
                user_qr_value = user_data.get('qr_code', '')
                if user_qr_value:
                    self._draw_qr_code_small(canvas_obj, user_qr_value, user_qr_x, qr_y, qr_size)
                else:
                    # This should not happen with INNER JOIN, but safety fallback
                    canvas_obj.setFont("Helvetica", 8)
                    canvas_obj.setFillColor("#999999")
                    canvas_obj.drawCentredString(user_qr_x + qr_size/2, qr_y + qr_size/2, "Geen QR")
                
                # Label for user QR (when user exists)
                canvas_obj.setFont("Helvetica-Bold", 12)
                canvas_obj.setFillColor(color)
                canvas_obj.drawCentredString(user_qr_x + qr_size/2, qr_y - 15, "GEBRUIKER QR")
                
                # User info below user QR (when user exists)
                canvas_obj.setFont("Helvetica", 10)
                canvas_obj.setFillColor("#666666")
                user_email = user_data.get('email', 'Geen email')
                if len(user_email) > 25:
                    user_email = user_email[:22] + "..."
                canvas_obj.drawCentredString(user_qr_x + qr_size/2, qr_y - 30, user_email)
            else:
                # No user found with RFID tag
                canvas_obj.setFont("Helvetica", 8)
                canvas_obj.setFillColor("#999999")
                canvas_obj.drawCentredString(user_qr_x + qr_size/2, qr_y + qr_size/2, "Geen User")
            
            # Move to next onboarding position
            y_pos -= onboarding_spacing
        
        # Add note if there are more items than can fit
        remaining_items = 0
        if onboarding_list and 'i' in locals():
            remaining_items = len(onboarding_list) - i - 1
        if remaining_items > 0:
            canvas_obj.setFont("Helvetica-Oblique", 10)
            canvas_obj.setFillColor("#666666")
            canvas_obj.drawCentredString(width/2, y_pos - 10, f"... en nog {remaining_items} configuraties (zie volgende pagina's)")
        
        # Add legend
        canvas_obj.setFont("Helvetica-Oblique", 10)
        canvas_obj.setFillColor("#666666")
        legend_y = 80
        if template_type == "GUEST":
            canvas_obj.drawCentredString(width/2, legend_y, "Links: Onboarding QR voor configuratie | Rechts: Gebruiker QR voor login")
        else:
            canvas_obj.drawCentredString(width/2, legend_y, "QR Codes voor kassa/toestel configuratie")
        
        # Footer with page info
        canvas_obj.setFont("Helvetica", 9)
        canvas_obj.setFillColor("#999999")
        canvas_obj.drawString(20, 15, f"Pagina {page_num} van {total_pages}")
        
        # Footer with generation info - better formatting
        canvas_obj.setFont("Helvetica", 10)
        canvas_obj.setFillColor("#666666")
        current_time = datetime.now().strftime("%d/%m/%Y %H:%M")
        footer_text = f"anyKrowd NV - gegenereerd op: {current_time} - CLIENT: {tenant_name}"
        canvas_obj.drawCentredString(width/2, 30, footer_text)








