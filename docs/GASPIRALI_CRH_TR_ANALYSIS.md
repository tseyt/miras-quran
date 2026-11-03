# İsmail Gaspıralı (`"Dilde, fikirde, işte birlik"`) & Crimean Tatar ↔ Turkish Quranic Bridging Analysis

## A. Verbatim Primary-Source Evidence & Corpus Measurements

### 1. Direct Textual Lineage of Dizen & Qurtnezir (`[CORROBORATED]`)

- **Primary Source Coordinate**: Sait Dizen & Zakir Qurtnezir, *Къур'ан-ы Керим ве изаатлы манасы* (*Qur'an-ı Kerim ve izaatlı manası*), 2nd ed., Simferopol, 2005, Page 564 (`Файдаланылгъан менбалар` / Bibliography, Item `1).`):
  > `1). Къур'ан-ы Керим ве ачыкъламалы меали. Азырлагъанлар Проф., д-р Али ОЗЕК ве дигерлери. Анкъара, 1993.`
  > *(Prof. Dr. Ali Özek et al., Kur'an-ı Kerim ve Açıklamalı Meali, Türkiye Diyanet Vakfı, Ankara, 1993; items 2–8 on p. 564 likewise cite Istanbul and Ankara Turkish tafsirs and lexicons from 1979–1995.)*
- **Mufti Emirali Ablayev's 2004 Preface (`p. 2`, `[VERIFIED]`)**:
  > `Бу иште бизге тюрк къардашларымыз ярдымджы олдылар.`
  > *("In this work our Turkish brothers assisted us.")*
- **2005 Glossary (`Лугъат`, `pp. 549–561`, `495` entries in `src/data/glossary/crh-quranic-glossary.json`, `[CORROBORATED]`)**:
  Dizen & Qurtnezir adopted Oghuz/Turkish literary lexemes from the 1993 Ankara TDV *Meal* inside the verse translation and explicitly glossed them into everyday Kipchak Crimean Tatar in the back-of-book Glossary:

| Adopted Oghuz / Literary Term in CRH Verse Text | Dizen-Qurtnezir 2005 Glossary Definition (Everyday Kipchak CRH) | Turkish (`tr/diyanet`) Cognate |
| :--- | :--- | :--- |
| `булмакъ` (`bulmaq`) | `тапмакъ.` (`tapmaq`) | `bulmak` |
| `баты` (`batı`) | `гъарп (запад).` (`ğarp`) | `batı` |
| `догъу` (`doğu`) | `шаркъ, кунь догъгъан тараф.` (`şarq`) | `doğu` |
| `дегер` (`deger`) | `къыймет.` (`qıymet`) | `değer` |
| `денъемек` (`deñemek`) | `сынамакъ.` (`sınamaq`) | `denemek` |
| `дестек` (`destek`) | `ярдым, къол тутув.` (`yardım, qol tutuv`) | `destek` |
| `ёрум` (`yorum`) | `тефсир, анълатув.` (`tefsir, añlatuv`) | `yorum` |
| `суч` (`suç`) | `къабаат, джинает.` (`qabaat, cinayet`) | `suç` |
| `тилемек` (`tilemek`) | `истемек.` (`istemek`) | `dilemek` |
| `узеринде` (`üzerinde`) | `усьтюнде.` (`üstünde`) | `üzerinde` |
| `эйи` (`eyi`) | `яхшы.` (`yahşı`) | `iyi` |
| `юзь` (`yüz`) | `бет, чырай.` (`bet, çıray`) | `yüz` |

---

### 2. Full 6,236-Verse Empirical Metrics (`crh/dizen-qurtnezir` vs. `tr/diyanet` & `tr/elmalili`, `[CORROBORATED]`)

| Corpus Metric (`114` Surahs, `6,236` Verses) | `@ HEAD` (Pre-Fix) | Rebuilt Canonical CRH (`Latn`) | Delta |
| :--- | :---: | :---: | :---: |
| **CRH Verse Body Tokens** (excluding `>= 7`-word *izaat* footnotes) | — | `114,927` (`64.59%`) | — |
| **CRH Parenthetical *İzaat* Commentary Tokens** (`1,442` footnotes) | — | `63,008` (`35.41%`) | — |
| **Same-Verse Exact Word Identity** with `tr/diyanet` $\cup$ `tr/elmalili` | `18.80%` | **`26.53%`** | **`+7.73 pp` (`+41.1%` relative)** |
| **Same-Verse Exact + Regular Sound-Law Cognate Match** | — | **`52.98%`** | — |
| **Corpus-Wide Exact Turkish Vocabulary Match** | `37.03%` | **`41.32%`** | **`+4.29 pp`** |
| **Corpus-Wide Regular Sound-Law Cognate Transparency** | — | **`81.01%`** | — |

- **Immediate Orthographic Lift (`+41.1%` relative exact-match gain with zero lexical mutation)**:
  Restoring Surah alignment (`30` previously shifted surahs), stripping Cyrillic homoglyphs (`Allaһ` $\to$ `Allah`: `1,564` exact same-verse hits), and restoring standard Crimean Tatar `ö / ü / â` vowel harmony (`büyük` `145×`, `inkâr` `135×`, `güzel` `126×`, `yüz` `99×`, `böyle` `89×`) raises same-verse exact Turkish word identity from `18.80%` to `26.53%` without altering a single word chosen by Dizen & Qurtnezir.

---

### 3. Internal Dialect Stratigraphy of Dizen & Qurtnezir (`[CORROBORATED]`)

Crimean Tatar comprises three historical dialect zones:
1. **Southern Coastal (*Yalıboyu*)** — Oghuz-aligned, closest to Ottoman/Republican Turkish.
2. **Central / Bakhchysarai (*Orta Yolaq*)** — Oghuz-Kipchak transitional zone; historical base of **İsmail Gaspıralı's** *Tercüman* (`1883–1918`) and modern literary Crimean Tatar.
3. **Northern Steppe (*Çöl*)** — Kipchak-Nogai.

Token counts across all `114,927` verse-body words in `crh/dizen-qurtnezir`:

| Semantic Slot | Oghuz / *Orta Yolaq* Form in Dizen-Qurtnezir | Northern Kipchak Form in Dizen-Qurtnezir | Oghuz / *Orta Yolaq* Share |
| :--- | :--- | :--- | :---: |
| **"to become / be"** | `ol-` (`olğan`, `oldı`, `olur`, `olacaq`): **`1,398`** | `bol-` (`bolğan`, `boldı`): **`3`** | **`99.8%`** |
| **"is not" (negation)** | `degil` / `degildir`: **`184`** | `tüvül`: **`0`** | **`100.0%`** |
| **"to send (revelation/messengers)"** | `yolla-`: **`265`** | `yiber-`: **`3`** | **`98.9%`** |
| **"to speak / say"** | `söyle-`: **`182`** | `ayt-`: **`23`** | **`88.8%`** |
| **"to find / be found"** | `bul-` / `bulun-`: **`138`** | `tap-`: **`114`** | **`54.8%`** |
| **"good / beautiful"** | `güzel`: **`193`** (+ `eyi`) | `yahşı`: **`327`** | **`37.1%`** (complementary) |
| **"to eat" / "to protect" / "to seek"** | — | `aşa-` (`146`), `qorçala-` (`110`), `qıdır-` (`29`) | **`0.0%`** (pure CRH Kipchak) |

---

## B. Structural Analysis

### 1. Boilerplate-Stripped Delta Table: CRH (`dizen-qurtnezir`) vs. Turkish (`diyanet` / `elmalili`)

| Linguistic Layer | `Shared Kernel (Unify)` (Orthography, Tooling & CIDs) | `Hard Divergence (Keep Separate)` (Core Crimean Tatar Identity) |
| :--- | :--- | :--- |
| **Alphabet & Vowel Harmony** | Shared 31-letter Turkic Latin base (`a, e, ı, i, o, ö, u, ü, ç, ğ, ş, â`), eliminating artificial Soviet Cyrillic graphic distance (`буюк` $\to$ `büyük`, `гузель` $\to$ `güzel`, `инкяр` $\to$ `inkâr`). | Distinct Crimean Tatar velar/uvular & nasal phonemes **`q`** (`Къур'ан` $\to$ `Qur'an`, `qalb`, `aqiqat`) and **`ñ`** (`Allahnıñ`, `saña`, `yalıñız`) which encode minimal pairs in CRH. |
| **Sacred & Abstract Lexicon** | Shared Arabic-Persian-Turkic Quranic terminology (`Allah`, `Rabb`, `rahmet`, `iman`, `namaz`, `zekât`, `ahiret`, `cennet`, `ceennem`, `mü'min`, `kâfir`, `munafıq`, `sabır`, `şükür`, `tevbe`/`tövbe`) + *Orta Yolaq* verbs (`ol-`, `degil`, `yolla-`, `söyle-`). | Core Crimean Tatar everyday roots (`yahşı`, `aşa-`, `qorçala-`, `tap-`, `qıdır-`, `aqwam`/`qavm`, `ber-`, `bar`/`yoq`, `eki`, `köster-`, `kün`, `köz`, `tüşün-`). |
| **Case, Participle & Pronoun Morphology** | Parallel left-branching Turkic SOV clause order, identical Concept ID (`cid`) chunk boundaries, and regular 1-to-1 suffix correspondence. | Defining Crimean Tatar grammatical suffixes & pronouns: genitive **`-nıñ/-niñ`** (vs TR `-ın/-in`), dative **`-ğa/-ge/-qa/-ke`** (vs TR `-a/-e`), accusative **`-nı/-ni`** (vs TR `-ı/-i`), past participle **`-ğan/-gen/-qan/-ken`** (vs TR `-an/-en`), verbal noun **`-uv/-üv`** (vs TR `-ma/-me`), instrumental **`-nen`** (vs TR `-le`), pronouns **`men`**, **`olar`**, **`saña`**, **`maña`**, **`öz`**, postposition **`içün`**. |
| **Exegetical Apparatus** | Shared 1993 Ankara TDV *Açıklamalı Meal* theological framework (`1,442` footnotes) and `495`-entry Glossary (`src/data/glossary/crh-quranic-glossary.json`). | Muftiyat of Crimea institutional canonization (Decision `15/10/2004`), preserving post-deportation homeland (*Vatan*) liturgical continuity (including the Crimean Tatar *Hatim Duası* on `pp. 562–563`). |

---

### 2. Dialectical Evaluation & Calibrated JEV Ranking (`[RIVAL DESIGN]`)

Evaluated via `genai.DecisionService.CreateDecision` (`usul_jev.py rank-designs --json` on `scratch/gaspirali_designs.json`) across **`P0 INVARIANTS` > `P1 CORE GOALS` > `P2 POLISH`**:

| Rank | Candidate Architecture | `P0` Invariant Status (`p0_safe_prob` / Band) | `P1` Core Fit (`0–4`) | `P2` Polish (`0–2`) | Verdict & Structural Rationale |
| :---: | :--- | :---: | :---: | :---: | :--- |
| **1** | **`[RIVAL DESIGN C]` Canonical Text Preservation + Standard `ö/ü/â` Orthography + Non-Destructive Semantic/Glossary Bridge** | **`PASS`** (`0.9612` — **`CERTAIN`**) | **`3.66 / 4.00`** (`73.0%` Exemplary `4/4`) | **`1.74 / 2.00`** (**`LIKELY`**) | **Selected & Implemented.** Honors Dizen & Qurtnezir's existing Bakhchysarai *Orta Yolaq* / Gaspıralı synthesis, achieves a `+41.1%` relative jump in exact CRH↔TR lexical match (`26.53%`) and `81.01%` cognate transparency purely through accurate orthography & alignment, preserves Muftiyat Decision `15/10/2004` intact, and bridges CRH↔TR via parallel UI + `crh-quranic-glossary.json` + CIDs. |
| **2** | **`[RIVAL DESIGN B]` Synthetic Machine-Hybridized `crh-ortaturk` Fork Translation** | **`DISQUALIFIED_P0_RISK`** (`0.1157` — **`LIKELY`** unsafe) | `1.22 / 4.00` (`POLARIZED`) | `0.63 / 2.00` | **Rejected.** Algorithmic hybridization of sacred scripture without scholarly/Muftiyat oversight risks subtle doctrinal distortion (`taḥrīf al-maʻnā`), confuses learners about authentic `crh` grammar, and has zero standing for Quran.com / QUL onboarding. |
| **3** | **`[RIVAL DESIGN A]` Destructive In-Place Lexical & Morphological Turkification** | **`DISQUALIFIED_P0_RISK`** (`0.0126` — **`CERTAIN`** violation) | `0.24 / 4.00` (`80.9%` Poor `0/4`) | `0.32 / 2.00` | **Rejected.** Overwriting `-ğan` $\to$ `-an`, `-nıñ` $\to$ `-ın`, `olar` $\to$ `onlar`, `aşa-` $\to$ `ye-` destroys the grammatical core of a UNESCO severely endangered language, falsifies attribution to Sait Dizen & Zakir Qurtnezir, and duplicates `tr/diyanet` (which `miras-quran` already ships side-by-side). |

### Historical & Philological Counterexample Against Textual Assimilation (`[COUNTEREXAMPLE]`)

1. **Gaspıralı's *Tercüman* Was a Newspaper Bridge, Not Vernacular Erasure**: İsmail Gaspıralı (`1851–1914`) crafted *Tercüman*'s simplified Oghuz-based literary koiné so readers from Kazan, Crimea, Baku, and Istanbul could share a single print periodical under Tsarist censorship. For **Crimean Tatar Quranic exegesis**, however, the explicit institutional purpose stated by Mufti Emirali Ablayev (`2005, p. 2`) is enabling Crimean Tatars to understand divine commands **`ана тиллеринде`** (*in their mother tongue*).
2. **Dizen & Qurtnezir Already Built the Bridge**: Because Dizen & Qurtnezir translated directly alongside the 1993 Ankara TDV *Meal* in the Bakhchysarai *Orta Yolaq* literary register (`ol-` `99.8%`, `degil` `100%`, `yolla-` `98.9%`, `söyle-` `88.8%`) and attached a `495`-entry Glossary mapping literary Turkish/Arabic terms to Kipchak Crimean Tatar, **their 2005 text is already the authentic realization of Gaspıralı's bridge**. Pushing it any further toward Istanbul Turkish crosses the line from *bridging* (`köpür`) into *linguistic erasure*.

---

## C. Regular Sound-Law & Morphological Bridge Reference (For Turkish↔CRH Readers in `miras-quran`)

With standard CRH Latin orthography restored, a Turkish reader (or Crimean Tatar reader consulting `tr/diyanet` and `tr/elmalili` in `miras-quran`) can read **`81.01%`** of the vocabulary immediately via six regular correspondences:

| Rule | Turkish (`tr`) | Crimean Tatar (`crh`) | Quranic Examples (`crh` $\leftrightarrow$ `tr`) |
| :--- | :--- | :--- | :--- |
| **1. Back Velar Stop & Velar Nasal** | `k` (back), `n` | **`q`**, **`ñ`** | `Qur'an` $\leftrightarrow$ `Kur'an`, `qalb` $\leftrightarrow$ `kalp`, `Allahnıñ` $\leftrightarrow$ `Allah'ın`, `saña` $\leftrightarrow$ `sana`, `yalıñız` $\leftrightarrow$ `yalnız` |
| **2. Initial Voiceless `k- / t-` & Labial `b-`** | `g-`, `d-`, `v-` | **`k-`**, **`t-`**, **`b-`** | `kelmek` $\leftrightarrow$ `gelmek`, `körmek` $\leftrightarrow$ `görmek`, `kün` $\leftrightarrow$ `gün`, `köstermek` $\leftrightarrow$ `göstermek`, `tüşünmek` $\leftrightarrow$ `düşünmek`, `bermek` $\leftrightarrow$ `vermek`, `bar` $\leftrightarrow$ `var` |
| **3. Participle `-ğan/-gen` & Verbal Noun `-uv/-üv`** | `-an/-en`, `-dıq`, `-ma/-me` | **`-ğan/-gen`**, **`-uv/-üv`** | `olğan` $\leftrightarrow$ `olan`, `etken` $\leftrightarrow$ `eden`, `yaratılğan` $\leftrightarrow$ `yaratılan`, `oquv` $\leftrightarrow$ `okuma`, `añlatuv` $\leftrightarrow$ `anlatma` |
| **4. Case Suffixes (Gen / Dat / Acc / Inst)** | `-(n)ın`, `-(y)a`, `-(y)ı`, `-le` | **`-nıñ`**, **`-ğa/-qa`**, **`-nı`**, **`-nen`** | `alemlerniñ` $\leftrightarrow$ `âlemlerin`, `Allahqa` $\leftrightarrow$ `Allah'a`, `yolnı` $\leftrightarrow$ `yolu`, `adınen` $\leftrightarrow$ `adıyla` |
| **5. Personal & Reflexive Pronouns** | `ben`, `onlar`, `kendi` | **`men`**, **`olar`**, **`öz`** | `menim` $\leftrightarrow$ `benim`, `olarnıñ` $\leftrightarrow$ `onların`, `özlerine` $\leftrightarrow$ `kendilerine` |
| **6. Core Kipchak Everyday Verbs & Adjectives** | `iyi`, `yemek`, `bulmak`, `korumak`, `aramak` | **`yahşı`**, **`aşamaq`**, **`tapmaq`**, **`qorçalamaq`**, **`qıdırmaq`** | Indexed bidirectional bridge in `src/data/glossary/crh-quranic-glossary.json` |
