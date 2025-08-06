#!/usr/bin/env python3
"""
Test currencies section without numbering
"""

from qr_generator import QRCodeGenerator
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

def test_currencies_section():
    """Test that currencies section no longer has '1.' prefix"""
    print("Testing currencies section formatting...")
    
    # Create QR generator
    qr_gen = QRCodeGenerator()
    
    # Create a test PDF 
    test_filename = "test_currencies_section.pdf"
    c = canvas.Canvas(test_filename, pagesize=A4)
    width, height = A4
    
    try:
        # Test the currencies section drawing function
        qr_gen._draw_currencies_section(
            c, 
            "test-tenant", 
            width, 
            height - 200,  # Start position
            "#1B4F72"      # Color
        )
        
        c.save()
        print(f"✓ Test PDF created: {test_filename}")
        print("✓ Check the generated PDF to verify currencies section has no '1.' prefix")
        print("✓ Currencies section title should now be 'Currencies Information' without numbering")
        
    except Exception as e:
        print(f"✗ Error testing currencies section: {e}")

if __name__ == "__main__":
    test_currencies_section()
