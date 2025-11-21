import re
import os

def convert_to_md(input_path, output_path):
    print(f"Reading from {input_path}")
    with open(input_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Normalize newlines
    text = text.replace('\r\n', '\n')

    # 1. Insert newlines before embedded verses
    # Pattern: space, number, dot, space, (Uppercase or open paren)
    verse_start_pattern = re.compile(r'(\s)((?:\d+(?:-\d+)?)\.\s+(?:[A-ZİıĞğÜüŞşÖöÇçÂâÎîÛû\-\'\(]))')
    text = verse_start_pattern.sub(r'\n\2', text)
    
    # 2. Split into lines
    raw_lines = text.split('\n')
    
    # 3. Merge lines to form full paragraphs/verses
    merged_lines = []
    current_line = ""
    
    # Regex to identify if a line STARTS a new block (Verse or Surah Header)
    # Surah Header: "1. el-FAATİһA"
    surah_start_pattern = re.compile(r'^(\d+)\.\s+(el-[A-ZİıĞğÜüŞşÖöÇçÂâÎîÛû\-\'һ ]+|[A-ZİıĞğÜüŞşÖöÇçÂâÎîÛû\-\'һ ]+)$')
    # Verse Start: "1. "
    verse_start_pattern_line = re.compile(r'^(\d+(?:-\d+)?)\.\s+')
    
    # Specific Headers list (exact matches or starts with)
    known_headers = [
        "Qur’an-ı Kerim ve izaatlı manası",
        "Söz başı",
        "Ekinci neşirge söz başı",
        "Qur’an ve manası",
        "SAİT DİZEN, ZAKİR QURTNEZİR."
    ]

    for line in raw_lines:
        line = line.strip()
        if not line:
            # Blank line -> End current block
            if current_line:
                merged_lines.append(current_line)
                current_line = ""
            merged_lines.append("") # Preserve blank line
            continue
        
        # Check if this line starts a new block
        is_new_block = False
        
        # Check Headers
        if any(line.startswith(h) for h in known_headers):
            is_new_block = True
        elif surah_start_pattern.match(line):
            is_new_block = True
        elif verse_start_pattern_line.match(line):
            is_new_block = True
        
        if is_new_block:
            if current_line:
                merged_lines.append(current_line)
            current_line = line
        else:
            # Continuation of previous line
            if current_line:
                current_line += " " + line
            else:
                current_line = line
    
    if current_line:
        merged_lines.append(current_line)
        
    # 4. Process Merged Lines to Markdown
    output_lines = []
    
    # Re-compile patterns for processing
    verse_pattern = re.compile(r'^(\d+(?:-\d+)?)\.\s+(.*)')
    
    headers_map = {
        "Qur’an-ı Kerim ve izaatlı manası": "# Qur’an-ı Kerim ve izaatlı manası",
        "Söz başı": "# Söz başı",
        "Ekinci neşirge söz başı": "## Ekinci neşirge söz başı",
        "Qur’an ve manası": "# Qur’an ve manası",
        "SAİT DİZEN, ZAKİR QURTNEZİR.": "# SAİT DİZEN, ZAKİR QURTNEZİR."
    }

    for line in merged_lines:
        if not line:
            output_lines.append("")
            continue
        
        # Check Headers
        if line in headers_map:
            output_lines.append(headers_map[line])
            continue
        
        # Check Surah Header
        surah_match = surah_start_pattern.match(line)
        if surah_match:
            output_lines.append(f"# {line}")
            continue
        
        # Check Verse
        verse_match = verse_pattern.match(line)
        if verse_match:
            number = verse_match.group(1)
            content = verse_match.group(2)
            
            # Check for commentary at the end
            last_paren_idx = content.rfind(' (')
            if last_paren_idx != -1:
                commentary = content[last_paren_idx+1:] # includes (
                if commentary.endswith(')') and len(commentary) > 15:
                    verse_text = content[:last_paren_idx]
                    output_lines.append(f"{number}. {verse_text}")
                    output_lines.append(f"{commentary}")
                    continue
            
            output_lines.append(f"{number}. {content}")
            continue
        
        # Default: just text
        output_lines.append(line)
    
    print(f"Writing to {output_path}")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))
    print("Done.")

if __name__ == "__main__":
    convert_to_md(
        '/Users/tanerseyt/Documents/Code/miras-quran/translations/quran-crh-dizen-qurtnezir-lat.txt',
        '/Users/tanerseyt/Documents/Code/miras-quran/translations/quran-crh-dizen-qurtnezir-lat.md'
    )
