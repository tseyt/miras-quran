import re
import sys

def find_errors(filename):
    print(f"Scanning {filename}...")
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    verse_pattern = re.compile(r'^(\d+)(?:-(\d+))?\.\s')
    
    last_verse_end = 0
    current_surah = 0
    paren_depth = 0
    
    errors = []

    for i, line in enumerate(lines):
        line = line.strip()
        
        if line.startswith('#') and re.search(r'#\s*(\d+)\.', line):
            match = re.search(r'#\s*(\d+)\.', line)
            current_surah = int(match.group(1))
            last_verse_end = 0
            paren_depth = 0
            continue
        
        # Determine if verse BEFORE updating depth (assuming numbered lists in comments are indented or valid text)
        # We use the same look-ahead/look-behind logic idea? 
        # Actually just simplified: check depth before processing.
        
        is_verse = False
        match = verse_pattern.match(line)
        if match:
            if paren_depth == 0:
                is_verse = True
        
        if is_verse and match:
            start_verse = int(match.group(1))
            end_verse = int(match.group(2)) if match.group(2) else start_verse
            
            expected_next = last_verse_end + 1
            
            if last_verse_end == 0:
                if start_verse != 1:
                    pass 
            else:
                if start_verse != expected_next:
                    errors.append({
                        'line_num': i + 1,
                        'surah': current_surah,
                        'text': line[:50],
                        'expected': expected_next,
                        'found': start_verse,
                        'prev_end': last_verse_end
                    })
            
            last_verse_end = end_verse
            
        # Update depth
        # Note: simplistic count. Handles ( ... ) on same line or multi lines.
        open_p = line.count('(')
        close_p = line.count(')')
        paren_depth += (open_p - close_p)
        if paren_depth < 0: paren_depth = 0

    if not errors:
        print(f"No errors found in {filename}.")
    else:
        print(f"Found {len(errors)} potential errors in {filename}:")
        for err in errors:
            print(f"Line {err['line_num']} (Surah {err['surah']}): Expected {err['expected']}, Found {err['found']} (Prev ended at {err['prev_end']})")
            print(f"  Content: {err['text']}...")
    print("-" * 40)
    return errors

if __name__ == "__main__":
    files = [
        'translations/quran-crh-dizen-qurtnezir.md',
        'translations/quran-crh-dizen-qurtnezir-lat.md'
    ]
    for f in files:
        find_errors(f)
