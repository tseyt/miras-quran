#!/usr/bin/env python3
"""Export Crimean Tatar (CRH) Quran translations & metadata for Tarteel QUL and Quran.com.

Generates QUL (Quranic Universal Library, https://qul.tarteel.ai) & Quran.com API v4
submission packages in both Crimean Tatar Latin (`crh-Latn`) and Cyrillic (`crh-Cyrl`):
  - exports/quran-com/metadata/language-crh.json
  - exports/quran-com/metadata/chapters-crh-latn.json
  - exports/quran-com/metadata/chapters-crh-cyrl.json
  - exports/quran-com/crh-dizen-qurtnezir-latn/{simple,translation-with-footnote-tags,translation-with-inline-footnote,grouped-verses}.json
  - exports/quran-com/crh-dizen-qurtnezir-cyrl/{simple,translation-with-footnote-tags,translation-with-inline-footnote,grouped-verses}.json
  - Optional `--sqlite <dir>`: QUL-schema `.sqlite` databases (`translations` + `foot_notes` tables)
"""

from __future__ import annotations

import argparse
import json
import re
import sqlite3
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent

CYR_MD_PATH = REPO_ROOT / "translations" / "quran-crh-dizen-qurtnezir.md"
LAT_MD_PATH = REPO_ROOT / "translations" / "quran-crh-dizen-qurtnezir-lat.md"
MERGED_META_PATH = REPO_ROOT / "src" / "data" / "translations" / "crh" / "dizen-qurtnezir-merged-ranges.json"
CORE_DIR = REPO_ROOT / "src" / "data" / "core"
DEFAULT_OUT_DIR = REPO_ROOT / "exports" / "quran-com"

# List-marker-safe matcher inside parenthetical commentary (mirrors VerseCard.jsx)
LIST_MARKER_AT_CLOSE_RE = re.compile(
    r"(?:"
    r"(?:^\s*|[:;!?]\s+|[»\"”]\.?\s+|[^\W\d_]{2,}\.\s+)[1-9]"
    r"|"
    r"(?:^\s*|[:;!?]\s+|[»\"”]\.?\s+|[^\W\d_]{2,}[.,]\s+)[abvgdeабвгде]"
    r")\)$",
    re.IGNORECASE | re.UNICODE,
)
AFTER_LIST_MARKER_RE = re.compile(r"^(?:\.\s+\S|\s+\S)")

