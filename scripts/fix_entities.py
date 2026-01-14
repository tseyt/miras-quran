import os
import re

directory = '/Users/tanerseyt/Documents/Code/miras-quran/src/data/translations/tr/elmalili'

# Entities to replace
replacements = {
    '&quot;': '"',
    '&amp;': '&',
    '&#39;': "'",
    '&lt;': '<',
    '&gt;': '>'
}

def clean_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    for entity, char in replacements.items():
        content = content.replace(entity, char)

    if content != original_content:
        print(f"Fixing {filepath}")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    else:
        # print(f"No changes for {filepath}")
        pass

for filename in os.listdir(directory):
    if filename.endswith(".yaml"):
        filepath = os.path.join(directory, filename)
        clean_file(filepath)
