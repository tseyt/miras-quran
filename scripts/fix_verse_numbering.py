import re
import sys

def fix_verse_numbering(filename):
    print(f"Processing {filename}...")
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    # Regex to match verse start: "N. Text" or "N-M. Text"
    verse_pattern = re.compile(r'^(\d+)(?:-(\d+))?\.\s(.*)')
    
    current_surah = 0
    next_expected_verse = 1
    current_offset = 0
    
    # Track parenthesis depth to avoid numbering inside commentaries
    paren_depth = 0
    
    for line_idx, line in enumerate(lines):
        stripped = line.strip()
        
        # Update parenthesis depth based on THIS line's content BEFORE processing verse logic?
        # A verse line might start with "1. (Text...".
        # A commentary line might be "1. Text" inside a block started previously.
        
        # We should count parens in the line.
        # But we need to know if we are ALREADY in a block at the START of the line.
        # So we use `paren_depth` calculated from previous lines.
        
        # However, checking if the line *itself* is a verse happens first.
        # If we are in depth > 0, we treat it as non-verse.
        
        is_surah_header = line.startswith('#') and re.search(r'#\s*(\d+)\.', line)
        
        if is_surah_header:
            surah_match = re.search(r'#\s*(\d+)\.', line)
            current_surah = int(surah_match.group(1))
            next_expected_verse = 1
            current_offset = 0
            paren_depth = 0 # Reset depth at Surah start just in case
            new_lines.append(line)
            continue
            
        # Check if it *looks* like a verse
        match = verse_pattern.match(line)
        
        is_verse_candidate = False
        if match:
            # It matches the pattern.
            # But is it inside commentary?
            if paren_depth > 0:
                # Likely a list item in commentary
                # But double check: could it be a verse inside parens? (Very rare in this dataset)
                # We assume verses are top level.
                is_verse_candidate = False
            else:
                is_verse_candidate = True
        
        if is_verse_candidate and match:
            files_start = int(match.group(1))
            files_end_str = match.group(2)
            files_end = int(files_end_str) if files_end_str else files_start
            rest_of_line = match.group(3)
            
            # Logic to detecting numbering errors
            
            # 1. Reset logic if file says 1 and we expect something else (and 1 is plausible)
            if files_start == 1 and next_expected_verse != 1:
                # Forced reset
                next_expected_verse = 1
                current_offset = 0
            
            current_val_start = files_start + current_offset
            
            # 2. Check for lag (File < Expected)
            if current_val_start < next_expected_verse:
                # We need to increase offset
                possible_new_offset = next_expected_verse - files_start
                if possible_new_offset > current_offset:
                     # print(f"[Surah {current_surah}] Fix: Line {files_start} -> Expected {next_expected_verse}. Offset {current_offset}->{possible_new_offset}")
                     current_offset = possible_new_offset
            
            elif current_val_start > next_expected_verse:
                 # File > Expected.
                 # Maybe we over-offset? Or file skipped a number?
                 # If files_start matches expected, reset offset to 0.
                 if files_start == next_expected_verse:
                     current_offset = 0
                 else:
                     # Try to align
                     possible_new_offset = next_expected_verse - files_start
                     # Allow backward shifts too, assuming we don't skip verses in this corpus.
                     # But let's be careful about huge jumps?
                     # If gap is > 50, maybe warn? But for now, just fix it.
                     current_offset = possible_new_offset
            
            # Calculate final numbers
            final_start = files_start + current_offset
            if files_end_str:
                # Determine gap
                gap = files_end - files_start
                final_end = final_start + gap
            else:
                final_end = final_start
            
            # Reconstruct
            if files_end_str:
                prefix = f"{final_start}-{final_end}."
            else:
                prefix = f"{final_start}."
            
            new_lines.append(f"{prefix} {rest_of_line}\n")
            
            next_expected_verse = final_end + 1
            
        else:
            new_lines.append(line)
        
        # Update parenthesis depth for NEXT line
        # Count unescaped parens? Simple count is enough usually.
        open_p = line.count('(')
        close_p = line.count(')')
        paren_depth += (open_p - close_p)
        if paren_depth < 0: paren_depth = 0 # Should not happen usually

    with open(filename, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print(f"Finished {filename}.")

if __name__ == "__main__":
    files = [
        'translations/quran-crh-dizen-qurtnezir.md',
        'translations/quran-crh-dizen-qurtnezir-lat.md'
    ]
    for f in files:
        fix_verse_numbering(f)