# Localized Crimean Tatar translated meanings for all 114 Surahs (Latn, Cyrl)
SURAH_MEANINGS_CRH: dict[int, tuple[str, str]] = {
    1: ("Açış", "Ачыш"),
    2: ("Sığır", "Сыгъыр"),
    3: ("İmran ailesi", "Имран аилеси"),
    4: ("Qadınlar", "Къадынлар"),
    5: ("Sofra", "Софра"),
    6: ("En'am (Ayvanlar)", "Эн'ам (Айванлар)"),
    7: ("A'raf (Yüksek yerler)", "А'раф (Юксек ерлер)"),
    8: ("Ğanimetler", "Гъаниметлер"),
    9: ("Tövbe", "Тёвбе"),
    10: ("Yunus", "Юнус"),
    11: ("Hud", "Худ"),
    12: ("Yusuf", "Юсуф"),
    13: ("ökürüv (Kök gürültisi)", "Кёк гурюльтиси"),
    14: ("İbrahim", "Ибрахим"),
    15: ("Hicr", "Хиджр"),
    16: ("Balqurt", "Балкъурт"),
    17: ("Gece yürüşi (İsra)", "Гедже юрюши (Исра)"),
    18: ("Qoba", "Къоба"),
    19: ("Meryem", "Мерьем"),
    20: ("Ta-Ha", "Та-Ха"),
    21: ("Peyğamberler", "Пейгъамберлер"),
    22: ("Hac", "Хадж"),
    23: ("Mü'minler", "Му'минлер"),
    24: ("Nur", "Нур"),
    25: ("Furqan (Ayırıcı)", "Фуркъан (Айырыджы)"),
    26: ("Şairler", "Шаирлер"),
    27: ("Qarışqa", "Къарышкъа"),
    28: ("Qıssalar", "Къыссалар"),
    29: ("Örümçek", "Орюмчек"),
    30: ("Rumlar", "Румлар"),
    31: ("Loqman", "Локъман"),
    32: ("Secde", "Седжде"),
    33: ("Toplulıqlar (Ahzab)", "Топлулыкълар (Ахзаб)"),
    34: ("Sebe'", "Себе'"),
    35: ("Yaratıcı (Fatır)", "Яратыджы (Фатыр)"),
    36: ("Ya-Sin", "Я-Син"),
    37: ("Saf tizilgenler", "Саф тизильгенлер"),
    38: ("Sad", "Сад"),
    39: ("Zümer (Zümreler)", "Зюмер (Зюмрелер)"),
    40: ("Mü'min ( Bağışlayıcı)", "Му'мин (Багъышлайыджы)"),
    41: ("Açıqlanğan (Fussilet)", "Ачыкълангъан (Фуссилет)"),
    42: ("Şura (Meşveret)", "Шура (Мешверет)"),
    43: ("Zuhruf (Ziyynet)", "Зухруф (Зийнет)"),
    44: ("Duman", "Думан"),
    45: ("Tiz çökkenler", "Тиз чёккенлер"),
    46: ("Ahqaf (Qum töpeleri)", "Ахкъаф (Къум тёпелери)"),
    47: ("Muhammed", "Мухаммед"),
    48: ("Fetih (Ğalebe)", "Фетих (Гъалебе)"),
    49: ("Ocalar (Hucurat)", "Одалар (Худжурат)"),
    50: ("Qaf", "Къаф"),
    51: ("Savurğanlar", "Савургъанлар"),
    52: ("Tur dağı", "Тур дагъы"),
    53: ("Yıldız", "Йылдыз"),
    54: ("Ay", "Ай"),
    55: ("Rahman", "Рахман"),
    56: ("Vaqia (Qıyamet vaqiası)", "Вакъиа (Къыямет вакъиасы)"),
    57: ("Demir", "Демир"),
    58: ("Mücadele", "Муджаделе"),
    59: ("Haşr (Toplanuv)", "Хашр (Топланув)"),
    60: ("İmtian etilgen qadın", "Имтиан этильген къадын"),
    61: ("Saf", "Саф"),
    62: ("Cuma", "Джума"),
    63: ("Munafıqlar", "Мунафыкълар"),
    64: ("Aldanuvnıñ ortağa çıquvı", "Алданувнынъ ортагъа чыкъувы"),
    65: ("Talâq (Boşanuv)", "Талякъ (Бошанув)"),
    66: ("Tahrim (Aram qıluv)", "Тахрим (Арам къылув)"),
    67: ("Mülk (Akimiyet)", "Мульк (Акимиет)"),
    68: ("Qalem", "Къалем"),
    69: ("Aqiqat (Muhaqqaq kün)", "Акъикъат (Мухакъкъакъ кунь)"),
    70: ("Maaric (Yükseliş dereceleri)", "Мааридж (Юкселиш дереджелери)"),
    71: ("Nuh", "Нух"),
    72: ("Cinler", "Джинлер"),
    73: ("Örtüngen", "Орьтюнген"),
    74: ("Bürüngen", "Бюрюнген"),
    75: ("Qıyamet", "Къыямет"),
    76: ("İnsan", "Инсан"),
    77: ("Yollanılğanlar", "Ёлланылгъанлар"),
    78: ("Büyük haber", "Буюк хабер"),
    79: ("Söküp çıqarğanlar", "Сёкюп чыкъаргъанлар"),
    80: ("Qaş çattı", "Къаш чатты"),
    81: ("Türüлюв (Küneşniñ dürülüvi)", "Кюнешнинъ дюрюлюви"),
    82: ("Yarıluv", "Ярылув"),
    83: ("Ölçüde aldatqanlar", "Ольчюде алдаткъанлар"),
    84: ("Parçalanuv", "Парчаланув"),
    85: ("Burclar", "Бурджлар"),
    86: ("Gece yıldızı (Tarıq)", "Гедже йылдызы (Тарыкъ)"),
    87: ("Eñ Yüce", "Энъ Юдже"),
    88: ("Quşatqan vaqia", "Къушаткъан вакъиа"),
    89: ("Fecr (Tan)", "Феджр (Танъ)"),
    90: ("Şeer (Mekke)", "Шеэр (Мекке)"),
    91: ("Küneş", "Кунеш"),
    92: ("Gece", "Гедже"),
    93: ("Quşluq vaqtı", "Къушлукъ вакъты"),
    94: ("Ferahlıq (İnşirah)", "Ферахлыкъ (Инширах)"),
    95: ("İncir", "Инджир"),
    96: ("Alaq (Uyuşqan qan)", "Алякъ (Уюшкъан къан)"),
    97: ("Qadir gecesi", "Къадир геджеси"),
    98: ("Açıq delil", "Ачыкъ делиль"),
    99: ("Zelzele", "Зелзеле"),
    100: ("Çapqan atlar", "Чапкъан атлар"),
    101: ("Qaria (Qaqıcı qıyamet)", "Къариа (Къакъыджы къыямет)"),
    102: ("Çoqlaşuv yarışması", "Чокълашув ярышмасы"),
    103: ("Asır (Zaman)", "Асыр (Заман)"),
    104: ("Qıybetçi", "Къыйбетчи"),
    105: ("Fil", "Филь"),
    106: ("Qureyş", "Къурейш"),
    107: ("Maun (Yardım)", "Маун (Ярдым)"),
    108: ("Kevser (Bol nimet)", "Кевсер (Бол нимет)"),
    109: ("Kâfirler", "Кяфирлер"),
    110: ("Yardım (Nasr)", "Ярдым (Наср)"),
    111: ("Mesed (Örülgen yip)", "Месед (Орюльген йип)"),
    112: ("İhlâs (Samimiylik)", "Ихляс (Самимийлик)"),
    113: ("Felâq (Tan aydınlığı)", "Фелякъ (Танъ айдынлыгъы)"),
    114: ("İnsanlar", "Инсанлар"),
}
# Fix clean capitalization on 13, 40, 49, 81
SURAH_MEANINGS_CRH[13] = ("Kök gürültisi (Ra'd)", "Кок гурюльтиси (Ра'д)")
SURAH_MEANINGS_CRH[40] = ("Mü'min (Bağışlayıcı)", "Му'мин (Багъышлайыджы)")
SURAH_MEANINGS_CRH[49] = ("Odalar (Hucurat)", "Одалар (Худжурат)")
SURAH_MEANINGS_CRH[81] = ("Küneşniñ dürülüvi (Tekvir)", "Кунешнинъ дюрюлюви (Теквир)")


