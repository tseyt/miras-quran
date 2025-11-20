import yaml
import json
import sys

def validate_and_build(yaml_path, json_output_path):
    print(f"Reading {yaml_path}...")
    with open(yaml_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    surah_list = []
    quran_content = {}

    print("Validating integrity...")
    
    for surah in data['surahs']:
        # Build Metadata for Navigation
        surah_meta = {
            'id': surah['id'],
            'title': surah['title'],
            'english': surah['english'],
            'type': surah['type'],
            'verses': surah['total_verses']
        }
        surah_list.append(surah_meta)

        # Build Content
        verse_content = []
        for v_data in surah['content']:
            verse_num = v_data['verse']
            segments = v_data['segments']
            
            # VALIDATION: Ensure CIDs in translations exist in Arabic source
            arabic_cids = {s['cid'] for s in segments['arabic'] if s['cid'] != 0}
            
            for lang, segs in segments.items():
                if lang == 'arabic': continue
                lang_cids = {s['cid'] for s in segs if s['cid'] != 0}
                
                # Check if translation uses a CID not present in Arabic (Orphan concept)
                diff = lang_cids - arabic_cids
                if diff:
                    print(f"WARNING: Surah {surah['id']} Verse {verse_num} [{lang}]: CIDs {diff} found but not present in Arabic source.")

            verse_content.append({
                'id': verse_num, # Using verse num as ID for simplicity within surah context
                'verse': verse_num,
                'segments': segments
            })
        
        quran_content[surah['id']] = verse_content

    output = {
        "SURAH_LIST": surah_list,
        "QURAN_CONTENT": quran_content
    }

    print(f"Writing to {json_output_path}...")
    with open(json_output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print("Build complete.")

if __name__ == "__main__":
    validate_and_build('data/quran_data.yaml', 'src/quran_data.json')
