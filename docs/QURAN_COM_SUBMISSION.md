# Submitting Crimean Tatar (`crh`) to Tarteel QUL & Quran.com

## 1. Upstream Architecture & Ingestion Path

Quran.com (Quran.Foundation) ingests translations, footnotes, grouped-verse mappings, and localized chapter metadata upstream via **Tarteel's Quranic Universal Library (QUL)** (`https://qul.tarteel.ai` / `https://github.com/TarteelAI/quranic-universal-library`), which exports validated datasets to `quran/quran.com-api` (API v4) and surfaces them in `quran/quran.com-frontend-next`.

Adding **Crimean Tatar (`crh`)** requires two coordinated upstream tracks:

| Track | Target Repository / Portal | Scope | Prepared Assets in `exports/quran-com/` |
| :--- | :--- | :--- | :--- |
| **Track 1: Translation, Footnotes, Grouped Ayahs & Chapter Names** | `TarteelAI/quranic-universal-library` (`qul.tarteel.ai`) | Register ISO 639-3 `crh` (`Qırımtatarca`), onboard 114 localized Surah names, and import `crh-dizen-qurtnezir-latn` + `crh-dizen-qurtnezir-cyrl` (`6,236` ayahs, `1,442` structured footnotes, `325` grouped ayah ranges) | `metadata/language-crh.json`<br>`metadata/chapters-crh-latn.json`<br>`metadata/chapters-crh-cyrl.json`<br>`crh-dizen-qurtnezir-latn/*.json`<br>`crh-dizen-qurtnezir-cyrl/*.json`<br>`--sqlite` QUL `.sqlite` builds |
| **Track 2: Quran.com Content Sync & Optional UI Locale** | `feedback.quran.com` & `quran/quran.com-frontend-next` | Sync QUL translation IDs to Quran.com production API v4 (`es_analyzer_default: "turkish"`), enable translation picker under `Crimean Tatar (Qırımtatarca)`, and optionally onboard `crh` UI strings in Lokalise / `i18n.json` | Copy-pasteable submission payloads below |

---

## 2. Canonical Provenance & Institutional Authorization