def is_list_marker_close(text: str, open_idx: int, close_idx: int) -> bool:
    if close_idx <= open_idx + 3 and text[open_idx + 1 : close_idx].strip().lower() in (
        "a", "b", "v", "g", "d", "e", "а", "б", "в", "г", "д", "е", "1", "2", "3",
    ):
        rest = text[close_idx + 1 :]
        if re.search(r"(?:[:;.!?]\s+|[»\"”]\.?\s+)[bvgd2бвгд]\)", rest, re.IGNORECASE):
            return True
        return False
    prefix = text[open_idx + 1 : close_idx + 1]
    suffix = text[close_idx + 1 :]
    return bool(LIST_MARKER_AT_CLOSE_RE.search(prefix) and AFTER_LIST_MARKER_RE.match(suffix))


def split_verse_and_footnotes(
    text: str,
    next_fn_id: int,
    min_footnote_words: int = 7,
) -> tuple[str, str, str, dict[str, str], int]:
    """Return (simple_text, tagged_text, inline_fn_text, footnotes_dict, updated_next_fn_id)."""
    simple_parts: list[str] = []
    tagged_parts: list[str] = []
    inline_parts: list[str] = []
    footnotes: dict[str, str] = {}
    local_fn_num = 0
    i = 0
    n = len(text)

    while i < n:
        open_idx = text.find("(", i)
        if open_idx == -1:
            tail = text[i:]
            simple_parts.append(tail)
            tagged_parts.append(tail)
            inline_parts.append(tail)
            break

        if open_idx > i:
            seg = text[i:open_idx]
            simple_parts.append(seg)
            tagged_parts.append(seg)
            inline_parts.append(seg)

        depth = 1
        close_idx = open_idx + 1
        while close_idx < n and depth > 0:
            ch = text[close_idx]
            if ch == "(":
                depth += 1
            elif ch == ")" and not is_list_marker_close(text, open_idx, close_idx):
                depth -= 1
            close_idx += 1

        if depth != 0:
            raise ValueError(f"Unbalanced parentheses in verse text: {text[open_idx:open_idx+80]!r}")

        inner = text[open_idx + 1 : close_idx - 1].strip()
        attached_to_stem = open_idx > 0 and text[open_idx - 1].isalpha()
        word_count = len(inner.split())

        if not attached_to_stem and word_count >= min_footnote_words:
            # Extract as structured QUL footnote
            fn_id_str = str(next_fn_id)
            next_fn_id += 1
            local_fn_num += 1
            fn_clean = inner if inner.endswith((".", "!", "?", "»", '"')) else inner + "."
            footnotes[fn_id_str] = fn_clean

            # Check if a period immediately follows `)` in `(commentary).`
            has_trailing_dot = close_idx < n and text[close_idx] == "."
            prev_joined = "".join(simple_parts).rstrip()
            prev_already_ended = prev_joined.endswith((".", "!", "?", "»", '"'))

            # Trim trailing space before footnote tag
            if tagged_parts and tagged_parts[-1].endswith(" "):
                tagged_parts[-1] = tagged_parts[-1].rstrip(" ")

            if has_trailing_dot:
                close_idx += 1
                if not prev_already_ended:
                    if simple_parts and simple_parts[-1].endswith(" "):
                        simple_parts[-1] = simple_parts[-1].rstrip(" ")
                    simple_parts.append(".")
                    tagged_parts.append(f".<sup foot_note=\"{fn_id_str}\">{local_fn_num}</sup>")
                    inline_parts.append(f". [[{fn_clean}]]")
                else:
                    tagged_parts.append(f"<sup foot_note=\"{fn_id_str}\">{local_fn_num}</sup>")
                    inline_parts.append(f" [[{fn_clean}]]")
            else:
                tagged_parts.append(f"<sup foot_note=\"{fn_id_str}\">{local_fn_num}</sup>")
                inline_parts.append(f" [[{fn_clean}]]")
        else:
            raw_paren = text[open_idx:close_idx]
            simple_parts.append(raw_paren)
            tagged_parts.append(raw_paren)
            inline_parts.append(raw_paren)

        i = close_idx

    def _tidy(s: str) -> str:
        s = re.sub(r"\s+([.,;:!?])", r"\1", s)
        s = re.sub(r"\s{2,}", " ", s)
        return s.strip()

    return (
        _tidy("".join(simple_parts)),
        _tidy("".join(tagged_parts)),
        _tidy("".join(inline_parts)),
        footnotes,
        next_fn_id,
    )


