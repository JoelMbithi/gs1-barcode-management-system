
import os
from pathlib import Path
from datetime import datetime

#  PATHS
BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output"
BARCODE_DIR = OUTPUT_DIR / "barcodes"
EXCEL_DIR = OUTPUT_DIR / "excel"
DATA_DIR = BASE_DIR / "data"
CERTIFICATE_DIR = BASE_DIR / "certificates"

# Create directories
for directory in [OUTPUT_DIR, BARCODE_DIR, EXCEL_DIR, DATA_DIR, CERTIFICATE_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# ============================================
# 🔴🔴🔴 CRITICAL - YOUR REAL GS1 KENYA INFORMATION 🔴🔴🔴
# ============================================
# YOU MUST REPLACE THESE WITH YOUR ACTUAL GS1 KENYA DATA
# AFTER PAYING GS1 KENYA, YOU WILL RECEIVE THESE
# ============================================

#  STEP 1: GET THIS FROM GS1 KENYA AFTER PAYMENT
# They will email you a certificate with these details
YOUR_GS1_KENYA_STATUS = "ACTIVE"  # ACTIVE, PENDING, EXPIRED

#  STEP 2: YOUR UNIQUE COMPANY PREFIX FROM GS1 KENYA
# Example formats:
# - Small company: 614123 (6 digits)
# - Medium company: 6141234 (7 digits)  
# - Large company: 61412345 (8 digits)
# - Enterprise: 614123456 (9 digits)

YOUR_COMPANY_PREFIX = "61412345"  #  REPLACE WITH YOUR REAL NUMBER!

#  STEP 3: YOUR COMPANY REGISTRATION DETAILS
YOUR_COMPANY_NAME = "YOUR COMPANY NAME LTD"  # As registered with GS1 Kenya
YOUR_BUSINESS_REGISTRATION = "C123456"  # Your company registration number
YOUR_KRA_PIN = "P051234567K"  # Your KRA PIN
YOUR_ADDRESS = "P.O. Box 12345-00100, Nairobi, Kenya"

#  STEP 4: GS1 KENYA CERTIFICATE DETAILS
GS1_CERTIFICATE_NUMBER = "GS1-KE-2024-XXXXX"  # From your certificate
GS1_MEMBERSHIP_EXPIRY = "2025-12-31"  # When you must renew
GS1_REGISTRATION_DATE = "2024-01-15"  # When you registered

#  STEP 5: YOUR ASSIGNED BARCODE RANGE
# GS1 Kenya gives you a specific range based on your prefix
# Format: First 12 digits without check digit
BARCODE_RANGE_START = f"{YOUR_COMPANY_PREFIX}00000"  # First product
BARCODE_RANGE_END = f"{YOUR_COMPANY_PREFIX}99999"    # Last product (100,000 products)

# ============================================
# GS1 KENYA OFFICIAL CONTACT (DO NOT CHANGE)
# ============================================
GS1_KENYA = {
    'name': 'GS1 Kenya',
    'phone': '+254 20 802 5760',
    'email': 'info@gs1kenya.org',
    'website': 'www.gs1kenya.org',
    'address': '14th Floor, Kenya Re Towers, Upper Hill, Nairobi'
}

# ============================================
# LEGAL DISCLAIMERS
# ============================================
LEGAL_DISCLAIMER = f"""
LEGAL BARCODE CERTIFICATION - GS1 KENYA OFFICIAL
═══════════════════════════════════════════════════
Company: {YOUR_COMPANY_NAME}
GS1 Kenya Prefix: {YOUR_COMPANY_PREFIX}
Certificate No: {GS1_CERTIFICATE_NUMBER}
Valid Until: {GS1_MEMBERSHIP_EXPIRY}

This certifies that the barcodes in this document are:
 Legally registered with GS1 Kenya
 Paid for and valid for retail sale
 Unique to {YOUR_COMPANY_NAME}
 Recognized by all Kenyan supermarkets

VERIFY AT: www.gs1kenya.org/verify/{YOUR_COMPANY_PREFIX}
═══════════════════════════════════════════════════
"""

# ============================================
# DEMO MODE WARNING (Shown if no real prefix)
# ============================================
DEMO_MODE_WARNING = f"""
╔══════════════════════════════════════════════════════════════════╗
║   LEGAL WARNING - DEMO MODE ACTIVE                               ║
╚══════════════════════════════════════════════════════════════════╝




"""