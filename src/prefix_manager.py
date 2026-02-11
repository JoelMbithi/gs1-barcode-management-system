
import json
from datetime import datetime
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import config

class BarcodeSeriesManager:
     """
    Manages your legal barcode series from GS1 Kenya
    Ensures you NEVER generate duplicate or out-of-range barcodes
    """
     
     def __init__(self):
          self.company_prefix = config.YOUR_COMPANY_PREFIX
          self.range_start = int(config.BARCODE_RANGE_START)
          self.range_end = int(config.BARCODE_RANGE_END)
          self.series_file = config.DATA_DIR/ "barcode_series.json"
          self.load_series()
    
     def load_series(self):
           """Load your used barcode numbers"""
           if os.path.exists(self.series_file):
                with open(self.series_file,'r') as f:
                     self.used_barcodes = json.load(f)

           else:
                self.used_barcodes = {
                     'company_prefix' : self.company_prefix,
                     'last_used_number': self.range_start -1, #start from beginning
                     'used_numbers': [],
                     'reserved_ranges':[]
                }
                self.save_series()
     
     def save_series(self):
            """Save your barcode usage"""
            with open(self.series_file, 'w') as f:
                 json.dump(self.used_barcodes,f, indent=2)

     def get_next_available_barcode(self, quantity=1):
           """
                  Get the next available barcode numbers in your legal range
                  
                  This ensures:
                  1. You never reuse a barcode number
                  2. You never go outside your assigned range
                  3. You can track all your issued barcodes
                  """
           available_numbers= []

           for _ in range(quantity):
                #Get next number
                next_number = self.used_barcodes["last_used_number"] + 1

                #check if within legal range

                if next_number > self.range_end:
                     raise ValueError(f"""
                            YOU HAVE USED ALL YOUR BARCODE NUMBERS!
                            Your GS1 Kenya range: {self.range_start} to {self.range_end}
                            You have assigned: {self.used_barcodes['last_used_number'] - self.range_start + 1} products
                            
                                SOLUTION: 
                            1. Contact GS1 Kenya: {config.GS1_KENYA['phone']}
                            2. Purchase additional barcode numbers
                            3. They will extend your range
                                            """)
                
                #formart as 12 digit string without check digit

                barcode_12 = str(next_number).zfill(12)

                #verify it starts with prefix
                if not barcode_12.startswith(self.company_prefix):
                     raise ValueError(f"""
                            BARCODE OUTSIDE YOUR ASSIGNED RANGE!
                            Your prefix: {self.company_prefix}
                            Generated: {barcode_12}
                            
                            Your barcodes MUST start with {self.company_prefix}
                                            """)
                
                available_numbers.append(barcode_12)
                self.used_barcodes['last_used_number'] = next_number
                self.used_barcodes['used_numbers'].append({
                     'barcode_12':barcode_12,
                     'assigned-date': datetime.now().isoformat(),
                     'product_code': barcode_12[-5:]# Last 5 digits
                })

                self.save_series()
                return available_numbers[0] if quantity == 1 else available_numbers
           


     def reserve_barcode_range(self, start_suffix, end_suffix, product_line):
        """
        Reserve a specific range for a product line
        
        Example: Reserve 1000-1999 for "Maize Flour" products
        """
        start_12 = f"{self.company_prefix}{str(start_suffix).zfill(5)}"
        end_12 = f"{self.company_prefix}{str(end_suffix).zfill(5)}"
        
        reserved_range = {
            'start': start_12,
            'end': end_12,
            'product_line': product_line,
            'reserved_date': datetime.now().isoformat()
        }
        
        self.used_barcodes['reserved_ranges'].append(reserved_range)
        self.save_series()
        
        return reserved_range
    
     def get_series_statistics(self):
        """Get usage statistics of your legal barcode range"""
        total_capacity = self.range_end - self.range_start + 1
        used_count = self.used_barcodes['last_used_number'] - self.range_start + 1
        available_count = total_capacity - used_count
        usage_percentage = (used_count / total_capacity) * 100
        
        return {
            'company_prefix': self.company_prefix,
            'range_start': self.range_start,
            'range_end': self.range_end,
            'total_capacity': total_capacity,
            'used_count': used_count,
            'available_count': available_count,
            'usage_percentage': usage_percentage,
            'membership_expiry': config.GS1_MEMBERSHIP_EXPIRY
        }
    
     def verify_barcode_legal(self, barcode_13):
        """
        Verify if a complete barcode (13 digits) is legal for YOUR company
        """
        # Check if it starts with your prefix
        if not barcode_13.startswith(self.company_prefix):
            return False, f"Not your company prefix. Expected {self.company_prefix}"
        
        # Check if it's in your assigned range
        barcode_12 = barcode_13[:12]
        barcode_num = int(barcode_12)
        
        if barcode_num < self.range_start or barcode_num > self.range_end:
            return False, f"Outside your assigned GS1 Kenya range"
        
        # Check if it's been issued
        for used in self.used_barcodes['used_numbers']:
            if used['barcode_12'] == barcode_12:
                return True, f"Valid - Issued on {used['assigned_date']}"
        
        return False, f"Valid range but not yet issued"