def parse_markdown_surah_verses(md_path: Path) -> dict[int, dict[int, str]]:
    """Parse canonical `# <id>. <TITLE>` and `<v>. <text>` lines from rebuilt Markdown."""
    surah_verses: dict[int, dict[int, str]] = {}
    cur_sid: int | None = None
    for raw_ln in md_path.read_text(encoding="utf-8").splitlines():
        m_h = re.match(r"^#\s+(\d+)\.\s+(.+)$", raw_ln)
        if m_h:
            cur_sid = int(m_h.group(1))
            surah_verses[cur_sid] = {}
            continue
        if cur_sid is not None and raw_ln.startswith("# "):
            # Reached Glossary / Back matter after Surah 114
            cur_sid = None
            continue
        if cur_sid is not None:
            m_v = re.match(r"^(\d+)\.\s+(.+)$", raw_ln)
            if m_v:
                vnum = int(m_v.group(1))
                surah_verses[cur_sid][vnum] = m_v.group(2).strip()
    assert len(surah_verses) == 114, f"Expected 114 surahs in {md_path.name}, got {len(surah_verses)}"
    return surah_verses


def load_core_metadata() -> dict[int, dict[str, object]]:
    meta: dict[int, dict[str, object]] = {}
    for p in sorted(CORE_DIR.glob("*.yaml")):
        txt = p.read_text(encoding="utf-8")
        sid = int(re.search(r"^id:\s*(\d+)", txt, re.M).group(1))
        title_en_tr = re.search(r'^title:\s*"?([^"\n]+)"?', txt, re.M).group(1).strip()
        english = re.search(r'^english:\s*"?([^"\n]+)"?', txt, re.M).group(1).strip()
        rev_type = re.search(r"^type:\s*(\S+)", txt, re.M).group(1).strip()
        total = int(re.search(r"^total_verses:\s*(\d+)", txt, re.M).group(1))
        meta[sid] = {
            "id": sid,
            "name_arabic_translit": title_en_tr,
            "english_meaning": english,
            "revelation_place": "makkah" if rev_type.lower().startswith("mak") else "madinah",
            "verses_count": total,
        }
    assert len(meta) == 114
    return meta


