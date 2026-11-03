#!/usr/bin/env python3
"""Rebuild all Crimean Tatar (CRH) Markdown, YAML, and Glossary files directly from the 2005 PDF.

Primary Source:
  translations/quran-crh-dizen-qurtnezir.pdf
  (Sait Dizen & Zakir Qurtnezir, "Qur'an-ı Kerim ve izaatlı manası", 2nd ed., Simferopol, 2005;
   Qırım Musulmanları Diniy İdaresi Decision 15/10/2004)

Outputs:
  - translations/quran-crh-dizen-qurtnezir.md (Canonical Cyrillic Markdown)
  - translations/quran-crh-dizen-qurtnezir-lat.md (Canonical Latin Markdown)
  - src/data/translations/crh/dizen-qurtnezir/*.yaml (114 aligned Surah YAML files, 6,236 verses)
  - src/data/translations/crh/dizen-qurtnezir-merged-ranges.json (325 author-merged ranges + intros)
  - src/data/glossary/crh-quranic-glossary.json (Structured Lugat glossary from pp. 549-561)
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import textwrap
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

from crh_orthography import (
    check_balanced_parens,
    clean_pdf_cyrillic_text,
    cyrillic_to_latin_crh,
    join_pdf_lines,
)

PDF_PATH = REPO_ROOT / "translations" / "quran-crh-dizen-qurtnezir.pdf"
CYR_MD_OUT = REPO_ROOT / "translations" / "quran-crh-dizen-qurtnezir.md"
LAT_MD_OUT = REPO_ROOT / "translations" / "quran-crh-dizen-qurtnezir-lat.md"
CRH_YAML_DIR = REPO_ROOT / "src" / "data" / "translations" / "crh" / "dizen-qurtnezir"
CORE_YAML_DIR = REPO_ROOT / "src" / "data" / "core"
MERGED_META_OUT = REPO_ROOT / "src" / "data" / "translations" / "crh" / "dizen-qurtnezir-merged-ranges.json"
GLOSSARY_OUT = REPO_ROOT / "src" / "data" / "glossary" / "crh-quranic-glossary.json"

RU_ROMAN_MAP = {
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "yo", "ж": "zh",
    "з": "z", "и": "i", "й": "y", "к": "k", "л": "l", "м": "m", "н": "n", "о": "o",
    "п": "p", "р": "r", "с": "s", "т": "t", "у": "u", "ф": "f", "х": "kh", "ц": "ts",
    "ч": "ch", "ш": "sh", "щ": "shch", "ъ": "", "ы": "y", "ь": "'", "э": "e", "ю": "yu", "я": "ya",
}


def romanize_ru(text: str) -> str:
    out = []
    for ch in text:
        low = ch.lower()
        if low in RU_ROMAN_MAP:
            rep = RU_ROMAN_MAP[low]
            out.append(rep.capitalize() if ch.isupper() else rep)
        else:
            out.append(ch)
    return "".join(out)


def extract_pdf_pages(pdf_path: Path) -> list[str]:
    res = subprocess.run(
        ["pdftotext", "-layout", str(pdf_path), "-"],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    pages = res.stdout.split("\f")
    # Drop trailing empty page after final form-feed if empty
    while pages and not pages[-1].strip():
        pages.pop()
    return pages


def load_core_surah_specs() -> dict[int, dict[str, object]]:
    specs: dict[int, dict[str, object]] = {}
    for p in sorted(CORE_YAML_DIR.glob("*.yaml")):
        txt = p.read_text(encoding="utf-8")
        m_id = re.search(r"^(?:id|surah_id):\s*(\d+)", txt, re.M)
        if not m_id:
            continue
        sid = int(m_id.group(1))
        vnums = [int(x) for x in re.findall(r"^\s*-\s+verse:\s*(\d+)", txt, re.M)]
        specs[sid] = {
            "id": sid,
            "file": p.name,
            "total": len(vnums),
        }
    assert len(specs) == 114, f"Expected 114 core surahs, found {len(specs)}"
    return specs


def strip_running_chrome(page_text: str, page_no: int) -> list[str]:
    out = []
    for ln in page_text.split("\n"):
        s = ln.strip()
        if s == "Къур'ан-ы Керим ве изаатлы манасы" and page_no >= 2:
            continue
        if re.match(r"^\d+$", s):
            continue
        out.append(ln)
    return out


def parse_paragraphs(lines: list[str], heading_set: dict[str, str] | None = None) -> list[str]:
    """Join wrapped PDF lines into clean Markdown paragraphs."""
    heading_set = heading_set or {}
    blocks: list[str] = []
    cur: list[str] = []

    def flush():
        if cur:
            joined = join_pdf_lines(cur)
            blocks.append(clean_pdf_cyrillic_text(joined))
            cur.clear()

    for ln in lines:
        s = ln.strip()
        if not s:
            flush()
            continue
        if s in heading_set:
            flush()
            blocks.append(f"{heading_set[s]} {clean_pdf_cyrillic_text(s)}")
            continue
        if re.match(r"^\d+\)?[.)]\s+", s):
            flush()
            cur.append(s)
            continue
        cur.append(s)
    flush()
    return blocks


def parse_front_matter(pages: list[str]) -> list[str]:
    """Parse Pages 1-5 front matter (before '1. эль-ФААТИhА' on page 6)."""
    fm_lines: list[str] = []
    for pno in range(1, 6):
        fm_lines.extend(strip_running_chrome(pages[pno - 1], pno))

    headings = {
        "Къур'ан-ы Керим ве изаатлы манасы": "#",
        "Сёз башы": "#",
        "Экинджи неширге сёз башы": "##",
        "Къур'ан ве манасы": "#",
        "САИТ ДИЗЕН, ЗАКИР КЪУРТНЕЗИР.": "#",
    }
    return parse_paragraphs(fm_lines, headings)


def parse_surahs(pages: list[str], core_specs: dict[int, dict[str, object]]) -> list[dict]:
    body_lines: list[tuple[int, str]] = []
    for pno in range(5, 509):
        for ln in strip_running_chrome(pages[pno - 1], pno):
            body_lines.append((pno, ln))

    next_surah = 1
    surah_starts: dict[int, tuple[int, int, str]] = {}
    for idx, (pno, ln) in enumerate(body_lines):
        if pno < 6 and next_surah == 1 and not ln.lstrip().startswith("1."):
            continue
        m_raw = re.match(rf"^({next_surah}\.)(\s+)(.+)$", ln)
        if m_raw:
            title_cand = m_raw.group(3).strip()
            upper_chars = sum(1 for c in title_cand if c.isupper())
            if upper_chars >= 2 and len(title_cand) < 40 and not title_cand.endswith((".", ",", ":", ";", "!", "?")):
                surah_starts[next_surah] = (idx, pno, title_cand)
                next_surah += 1
                if next_surah > 114:
                    break

    assert len(surah_starts) == 114, f"Expected 114 surah headers, got {len(surah_starts)}"

    surahs = []
    s_list = sorted(surah_starts.keys())
    for i, sid in enumerate(s_list):
        start_idx = surah_starts[sid][0] + 1
        end_idx = surah_starts[s_list[i + 1]][0] if i + 1 < len(s_list) else len(body_lines)
        intro_raw_lines: list[str] = []
        verse_blocks: list[dict] = []
        cur_v: dict | None = None

        for j in range(start_idx, end_idx):
            _, raw_l = body_lines[j]
            if not raw_l.strip():
                if cur_v is None:
                    intro_raw_lines.append("")
                continue
            m_v = re.match(r"^\s{0,2}(\d+)(?:-(\d+))?\.\s+(.*)$", raw_l)
            if m_v:
                a = int(m_v.group(1))
                b = int(m_v.group(2)) if m_v.group(2) else a
                cur_v = {
                    "start": a,
                    "end": b,
                    "key": f"{a}" if a == b else f"{a}-{b}",
                    "lines": [m_v.group(3)],
                }
                verse_blocks.append(cur_v)
            else:
                if cur_v is None:
                    intro_raw_lines.append(raw_l)
                else:
                    cur_v["lines"].append(raw_l)

        title_cyr = clean_pdf_cyrillic_text(surah_starts[sid][2])
        title_lat = cyrillic_to_latin_crh(title_cyr)
        intro_paras_cyr = parse_paragraphs(intro_raw_lines)
        intro_paras_lat = [cyrillic_to_latin_crh(p) for p in intro_paras_cyr]

        # Validate coverage and clean each verse block
        expected_total = int(core_specs[sid]["total"])
        covered: list[int] = []
        cleaned_blocks = []
        for vb in verse_blocks:
            covered.extend(range(vb["start"], vb["end"] + 1))
            joined = join_pdf_lines(vb["lines"])
            cyr_txt = clean_pdf_cyrillic_text(joined, surah_id=sid, verse_key=vb["key"])
            d, neg = check_balanced_parens(cyr_txt)
            if d != 0 or neg:
                raise ValueError(f"Unbalanced parens in {sid}:{vb['key']}: depth={d}, neg={neg}")
            lat_txt = cyrillic_to_latin_crh(cyr_txt)
            cleaned_blocks.append({
                "start": vb["start"],
                "end": vb["end"],
                "key": vb["key"],
                "text_cyrl": cyr_txt,
                "text_latn": lat_txt,
            })

        if covered != list(range(1, expected_total + 1)):
            raise ValueError(f"Surah {sid} coverage mismatch: expected 1..{expected_total}, got {covered[:5]}..{covered[-5:]}")

        surahs.append({
            "id": sid,
            "title_cyrl": title_cyr,
            "title_latn": title_lat,
            "intro_cyrl": intro_paras_cyr,
            "intro_latn": intro_paras_lat,
            "blocks": cleaned_blocks,
        })

    return surahs


def parse_glossary(pages: list[str]) -> list[dict]:
    """Parse the 2-column Glossary ('Лугъат') on pages 549-561."""
    entries: list[dict] = []
    cur_section = ""
    cur_entry: dict | None = None

    for pno in range(549, 562):
        lines = strip_running_chrome(pages[pno - 1], pno)
        for ln in lines:
            if not ln.strip():
                continue
            s = ln.strip()
            if s == "Къыйын анълашылгъан базы сёзлер ве ибарелернинъ лугъаты":
                continue

            indent = len(ln) - len(ln.lstrip())
            # Letter section headers: 1-2 Cyrillic letters at col 0 (А, Б, ..., Дж, Къ, Гъ, Я)
            if indent == 0 and re.match(r"^[А-ЯЁҺ][а-яёһъ]?$", s):
                cur_section = clean_pdf_cyrillic_text(s)
                cur_entry = None
                continue

            m_split = re.match(r"^(\S+(?:\s\S+)*?)(\s{2,})(.+)$", ln)
            if m_split and indent < 6:
                col1 = m_split.group(1).strip()
                col2 = m_split.group(3).strip()
                # Check if this is a wrapped continuation of both columns (e.g. `антлашув` / `(анълашув)`)
                if (
                    cur_entry is not None
                    and col1.startswith("(")
                    and not cur_entry["def_raw"].rstrip().endswith((".", "!", "?"))
                ):
                    cur_entry["term_raw"] += " " + col1
                    cur_entry["def_raw"] += " " + col2
                else:
                    cur_entry = {
                        "section_cyrl": cur_section,
                        "term_raw": col1,
                        "def_raw": col2,
                    }
                    entries.append(cur_entry)
            elif cur_entry is not None:
                if indent >= 12:
                    cur_entry["def_raw"] += " " + s
                else:
                    cur_entry["term_raw"] += " " + s

    structured: list[dict] = []
    # Known Russian-only or trailing Russian parenthetical glosses in the 2005 Glossary
    for e in entries:
        term_cyr = clean_pdf_cyrillic_text(join_pdf_lines([e["term_raw"]]))
        def_cyr = clean_pdf_cyrillic_text(join_pdf_lines([e["def_raw"]]))
        if "(" not in def_cyr and def_cyr.rstrip(".").endswith(")"):
            def_cyr = "(" + def_cyr
        if def_cyr.strip() == "мираж":
            def_cyr = "(мираж)."
        term_lat = cyrillic_to_latin_crh(term_cyr)
        sec_lat = cyrillic_to_latin_crh(e["section_cyrl"])

        # Detect Russian glosses in parentheses (words containing ц, щ, ы after ш/ж, -ость, -ение, -ть, etc., or when entire def is `(...)`)
        ru_glosses: list[str] = []

        def _replace_paren_for_lat(m: re.Match) -> str:
            inner = m.group(1).strip()
            # Heuristic: Russian glosses in Lugat either constitute the whole definition `(засада)`
            # or use Russian infinitives/adjectives/nouns (`-ть`, `-ый`, `-ий`, `-ое`, `-ство`, `-ние`, `орбитр`, `запад`, `восток`, `проказа`, `зависть`, `кризис`, `присяга`, `мох`, `клятва`, `долина`, `чума`)
            is_entire_def = def_cyr.strip().startswith("(") and def_cyr.strip().rstrip(".").endswith(")")
            looks_ru = is_entire_def or bool(
                re.search(
                    r"(?:ть(?:ся)?|ый|ий\b(?!\s+деври)|ое|ая|ство|ства|ние|ция|орбитр|запад|восток|проказа|зависть|кризис|присяга|клятва|долина|лощина|чума|мох|уровень|ранг|взятка|мираж|река|раздор|сперма|идол|засада|залог|догадка|трон|утешение|выставка|пропасть|выкуп|уловка|группа|натура|менструация|судья|владыка|горчица|юмор|граница|удод|гнев|прозрачный|разум|врач|доктор|безопасно|схватить|особенно|прибор|заочно|животное|факт|материалист)\b",
                    inner.lower(),
                )
            )
            if looks_ru:
                ru_glosses.append(inner)
                if is_entire_def:
                    return f"[ru: {romanize_ru(inner)}]"
                return ""
            return f"({cyrillic_to_latin_crh(inner)})"

        def_lat_pre = re.sub(r"\(([^()]+)\)", _replace_paren_for_lat, def_cyr)
        def_lat = cyrillic_to_latin_crh(def_lat_pre)
        def_lat = re.sub(r"\s+([.,;:])", r"\1", re.sub(r"\s{2,}", " ", def_lat)).strip()
        def_lat = re.sub(r",\s*\.", ".", def_lat)

        structured.append({
            "section_cyrl": e["section_cyrl"],
            "section_latn": sec_lat,
            "term_cyrl": term_cyr,
            "term_latn": term_lat,
            "definition_cyrl": def_cyr,
            "definition_latn": def_lat,
            "ru_gloss": "; ".join(ru_glosses) if ru_glosses else None,
        })

    return structured


def parse_back_matter(pages: list[str]) -> list[str]:
    """Parse Khatm Dua (pp. 562-563) and Bibliography (p. 564)."""
    bm_lines: list[str] = []
    for pno in range(562, 565):
        bm_lines.extend(strip_running_chrome(pages[pno - 1], pno))

    headings = {
        "Бир хатим дуасы": "#",
        "Ана тилимизде бойле де дуа этиле билир:": "##",
        "Файдаланылгъан менбалар": "#",
    }
    return parse_paragraphs(bm_lines, headings)


def format_folded_yaml_segment(text: str, cid: int = 0) -> list[str]:
    wrapped = textwrap.wrap(
        text,
        width=80,
        break_long_words=False,
        break_on_hyphens=False,
    )
    lines = ["      - text: >"]
    for wln in wrapped:
        lines.append(f"          {wln}")
    lines.append(f"        cid: {cid}")
    return lines


def write_surah_yamls(surahs: list[dict], core_specs: dict[int, dict[str, object]]) -> None:
    CRH_YAML_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Special handling for Surah 1 (001-Al-Fatiha.yaml): preserve granular CIDs 1..9 + fix orthography + attach izaat
    s1_blocks = {b["start"]: b["text_latn"] for b in surahs[0]["blocks"]}
    # Extract parenthetical izaat from 1:7 ("Aamin! (\"Aalemiin\" - ...)")
    s1_v7_full = s1_blocks[7]
    m_s1_comm = re.search(r"(\([^\"']*«?\"?Aalemiin.+)$", s1_v7_full)
    s1_comm_seg = f" {m_s1_comm.group(1)}" if m_s1_comm else ""

    fatiha_lines = [
        "surah_id: 1",
        "language: crh",
        "author: dizen-qurtnezir",
        "verses:",
        "  - verse: 1",
        "    segments:",
        "      - text: Rahman",
        "        cid: 3",
        "      - text: ve",
        "        cid: 0",
        "      - text: rahim",
        "        cid: 4",
        "      - text: olğan",
        "        cid: 0",
        "      - text: Allahnıñ",
        "        cid: 2",
        "      - text: adınen.",
        "        cid: 1",
        "  - verse: 2",
        "    segments:",
        "      - text: Hamd",
        "        cid: 1",
        "      - text: (maqtav ve maqtalmaq)",
        "        cid: 0",
        "      - text: alemlerniñ",
        "        cid: 4",
        "      - text: Rabbi",
        "        cid: 3",
        "      - text: Allahqa aittir.",
        "        cid: 2",
        "  - verse: 3",
        "    segments:",
        "      - text: O rahmandır",
        "        cid: 1",
        "      - text: ve rahimdir.",
        "        cid: 2",
        "  - verse: 4",
        "    segments:",
        "      - text: Ceza",
        "        cid: 3",
        "      - text: kününiñ",
        "        cid: 2",
        "      - text: saibidir.",
        "        cid: 1",
        "  - verse: 5",
        "    segments:",
        "      - text: (Rabbimiz!)",
        "        cid: 0",
        "      - text: Yalıñız Saña",
        "        cid: 1",
        "      - text: qullıq etermiz",
        "        cid: 2",
        "      - text: ve yalıñız Senden",
        "        cid: 3",
        "      - text: medet ümüt etermiz.",
        "        cid: 4",
        "  - verse: 6",
        "    segments:",
        "      - text: Bizge",
        "        cid: 1",
        "      - text: doğru",
        "        cid: 3",
        "      - text: yolnı",
        "        cid: 2",
        "      - text: köster.",
        "        cid: 1",
        "  - verse: 7",
        "    segments:",
        "      - text: Özlerine",
        "        cid: 2",
        "      - text: lütf ve ikram etken",
        "        cid: 3",
        "      - text: kimseleriñniñ",
        "        cid: 4",
        "      - text: yolunı;",
        "        cid: 1",
        "      - text: ğadapqa oğrağanlarnıñ",
        "        cid: 6",
        "      - text: ve",
        "        cid: 8",
        "      - text: sapqanlarnıñ",
        "        cid: 9",
        "      - text: yolunı",
        "        cid: 7",
        "      - text: degil!",
        "        cid: 5",
    ]
    if s1_comm_seg:
        fatiha_lines.extend(format_folded_yaml_segment(s1_comm_seg.strip(), cid=0))

    (CRH_YAML_DIR / str(core_specs[1]["file"])).write_text(
        "\n".join(fatiha_lines) + "\n", encoding="utf-8"
    )

    # 2. Surahs 2..114
    for s in surahs[1:]:
        sid = s["id"]
        fname = str(core_specs[sid]["file"])
        out_lines = [
            f"surah_id: {sid}",
            "language: crh",
            "author: dizen-qurtnezir",
            "verses:",
        ]
        for b in s["blocks"]:
            start_v = b["start"]
            end_v = b["end"]
            out_lines.append(f"  - verse: {start_v}")
            out_lines.append("    segments:")
            out_lines.extend(format_folded_yaml_segment(b["text_latn"], cid=0))
            for cont_v in range(start_v + 1, end_v + 1):
                out_lines.append(f"  - verse: {cont_v}")
                out_lines.append("    segments:")
                out_lines.extend(format_folded_yaml_segment(f"[{start_v} ayetine baq.]", cid=0))

        (CRH_YAML_DIR / fname).write_text("\n".join(out_lines) + "\n", encoding="utf-8")


def write_markdown_editions(
    front_matter_cyr: list[str],
    surahs: list[dict],
    glossary: list[dict],
    back_matter_cyr: list[str],
) -> None:
    cyr_lines: list[str] = []
    lat_lines: list[str] = []

    for blk in front_matter_cyr:
        cyr_lines.append(blk)
        cyr_lines.append("")
        lat_lines.append(cyrillic_to_latin_crh(blk))
        lat_lines.append("")

    for s in surahs:
        sid = s["id"]
        cyr_lines.append(f"# {sid}. {s['title_cyrl']}")
        cyr_lines.append("")
        lat_lines.append(f"# {sid}. {s['title_latn']}")
        lat_lines.append("")

        for p_cyr, p_lat in zip(s["intro_cyrl"], s["intro_latn"]):
            cyr_lines.append(p_cyr)
            cyr_lines.append("")
            lat_lines.append(p_lat)
            lat_lines.append("")

        for b in s["blocks"]:
            sv, ev = b["start"], b["end"]
            cyr_lines.append(f"{sv}. {b['text_cyrl']}")
            lat_lines.append(f"{sv}. {b['text_latn']}")
            for cv in range(sv + 1, ev + 1):
                cyr_lines.append(f"{cv}. [{sv} аетине бакъ.]")
                lat_lines.append(f"{cv}. [{sv} ayetine baq.]")
        cyr_lines.append("")
        lat_lines.append("")

    # Glossary section
    cyr_lines.append("# Къыйын анълашылгъан базы сёзлер ве ибарелернинъ лугъаты")
    cyr_lines.append("")
    cyr_lines.append("| Сёз / Ибаре | Манасы |")
    cyr_lines.append("| :--- | :--- |")

    lat_lines.append("# Qıyın añlaşılğan bazı sözler ve ibarelerniñ luğatı")
    lat_lines.append("")
    lat_lines.append("| Söz / İbare | Manası |")
    lat_lines.append("| :--- | :--- |")

    last_sec = None
    for g in glossary:
        if g["section_cyrl"] and g["section_cyrl"] != last_sec:
            last_sec = g["section_cyrl"]
            cyr_lines.append(f"| **{g['section_cyrl']}** | |")
            lat_lines.append(f"| **{g['section_latn']}** | |")
        t_c = g["term_cyrl"].replace("|", "\\|")
        d_c = g["definition_cyrl"].replace("|", "\\|")
        t_l = g["term_latn"].replace("|", "\\|")
        d_l = g["definition_latn"].replace("|", "\\|")
        cyr_lines.append(f"| {t_c} | {d_c} |")
        lat_lines.append(f"| {t_l} | {d_l} |")

    cyr_lines.append("")
    lat_lines.append("")

    # Back matter (Khatm Dua & Bibliography — note Russian titles in Bibliography items 9-11!)
    bib_ru_overrides = {
        "9).": "9). Koran. İ.Yu.Kraçkovskiyniñ tercimesi. Moskva, 1990.",
        "10).": "10). Koran. Perevody smyslov. Valeriya Porohova-ar-Roşdniñ tercimesi. Moskva, 1991.",
        "11).": "11). Lyutsian İppolitoviç KLİMOVİÇ. Kniga o Korane. Moskva, 1986.",
    }
    for blk in back_matter_cyr:
        cyr_lines.append(blk)
        cyr_lines.append("")
        prefix = blk.split(" ", 1)[0]
        if prefix in bib_ru_overrides:
            blk_lat = bib_ru_overrides[prefix]
        else:
            blk_lat = cyrillic_to_latin_crh(blk)
        lat_lines.append(blk_lat)
        lat_lines.append("")

    CYR_MD_OUT.write_text("\n".join(cyr_lines).rstrip() + "\n", encoding="utf-8")
    LAT_MD_OUT.write_text("\n".join(lat_lines).rstrip() + "\n", encoding="utf-8")


def main() -> None:
    print(f"Extracting primary PDF: {PDF_PATH}")
    pages = extract_pdf_pages(PDF_PATH)
    print(f"  Extracted {len(pages)} pages.")

    core_specs = load_core_surah_specs()
    front_matter_cyr = parse_front_matter(pages)
    surahs = parse_surahs(pages, core_specs)
    glossary = parse_glossary(pages)
    back_matter_cyr = parse_back_matter(pages)

    merged_ranges = []
    surah_intros = []
    for s in surahs:
        surah_intros.append({
            "surah_id": s["id"],
            "title_cyrl": s["title_cyrl"],
            "title_latn": s["title_latn"],
            "intro_cyrl": s["intro_cyrl"],
            "intro_latn": s["intro_latn"],
        })
        for b in s["blocks"]:
            if b["end"] > b["start"]:
                merged_ranges.append({
                    "surah_id": s["id"],
                    "start_verse": b["start"],
                    "end_verse": b["end"],
                })

    write_surah_yamls(surahs, core_specs)
    write_markdown_editions(front_matter_cyr, surahs, glossary, back_matter_cyr)

    MERGED_META_OUT.parent.mkdir(parents=True, exist_ok=True)
    MERGED_META_OUT.write_text(
        json.dumps(
            {
                "source": "Sait Dizen & Zakir Qurtnezir, Qur'an-ı Kerim ve izaatlı manası (2nd ed., Simferopol, 2005)",
                "approval": "Qırım Musulmanları Diniy İdaresi Decision 15/10/2004",
                "merged_ranges_count": len(merged_ranges),
                "merged_ranges": merged_ranges,
                "surah_metadata": surah_intros,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    GLOSSARY_OUT.parent.mkdir(parents=True, exist_ok=True)
    GLOSSARY_OUT.write_text(
        json.dumps(
            {
                "title_cyrl": "Къыйын анълашылгъан базы сёзлер ве ибарелернинъ лугъаты",
                "title_latn": "Qıyın añlaşılğan bazı sözler ve ibarelerniñ luğatı",
                "source_pages": "549-561",
                "entry_count": len(glossary),
                "entries": glossary,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    print(f"  Rebuilt 114 Surah YAMLs in {CRH_YAML_DIR}")
    print(f"  Rebuilt {CYR_MD_OUT.name} and {LAT_MD_OUT.name}")
    print(f"  Saved {len(merged_ranges)} merged ranges to {MERGED_META_OUT.relative_to(REPO_ROOT)}")
    print(f"  Saved {len(glossary)} glossary entries to {GLOSSARY_OUT.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
