# gs1-barcode-management-system
A GS1 Kenya compliant EAN-13 barcode generator for Kenyan businesses selling in supermarkets.

---

## What is this?

If you manufacture or distribute products in Kenya, you need barcodes. Supermarkets like Naivas, Quickmart, Carrefour, and Tuskys require EAN-13 barcodes on every product.

This system generates those barcodes. It creates the actual PNG images and exports everything to Excel with the barcodes embedded.

I built this because I couldn't find a simple, affordable tool that specifically supports Kenya's GS1 prefix.

---

## What does it do?

- Generates EAN-13 barcodes with Kenya's prefix (614 for demo, 616 for real GS1 members)
- Calculates check digits automatically using the official GS1 algorithm
- Creates high-resolution PNG files ready for printing
- Exports professional Excel catalogs with barcode images embedded
- Tracks every barcode you've ever issued (so you never reuse numbers)
- Organizes products by categories with reserved barcode ranges

---

## Who is this for?

- Kenyan food manufacturers
- Local product distributors  
- Importers preparing for retail
- E-commerce sellers
- Anyone selling products in Kenyan supermarkets

---

## Before you start

**Two ways to use this system:**

### 1. DEMO Mode (Free, for testing)
- No registration required
- Generate unlimited test barcodes
- All features work
- **NOT legal for actual sales**
- Barcodes start with 614

### 2. PRODUCTION Mode (Legal, for real sales)
- You must register with GS1 Kenya first
- Pay annual fee (KSh 15,000 - 50,000)
- Get your official company prefix (starts with 616)
- Update one line in config.py
- **100% legal, accepted by all supermarkets**

---

## Quick start (DEMO mode)

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/kenya-barcode-system.git
cd kenya-barcode-system

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the system
python main.py

# 5. When prompted, type 'no' for DEMO mode
Are you generating barcodes for REAL products to sell? (yes/no): no

kenya-barcode-system/
│
├── src/                    # Source code
│   ├── barcode_generator.py    # Creates the actual barcodes
│   ├── excel_exporter.py       # Exports to Excel with images
│   ├── gs1_kenya_verifier.py  # Handles legal verification
│   └── prefix_manager.py      # Tracks your barcode numbers
│
├── data/                   # Your product data
│   └── products.csv            # Add your products here
│
├── output/                 # Generated files
│   ├── barcodes/              # PNG barcode images
│   └── excel/                 # Excel catalogs
│
├── config.py               # Your GS1 Kenya settings
├── main.py                 # Run the system
└── requirements.txt        # Python packages
