#!/usr/bin/env python3
"""
Clean and normalize CRH translation markdown files.
This script normalizes both the Cyrillic and Latin versions to have consistent structure.
"""

import re
import sys

def clean_crh_file(input_path: str, output_path: str = None):
    """
    Clean and normalize a CRH translation markdown file.
    
    Cleaning operations:
    1. Normalize surah headers to `# N. SURAH_NAME` format
    2. Remove excessive blank lines (max 1 between sections)
    3. Ensure verse numbers are on their own lines properly formatted
    4. Remove trailing whitespace
    """
    
    if output_path is None:
        output_path = input_path
    
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    cleaned_lines = []
    prev_blank = False
    in_front_matter = True
    
    # Patterns - match both # and ## for surah headers
    surah_header_pattern = re.compile(r'^#{1,2}\s*(\d+)\.\s*(.+?)\s*$')
    verse_pattern = re.compile(r'^(\d+)\.\s+(.+)$')
    
    for i, line in enumerate(lines):
        # Strip trailing whitespace
        line = line.rstrip()
        
        # Check for surah header
        surah_match = surah_header_pattern.match(line)
        if surah_match:
            in_front_matter = False
            surah_num = surah_match.group(1)
            surah_name = surah_match.group(2).strip()
            # Normalize to consistent format
            line = f"# {surah_num}. {surah_name}"
            # Ensure blank line before surah header (unless at start)
            if cleaned_lines and cleaned_lines[-1] != '':
                cleaned_lines.append('')
        
        # Handle blank lines - don't stack them
        if line == '':
            if prev_blank:
                continue  # Skip consecutive blank lines
            prev_blank = True
        else:
            prev_blank = False
        
        cleaned_lines.append(line)
    
    # Remove trailing blank lines
    while cleaned_lines and cleaned_lines[-1] == '':
        cleaned_lines.pop()
    
    # Write cleaned content
    cleaned_content = '\n'.join(cleaned_lines)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(cleaned_content)
    
    print(f"Cleaned {input_path}")
    print(f"  Original lines: {len(lines)}")
    print(f"  Cleaned lines: {len(cleaned_lines)}")
    
    return len(cleaned_lines)


def compare_files(cyr_path: str, lat_path: str):
    """Compare the structure of both files and report differences."""
    
    with open(cyr_path, 'r', encoding='utf-8') as f:
        cyr_lines = f.read().split('\n')
    
    with open(lat_path, 'r', encoding='utf-8') as f:
        lat_lines = f.read().split('\n')
    
    # Find surah headers in each file
    surah_pattern = re.compile(r'^#\s*(\d+)\.\s*(.+)$')
    
    cyr_surahs = []
    lat_surahs = []
    
    for i, line in enumerate(cyr_lines):
        match = surah_pattern.match(line)
        if match:
            cyr_surahs.append((int(match.group(1)), match.group(2), i + 1))
    
    for i, line in enumerate(lat_lines):
        match = surah_pattern.match(line)
        if match:
            lat_surahs.append((int(match.group(1)), match.group(2), i + 1))
    
    print(f"\nComparison:")
    print(f"  Cyrillic file: {len(cyr_lines)} lines, {len(cyr_surahs)} surahs")
    print(f"  Latin file: {len(lat_lines)} lines, {len(lat_surahs)} surahs")
    
    # Check for missing surahs
    cyr_nums = set(s[0] for s in cyr_surahs)
    lat_nums = set(s[0] for s in lat_surahs)
    
    if cyr_nums != lat_nums:
        print(f"\n  ⚠️  Surah count mismatch!")
        missing_in_lat = cyr_nums - lat_nums
        missing_in_cyr = lat_nums - cyr_nums
        if missing_in_lat:
            print(f"    Missing in Latin: {sorted(missing_in_lat)}")
        if missing_in_cyr:
            print(f"    Missing in Cyrillic: {sorted(missing_in_cyr)}")
    else:
        print(f"\n  ✅ Both files have same {len(cyr_nums)} surahs")


if __name__ == '__main__':
    import os
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    translations_dir = os.path.join(base_dir, 'translations')
    
    cyr_path = os.path.join(translations_dir, 'quran-crh-dizen-qurtnezir.md')
    lat_path = os.path.join(translations_dir, 'quran-crh-dizen-qurtnezir-lat.md')
    
    print("Cleaning CRH translation files...\n")
    
    # Clean both files
    print("=" * 50)
    clean_crh_file(cyr_path)
    print()
    print("=" * 50)
    clean_crh_file(lat_path)
    print()
    
    # Compare structure
    print("=" * 50)
    compare_files(cyr_path, lat_path)
