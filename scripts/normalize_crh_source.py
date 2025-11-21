#!/usr/bin/env python3
"""
Normalize CRH (Crimean Tatar) source files by:
1. Removing line numbers
2. Removing carriage returns
3. Preserving structure (surahs, verses, commentary)
4. Creating a clean, parseable format
"""

import re
from pathlib import Path

def normalize_crh_file(input_path: Path, output_path: Path):
    """
    Normalize a CRH source file by removing line numbers and cleaning up formatting.
    
    Args:
        input_path: Path to the input file
        output_path: Path to the output file
    """
    print(f"Reading from: {input_path}")
    
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove carriage returns
    content = content.replace('\r\n', '\n').replace('\r', '\n')
    
    lines = content.split('\n')
    normalized_lines = []
    
    for line in lines:
        # Remove line numbers (format: "number: text" or "number. text")
        # Match patterns like "1: ", "123: ", "1. ", "123. "
        cleaned = re.sub(r'^\d+[:\.]\s*', '', line)
        normalized_lines.append(cleaned)
    
    # Join lines back together
    normalized_content = '\n'.join(normalized_lines)
    
    # Write to output
    print(f"Writing to: {output_path}")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(normalized_content)
    
    print(f"✓ Normalized {len(lines)} lines")

def main():
    """Main function to normalize both CRH source files."""
    base_dir = Path(__file__).parent.parent
    data_dir = base_dir / 'src' / 'data'
    
    # Normalize Latin transliteration file
    latin_input = data_dir / 'quran-crh-dizen-qurtnezir-lat.txt'
    latin_output = data_dir / 'quran-crh-dizen-qurtnezir-lat-normalized.txt'
    
    if latin_input.exists():
        normalize_crh_file(latin_input, latin_output)
    else:
        print(f"Warning: {latin_input} not found")
    
    # Normalize Cyrillic file
    cyrillic_input = data_dir / 'quran-crh-dizen-qurtnezir.md'
    cyrillic_output = data_dir / 'quran-crh-dizen-qurtnezir-normalized.md'
    
    if cyrillic_input.exists():
        normalize_crh_file(cyrillic_input, cyrillic_output)
    else:
        print(f"Warning: {cyrillic_input} not found")
    
    print("\n✓ Normalization complete!")
    print("\nNext steps:")
    print("1. Review the normalized files")
    print("2. Run parse_crh_verses.py to extract verses")
    print("3. Validate the parsed data")

if __name__ == '__main__':
    main()
