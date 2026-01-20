#!/usr/bin/env python3
"""
Unmerge merged verses in CRH translation files.

This script expands merged verse patterns like "24-26." into individual verses:
- First verse (24) gets the full content
- Subsequent verses (25, 26) get a reference placeholder: [24 ayetine baq.]

Usage:
    python3 scripts/unmerge_verses.py                    # Process both files
    python3 scripts/unmerge_verses.py --dry-run          # Preview without modifying
    python3 scripts/unmerge_verses.py --file <path>      # Process specific file
"""

import re
import sys
import argparse


def unmerge_verses(filename, dry_run=False):
    """
    Process a CRH translation file and unmerge merged verses.
    
    Args:
        filename: Path to the markdown file
        dry_run: If True, only report what would be changed
        
    Returns:
        dict with statistics about the operation
    """
    print(f"\n{'[DRY RUN] ' if dry_run else ''}Processing {filename}...")
    
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Pattern to match merged verses: "N-M. Text..." at start of line
    merged_pattern = re.compile(r'^(\d+)-(\d+)\.\s+(.*)')
    
    new_lines = []
    stats = {
        'merged_found': 0,
        'verses_expanded': 0,
        'surahs_affected': set()
    }
    
    current_surah = 0
    
    for line_idx, line in enumerate(lines):
        # Track surah for reporting
        surah_match = re.search(r'^#\s*(\d+)\.', line)
        if surah_match:
            current_surah = int(surah_match.group(1))
        
        # Check if this line starts with a merged verse pattern
        # Note: Verses always start at column 0 in this corpus, so no need
        # to filter by parenthesis depth (which was causing false negatives)
        match = merged_pattern.match(line)
        
        if match:
            start = int(match.group(1))
            end = int(match.group(2))
            content = match.group(3)
            
            # Count statistics
            stats['merged_found'] += 1
            stats['verses_expanded'] += (end - start)  # Additional verses created
            stats['surahs_affected'].add(current_surah)
            
            if dry_run:
                print(f"  Line {line_idx + 1} (Surah {current_surah}): {start}-{end}. -> verses {start} to {end}")
            
            # First verse gets the full content
            new_lines.append(f"{start}. {content}\n")
            
            # Subsequent verses get placeholder reference
            for verse_num in range(start + 1, end + 1):
                placeholder = f"[{start} ayetine baq.]\n"
                new_lines.append(f"{verse_num}. {placeholder}")
        else:
            new_lines.append(line)
    
    # Write output if not dry run
    if not dry_run:
        with open(filename, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print(f"  Wrote {len(new_lines)} lines to {filename}")
    
    # Convert set to count for JSON serializability
    stats['surahs_affected'] = len(stats['surahs_affected'])
    
    return stats


def main():
    parser = argparse.ArgumentParser(
        description='Unmerge merged verses in CRH translation files'
    )
    parser.add_argument(
        '--dry-run', 
        action='store_true',
        help='Preview changes without modifying files'
    )
    parser.add_argument(
        '--file',
        type=str,
        help='Process a specific file instead of all CRH files'
    )
    
    args = parser.parse_args()
    
    # Default files to process
    default_files = [
        'translations/quran-crh-dizen-qurtnezir-lat.md',
        'translations/quran-crh-dizen-qurtnezir.md'
    ]
    
    files_to_process = [args.file] if args.file else default_files
    
    total_stats = {
        'merged_found': 0,
        'verses_expanded': 0,
        'files_processed': 0
    }
    
    for filepath in files_to_process:
        try:
            stats = unmerge_verses(filepath, dry_run=args.dry_run)
            total_stats['merged_found'] += stats['merged_found']
            total_stats['verses_expanded'] += stats['verses_expanded']
            total_stats['files_processed'] += 1
            
            print(f"  Stats: {stats['merged_found']} merged ranges expanded, "
                  f"{stats['verses_expanded']} new verses added, "
                  f"across {stats['surahs_affected']} surahs")
        except FileNotFoundError:
            print(f"  ERROR: File not found: {filepath}")
            continue
    
    print(f"\n{'[DRY RUN] ' if args.dry_run else ''}Summary:")
    print(f"  Files processed: {total_stats['files_processed']}")
    print(f"  Total merged ranges found: {total_stats['merged_found']}")
    print(f"  Total new verses added: {total_stats['verses_expanded']}")
    
    if args.dry_run:
        print("\nRun without --dry-run to apply changes.")


if __name__ == "__main__":
    main()
