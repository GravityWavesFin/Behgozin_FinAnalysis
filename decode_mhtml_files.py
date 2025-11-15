"""
Decode و پاکسازی کامل فایل‌های MHTML
این اسکریپت همه فایل‌ها رو از quoted-printable decode می‌کنه
"""

import os
import quopri
from pathlib import Path
import shutil


def decode_mhtml_file(file_path):
    """Decode یک فایل MHTML و بازگشت محتوای decode شده"""
    try:
        # Read as binary first
        with open(file_path, 'rb') as f:
            content_bytes = f.read()
        
        # Decode the entire content from quoted-printable
        # This will decode all =XX sequences
        decoded_bytes = quopri.decodestring(content_bytes)
        
        # Now decode to text
        try:
            text = decoded_bytes.decode('utf-8')
        except UnicodeDecodeError:
            try:
                text = decoded_bytes.decode('windows-1256')
            except:
                text = decoded_bytes.decode('latin-1', errors='ignore')
        
        return text
            
    except Exception as e:
        print(f"Error decoding {file_path}: {e}")
        import traceback
        traceback.print_exc()
        return None


def process_all_mhtml_files(base_dir='Data'):
    """پردازش تمام فایل‌های MHTML در همه فولدرها"""
    
    folders = [
        'Zfajr', 'Kaveh', 'Gkowthar', 'Renik', 'Qshir', 
        'Zdasht', 'Vsana', 'Kgaz', 'Tliseh'
    ]
    
    total_processed = 0
    total_failed = 0
    
    for folder in folders:
        folder_path = os.path.join(base_dir, folder)
        if not os.path.exists(folder_path):
            print(f"Folder not found: {folder_path}")
            continue
        
        print(f"\n{'='*60}")
        print(f"Processing folder: {folder}")
        print(f"{'='*60}")
        
        # یافتن همه فایل‌های MHTML
        mhtml_files = list(Path(folder_path).glob('*.mhtml'))
        
        for file_path in mhtml_files:
            file_name = file_path.name
            
            # ایجاد backup
            backup_path = file_path.with_suffix('.mhtml.bak')
            if not backup_path.exists():
                shutil.copy2(file_path, backup_path)
                print(f"  Backup created: {file_name}.bak")
            
            # Decode
            print(f"  Decoding: {file_name}...", end=' ')
            decoded_content = decode_mhtml_file(file_path)
            
            if decoded_content:
                # ذخیره فایل decode شده
                try:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(decoded_content)
                    print("✓ Success")
                    total_processed += 1
                except Exception as e:
                    print(f"✗ Failed to save: {e}")
                    total_failed += 1
            else:
                print("✗ Failed to decode")
                total_failed += 1
    
    print(f"\n{'='*60}")
    print("Summary:")
    print(f"  Total processed: {total_processed}")
    print(f"  Total failed: {total_failed}")
    print(f"{'='*60}")
    
    if total_failed > 0:
        print("\n⚠️  Some files failed. Original backups saved with .bak extension")
    else:
        print("\n✓ All files decoded successfully!")
        print("   Original backups saved with .bak extension")


if __name__ == "__main__":
    print("="*60)
    print("MHTML File Decoder")
    print("="*60)
    print("\nThis will decode all MHTML files and create backups.")
    
    response = input("\nContinue? (yes/no): ").strip().lower()
    
    if response in ['yes', 'y']:
        process_all_mhtml_files()
        print("\n✓ Done! You can now run the analysis again.")
    else:
        print("Cancelled.")
