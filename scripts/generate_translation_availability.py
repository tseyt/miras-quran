import os
import json

TRANSLATIONS_DIR = "src/data/translations"
OUTPUT_FILE = "src/data/translationAvailability.json"

def main():
    availability = {} # surah_id (str) -> list of "lang-author"
    
    # Initialize for all 114 surahs to ensure no undefined keys
    for i in range(1, 115):
        availability[str(i)] = []

    if not os.path.exists(TRANSLATIONS_DIR):
        print(f"Directory {TRANSLATIONS_DIR} does not exist.")
        return

    # Iterate languages
    for lang in os.listdir(TRANSLATIONS_DIR):
        lang_path = os.path.join(TRANSLATIONS_DIR, lang)
        if not os.path.isdir(lang_path):
            continue
            
        # Iterate authors
        for author in os.listdir(lang_path):
            author_path = os.path.join(lang_path, author)
            if not os.path.isdir(author_path):
                continue
                
            # Iterate files
            for filename in os.listdir(author_path):
                if filename.endswith(".yaml"):
                    try:
                        # filename format: 001-Subject.yaml
                        surah_id_str = filename.split('-')[0]
                        surah_id = str(int(surah_id_str)) # remove leading zeros
                        
                        key = f"{lang}-{author}"
                        
                        if surah_id in availability:
                            if key not in availability[surah_id]:
                                availability[surah_id].append(key)
                        else:
                            # Should have been initialized but just in case
                            availability[surah_id] = [key]
                            
                    except ValueError:
                        print(f"Skipping invalid filename: {filename}")

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(availability, f, indent=2)
    
    print(f"Generated {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
