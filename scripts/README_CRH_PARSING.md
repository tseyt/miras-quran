# Crimean Tatar (CRH) Primary-Source Pipeline & Orthography

## Canonical Pipeline Architecture

All Crimean Tatar (`crh`) files in `miras-quran` are deterministically generated directly from the digital 2nd edition PDF (`translations/quran-crh-dizen-qurtnezir.pdf`, Sait Dizen & Zakir Qurtnezir, *Къур'ан-ы Керим ве изаатлы манасы*, Qırım Musulmanları Diniy İdaresi Decision `15/10/2004`, Simferopol, 2005, 564 pages).

| Script | Responsibility | Generated / Verified Targets |
| :--- | :--- | :--- |
| `scripts/crh_orthography.py` | Cleans 2005 PDF Cyrillic extraction artifacts (Latin homoglyphs `Аллаh` $\to$ `Аллаһ`, hyphenated line wraps, 52 unclosed/unopened parenthetical typos in the 2005 typesetting) and implements vowel-harmony-aware Crimean Tatar Cyrillic $\to$ Latin transliteration (`ö`, `ü`, `â`, `ğ`, `q`, `ñ`, `c`, `ş`, `ç`). | Imported by `rebuild_crh_from_pdf.py` |
| `scripts/rebuild_crh_from_pdf.py` | Extracts all 564 PDF pages via `pdftotext -layout`, aligns all 114 Surahs and 6,236 verses against `src/data/core/*.yaml`, preserves granular Concept IDs (`cid: 1..9`) in `001-Al-Fatiha.yaml`, indexes the 325 author-merged verse ranges, and parses the 495-entry back-of-book Glossary (`Лугъат`, pp. 549–561). | `translations/quran-crh-dizen-qurtnezir.md`<br>`translations/quran-crh-dizen-qurtnezir-lat.md`<br>`src/data/translations/crh/dizen-qurtnezir/*.yaml`<br>`src/data/translations/crh/dizen-qurtnezir-merged-ranges.json`<br>`src/data/glossary/crh-quranic-glossary.json` |
| `scripts/export_quran_com.py` | Splits standalone `>= 7`-word parenthetical *izaat* commentaries into `1,442` structured `<sup foot_note="id">n</sup>` footnotes while keeping short `<= 6`-word lexical clarifications inline, and exports dual-script (`crh-Latn` & `crh-Cyrl`) Tarteel QUL / Quran.com datasets + optional `.sqlite` builds. | `exports/quran-com/metadata/*.json`<br>`exports/quran-com/crh-dizen-qurtnezir-latn/*.json`<br>`exports/quran-com/crh-dizen-qurtnezir-cyrl/*.json` |
| `scripts/validate_data.py` | End-to-end integrity validator checking 114/114 surahs, 6,236/6,236 sequential verses, zero script leakage/homoglyphs, zero unbalanced parentheses, zero appendix bleed, CID referential integrity, and QUL JSON/SQLite schema compliance. | Exit code `0` on full pass |

## Historical Defects Resolved from Earlier OCR Pipeline

1. **30 Misaligned Surahs & 110 Missing Verses (`6,126` $\to$ `6,236`)**: Earlier text-scraping scripts missed unnumbered/shifted surah headers starting around Surah 78–113, causing Surah 85 (`085-Al-Buruj.yaml`) to hold Surah 86 (*At-Tariq*) and shifting 30 surah files out of alignment with Arabic core.
2. **1,356-Line Appendix Bleed in `114-An-Nas.yaml`**: Surah 114 on PDF p. 508 is printed as a single merged range `1-6.`; earlier scripts failed to stop before p. 509 (`Илявелер / Мевзулар боюнджа мундеридже`) and dumped 56 pages of thematic index, glossary, khatm dua, and bibliography into verse `114:6`.
3. **59 Unsplit Embedded Verses**: Line-wrap collisions in the PDF caused inline verse numbers to merge into preceding verses.
4. **Mixed-Script Homoglyphs & Vowel Flattening**: Replaced mixed Cyrillic/Latin `Allaһ` (`U+04BB` in Latin text) and flattened `o/u/ya` vowels (`buyuk`, `guzel`, `boyle`, `inkyar`) with standard Crimean Tatar Latin orthography (`Allah`, `büyük`, `güzel`, `böyle`, `inkâr`).
5. **Frontend Script Toggle & Commentary List-Marker Bug**: Fixed `src/utils/transliteration.js` (`transliterateCrh` syllable-aware `ö/ü/â` and `'` handling) and `src/components/VerseCard.jsx` (`isListMarkerClose` preventing `a).`, `b).`, `v).`, `1).` inside commentary from prematurely closing `<CollapsibleCommentary>`).