| Field | Value |
| :--- | :--- |
| **Title (Latin / Cyrillic)** | *Qur'an-ı Kerim ve izaatlı manası* / *Къур'ан-ы Керим ве изаатлы манасы* |
| **Translators** | **Sait Dizen & Zakir Qurtnezir** |
| **Edition & Imprint** | 2nd revised edition (*2-ci neşiri*), Simferopol (Aqmescit), Crimea, 2005 (`564` pages; 1st ed. 1998, `5,000` copies) |
| **Institutional Approval** | **Religious Administration of Muslims of Crimea (*Qırım Musulmanları Diniy İdaresi* / Muftiyat)**, Official Decision dated **`15/10/2004`**, Preface signed by **Mufti Emirali Ablayev** (*Oktyabr, 2004*) |
| **Language & Scripts** | Crimean Tatar (`ISO 639-3: crh`), dual-script delivery: **`crh-Latn`** (official Crimean Tatar Latin alphabet per 1992 Qırım Yuqarı Şurası resolution & 2021 Cabinet of Ministers Resolution No. 993) and **`crh-Cyrl`** (2005 Simferopol print Cyrillic, pure Unicode `U+0400..U+04FF` with zero Latin homoglyphs) |
| **UNESCO Status** | Severely Endangered Indigenous Language (UNESCO *Atlas of the World's Languages in Danger*) |

---

## 3. Structural Specification of Generated Export Files

Regenerate all JSON and optional SQLite artifacts anytime from the verified source pipeline:

```bash
# 1. Rebuild canonical Markdown, 114 Surah YAMLs, merged-range index, and 495-entry Glossary from the 2005 PDF
python3 scripts/rebuild_crh_from_pdf.py

# 2. Export QUL / Quran.com JSON bundles (+ optional QUL SQLite databases)
python3 scripts/export_quran_com.py --sqlite /tmp/qul-sqlite

# 3. Run full integrity validation across all 6,236 verses and QUL schemas
python3 scripts/validate_data.py
```

### Export Inventory (`exports/quran-com/`)

| Path | Schema & Purpose | Verified Counts |
| :--- | :--- | :--- |
| `metadata/language-crh.json` | Language descriptor (`iso_code: "crh"`, `native_name: "Qırımtatarca"`, `direction: "ltr"`, `es_analyzer_default: "turkish"`) + resource descriptors for `Latn` and `Cyrl` | `2` resources |
| `metadata/chapters-crh-latn.json` | 114 Surah names (`el-Faatiha`..`en-Naas`), Crimean Tatar translated meanings (`Açış`..`İnsanlar`), revelation places (`Mekke`/`Medine`), verse counts, and Dizen-Qurtnezir surah introductions | `114` chapters |
| `metadata/chapters-crh-cyrl.json` | Cyrillic counterpart of the 114 Surah metadata (`эль-Фаатиһа`..`эн-Наас`, `Ачыш`..`Инсанлар`, `Мекке`/`Медине`) | `114` chapters |
| `crh-dizen-qurtnezir-{latn,cyrl}/simple.json` | Flat `{"S:V": "verse translation"}` map with long parenthetical *izaat* commentaries stripped cleanly (preserving short `<= 6`-word inline lexical clarifications) | `6,236` keys |
| `crh-dizen-qurtnezir-{latn,cyrl}/translation-with-footnote-tags.json` | Canonical QUL footnote schema: `{"S:V": {"t": "...<sup foot_note=\"10001\">1</sup>", "f": {"10001": "..."}}}` extracting all standalone `>= 7`-word *izaat* commentaries into structured footnotes | `6,236` keys, `1,442` footnotes |
| `crh-dizen-qurtnezir-{latn,cyrl}/translation-with-inline-footnote.json` | QUL inline-bracket schema (`Text [[Footnote]]`) | `6,236` keys |
| `crh-dizen-qurtnezir-{latn,cyrl}/grouped-verses.json` | Explicit range mapping for all `5,677` translation units (`5,352` single ayahs + `325` author-merged multi-ayah blocks covering `884` ayahs, e.g. `2:40-41`, `85:1-7`, `114:1-6`) so QUL/Quran.com renders combined ayah cards natively rather than showing placeholder cross-references | `5,677` units (`325` grouped ranges = `6,236` ayahs) |
| `--sqlite` (`crh-dizen-qurtnezir-{latn,cyrl}.sqlite`) | Ready-to-import QUL SQLite database with `translations(sura, ayah, ayah_key, text)` and `foot_notes(id, ayah_key, text)` tables | `6,236` rows + `1,442` footnotes |

> **Grouped-Verse Handling Note**: In the 2005 Simferopol edition, Dizen & Qurtnezir translated `325` multi-ayah passages syntactically as single combined sentences (for instance, Surah 114 *en-Naas* is printed as `1-6.` because Crimean Tatar left-branching SOV syntax places the main verb `sığınırım!` at the end of `114:1` while `114:6` sits at the beginning of the clause).
> - If importing into QUL's **grouped-ayah / range** pipeline, use `grouped-verses.json` so Quran.com groups `114:1-6` into one card.
> - If importing into a flat `6,236`-row table without range grouping, `simple.json` and `translation-with-footnote-tags.json` populate continuation verses with explicit cross-references (`[114:1 ayetine baqıñız]` / `[114:1 аетине бакъынъыз]`), or pass `--repeat-merged` to `scripts/export_quran_com.py` if full text repetition is preferred.

---

## 4. Copy-Pasteable Submission Templates

### A. GitHub Issue for `TarteelAI/quranic-universal-library`

Open a new issue at `https://github.com/TarteelAI/quranic-universal-library/issues/new` with the following title and body:

**Title:**
`[New Language & Translation] Add Crimean Tatar (crh — Latn & Cyrl): Sait Dizen & Zakir Qurtnezir (Muftiyat of Crimea, 2005)`

**Body:**
```markdown
Assalamu alaikum wa rahmatullahi wa barakatuh,

We have prepared a fully validated, dual-script QUL import package to add **Crimean Tatar (`ISO 639-3: crh` / `Qırımtatarca`)**—a UNESCO-listed severely endangered Turkic language—to the Quranic Universal Library (QUL) and downstream to Quran.com.

### 1. Source & Institutional Authorization
- **Book Title**: *Qur'an-ı Kerim ve izaatlı manası* (*Къур'ан-ы Керим ве изаатлы манасы*)
- **Translators**: **Sait Dizen & Zakir Qurtnezir**
- **Edition**: 2nd revised edition, Simferopol (Aqmescit), 2005 (564 pages)
- **Official Approval**: Published by the **Religious Administration of Muslims of Crimea (*Qırım Musulmanları Diniy İdaresi* / Muftiyat)** pursuant to **Decision `15/10/2004`**, with preface by **Mufti Emirali Ablayev**.

### 2. Language Metadata (`crh`)
- **ISO 639-3**: `crh` (`crh-Latn` primary official alphabet, `crh-Cyrl` 2005 print Cyrillic)
- **English Name**: `Crimean Tatar`
- **Native Name**: `Qırımtatarca` (`Къырымтатарджа`)
- **Direction**: `ltr`
- **Recommended Elasticsearch Analyzer**: `turkish`

### 3. Validated QUL Assets Ready for Import
Repository path: `https://github.com/tseyt/miras-quran/tree/main/exports/quran-com`

1. **Language & 114 Localized Chapter Names (`Latn` & `Cyrl`)**:
   - `exports/quran-com/metadata/language-crh.json`
   - `exports/quran-com/metadata/chapters-crh-latn.json` (114 surah names, Crimean Tatar translated meanings, revelation places, and surah introductions)
   - `exports/quran-com/metadata/chapters-crh-cyrl.json`
2. **Latin Script Edition (`crh-dizen-qurtnezir-latn`)**:
   - `simple.json` (6,236/6,236 verses, zero commentary bloat, zero Cyrillic character leakage)
   - `translation-with-footnote-tags.json` (6,236 verses + 1,442 structured `<sup foot_note="id">n</sup>` footnotes extracted from the edition's parenthetical *izaat* commentary)
   - `translation-with-inline-footnote.json` (`[[Footnote]]` format)
   - `grouped-verses.json` (explicit range mapping for all 325 author-merged multi-ayah blocks, e.g. `2:40-41`, `114:1-6`)
3. **Cyrillic Script Edition (`crh-dizen-qurtnezir-cyrl`)**:
   - `simple.json`, `translation-with-footnote-tags.json`, `translation-with-inline-footnote.json`, `grouped-verses.json` (6,236 verses, 1,442 footnotes, pure Unicode Cyrillic with all 2005 PDF OCR/homoglyph artifacts cleaned)
4. **QUL SQLite Builds**:
   - Reproducible via `python3 scripts/export_quran_com.py --sqlite <dir>` (`translations` + `foot_notes` tables).

### 4. Quality & Integrity Checks Passed
- `114/114` Surahs and `6,236/6,236` sequential verses verified against Uthmani Hafs numbering.
- `0` unbalanced parentheses, `0` mixed-script homoglyphs, and `100%` footnote tag-to-dictionary referential integrity verified by `scripts/validate_data.py`.

Please let us know if you prefer a direct PR or QUL CMS upload, or if you would like Latin (`crh-Latn`) as the primary `crh` translation and Cyrillic (`crh-Cyrl`) as a second `crh` translation option (similar to Uzbek/Kazakh dual-script offerings on Quran.com). Jazakumullahu khayran!
```

---

### B. Content Request for `feedback.quran.com` / Quran.Foundation

Once the QUL issue URL is created, post at `https://feedback.quran.com` (Category: **Translations / New Language Request**):

**Title:**
`Add Crimean Tatar (Qırımtatarca, ISO: crh) Translation — Sait Dizen & Zakir Qurtnezir (Muftiyat of Crimea)`

**Body:**
```markdown
Please add **Crimean Tatar (`crh` / `Qırımtatarca`)** to Quran.com's supported translation languages!

- **Translation**: *Qur'an-ı Kerim ve izaatlı manası* by **Sait Dizen & Zakir Qurtnezir** (2nd ed., Simferopol, 2005), officially approved by the Religious Administration of Muslims of Crimea (*Qırım Musulmanları Diniy İdaresi*, Decision `15/10/2004`).
- **Scripts Provided**: Both Official Crimean Tatar Latin (`crh-Latn`) and Cyrillic (`crh-Cyrl`), similar to Quran.com's dual-script Uzbek (`uz`) support.
- **Upstream QUL Package**: All 6,236 verses, 1,442 structured `<sup foot_note>` commentaries, 325 grouped ayah ranges, and all 114 localized Crimean Tatar Surah names/meanings are validated and ready in QUL format at:
  https://github.com/tseyt/miras-quran/tree/main/exports/quran-com
- **Upstream QUL Issue**: <paste TarteelAI/quranic-universal-library issue URL here>
```

---

### C. Optional UI Locale Onboarding (`quran/quran.com-frontend-next`)

Note that Quran.com allows **translations** in a new language (`crh`) immediately via API v4 without requiring full UI localization of `quran.com-frontend-next`. If you also wish to contribute a full Crimean Tatar website UI localization:

1. Open an issue in `https://github.com/quran/quran.com-frontend-next/issues` requesting `"crh"` (`Qırımtatarca`, `ltr`) to be added to Quran.Foundation's **Lokalise** project and `i18n.json` (`locales` array + `LOCALE_NAME` in `src/utils/locale.ts`).
2. Leverage `src/data/glossary/crh-quranic-glossary.json` and `exports/quran-com/metadata/chapters-crh-latn.json` for consistent Quranic UI terminology (`Sure`, `Ayet`, `Cüz`, `Tercime`, `Tefsir`, ` İzaat`).
