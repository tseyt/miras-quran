#!/usr/bin/env python3
"""
Parse CRH verses from normalized source files.
Separates verse text from commentary (text in parentheses).
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional

class CRHVerseParser:
    """Parser for CRH Quran verses."""
    
    # Mapping of CRH surah names (both Latin and Cyrillic) to standard surah numbers
    SURAH_NAME_MAP = {
        # Latin script names
        'el-FAATİhA': 1, 'el-FAATIHA': 1,
        'el-BAQARA': 2,
        'AAL-i İMRAN': 3, 'AAL-i IMRAN': 3,
        'en-NİSAA': 4, 'en-NISAA': 4,
        'el-MAA\'İDE': 5, 'el-MAAIDE': 5,
        'el-EN\'AAM': 6, 'el-ENAAM': 6,
        'el-A\'RAAF': 7, 'el-ARAAF': 7,
        'el-ENFAAL': 8,
        'et-TEVBE': 9,
        'YUNUS': 10,
        'HUUD': 11,
        'YUSUF': 12,
        'er-RA\'D': 13, 'er-RAD': 13,
        'İBRAHİM': 14, 'IBRAHIM': 14,
        'el-hİCR': 15, 'el-HICR': 15,
        'en-NAhL': 16, 'en-NAHL': 16,
        'el-İSRAA': 17, 'el-ISRAA': 17,
        'el-KEhF': 18, 'el-KEHF': 18,
        'MERYEM': 19,
        'TAA-hAA': 20, 'TAA-HAA': 20,
        'el-ENBİYAA': 21, 'el-ENBIYAA': 21,
        'el-hACC': 22, 'el-HACC': 22,
        'el-MU\'MİNUUN': 23, 'el-MUMINUUN': 23,
        'en-NUUR': 24,
        'el-FURQAN': 25,
        'eş-ŞU\'ARAA': 26, 'eş-SUARAA': 26,
        'en-NEML': 27,
        'el-QASAS': 28,
        'el-\'ANKEBUUt': 29, 'el-ANKEBUUT': 29,
        'er-RUUM': 30,
        'LUQMAN': 31,
        'es-SECDE': 32,
        'el-AhZAAB': 33, 'el-AHZAAB': 33,
        'SEBE\'': 34, 'SEBE': 34,
        'FAATİR': 35, 'FAATIR': 35,
        'YAA-SİİN': 36, 'YAA-SIIN': 36,
        'es-SAAFFAAT': 37,
        'SAAD': 38,
        'ez-ZUMER': 39,
        'ĞAAFİR': 40, 'GAAFIR': 40,
        'FUSSİLET': 41, 'FUSSILET': 41,
        'eş-ŞUURAA': 42, 'eş-SUURAA': 42,
        'ez-ZUhRUF': 43, 'ez-ZUHRUF': 43,
        'ed-DUhAAN': 44, 'ed-DUHAAN': 44,
        'el-CAASİYE': 45, 'el-CAASIYE': 45,
        'el-AhQAAF': 46, 'el-AHQAAF': 46,
        'MUhAMMED': 47, 'MUHAMMED': 47,
        'el-FETh': 48, 'el-FETH': 48,
        'el-hUCURAAt': 49, 'el-HUCURAAT': 49,
        'QAAF': 50,
        'ez-ZAARİYAAt': 51, 'ez-ZAARIYAAT': 51,
        'et-TUUR': 52,
        'en-NECM': 53,
        'el-QAMER': 54,
        'er-RAhMAAN': 55, 'er-RAHMAAN': 55,
        'el-VAAQİ\'A': 56, 'el-VAAQIA': 56,
        'el-hADİİD': 57, 'el-HADIID': 57,
        'el-MUCADİLE': 58, 'el-MUCADILE': 58,
        'el-hAŞR': 59, 'el-HASR': 59,
        'el-MUMTEhİNE': 60, 'el-MUMTEHINE': 60,
        'es-SAFF': 61,
        'el-CUMU\'A': 62, 'el-CUMUA': 62,
        'el-MUNAAFİQUUN': 63, 'el-MUNAAFIQUUN': 63,
        'et-TEĞAABüN': 64, 'et-TEGAABUN': 64,
        'et-TALÂAQ': 65, 'et-TALAAQ': 65,
        'et-TAhRİİM': 66, 'et-TAHRIIM': 66,
        'el-MULK': 67,
        'el-QALEM': 68,
        'el-hAAQQA': 69, 'el-HAAQQA': 69,
        'el-ME\'ARIC': 70, 'el-MEARIC': 70,
        'NUUh': 71, 'NUUH': 71,
        'el-CİNN': 72, 'el-CINN': 72,
        'el-MUZZEMMİL': 73, 'el-MUZZEMMIL': 73,
        'el-MUDDESSİR': 74, 'el-MUDDESSIR': 74,
        'el-QİYAAME': 75, 'el-QIYAAME': 75,
        'el-İNSAAN': 76, 'el-INSAAN': 76,
        'el-MURSELAAt': 77, 'el-MURSELAAT': 77,
        'en-NEBE\'': 78, 'en-NEBE': 78,
        'en-NAAZİ\'AAt': 79, 'en-NAAZIAT': 79,
        '\'ABESE': 80, 'ABESE': 80,
        'et-TEKVİİR': 81, 'et-TEKVIIR': 81,
        'el-İNFİTAAR': 82, 'el-INFITAAR': 82,
        'el-MUTAFFİFİİN': 83, 'el-MUTAFFIFIIN': 83,
        'el-İNŞİQAAQ': 84, 'el-INSIQAAQ': 84,
        'el-BURUUc': 85,
        'et-TAARİQ': 86, 'et-TAARIQ': 86,
        'el-A\'LAA': 87, 'el-ALAA': 87,
        'el-ĞAAŞİYE': 88, 'el-GAASIYE': 88,
        'el-FECR': 89,
        'el-BELED': 90,
        'eş-ŞEMS': 91, 'eş-SEMS': 91,
        'el-LEYL': 92,
        'ez-ZUhAA': 93, 'ez-ZUHAA': 93,
        'eş-ŞERh': 94, 'eş-SERH': 94,
        'et-TİİN': 95, 'et-TIIN': 95,
        'el-\'ALAQ': 96, 'el-ALAQ': 96,
        'el-QADR': 97,
        'el-BEYYİNE': 98, 'el-BEYYINE': 98,
        'ez-ZİLZAAL': 99, 'ez-ZILZAAL': 99,
        'el-\'AADİYAAt': 100, 'el-AADIYAAT': 100,
        'el-QAARİ\'A': 101, 'el-QAARIA': 101,
        'et-TEKAASUR': 102,
        'el-\'ASR': 103, 'el-ASR': 103,
        'el-hUMEZE': 104, 'el-HUMEZE': 104,
        'el-FİİL': 105, 'el-FIIL': 105,
        'QUREYŞİ': 106, 'QUREYSI': 106,
        'el-MAA\'UUN': 107, 'el-MAAUUN': 107,
        'el-KEVSER': 108,
        'el-KAAFİRUUN': 109, 'el-KAAFIRUUN': 109,
        'en-NASR': 110,
        'el-MESED': 111,
        'el-İhLAAS': 112, 'el-IHLAAS': 112,
        'el-FELEQ': 113,
        'en-NAAS': 114,
        # Cyrillic script names (if needed)
        'эль-ФААТИHА': 1,
        'эль-БАҚАРА': 2,
        # Add more Cyrillic mappings as needed
    }
    
    def __init__(self, source_file: Path):
        """
        Initialize parser with source file.
        
        Args:
            source_file: Path to normalized CRH source file
        """
        self.source_file = source_file
        self.content = self._load_file()
        self.surahs: Dict[int, Dict] = {}
    
    def _load_file(self) -> str:
        """Load and return file content."""
        with open(self.source_file, 'r', encoding='utf-8') as f:
            return f.read()
    
    def _extract_verse_number(self, text: str) -> Optional[int]:
        """
        Extract verse number from text like "1. Text" or "1\\. Text".
        
        Args:
            text: Text potentially containing verse number
            
        Returns:
            Verse number if found, None otherwise
        """
        # Match patterns like "1. ", "123. ", "1\\. ", etc.
        match = re.match(r'^(\d+)[\\.]\s+', text)
        if match:
            return int(match.group(1))
        return None
    
    def _separate_verse_and_commentary(self, text: str) -> Tuple[str, str]:
        """
        Separate verse text from commentary.
        Commentary is typically in parentheses at the end.
        
        Args:
            text: Full text containing verse and possibly commentary
            
        Returns:
            Tuple of (verse_text, commentary)
        """
        # Remove verse number if present
        text = re.sub(r'^\d+[\\.]\s+', '', text)
        
        # Find commentary in parentheses
        # Match parentheses that contain substantial text (likely commentary)
        # Look for opening paren followed by capital letter or specific keywords
        commentary_pattern = r'\s*\(([^)]{50,})\)\.?\s*$'
        match = re.search(commentary_pattern, text)
        
        if match:
            commentary = match.group(1).strip()
            verse_text = text[:match.start()].strip()
            return verse_text, commentary
        
        return text.strip(), ""
    
    def _is_surah_header(self, line: str) -> Optional[Tuple[int, str]]:
        """
        Check if line is a surah header.
        
        Args:
            line: Line to check
            
        Returns:
            Tuple of (surah_number, surah_name) if header, None otherwise
        """
        # First try: Match markdown bold headers with numbers like "**2. el-BAQARA**"
        # Allow for various prefixes (el-, en-, et-, etc.) and mixed case
        md_num_match = re.match(r'^\*\*(\d+)\.\s+([A-Za-zА-Яа-яİıĞğÜüŞşÖöÇç\-\'\s]+)\*\*\s*$', line.strip())
        if md_num_match:
            return int(md_num_match.group(1)), md_num_match.group(2)

        # Second try: Match markdown bold headers without numbers like "**el-FAATİhA**"
        md_match = re.match(r'^\*\*(.+?)\*\*\s*$', line.strip())
        if md_match:
            surah_name = md_match.group(1).strip()
            # Look up in our mapping
            surah_num = self.SURAH_NAME_MAP.get(surah_name)
            if surah_num:
                return surah_num, surah_name
        
        # Third try: Match patterns like "2. el-BAQARA" (plain text) - ONLY if it matches a known surah name
        # This prevents verses like "1. Elif..." from being matched as headers
        num_match = re.match(r'^(\d+)\.\s+([A-Za-zА-Яа-яİıĞğÜüŞşÖöÇç\-\'\s]+)', line)
        if num_match:
            name_part = num_match.group(2).strip()
            # Check if the name part (or a significant prefix) is in our map
            # or if it looks like a header (e.g. ALL CAPS)
            if name_part in self.SURAH_NAME_MAP or (name_part.isupper() and len(name_part) > 1) or name_part.startswith(('el-', 'en-', 'et-', 'es-')):
                 # Double check it's not a verse by ensuring it doesn't have long text
                 if len(name_part) < 50:
                     return int(num_match.group(1)), name_part
        
        return None
    
    def parse_surah(self, surah_number: int, start_line: int, end_line: int) -> Dict:
        """
        Parse a specific surah from the source.
        
        Args:
            surah_number: Surah number
            start_line: Starting line number in source
            end_line: Ending line number in source
            
        Returns:
            Dictionary containing surah data
        """
        lines = self.content.split('\n')[start_line:end_line]
        
        surah_data = {
            'number': surah_number,
            'verses': {}
        }
        
        current_verse = None
        current_text = []
        
        # Pre-process lines to handle multiple verses on one line
        expanded_lines = []
        for line in lines:
            # Split by verse number pattern
            parts = re.split(r'(\d+\.\s+)', line)
            
            if len(parts) > 1:
                current_chunk = parts[0]
                for i in range(1, len(parts), 2):
                    marker = parts[i]
                    content = parts[i+1] if i+1 < len(parts) else ''
                    
                    if current_chunk.strip():
                        expanded_lines.append(current_chunk)
                    
                    current_chunk = marker + content
                
                if current_chunk.strip():
                    expanded_lines.append(current_chunk)
            else:
                expanded_lines.append(line)
        
        lines = expanded_lines

        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if this is a new verse
            verse_num = self._extract_verse_number(line)
            


            if verse_num is not None:
                # Check if this is a valid new verse sequence
                # If verse_num is less than or equal to current_verse, it's likely a numbered list in commentary
                if current_verse is not None and verse_num <= current_verse:
                    # Treat as text continuation
                    current_text.append(line)
                    continue

                # Save previous verse if exists
                if current_verse is not None and current_text:
                    full_text = ' '.join(current_text)
                    verse_text, commentary = self._separate_verse_and_commentary(full_text)
                    surah_data['verses'][current_verse] = {
                        'text': verse_text,
                        'commentary': commentary
                    }
                
                # Start new verse
                current_verse = verse_num
                current_text = [line]
            else:
                # Continue current verse
                if current_verse is not None:
                    current_text.append(line)
        
        # Save last verse
        if current_verse is not None and current_text:
            full_text = ' '.join(current_text)
            verse_text, commentary = self._separate_verse_and_commentary(full_text)
            surah_data['verses'][current_verse] = {
                'text': verse_text,
                'commentary': commentary
            }
        
        return surah_data
    
    def find_surah_boundaries(self) -> Dict[int, Tuple[int, int]]:
        """
        Find line boundaries for each surah in the source.
        
        Returns:
            Dictionary mapping surah number to (start_line, end_line)
        """
        lines = self.content.split('\n')
        boundaries = {}
        
        for i, line in enumerate(lines):
            header = self._is_surah_header(line)
            if header:
                surah_num, _ = header
                boundaries[surah_num] = i
        
        # Convert to (start, end) tuples
        surah_nums = sorted(boundaries.keys())
        result = {}
        
        for i, surah_num in enumerate(surah_nums):
            start = boundaries[surah_num]
            end = boundaries[surah_nums[i + 1]] if i + 1 < len(surah_nums) else len(lines)
            result[surah_num] = (start, end)
        
        return result
    
    def parse_all(self) -> Dict[int, Dict]:
        """
        Parse all surahs from the source.
        
        Returns:
            Dictionary mapping surah number to surah data
        """
        boundaries = self.find_surah_boundaries()
        
        for surah_num, (start_line, end_line) in boundaries.items():
            # Skip the header line itself
            self.surahs[surah_num] = self.parse_surah(surah_num, start_line + 1, end_line)
        
        return self.surahs
    
    def save_to_json(self, output_path: Path):
        """
        Save parsed data to JSON file.
        
        Args:
            output_path: Path to output JSON file
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.surahs, f, ensure_ascii=False, indent=2)
        
        print(f"✓ Saved parsed data to {output_path}")

def main():
    """Main function to parse CRH verses."""
    base_dir = Path(__file__).parent.parent
    data_dir = base_dir / 'src' / 'data'
    
    # Parse Latin transliteration
    latin_source = data_dir / 'quran-crh-dizen-qurtnezir-lat.md'
    
    if not latin_source.exists():
        print(f"Error: {latin_source} not found")
        print("Please run format_crh_latin.py first")
        return
    
    print("Parsing CRH verses from Latin transliteration...")
    parser = CRHVerseParser(latin_source)
    surahs = parser.parse_all()
    
    print(f"✓ Parsed {len(surahs)} surahs")
    
    # Show sample
    if 2 in surahs:
        surah_2 = surahs[2]
        print(f"\nSurah 2 (El-Baqarah): {len(surah_2['verses'])} verses")
        if 1 in surah_2['verses']:
            v1 = surah_2['verses'][1]
            print(f"  Verse 1: {v1['text'][:50]}...")
            if v1['commentary']:
                print(f"  Commentary: {v1['commentary'][:50]}...")
    
    # Save to JSON
    output_path = data_dir / 'crh-verses-parsed.json'
    parser.save_to_json(output_path)
    
    print("\n✓ Parsing complete!")

if __name__ == '__main__':
    main()
