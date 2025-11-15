"""
Extract only HTML tables from MHTML files (ignoring quoted-printable encoding issues)
"""

import os
import re
from bs4 import BeautifulSoup
import quopri

def extract_html_from_mhtml(file_path):
    """Extract HTML content from MHTML file"""
    try:
        # Try UTF-8 first
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except:
        # Fallback to latin-1
        with open(file_path, 'r', encoding='latin-1') as f:
            content = f.read()
    
    # Find HTML section in MHTML
    # MHTML has sections separated by boundaries
    # HTML usually comes after Content-Type: text/html
    
    # Look for the HTML section
    html_match = re.search(r'Content-Type: text/html.*?charset[=:][\s"]*([\w-]+)', content, re.IGNORECASE | re.DOTALL)
    
    if html_match:
        # Find where HTML starts (after headers)
        start_pos = html_match.end()
        # Find next boundary or end of file
        next_boundary = re.search(r'\n------', content[start_pos:])
        if next_boundary:
            html_content = content[start_pos:start_pos + next_boundary.start()]
        else:
            html_content = content[start_pos:]
    else:
        # If no clear HTML section, use entire content
        html_content = content
    
    return html_content

def decode_if_quoted_printable(html_content):
    """Decode quoted-printable if present"""
    # Check if content is quoted-printable encoded
    if '=D8=A7' in html_content or '=3D' in html_content:
        try:
            # Try to decode quoted-printable
            decoded = quopri.decodestring(html_content.encode('latin-1'))
            return decoded.decode('utf-8', errors='ignore')
        except:
            pass
    
    return html_content

def extract_tables_from_mhtml(file_path):
    """Extract all tables from MHTML file"""
    print(f"\n📄 Processing: {os.path.basename(file_path)}")
    
    # Extract HTML
    html_content = extract_html_from_mhtml(file_path)
    
    # Try to decode if quoted-printable
    html_content = decode_if_quoted_printable(html_content)
    
    # Parse with BeautifulSoup
    soup = BeautifulSoup(html_content, 'lxml')
    
    # Find all tables
    tables = soup.find_all('table')
    
    print(f"   Found {len(tables)} table(s)")
    
    if tables:
        # Show preview of first table
        first_table = tables[0]
        rows = first_table.find_all('tr')[:3]
        print(f"   Preview (first 3 rows):")
        for i, row in enumerate(rows):
            cells = row.find_all(['td', 'th'])
            if cells:
                cell_texts = [cell.get_text(strip=True)[:20] for cell in cells[:4]]
                print(f"      Row {i+1}: {' | '.join(cell_texts)}")
    
    return tables

def test_all_companies():
    """Test extraction for all companies"""
    
    companies = {
        'زفجر': 'Data/Zfajr',
        'کاوه': 'Data/Kaveh',
        'گکوثر': 'Data/Gkowthar',
        'رنیک': 'Data/Renik',
        'قشیر': 'Data/Qshir',
        'زدشت': 'Data/Zdasht',
        'وسنا': 'Data/Vsana',
        'کگاز': 'Data/Kgaz',
        'تلیسه': 'Data/Tliseh'
    }
    
    print("="*70)
    print("Testing Table Extraction from MHTML Files")
    print("="*70)
    
    for company, folder in companies.items():
        print(f"\n{'='*70}")
        print(f"Company: {company}")
        print(f"{'='*70}")
        
        if not os.path.exists(folder):
            print(f"   ❌ Folder not found: {folder}")
            continue
        
        # Find income statement file
        files = os.listdir(folder)
        income_files = [f for f in files if 'سود' in f and f.endswith('.mhtml') and not f.endswith('.bak')]
        
        if income_files:
            file_path = os.path.join(folder, income_files[0])
            try:
                tables = extract_tables_from_mhtml(file_path)
                if tables:
                    print(f"   ✓ Successfully extracted {len(tables)} tables")
                else:
                    print(f"   ⚠️  No tables found")
            except Exception as e:
                print(f"   ❌ Error: {str(e)}")
        else:
            print(f"   ❌ No income statement file found")
    
    print("\n" + "="*70)
    print("Test Complete!")
    print("="*70)

if __name__ == '__main__':
    test_all_companies()