def normalize_display_title(orthoepic_title: str, is_cyrl: bool) -> str:
    """Convert all-caps tajwid header like 'el-FAATİhA' / 'AAL-İ İMRAAN' to clean Title Case."""
    def _tc_word(word: str) -> str:
        parts = word.split("-", 1)
        if len(parts) == 2 and parts[0].islower():
            prefix, main = parts[0], parts[1]
            return f"{prefix}-{_tc_word(main)}"
        if len(parts) == 2 and len(parts[1]) == 1:
            return f"{_tc_word(parts[0])}-{parts[1].lower()}"
        if is_cyrl:
            return word[:1].upper() + word[1:].lower()
        first = "İ" if word[:1] == "i" else word[:1].upper()
        rest = word[1:].replace("İ", "i").replace("I", "ı").lower()
        return first + rest

    return " ".join(_tc_word(tok) for tok in orthoepic_title.split())


def build_edition_exports(
    surah_verses: dict[int, dict[int, str]],
    core_meta: dict[int, dict[str, object]],
    merged_lookup: dict[tuple[int, int], int],
    continuation_of: dict[tuple[int, int], int],
    is_cyrl: bool,
    repeat_merged: bool = False,
) -> dict[str, object]:
    simple_map: dict[str, str] = {}
    tagged_map: dict[str, dict[str, object]] = {}
    inline_map: dict[str, str] = {}
    grouped_units: list[dict[str, object]] = []

    next_fn_id = 10001
    fn_total = 0

    for sid in range(1, 115):
        vcount = int(core_meta[sid]["verses_count"])
        vdict = surah_verses[sid]
        assert len(vdict) == vcount, f"Surah {sid} count mismatch: {len(vdict)} != {vcount}"

        # Precompute split result for each primary verse (non-continuation)
        primary_cache: dict[int, tuple[str, str, str, dict[str, str]]] = {}
        for v in range(1, vcount + 1):
            if (sid, v) in continuation_of:
                continue
            raw_txt = vdict[v]
            s_txt, t_txt, i_txt, fns, next_fn_id = split_verse_and_footnotes(raw_txt, next_fn_id)
            fn_total += len(fns)
            primary_cache[v] = (s_txt, t_txt, i_txt, fns)

            end_v = merged_lookup.get((sid, v), v)
            ayah_keys = [f"{sid}:{k}" for k in range(v, end_v + 1)]
            unit: dict[str, object] = {
                "from": f"{sid}:{v}",
                "to": f"{sid}:{end_v}",
                "is_grouped": end_v > v,
                "ayah_keys": ayah_keys,
                "text_simple": s_txt,
                "text_with_footnotes": t_txt,
            }
            if fns:
                unit["footnotes"] = fns
            grouped_units.append(unit)

        for v in range(1, vcount + 1):
            key = f"{sid}:{v}"
            if (sid, v) in continuation_of:
                start_v = continuation_of[(sid, v)]
                if repeat_merged:
                    s_txt, t_txt, i_txt, fns = primary_cache[start_v]
                    simple_map[key] = s_txt
                    tagged_map[key] = {"t": t_txt, **({"f": fns} if fns else {})}
                    inline_map[key] = i_txt
                else:
                    xref = (
                        f"[{sid}:{start_v} аетине бакъынъыз]"
                        if is_cyrl
                        else f"[{sid}:{start_v} ayetine baqıñız]"
                    )
                    simple_map[key] = xref
                    tagged_map[key] = {"t": xref}
                    inline_map[key] = xref
            else:
                s_txt, t_txt, i_txt, fns = primary_cache[v]
                simple_map[key] = s_txt
                tagged_map[key] = {"t": t_txt, **({"f": fns} if fns else {})}
                inline_map[key] = i_txt

    return {
        "simple": simple_map,
        "tagged": tagged_map,
        "inline": inline_map,
        "grouped": {
            "total_units": len(grouped_units),
            "grouped_ranges_count": sum(1 for u in grouped_units if u["is_grouped"]),
            "total_footnotes_count": fn_total,
            "units": grouped_units,
        },
    }


