# **Miras Quran \- Semantic Syntax Mapping**

**Miras Quran** is a modern, React-based Quranic language study tool designed to bridge the linguistic gap between the source Arabic and translations using **Semantic Concept Mapping**.

Unlike traditional word-by-word translations that often break under the weight of different grammar rules (like SVO vs SOV languages), Miras assigns a **Concept ID (CID)** to semantic chunks. This allows us to map "The Master of the Day of Judgment" (English) to "Ceza kunüniñ saibidir" (Crimean Tatar) accurately, even though the word order is completely reversed.

## **Features**

* **Semantic Highlighting:** Hover over a word in any language to see its equivalent concept in all other languages.  
* **Fluid Typography:** A custom density engine that scales padding, gaps, and font sizes together for optimal reading comfort.  
* **Multi-Language Support:** Built-in support for Arabic (Uthmani), English, Crimean Tatar (Latin), and Turkish.  
* **Developer Friendly:** Data is managed in strict YAML and compiled to JSON, making it easy to extend.

## **Getting Started**

### **Prerequisites**

* Node.js & NPM  
* Python 3 (for the data pipeline)

### **Installation**

1. Clone the repository.  
2. Install dependencies:  
   npm install

3. Run the development server:  
   npm run dev

## **Contributing Data**

The project uses a **modular file structure** that separates core Arabic data from translations, making it easy to add and maintain different language versions.

### **Directory Structure**

```
src/data/
├── core/                    # Arabic source text (114 files)
│   ├── 001-Al-Fatiha.yaml
│   ├── 002-Al-Baqarah.yaml
│   └── ...
├── translations/            # Translations organized by language/author
│   ├── en/
│   │   └── haleem/
│   │       ├── 001-Al-Fatiha.yaml
│   │       └── ...
│   ├── tr/
│   │   ├── elmalili/
│   │   └── diyanet/
│   ├── crh/                 # Crimean Tatar
│   ├── ru/                  # Russian
│   └── ua/                  # Ukrainian
├── quranData.js             # Dynamic loader for surahs & translations
└── translationAvailability.json
```

### **1. Core Surah Files**

Each surah in `src/data/core/` follows this format:

```yaml
id: 1
title: "Al-Fatihah"
english: The Opener
type: Makkah
total_verses: 7
verses:
  - verse: 1
    context_mapped: true
    segments:
      ar:
        - text: "بِسْمِ"
          cid: 1
        - text: "ٱللَّهِ"
          cid: 2
      ar-lat:
        - text: "bismi"
          cid: 1
        - text: "l-lahi"
          cid: 2
```

### **2. Adding a New Translation**

1. Create a folder under `src/data/translations/<lang-code>/<author-id>/`
2. Add YAML files matching the core surah filenames (e.g., `001-Al-Fatiha.yaml`)
3. Register the language/author in `src/constants/languages.js`

Translation files map segments to the same CIDs defined in the core Arabic:

```yaml
verses:
  - verse: 1
    segments:
      - text: "In the name of"
        cid: 1
      - text: "God"
        cid: 2
```

### **3. Context Mapping (Concept IDs)**

Miras uses **Concept IDs (CIDs)** to map semantic chunks across languages.
- `cid: 0` is used for particles or words that don't map directly to a core concept in the other language.
- `cid: >0` represents a unique semantic concept within that verse.

**Rule:** A CID used in a translation MUST exist in the Arabic source.

### **4. Validation**

After editing YAML files, run the validation script to ensure CID mapping integrity:

```bash
node scripts/validate_mapping.js
```

This script checks that every Concept ID (CID) used in translations exists in the corresponding Arabic core file.

## **Architecture**

* **VerseCard.jsx**: The main React component for displaying verses.
* **src/data/core/**: Arabic source files (one per surah) with CID-mapped segments.
* **src/data/translations/**: Translation files organized by `<language>/<author>/`.
* **src/data/quranData.js**: Dynamic loader for surahs and translations.
* **scripts/validate_data.py**: The data integrity validation tool.

## **Credits**

* **Crimean Tatar Translation:** Sait Dizen & Zakir Qurtnezir  
* **English Translation:** M.A.S. Abdel Haleem (Oxford World's Classics)  
* **Turkish Translation:** Elmalılı Hamdi Yazır

## **License**

MIT License. Use this code to build your own Quranic tools.
