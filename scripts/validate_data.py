import yaml
import sys
import os

def validate_data(yaml_path):
    print(f"Reading {yaml_path}...")
    try:
        with open(yaml_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: File not found at {yaml_path}")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML: {e}")
        sys.exit(1)

    print("Validating integrity...")
    
    issues_found = False

    for surah in data['surahs']:
        # Build Content
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
                    issues_found = True

    if issues_found:
        print("\nValidation complete with warnings.")
    else:
        print("\nValidation complete. No issues found.")

if __name__ == "__main__":
    # Determine the absolute path to the data file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    data_path = os.path.join(project_root, 'src', 'data', 'quran_data.yaml')
    
    validate_data(data_path)
