# **Miras Quran \- Semantic Syntax Mapping**

**Miras Quran** is a modern, React-based Quranic language study tool designed to bridge the linguistic gap between the source Arabic and translations using **Semantic Concept Mapping**.

Unlike traditional word-by-word translations that often break under the weight of different grammar rules (like SVO vs SOV languages), Miras assigns a **Concept ID (CID)** to semantic chunks. This allows us to map "The Master of the Day of Judgment" (English) to "Ceza kününiñ saibidir" (Crimean Tatar) accurately, even though the word order is completely reversed.

## **Features**

* **Semantic Highlighting:** Hover over a word in any language to see its equivalent concept in all other languages.  
* **Fluid Typography:** A custom density engine that scales padding, gaps, and font sizes together for optimal reading comfort.  
* **Multi-Language & Dual-Script Support:** Built-in support for Arabic (Uthmani), English, Crimean Tatar (official Latin `crh-Latn` and Cyrillic `crh-Cyrl` script toggle), Turkish (`Diyanet` & `Elmalılı`), Russian, and Ukrainian.  
* **Collapsible Exegetical Commentary (*İzaat*):** Automatically collapses multi-sentence parenthetical commentary blocks (preserving internal numbered/lettered sub-clauses) for distraction-free verse reading.  
* **Tarteel QUL & Quran.com Exports:** Ready-to-import datasets (`simple.json`, `translation-with-footnote-tags.json`, `grouped-verses.json`, localized 114 Surah metadata, and optional `.sqlite` exports) for onboarding Crimean Tatar (`crh`) onto [Tarteel QUL](https://qul.tarteel.ai) and [Quran.com](https://quran.com).

## **Getting Started**

### **Prerequisites**

* Node.js & NPM  
* Python 3 + `poppler-utils` (`pdftotext`, for regenerating CRH from the 2005 PDF)

### **Installation**

1. Clone the repository.  
2. Install dependencies:  
   `npm install`

3. Run the development server:  
   `npm run dev`

## **Contributing & Regenerating Data**

### **Directory Structure**

```
src/data/
├── core/                        # Arabic source text (114 files, 6,236 verses)
├── glossary/
│   └── crh-quranic-glossary.json # 495-entry Crimean Tatar Quranic Glossary (2005 pp. 549-561)
├── translations/                # Translations organized by language/author
│   ├── crh/
│   │   ├── dizen-qurtnezir/     # 114 aligned CRH Surah YAML files
│   │   └── dizen-qurtnezir-merged-ranges.json # 325 author-merged ranges + surah intros
│   ├── en/haleem/
│   ├── tr/{diyanet,elmalili}/
│   ├── ru/kuliev/
│   └── ua/yakubovych/
├── quranData.js                 # Dynamic loader for surahs & translations
└── translationAvailability.json

exports/quran-com/               # Tarteel QUL & Quran.com submission packages (crh-Latn & crh-Cyrl)
docs/
├── QURAN_COM_SUBMISSION.md      # Step-by-step QUL / Quran.com onboarding guide & issue templates
└── GASPIRALI_CRH_TR_ANALYSIS.md # Empirical 6,236-verse CRH<->TR study & JEV architectural analysis
```

### **Data Pipeline & Validation**

```bash
# 1. Rebuild canonical CRH Markdown, 114 YAMLs, merged ranges & Glossary from the 2005 PDF
python3 scripts/rebuild_crh_from_pdf.py

# 2. Export Tarteel QUL / Quran.com datasets (crh-Latn & crh-Cyrl)
python3 scripts/export_quran_com.py

# 3. Validate all 114 Surahs, 6,236 verses, orthography, parentheses & QUL exports
python3 scripts/validate_data.py

# 4. Validate Concept ID (CID) mappings against Arabic core
node scripts/validate_mapping.js
```

## **Credits**

* **Crimean Tatar Translation:** Sait Dizen & Zakir Qurtnezir (*Qur'an-ı Kerim ve izaatlı manası*, 2nd ed., Qırım Musulmanları Diniy İdaresi, Simferopol, 2005)  
* **English Translation:** M.A.S. Abdel Haleem (Oxford World's Classics)  
* **Turkish Translations:** Diyanet İşleri Başkanlığı & Elmalılı Hamdi Yazır

## **License**

MIT License. Use this code to build your own Quranic tools.
