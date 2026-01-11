import json
import os
import urllib.request
import time

CORE_DIR = "src/data/core"
API_BASE = "https://api.quran.com/api/v4"

def fetch_json(url):
    print(f"Fetching {url}...")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        return json.load(response)

def list_existing_files():
    files = {} # id -> filename
    if not os.path.exists(CORE_DIR):
        os.makedirs(CORE_DIR)
    for f in os.listdir(CORE_DIR):
        if f.endswith(".yaml"):
            try:
                num = int(f.split('-')[0])
                files[num] = f
            except ValueError:
                pass
    return files

def escape_yaml_string(s):
    if not s:
        return '""'
    # Remove single quotes to avoid YAML parsing issues
    s_clean = s.replace("'", "")
    # Escape backslashes and double quotes
    s_escaped = s_clean.replace('\\', '\\\\').replace('"', '\\"')
    return f'"{s_escaped}"'

def generate_yaml(surah_info, verses_data):
    lines = []
    lines.append(f"id: {surah_info['id']}")
    title = escape_yaml_string(surah_info['name_simple'])
    lines.append(f"title: {title}")
    lines.append(f"english: {surah_info['translated_name']['name']}")
    lines.append(f"type: {surah_info['revelation_place'].capitalize()}")
    lines.append(f"total_verses: {surah_info['verses_count']}")
    lines.append("verses:")
    
    for v in verses_data:
        lines.append(f"  - verse: {v['verse_key'].split(':')[1]}")
        lines.append("    context_mapped: true")
        lines.append("    segments:")
        
        # Arabic
        lines.append("      ar:")
        words = v.get('words', [])
        cid_counter = 1
        
        # Filter out "end" marker words
        content_words = [w for w in words if w['char_type_name'] != 'end']
        
        for w in content_words:
            text = escape_yaml_string(w['text_uthmani'])
            lines.append(f"        - text: {text}")
            lines.append(f"          cid: {cid_counter}")
            cid_counter += 1
            
        # Transliteration
        lines.append("      ar-lat:")
        cid_counter = 1
        for w in content_words:
            translit = w.get('transliteration', {}).get('text')
            # Handle null transliteration (sometimes happens)
            if translit is None:
                translit = ""
            text = escape_yaml_string(translit)
            lines.append(f"        - text: {text}")
            lines.append(f"          cid: {cid_counter}")
            cid_counter += 1

    return "\n".join(lines)

def main():
    existing_files = list_existing_files()
    
    # Fetch chapters
    chapters_data = fetch_json(f"{API_BASE}/chapters")
    chapters = chapters_data['chapters']
    
    for chapter in chapters:
        # For testing, we can limit to first 5 or specific ones, but task says "fill in... for the entire Quran"
        # We will do all.
        chapter_id = chapter['id']
        name_simple = chapter['name_simple'].replace(' ', '-')
        
        if not filename:
             # The API usually returns "Al-Fatihah", "Al-Baqarah" etc in name_simple
             # We want "Al-Fatiha", "Al-Baqarah".
             # API name_simple: "Al-Fatihah" -> we might want "Al-Fatiha"?
             # Actually user requested "Al-Fatiha". API returns "Al-Fatihah" (with h).
             # Let's trust the API name_simple but replace spaces with dashes.
             # And special case Fatihah -> Fatiha if needed, but "Al-Fatiha" is standard.
             # Actually, let's just use what api gives but ensure we map spaces to dashes.
             
             name_simple = chapter['name_simple'].replace(' ', '-')
             # Specific overrides based on user request "Al-Fatiha"
             if chapter_id == 1:
                 name_simple = "Al-Fatiha"
             
             filename = f"{chapter_id:03d}-{name_simple}.yaml"
        
        filepath = os.path.join(CORE_DIR, filename)
        
        print(f"Processing Surah {chapter_id}: {chapter['name_simple']} -> {filename}")
        
        # Fetch verses
        # We assume per_page=300 is enough for max surah size (286 for Baqarah)
        verses_url = f"{API_BASE}/verses/by_chapter/{chapter_id}?words=true&word_fields=text_uthmani,transliteration&per_page=300"
        verses_resp = fetch_json(verses_url)
        verses = verses_resp['verses']
        
        # Verify complete fetch
        if len(verses) < chapter['verses_count']:
             # Need pagination? API defaults page 1.
             # check meta
             if 'pagination' in verses_resp and verses_resp['pagination']['total_pages'] > 1:
                 # Fetch subsequent pages
                 for page in range(2, verses_resp['pagination']['total_pages'] + 1):
                     p_url = f"{verses_url}&page={page}"
                     p_resp = fetch_json(p_url)
                     verses.extend(p_resp['verses'])
        
        yaml_content = generate_yaml(chapter, verses)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(yaml_content)
            
        # Rate limit friendly
        time.sleep(0.5)

if __name__ == "__main__":
    main()
