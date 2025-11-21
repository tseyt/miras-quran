#!/usr/bin/env python3
"""
Format CRH Latin file to match Cyrillic .md structure.
Removes excessive whitespace and converts to markdown format.
"""

import re
from pathlib import Path


def format_crh_latin():
    """Format the Latin CRH file to match Cyrillic .md structure."""
    
    # Input and output paths
    input_file = Path("src/data/quran-crh-dizen-qurtnezir-lat.txt")
    output_file = Path("src/data/quran-crh-dizen-qurtnezir-lat.md")
    
    print(f"Reading from: {input_file}")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Normalize line endings
    content = content.replace('\r\n', '\n').replace('\r', '\n')
    
    lines = content.split('\n')
    formatted_lines = []
    
    # Track consecutive blank lines
    blank_count = 0
    prev_was_header = False
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Check if this is a blank line
        if not stripped:
            blank_count += 1
            # Only allow max 1 consecutive blank line (2 total with the blank line itself)
            if blank_count <= 1:
                formatted_lines.append('')
            continue
        else:
            blank_count = 0
        
        # Check if this looks like a header
        
        # Surah headers like "1. el-FAATİhA" or "2. el-BAQARA"
        # Match pattern: Number dot space (optional el-) Mixed Case
        if re.match(r'^\d+\.\s+(?:el-|en-|et-|eş-|er-|ez-|AAL-i\s+)?[A-Za-zİıĞğÜüŞşÖöÇç\-\'\s]+$', stripped):
            formatted_lines.append(f"**{stripped}**")
            continue
            
        # Specific headers from the beginning of the file
        if stripped in ['Qur\'an-ı Kerim ve izaatlı manası', 'Söz başı', 'Ekinci neşirge söz başı', 'Bismillâahirrahmaanirrahiim.', 'Qur\'an ve manası', 'Amin!', 'EMİRALİ ABLAYeV,']:
            formatted_lines.append(f"**{stripped}**")
            continue
            
        # Section headers (short lines that look like titles)
        # Exclude verse lines starting with numbers
        if (len(stripped) < 60 and 
              not re.match(r'^\d+\.', stripped) and 
              not stripped.startswith('(') and
              not any(word in stripped.lower() for word in ['olaraq', 'içün', 'kibi', 'olğan', 'ise', 'da', 'de'])):
            # Check if it might be a header
            if not stripped.endswith(('.', ',', ')', '!')) or len(stripped) < 30:
                # Look ahead to see if next non-empty line is longer (indicates this is a header)
                next_line_idx = i + 1
                while next_line_idx < len(lines) and not lines[next_line_idx].strip():
                    next_line_idx += 1
                
                if next_line_idx < len(lines):
                    next_line = lines[next_line_idx].strip()
                    if len(next_line) > len(stripped) * 1.5:
                        formatted_lines.append(f"**{stripped}**")
                        continue
        
        # Special formatting for "BİSMİLLYa" and similar
        if stripped in ['BİSMİLLYa', 'BISMILLYA', 'Bismillâahirrahmaanirrahiim']:
            formatted_lines.append(f"**{stripped}**")
            continue
        
        # Regular line - just add it
        formatted_lines.append(line.rstrip())
    
    # Join lines
    formatted_content = '\n'.join(formatted_lines)
    
    # Clean up excessive blank lines (more than 2 consecutive)
    formatted_content = re.sub(r'\n{3,}', '\n\n', formatted_content)
    
    # Clean up trailing whitespace
    formatted_content = '\n'.join(line.rstrip() for line in formatted_content.split('\n'))
    
    # Write output
    print(f"Writing to: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(formatted_content)
    
    # Stats
    original_lines = len(lines)
    formatted_line_count = len(formatted_content.split('\n'))
    blank_removed = original_lines - formatted_line_count
    
    print(f"\n✓ Formatting complete!")
    print(f"  Original lines: {original_lines}")
    print(f"  Formatted lines: {formatted_line_count}")
    print(f"  Blank lines removed: {blank_removed}")
    print(f"  Output: {output_file}")


if __name__ == "__main__":
    format_crh_latin()
