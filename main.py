import sys
import csv
from datetime import datetime

from src.barcode_generator import KenyaLegalBarcodeGenerator
from src.excel_exporter import KenyaLegalExcelExporter
from src.gs1_kenya_verifier import GS1KenyaLegalVerifier
from src.prefix_manager import BarcodeSeriesManager
import config

class KenyaLegalBarCodeSystem:
    """
    COMPLETE LEGAL BARCODE SYSTEM FOR KENYA
    GS1 Kenya Certified - 100% Legal for Retail
    """
    
    def __init__(self):
        print("\n" + "="*70)
        print("  KENYA LEGAL BARCODE SYSTEM - GS1 KENYA CERTIFIED")
        print("="*70)
        
        # Initialize components
        self.verifier = GS1KenyaLegalVerifier()
        self.generator = None
        self.exporter = KenyaLegalExcelExporter()
        self.series_manager = BarcodeSeriesManager()
        
        # Check legal status immediately
        self.legal_check()
    
    def legal_check(self):
        """
        STEP 1: VERIFY YOUR GS1 KENYA LEGAL STATUS
        This runs every time you start the system
        """
        status = self.verifier.verify_legal_status()
        
        if not status['can_sell']:
            print("\n  SYSTEM STARTING IN DEMO MODE")
            print("   You CANNOT use this for real products")
            
            response = input("\nAre you generating barcodes for REAL products to sell? (yes/no): ")
            
            if response.lower() == 'yes':
                print("\n SYSTEM HALTED - LEGAL REQUIREMENTS NOT MET")
                print("\n📞 TO MAKE YOUR BARCODES LEGAL:")
                print("   1. Call GS1 Kenya: 020 802 5760")
                print("   2. Pay annual fee: KSh 15,000 - 50,000")
                print("   3. Get your unique company prefix")
                print("   4. Update config.YOUR_COMPANY_PREFIX")
                print("\n Exiting system...")
                sys.exit(1)
            else:
                print("\n Continuing in DEMO mode for testing...\n")
                # Initialize generator in demo mode
                self.generator = KenyaLegalBarcodeGenerator()
        else:
            print("\n LEGAL STATUS VERIFIED - READY FOR PRODUCTION")
            # Initialize generator with legal status
            self.generator = KenyaLegalBarcodeGenerator()
    
    def setup_company_prefix(self):
        """
        STEP 2: SET YOUR REAL GS1 KENYA PREFIX
        THIS IS THE MOST IMPORTANT STEP!
        """
        print("\n" + "-"*70)
        print(" GS1 KENYA PREFIX CONFIGURATION")
        print("-"*70)
        
        print(f"\nCurrent prefix: {config.YOUR_COMPANY_PREFIX}")
        print(f"Company name: {config.YOUR_COMPANY_NAME}")
        print(f"Certificate: {config.GS1_CERTIFICATE_NUMBER}")
        print(f"Expiry: {config.GS1_MEMBERSHIP_EXPIRY}")
        
        print("\nTo change these, edit config.py file")
        
        if config.YOUR_COMPANY_PREFIX == "61412345":
            print("\n  WARNING: You are using the DEMO prefix!")
            print("   This is NOT legal for real products!")
    
    def reserve_product_ranges(self):
        """
        STEP 3: RESERVE BARCODE RANGES FOR DIFFERENT PRODUCTS
        This organizes your barcodes logically
        """
        print("\n" + "-"*70)
        print(" RESERVE BARCODE RANGES FOR PRODUCT LINES")
        print("-"*70)
        
        # Example: Reserve ranges for different product categories
        reserved_ranges = [
            (1000, 1999, "Maize Flour Products - All sizes"),
            (2000, 2999, "Cooking Oils - All variants"),
            (3000, 3999, "Tea & Coffee Products"),
            (4000, 4999, "Dairy Products"),
            (5000, 5999, "Beverages & Juices"),
            (6000, 6999, "Household Products"),
            (7000, 7999, "Personal Care"),
            (8000, 8999, "Electronics"),
            (9000, 9999, "Other Products")
        ]
        
        for start, end, description in reserved_ranges:
            self.generator.reserve_product_range(start, end, description)
        
        return reserved_ranges
    
    def load_products_from_csv(self, csv_file='data/products.csv'):
        """
        STEP 4: LOAD YOUR PRODUCTS
        """
        products = []
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    row['price_ksh'] = float(row['price_ksh'])
                    row['tax_rate'] = int(row['tax_rate'])
                    products.append(row)
            
            print(f"\n Loaded {len(products)} products from {csv_file}")
            return products
            
        except FileNotFoundError:
            print(f"\n Product file not found: {csv_file}")
            print("   Creating sample products...")
            return self._create_sample_products()
    
    def _create_sample_products(self):
        """Create sample products if no CSV exists"""
        return [
            {
                'product_name': 'Premium Maize Flour 2kg',
                'category': 'Food Staples',
                'manufacturer': config.YOUR_COMPANY_NAME,
                'price_ksh': 185.00,
                'tax_rate': 16,
                'barcode_suffix': '1001',
                'product_line': 'Maize Flour Products'
            },
            {
                'product_name': 'Pure Sunflower Oil 3L',
                'category': 'Cooking',
                'manufacturer': config.YOUR_COMPANY_NAME,
                'price_ksh': 550.00,
                'tax_rate': 16,
                'barcode_suffix': '2001',
                'product_line': 'Cooking Oils'
            }
        ]
    
    def generate_legal_barcodes(self, products):
        """
        STEP 5: GENERATE LEGAL BARCODES FOR ALL PRODUCTS
        """
        print("\n" + "="*70)
        print(" GENERATING LEGAL KENYAN BARCODES")
        print("="*70)
        
        products_with_barcodes = []
        
        for idx, product in enumerate(products, 1):
            print(f"\n--- Product {idx}/{len(products)} ---")
            
            # Get barcode suffix from CSV or generate
            custom_suffix = product.get('barcode_suffix', None)
            
            # Generate legal barcode
            barcode, image_path = self.generator.generate_legal_barcode(
                product_name=product['product_name'],
                custom_suffix=custom_suffix
            )
            
            if barcode and image_path:
                product_with_barcode = product.copy()
                product_with_barcode.update({
                    'barcode': barcode,
                    'barcode_image': image_path
                })
                products_with_barcodes.append(product_with_barcode)
        
        return products_with_barcodes
    
    def export_legal_catalog(self, products_with_barcodes):
        """
        STEP 6: EXPORT LEGAL EXCEL CATALOG
        """
        print("\n" + "="*70)
        print("EXPORTING LEGAL EXCEL CATALOG")
        print("="*70)
        
        excel_file = self.exporter.create_legal_product_catalog(products_with_barcodes)
        return excel_file
    
    def print_legal_compliance_report(self, products_with_barcodes, excel_file):
        """
        STEP 7: PRINT COMPLETE LEGAL COMPLIANCE REPORT
        """
        print("\n" + "="*70)
        print(" GS1 KENYA LEGAL COMPLIANCE REPORT")
        print("="*70)
        
        # Get statistics
        stats = self.series_manager.get_series_statistics()
        
        print(f"""
╔════════════════════════════════════════════════════════════════╗
                     LEGAL COMPLIANCE SUMMARY                     
══════════════════════════════════════════════════════════════════
                                                                  
  COMPANY INFORMATION                                             
  ├─ Name: {config.YOUR_COMPANY_NAME[:40]}                  
  ├─ GS1 Prefix: {config.YOUR_COMPANY_PREFIX}                                         
  ├─ Certificate: {config.GS1_CERTIFICATE_NUMBER}                              
  └─ Valid Until: {config.GS1_MEMBERSHIP_EXPIRY}                                         
                                                                  
  BARCODE USAGE                                                   
  ├─ Total Capacity: {stats['total_capacity']:,} products                              
  ├─ Used: {stats['used_count']:,} products ({stats['usage_percentage']:.1f}%)                            
  ├─ Available: {stats['available_count']:,} products                                
  └─ This Batch: {len(products_with_barcodes)} products                                
                                                                  
  OUTPUT FILES                                                    
   ├─ Barcode Images: {config.BARCODE_DIR}                    
   └─ Excel Catalog: {excel_file}                 
                                                                  
  VERIFICATION                                                    
  ├─ Status: {' LEGAL' if not self.verifier.is_demo_mode else ' DEMO'} - Certified by GS1 Kenya                    
  └─ Verify at: www.gs1kenya.org/verify/{config.YOUR_COMPANY_PREFIX}          

══════════════════════════════════════════════════════════════════
        """)
    
    def run(self):
        """
        MAIN EXECUTION - RUN THE ENTIRE SYSTEM
        """
        try:
            #  REMOVED DUPLICATE VERIFICATION!
            # The legal_check() already verified status in __init__
            
            # STEP 2: Show prefix info
            self.setup_company_prefix()
            
            # STEP 3: Reserve ranges (only needed once)
            if self.series_manager.get_series_statistics()['used_count'] == 0:
                self.reserve_product_ranges()
            
            # STEP 4: Load products
            products = self.load_products_from_csv()
            
            # STEP 5: Generate barcodes
            products_with_barcodes = self.generate_legal_barcodes(products)
            
            # STEP 6: Export Excel
            excel_file = self.export_legal_catalog(products_with_barcodes)
            
            # STEP 7: Print compliance report
            self.print_legal_compliance_report(products_with_barcodes, excel_file)
            
            print("\n SYSTEM EXECUTION COMPLETE")
            if self.verifier.is_demo_mode:
                print("     DEMO MODE - Not for real sales")
            else:
                print("    Your barcodes are LEGAL and ready for Kenyan supermarkets!")
            
        except KeyboardInterrupt:
            print("\n  System stopped by user")
        except Exception as e:
            print(f"\n System error: {e}")
            raise

def main():
    """
    ENTRY POINT - START THE SYSTEM
    """
    system = KenyaLegalBarCodeSystem()
    system.run()

if __name__ == "__main__":
    main()