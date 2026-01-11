import json
import os
import urllib.request
import time

TRANSLATIONS_DIR = "src/data/translations/en/haleem"
API_BASE = "https://api.quran.com/api/v4"
TRANSLATION_ID = 85  # Abdel Haleem

def fetch_json(url):
    print(f"Fetching {url}...")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        return json.load(response)

def escape_yaml_string(s):
    if not s:
        return '""'
    # Remove single quotes to avoid YAML parsing issues if simple
    # But for translations we might want to keep them? 
    # The core script removes them. Let's try to keep them if possible, but escaped?
    # Actually, for simplicity and consistency with core, let's follow core's lead but maybe be smarter if needed.
    # Core script: s_clean = s.replace("'", "")
    # That might be too aggressive for English text like "God's".
    # Better to just use double quotes and escape internal double quotes and backslashes.
    s_clean = s.replace('\\', '\\\\').replace('"', '\\"')
    return f'"{s_clean}"'

def generate_translation_yaml(surah_id, verses_data):
    lines = []
    lines.append(f"surah_id: {surah_id}")
    lines.append("language: en")
    lines.append("author: haleem")
    lines.append("verses:")
    
    for v in verses_data:
        # structure: { "id": ..., "verse_key": "1:1", ..., "words": [ ... ] }
        
        verse_num = v['verse_key'].split(':')[1]
        lines.append(f"  - verse: {verse_num}")
        lines.append("    segments:")
        
        cid_counter = 1
        words = v.get('words', [])
        # Filter out end markers
        content_words = [w for w in words if w['char_type_name'] != 'end']
        
        for w in content_words:
            # Get translation text
            trans_text = ""
            if 'translation' in w and w['translation']:
                trans_text = w['translation'].get('text', "")
            
            # Fallback if empty? usually not empty.
            if not trans_text:
                trans_text = ""
                
            escaped_text = escape_yaml_string(trans_text)
            lines.append(f"      - text: {escaped_text}")
            lines.append(f"        cid: {cid_counter}")
            cid_counter += 1
            
    return "\n".join(lines)

def main():
    if not os.path.exists(TRANSLATIONS_DIR):
        os.makedirs(TRANSLATIONS_DIR)
        
    # Fetch chapters to get names for filenames
    chapters_data = fetch_json(f"{API_BASE}/chapters?language=en")
    chapters = chapters_data['chapters']
    
    for chapter in chapters:
        chapter_id = chapter['id']
        name_simple = chapter['name_simple'].replace(' ', '-')
        
        # Apply naming convention overrides
        if chapter_id == 1:
            name_simple = "Al-Fatiha"
            
        filename = f"{chapter_id:03d}-{name_simple}.yaml"
        filepath = os.path.join(TRANSLATIONS_DIR, filename)
        
        print(f"Processing Translation Surah {chapter_id}: {filename}")
        
        # Fetch verses with translation
        # per_page=300 covers all except maybe Baqarah? Baqarah is 286. 300 is fine.
        # We need words=true and word_fields=translation for CID mapping (English WBW)
        verses_url = f"{API_BASE}/verses/by_chapter/{chapter_id}?words=true&word_fields=translation&per_page=300"
        verses_resp = fetch_json(verses_url)
        verses = verses_resp['verses']
        
        # Pagination check
        if 'pagination' in verses_resp and verses_resp['pagination']['total_pages'] > 1:
             for page in range(2, verses_resp['pagination']['total_pages'] + 1):
                 p_url = f"{verses_url}&page={page}"
                 p_resp = fetch_json(p_url)
                 verses.extend(p_resp['verses'])
        
        yaml_content = generate_translation_yaml(chapter_id, verses)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(yaml_content)
            
        time.sleep(0.2)

if __name__ == "__main__":
    main()
