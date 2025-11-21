import re

def analyze_headers(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    surah_pattern = re.compile(r'^\d+\.\s+el-[A-ZİıĞğÜüŞşÖöÇçÂâÎîÛû\-\']+')
    # Also check for lines that might be headers but not surahs (short, uppercase, etc)
    
    potential_surahs = []
    for i, line in enumerate(lines):
        line = line.strip()
        if surah_pattern.match(line):
            potential_surahs.append((i + 1, line))
        elif line.isupper() and len(line) < 100 and not line.startswith('('):
             # Just to see if there are other headers like "SAİT DİZEN..."
             print(f"Potential Header at {i+1}: {line}")

    print(f"Found {len(potential_surahs)} potential Surah headers.")
    if len(potential_surahs) > 0:
        print("First 5:", potential_surahs[:5])
        print("Last 5:", potential_surahs[-5:])

analyze_headers('/Users/tanerseyt/Documents/Code/miras-quran/translations/quran-crh-dizen-qurtnezir-lat.txt')
