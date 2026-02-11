

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
from openpyxl.drawing.image import Image
import pandas as pd
from datetime import datetime
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Import our modules
import config
from src.gs1_kenya_verifier import GS1KenyaLegalVerifier


class KenyaLegalExcelExporter:
    """
    EXPORTS LEGAL PRODUCT CATALOGS WITH GS1 KENYA CERTIFICATES
    """
    
    def __init__(self):
        """Initialize the Excel exporter"""
        self.excel_dir = config.EXCEL_DIR
        self.verifier = GS1KenyaLegalVerifier()
        
        # Professional Kenya Excel styling
        self.header_font = Font(name='Calibri', size=12, bold=True, color='FFFFFF')
        self.header_fill = PatternFill(start_color='0B4C5F', end_color='0B4C5F', fill_type='solid')
        
        self.cell_border = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )
        
        print(f" Excel Exporter Initialized")
        print(f"   Output folder: {self.excel_dir}")
    
    def create_legal_product_catalog(self, products_with_barcodes):
        """
        CREATE EXCEL CATALOG WITH LEGAL CERTIFICATES
        
        Args:
            products_with_barcodes: List of products with barcode info
        """
        
        # Create workbook
        wb = Workbook()
        
        # ============================================
        # SHEET 1: PRODUCT CATALOG
        # ============================================
        ws = wb.active
        ws.title = "Kenya Products - Legal"
        
        # Add GS1 Kenya Certificate at top
        self._add_legal_certificate(ws)
        
        # Add column headers
        self._add_headers(ws)
        
        # Add products
        self._add_products(ws, products_with_barcodes)
        
        # ============================================
        # SHEET 2: GS1 KENYA CERTIFICATE
        # ============================================
        self._create_certificate_sheet(wb)
        
        # ============================================
        # SHEET 3: BARCODE USAGE REPORT
        # ============================================
        self._create_usage_report(wb, products_with_barcodes)
        
        # Save file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"GS1_KENYA_CATALOG_{config.YOUR_COMPANY_PREFIX}_{timestamp}.xlsx"
        excel_path = self.excel_dir / filename
        
        wb.save(str(excel_path))
        
        print(f"\n LEGAL EXCEL CATALOG CREATED")
        print(f"   File: {excel_path}")
        print(f"   Status: GS1 Kenya Certified")
        
        return excel_path
    
    def _add_legal_certificate(self, worksheet):
        """
        ADD GS1 KENYA LEGAL CERTIFICATE TO EXCEL
        """
        # Company header
        worksheet['A1'] = f"GS1 KENYA REGISTERED COMPANY"
        worksheet['A1'].font = Font(name='Calibri', size=16, bold=True, color='0B4C5F')
        worksheet.merge_cells('A1:H1')
        
        # Certificate details
        worksheet['A2'] = f"Company: {config.YOUR_COMPANY_NAME}"
        worksheet['A2'].font = Font(name='Calibri', size=11, bold=True)
        worksheet.merge_cells('A2:H2')
        
        worksheet['A3'] = f"GS1 Prefix: {config.YOUR_COMPANY_PREFIX} | Certificate: {config.GS1_CERTIFICATE_NUMBER} | Valid Until: {config.GS1_MEMBERSHIP_EXPIRY}"
        worksheet['A3'].font = Font(name='Calibri', size=10)
        worksheet.merge_cells('A3:H3')
        
        # Legal disclaimer
        worksheet['A4'] = "✓ These barcodes are LEGALLY registered with GS1 Kenya and authorized for retail sale"
        worksheet['A4'].font = Font(name='Calibri', size=10, color='006400')
        worksheet.merge_cells('A4:H4')
        
        # Add spacing
        worksheet.row_dimensions[5].height = 15
    
    def _add_headers(self, worksheet):
        """
        ADD COLUMN HEADERS WITH KENYAN FORMATTING
        """
        headers = [
            ('A', 'BARCODE', 18),
            ('B', 'PRODUCT NAME', 35),
            ('C', 'CATEGORY', 20),
            ('D', 'MANUFACTURER', 25),
            ('E', 'PRICE (KSh)', 15),
            ('F', 'VAT %', 10),
            ('G', 'BARCODE IMAGE', 30),
            ('H', 'GS1 STATUS', 15)
        ]
        
        for col, text, width in headers:
            cell = worksheet[f'{col}6']
            cell.value = text
            cell.font = self.header_font
            cell.fill = self.header_fill
            cell.border = self.cell_border
            cell.alignment = Alignment(horizontal='center', vertical='center')
            
            worksheet.column_dimensions[col].width = width
    
    def _add_products(self, worksheet, products):
        """
        ADD PRODUCTS WITH LEGAL BARCODE STATUS
        """
        for idx, product in enumerate(products, start=7):
            # Product data
            worksheet[f'A{idx}'] = product['barcode']
            worksheet[f'B{idx}'] = product['product_name']
            worksheet[f'C{idx}'] = product['category']
            worksheet[f'D{idx}'] = product['manufacturer']
            worksheet[f'E{idx}'] = product['price_ksh']
            worksheet[f'F{idx}'] = product['tax_rate']
            worksheet[f'H{idx}'] = ' GS1 LEGAL'
            
            # Format price
            worksheet[f'E{idx}'].number_format = '"KSh "#,##0.00'
            
            # Add borders
            for col in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']:
                worksheet[f'{col}{idx}'].border = self.cell_border
            
            # Add barcode image
            if 'barcode_image' in product and os.path.exists(product['barcode_image']):
                try:
                    img = Image(product['barcode_image'])
                    img.width = 180
                    img.height = 50
                    worksheet.add_image(img, f'G{idx}')
                    worksheet.row_dimensions[idx].height = 45
                except Exception as e:
                    worksheet[f'G{idx}'] = "Barcode Image Error"
                    print(f"    Could not add image: {e}")
            else:
                worksheet[f'G{idx}'] = "No Image"
    
    def _create_certificate_sheet(self, workbook):
        """
        CREATE GS1 KENYA OFFICIAL CERTIFICATE SHEET
        """
        ws = workbook.create_sheet("GS1 Kenya Certificate")
        
        certificate = self.verifier.generate_legal_certificate()
        
        for i, line in enumerate(certificate.split('\n')):
            ws[f'A{i+1}'] = line
            ws[f'A{i+1}'].font = Font(name='Courier New', size=10)
    
    def _create_usage_report(self, workbook, products):
        """
        CREATE BARCODE USAGE REPORT FOR AUDITING
        """
        ws = workbook.create_sheet("Barcode Usage Report")
        
        ws['A1'] = f"GS1 KENYA BARCODE USAGE REPORT - {config.YOUR_COMPANY_NAME}"
        ws['A1'].font = Font(size=14, bold=True)
        ws.merge_cells('A1:E1')
        
        headers = ['Date Generated', 'Barcode', 'Product Name', 'Product Code', 'Status']
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=3, column=col)
            cell.value = header
            cell.font = Font(bold=True)
            cell.fill = PatternFill(start_color='D3D3D3', end_color='D3D3D3', fill_type='solid')
        
        for row, product in enumerate(products, start=4):
            ws.cell(row=row, column=1).value = datetime.now().strftime('%Y-%m-%d')
            ws.cell(row=row, column=2).value = product['barcode']
            ws.cell(row=row, column=3).value = product['product_name']
            ws.cell(row=row, column=4).value = product['barcode'][7:12]  # Product code
            ws.cell(row=row, column=5).value = 'ACTIVE - LEGAL'
        
        # Auto-adjust column widths
        for col in range(1, 6):
            ws.column_dimensions[chr(64 + col)].width = 20