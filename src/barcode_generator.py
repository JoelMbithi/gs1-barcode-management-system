import barcode
from barcode import EAN13
from barcode.writer import ImageWriter
import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import config
from src.prefix_manager import BarcodeSeriesManager
from src.gs1_kenya_verifier import GS1KenyaLegalVerifier


class KenyaLegalBarcodeGenerator:
    """
    GENERATES 100% LEGAL KENYAN BARCODES
    Only uses your GS1 Kenya assigned prefix
    """
    
    def __init__(self):
        """Initialize the barcode generator"""
        self.series_manager = BarcodeSeriesManager()
        self.verifier = GS1KenyaLegalVerifier()
        self.barcode_dir = config.BARCODE_DIR

        # Verify legal status on startup
        self.legal_status = self.verifier.verify_legal_status()

        print(" KENYA LEGAL BARCODE GENERATOR")
        print("-" * 60)
        print(f"Company: {config.YOUR_COMPANY_NAME}")
        print(f"GS1 Prefix: {config.YOUR_COMPANY_PREFIX}")
        print(f"Status: {'✅ LEGAL' if self.legal_status['can_sell'] else '⚠️ DEMO'}")
        print(f"Valid Until: {config.GS1_MEMBERSHIP_EXPIRY}")
        print("=" * 60 + "\n")
             
    def calculate_check_digit(self, first_12_digits):
        """
        OFFICIAL GS1 CHECK DIGIT CALCULATION
        This is the SAME algorithm used by Kenyan supermarkets
        """
        digits = [int(d) for d in str(first_12_digits)]

        # Step 1: Sum odd positions (1,3,5,7,9,11)
        odd_sum = sum(digits[0:12:2])

        # Step 2: Sum even positions × 3 (2,4,6,8,10,12)
        even_sum = sum(digits[1:12:2]) * 3

        # Step 3: Calculate total 
        total = odd_sum + even_sum

        # Step 4: Find check digit
        check_digit = (10 - (total % 10)) % 10

        return str(check_digit)

    def generate_legal_barcode(self, product_name="", custom_suffix=None):
        """
        GENERATE A LEGAL KENYAN BARCODE WITHIN YOUR ASSIGNED RANGE
        
        Args:
            product_name: Name of product (for filename)
            custom_suffix: Optional specific 4-5 digit suffix (if reserved)
        
        Returns:
            barcode_number: 13-digit legal barcode
            image_path: Path to PNG file
        """
        
        # STEP 1: Check if you can legally generate barcodes
        if not self.legal_status['can_sell'] and not self.verifier.is_demo_mode:
            print("\n❌ CANNOT GENERATE LEGAL BARCODES")
            print("   Your GS1 Kenya registration is not valid")
            print(f"   Call: {config.GS1_KENYA['phone']}")
            return None, None
        
        # STEP 2: Get next available barcode number
        try:
            if custom_suffix is not None:
                # ✅ FIXED: Use suffix as-is without zfill(5)!
                suffix_str = str(custom_suffix)
                barcode_12 = f"{self.series_manager.company_prefix}{suffix_str}"
                
                # Verify it's exactly 12 digits
                if len(barcode_12) != 12:
                    print(f"\n❌ ERROR: Barcode base must be 12 digits")
                    print(f"   Got: {barcode_12} ({len(barcode_12)} digits)")
                    print(f"   Prefix: {self.series_manager.company_prefix} ({len(self.series_manager.company_prefix)} digits)")
                    print(f"   Suffix: {suffix_str} ({len(suffix_str)} digits)")
                    print(f"   Total: {len(barcode_12)} digits (should be 12)")
                    return None, None
            else:
                # Get next available number automatically
                barcode_12 = self.series_manager.get_next_available_barcode()
        except ValueError as e:
            print(f"\n❌ {e}")
            return None, None
        
        # STEP 3: Calculate check digit
        check_digit = self.calculate_check_digit(barcode_12)
        
        # STEP 4: Complete 13-digit barcode
        barcode_13 = f"{barcode_12}{check_digit}"
        
        # STEP 5: Verify it's exactly 13 digits
        if len(barcode_13) != 13:
            print(f"\n❌ ERROR: Final barcode must be 13 digits")
            print(f"   Got: {barcode_13} ({len(barcode_13)} digits)")
            return None, None
        
        # STEP 6: Generate image
        try:
            # Create EAN-13 object
            ean = EAN13(barcode_13, writer=ImageWriter())
            
            # Create filename
            safe_name = "".join(c for c in product_name if c.isalnum() or c in (' ', '-', '_')).strip()
            if not safe_name:
                safe_name = f"product_{barcode_12[-4:]}"  # Last 4 digits
            
            timestamp = datetime.now().strftime("%Y%m%d")
            filename = f"{safe_name[:30]}_{barcode_13}_{timestamp}"
            
            # Save image
            image_path = self.barcode_dir / filename
            ean.save(str(image_path))
            image_path = f"{image_path}.png"
            
            # Determine status (LEGAL or DEMO)
            is_legal = self.legal_status['can_sell'] and not self.verifier.is_demo_mode
            status = "✅ LEGAL" if is_legal else "⚠️ DEMO"
            status_text = "GS1 Kenya Registered" if is_legal else "DEMO MODE - Not for retail"
            
            # Print success with verification
            print(f"\n{status} KENYAN BARCODE GENERATED")
            print(f"   ┌──────────────────────────────────────")
            print(f"   │ Barcode: {barcode_13}")
            print(f"   │ Status:  {status_text}")
            print(f"   │ Company: {config.YOUR_COMPANY_NAME}")
            print(f"   │ Prefix:  {config.YOUR_COMPANY_PREFIX}")
            print(f"   │ Product Code: {barcode_12[-4:]}")  # Show last 4 digits
            print(f"   │ Check Digit: {check_digit}")
            print(f"   │ Image:   {os.path.basename(image_path)}")
            print(f"   └──────────────────────────────────────")
            
            return barcode_13, image_path
            
        except Exception as e:
            print(f"\n❌ ERROR GENERATING BARCODE: {e}")
            return None, None
    
    def reserve_product_range(self, start_suffix, end_suffix, product_line):
        """
        RESERVE A RANGE OF BARCODES FOR A SPECIFIC PRODUCT LINE
        
        Example: 
        reserve_product_range(1000, 1999, "Maize Flour - 2kg")
        
        This ensures all your 2kg maize flour products
        have barcodes in the range 6141234510000-6141234519999
        """
        reserved = self.series_manager.reserve_barcode_range(
            start_suffix, end_suffix, product_line
        )
        
        print(f"\n✅ RANGE RESERVED FOR: {product_line}")
        print(f"   From: {reserved['start']}")
        print(f"   To:   {reserved['end']}")
        print(f"   Total: {end_suffix - start_suffix + 1} products")
        
        return reserved
    
    def get_legal_status_report(self):
        """Get complete legal status report"""
        stats = self.series_manager.get_series_statistics()
        legal = self.verifier.verify_legal_status()
        
        return {
            'legal_status': legal,
            'usage_stats': stats,
            'certificate': self.verifier.generate_legal_certificate()
        }