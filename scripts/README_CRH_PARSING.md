# CRH Translation Normalization and Parsing

## Overview
This directory contains scripts to normalize and parse the Crimean Tatar (CRH) Quran translation files.

## Problem Statement
The CRH verses in `quran_data.yaml` are too long and contain commentary mixed with verse text. This is because the original source files (`quran-crh-dizen-qurtnezir-lat.txt` and `quran-crh-dizen-qurtnezir.md`) have:
1. Line numbers at the start of each line
2. Extensive commentary in parentheses that should be separated from verse text
3. Verses that need proper segmentation

## File Structure

### Source Files
- `src/data/quran-crh-dizen-qurtnezir-lat.txt` - Original Latin script CRH translation (with line numbers)
- `src/data/quran-crh-dizen-qurtnezir.md` - Original Cyrillic script CRH translation (with line numbers)

### Normalized Files (Generated)
- `src/data/quran-crh-dizen-qurtnezir-lat-normalized.txt` - Cleaned Latin script (line numbers removed)
- `src/data/quran-crh-dizen-qurtnezir-normalized.md` - Cleaned Cyrillic script (line numbers removed)

### Parsed Files (Generated)
- `src/data/crh-verses-parsed.json` - Extracted verses with commentary separated

## CRH Source File Format

### Surah Headers
Surahs are identified by headers like:
```
el-FAATİhA
el-BAQARA
```

Note: Surah headers do NOT include numbers in the source files.

### Verse Format
Verses are numbered with format: `<number>. <verse text>`

Example:
```
1. Elif. Lâam. Miim.
2. O kitap (Qur'an), onda asla şube yoktır...
```

### Commentary Format
Commentary appears in parentheses `(...)` and can span multiple lines. Commentary typically:
- Explains terminology
- Provides historical context
- References hadith and other sources
- Can be very extensive (50+ lines for some verses)

Example from Surah 2, Verse 5:
```
92: İşte, olar Rabblerinden kelgen bir hidayet uzerindedirler ve qurtulışqa  
    irişkenler de yalıñız olardır. 
93: (Qur'an sureleriniñ bazılarınıñ başında "el-huruf'ul-muqattaa" denilgen bir  
    taqım arifler bar ve olar olğan sureleriniñ bir ayetidir...
    [commentary continues for many lines]
104: ...işaret etilmekte).
```

## Scripts

### 1. normalize_crh_source.py
**Purpose**: Remove line numbers and clean up formatting from source files.

**What it does**:
- Removes line numbers (format: `number: text` or `number. text`)
- Removes carriage returns
- Preserves all other structure

**Usage**:
```bash
python3 scripts/normalize_crh_source.py
```

**Output**:
- `src/data/quran-crh-dizen-qurtnezir-lat-normalized.txt`
- `src/data/quran-crh-dizen-qurtnezir-normalized.md`

### 2. parse_crh_verses.py
**Purpose**: Extract verses and separate commentary.

**Current Status**: ⚠️ NEEDS UPDATE

**Issues**:
- Surah header detection pattern expects numbered headers (e.g., "2. el-BAQARA")
- Actual format is just "el-BAQARA" without numbers
- Needs to handle multi-line commentary properly
- Needs to map CRH surah names to standard surah numbers

**Planned Features**:
- Detect surah boundaries by name
- Extract verse numbers and text
- Separate commentary from verse text
- Map to standard Quran surah/verse numbering
- Output structured JSON

## Next Steps

1. **Update parse_crh_verses.py**:
   - Fix surah header detection to match actual format
   - Create mapping of CRH surah names to numbers
   - Improve commentary extraction logic
   - Handle edge cases (verses without commentary, multi-paragraph commentary)

2. **Create Integration Script**:
   - Merge parsed CRH verses into `quran_data.yaml`
   - Ensure proper alignment with Arabic, English, Turkish, and transliteration
   - Validate verse counts match

3. **Validation**:
   - Compare verse counts with standard Quran
   - Check for missing or duplicate verses
   - Verify commentary is properly separated

## Example Data Structure

### Current (Incorrect) - Verse 5, Surah 2 in quran_data.yaml:
```yaml
- verse: 5
  segments:
    crh:
    - text: 'İşte, olar Rabblerinden kelgen bir hidayet uzerindedirler ve qurtulışqa irişkenler de yalıñız olardır. (Qur''an sureleriniñ bazılarınıñ başında "el-huruf''ul-muqattaa" denilgen bir taqım arifler bar... [VERY LONG COMMENTARY CONTINUES]'
      cid: 0
```

### Desired (Correct):
```yaml
- verse: 5
  segments:
    crh:
    - text: 'İşte, olar Rabblerinden kelgen bir hidayet uzerindedirler ve qurtulışqa irişkenler de yalıñız olardır.'
      cid: 0
  commentary:
    crh: 'Qur''an sureleriniñ bazılarınıñ başında "el-huruf''ul-muqattaa" denilgen bir taqım arifler bar...'
```

## References

- Original translation: "Qur'an-ı Kerim ve izaatlı manası" by Sait Dizen and Zakir Qurtnezir
- Published by: Qırım musulmanları Diniy idaresi (Religious Administration of Crimean Muslims)
- Edition: 2nd edition, 2005