def write_qul_sqlite(db_path: Path, tagged_map: dict[str, dict[str, object]]) -> None:
    if db_path.exists():
        db_path.unlink()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    try:
        cur = conn.cursor()
        cur.execute(
            "CREATE TABLE translations ("
            "sura INTEGER NOT NULL, "
            "ayah INTEGER NOT NULL, "
            "ayah_key TEXT PRIMARY KEY, "
            "text TEXT NOT NULL)"
        )
        cur.execute(
            "CREATE TABLE foot_notes ("
            "id INTEGER PRIMARY KEY, "
            "ayah_key TEXT NOT NULL, "
            "text TEXT NOT NULL)"
        )
        for ayah_key, payload in tagged_map.items():
            sura_s, ayah_s = ayah_key.split(":")
            cur.execute(
                "INSERT INTO translations (sura, ayah, ayah_key, text) VALUES (?, ?, ?, ?)",
                (int(sura_s), int(ayah_s), ayah_key, str(payload["t"])),
            )
            fns = payload.get("f") or {}
            if isinstance(fns, dict):
                for fn_id, fn_txt in fns.items():
                    cur.execute(
                        "INSERT INTO foot_notes (id, ayah_key, text) VALUES (?, ?, ?)",
                        (int(fn_id), ayah_key, str(fn_txt)),
                    )
        conn.commit()
    finally:
        conn.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Export CRH Quran datasets for QUL / Quran.com")
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--repeat-merged", action="store_true", help="Repeat combined text on continuation verses")
    parser.add_argument("--sqlite", type=Path, default=None, help="Optional directory to emit QUL .sqlite databases")
    args = parser.parse_args()

    merged_meta = json.loads(MERGED_META_PATH.read_text(encoding="utf-8"))
    merged_lookup: dict[tuple[int, int], int] = {}
    continuation_of: dict[tuple[int, int], int] = {}
    for mr in merged_meta["merged_ranges"]:
        sid, sv, ev = int(mr["surah_id"]), int(mr["start_verse"]), int(mr["end_verse"])
        merged_lookup[(sid, sv)] = ev
        for cv in range(sv + 1, ev + 1):
            continuation_of[(sid, cv)] = sv

    surah_intros_by_id = {int(s["surah_id"]): s for s in merged_meta["surah_metadata"]}
    core_meta = load_core_metadata()
    lat_verses = parse_markdown_surah_verses(LAT_MD_PATH)
    cyr_verses = parse_markdown_surah_verses(CYR_MD_PATH)

    out_dir: Path = args.out_dir
    meta_dir = out_dir / "metadata"
    lat_dir = out_dir / "crh-dizen-qurtnezir-latn"
    cyr_dir = out_dir / "crh-dizen-qurtnezir-cyrl"
    for d in (meta_dir, lat_dir, cyr_dir):
        d.mkdir(parents=True, exist_ok=True)

    # 1. Language & resource metadata
    language_json = {
        "iso_code": "crh",
        "bcp47_tags": ["crh", "crh-Latn", "crh-Cyrl"],
        "name": "Crimean Tatar",
        "native_name": "Qırımtatarca",
        "native_name_cyrl": "Къырымтатарджа",
        "direction": "ltr",
        "default_script": "Latn",
        "es_analyzer_default": "turkish",
        "resources": [
            {
                "slug": "crh-dizen-qurtnezir-latn",
                "name": "Sait Dizen & Zakir Qurtnezir (Latin)",
                "author_name": "Sait Dizen, Zakir Qurtnezir",
                "language_iso_code": "crh",
                "script": "Latn",
                "source_book": "Qur'an-ı Kerim ve izaatlı manası (2-ci neşiri, Aqmescit / Simferopol, 2005)",
                "institutional_approval": "Qırım Musulmanları Diniy İdaresi (Muftiyat) Decision 15/10/2004",
            },
            {
                "slug": "crh-dizen-qurtnezir-cyrl",
                "name": "Саит Дизен ве Закир Къуртнезир (Кирилл)",
                "author_name": "Саит Дизен, Закир Къуртнезир",
                "language_iso_code": "crh",
                "script": "Cyrl",
                "source_book": "Къур'ан-ы Керим ве изаатлы манасы (2-джи нешири, Акъмесджит / Симферополь, 2005)",
                "institutional_approval": "Къырым Мусульманлары Диний Идареси (Муфтият) 15/10/2004 къарары",
            },
        ],
    }
    (meta_dir / "language-crh.json").write_text(
        json.dumps(language_json, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    # 2. Localized 114 Chapter / Surah metadata (Latn & Cyrl)
    chapters_latn = []
    chapters_cyrl = []
    for sid in range(1, 115):
        c = core_meta[sid]
        intro_entry = surah_intros_by_id[sid]
        meaning_lat, meaning_cyr = SURAH_MEANINGS_CRH[sid]
        rev_lat = "Mekke" if c["revelation_place"] == "makkah" else "Medine"
        rev_cyr = "Мекке" if c["revelation_place"] == "makkah" else "Медине"

        chapters_latn.append({
            "id": sid,
            "revelation_place": c["revelation_place"],
            "revelation_place_crh": rev_lat,
            "verses_count": c["verses_count"],
            "name_crh": normalize_display_title(intro_entry["title_latn"], is_cyrl=False),
            "name_orthoepic": intro_entry["title_latn"],
            "translated_name": {
                "language_name": "crimean tatar",
                "name": meaning_lat,
            },
            "surah_intro": " ".join(intro_entry["intro_latn"]),
        })
        chapters_cyrl.append({
            "id": sid,
            "revelation_place": c["revelation_place"],
            "revelation_place_crh": rev_cyr,
            "verses_count": c["verses_count"],
            "name_crh": normalize_display_title(intro_entry["title_cyrl"], is_cyrl=True),
            "name_orthoepic": intro_entry["title_cyrl"],
            "translated_name": {
                "language_name": "crimean tatar",
                "name": meaning_cyr,
            },
            "surah_intro": " ".join(intro_entry["intro_cyrl"]),
        })

    (meta_dir / "chapters-crh-latn.json").write_text(
        json.dumps(chapters_latn, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (meta_dir / "chapters-crh-cyrl.json").write_text(
        json.dumps(chapters_cyrl, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    # 3. Build & write QUL JSON files for Latn and Cyrl
    lat_exports = build_edition_exports(
        lat_verses, core_meta, merged_lookup, continuation_of, is_cyrl=False, repeat_merged=args.repeat_merged
    )
    cyr_exports = build_edition_exports(
        cyr_verses, core_meta, merged_lookup, continuation_of, is_cyrl=True, repeat_merged=args.repeat_merged
    )

    for target_dir, bundle in ((lat_dir, lat_exports), (cyr_dir, cyr_exports)):
        (target_dir / "simple.json").write_text(
            json.dumps(bundle["simple"], ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        (target_dir / "translation-with-footnote-tags.json").write_text(
            json.dumps(bundle["tagged"], ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        (target_dir / "translation-with-inline-footnote.json").write_text(
            json.dumps(bundle["inline"], ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        (target_dir / "grouped-verses.json").write_text(
            json.dumps(bundle["grouped"], ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

    if args.sqlite is not None:
        write_qul_sqlite(args.sqlite / "crh-dizen-qurtnezir-latn.sqlite", lat_exports["tagged"])
        write_qul_sqlite(args.sqlite / "crh-dizen-qurtnezir-cyrl.sqlite", cyr_exports["tagged"])
        print(f"  Generated QUL SQLite databases in {args.sqlite}")

    print(
        f"Exported QUL / Quran.com CRH packages to {out_dir}:\n"
        f"  - Latn: {len(lat_exports['simple'])} verses, "
        f"{lat_exports['grouped']['total_footnotes_count']} footnotes, "
        f"{lat_exports['grouped']['grouped_ranges_count']} grouped ranges\n"
        f"  - Cyrl: {len(cyr_exports['simple'])} verses, "
        f"{cyr_exports['grouped']['total_footnotes_count']} footnotes, "
        f"{cyr_exports['grouped']['grouped_ranges_count']} grouped ranges"
    )


if __name__ == "__main__":
    main()
