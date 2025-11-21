# **Miras Quran \- Semantic Syntax Mapping**

**Miras Quran** is a modern, React-based Quranic language study tool designed to bridge the linguistic gap between the source Arabic and translations using **Semantic Concept Mapping**.

Unlike traditional word-by-word translations that often break under the weight of different grammar rules (like SVO vs SOV languages), Miras assigns a **Concept ID (CID)** to semantic chunks. This allows us to map "The Master of the Day of Judgment" (English) to "Ceza kunüniñ saibidir" (Crimean Tatar) accurately, even though the word order is completely reversed.

## **Features**

* **Semantic Highlighting:** Hover over a word in any language to see its equivalent concept in all other languages.  
* **Fluid Typography:** A custom density engine that scales padding, gaps, and font sizes together for optimal reading comfort.  
* **Multi-Language Support:** Built-in support for Arabic (Uthmani), English, Crimean Tatar (Latin), and Turkish.  
* **Developer Friendly:** Data is managed in strict YAML and compiled to JSON, making it easy for backend engineers to extend.

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

The project separates data from logic. The source of truth is `src/data/quran_data.yaml`.

### **1. Adding a New Surah**

Open `src/data/quran_data.yaml` and add a new entry under `surahs`:

```yaml
  - id: 114
    title: "An-Nas"
    english: "Mankind"
    type: "Meccan"
    total_verses: 6
    content:
      - verse: 1
        segments:
          arabic: ...
          english: ...
```

### **2. Adding a New Language**

1. Add the language metadata to the `meta.languages` list in `src/data/quran_data.yaml`.
2. Add the segments to every verse in `content`.
3. Update `src/components/VerseCard.jsx` and `src/constants/theme.js` to render the new language block.

### **3. Context Mapping (Concept IDs)**

Miras uses **Concept IDs (CIDs)** to map semantic chunks across languages.
- `cid: 0` is used for particles or words that don't map directly to a core concept in the other language.
- `cid: >0` represents a unique semantic concept within that verse.

**Rule:** A CID used in a translation MUST exist in the Arabic source.

### **4. Validation**

After editing the YAML, run the validation script to ensure data integrity:

```bash
python3 scripts/validate_data.py
```

This script checks that every Concept ID (CID) used in a translation actually exists in the Arabic source text.

## **Architecture**

* **VerseCard.jsx**: The main React component for displaying verses.
* **src/data/quran_data.yaml**: The single source of truth for Quranic data.
* **scripts/validate_data.py**: The data integrity validation tool.

## **Credits**

* **Crimean Tatar Translation:** Sait Dizen & Zakir Qurtnezir  
* **English Translation:** M.A.S. Abdel Haleem (Oxford World's Classics)  
* **Turkish Translation:** Elmalılı Hamdi Yazır

## **License**

MIT License. Use this code to build your own Quranic tools.
