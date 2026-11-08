#!/usr/bin/env python3
"""ContextID (CID) Concept Alignment Pipeline for Crimean Tatar (CRH) & Turkish (TR) Quran Translations.

Maps full-verse literary translations in:
  - `src/data/translations/crh/dizen-qurtnezir/*.yaml` (Crimean Tatar — Dizen & Qurtnezir)
  - `src/data/translations/tr/diyanet/*.yaml` (Turkish — Diyanet İşleri Başkanlığı)
  - `src/data/translations/tr/elmalili/*.yaml` (Turkish — Elmalılı Hamdi Yazır)
to the word-level Arabic Concept IDs (`cid: 1..K`) defined in `src/data/core/*.yaml`.

Architecture & Invariants:
  1. 100% Text & Commentary Preservation:
     - Rejoining `segments` with spaces yields the exact original verse text.
     - All balanced parenthetical commentary blocks `(...)` (list-marker safe via `is_list_marker_close`)
       remain atomic segments with `cid: 0`.
     - Cross-reference notes (`[X ayetine baq.]`) and `merged_into` metadata are preserved intact.
  2. Multi-Signal Turkic SOV Alignment:
     - Combines Quran.com API v4 Turkish word-by-word (`wbw`) glosses (with automatic preposition+noun
       and English-fallback repair across all 77,429 Arabic words),
     - Vowel-harmony & geminate-normalized Turkic stem matching + CRH<->TR phonological correspondences,
     - Corpus-wide IBM Model 1 / smoothed Dice lexical association trained across all 6,236 verses,
     - Two-stage anchor disambiguation (unique lexical anchors first, then repeated stems resolved via
       syntactic neighbor concept adjacency),
     - Merged-range competitive alignment across multi-ayah translation blocks (`a..b`), projecting
       only verse `v`'s concepts onto verse `v` and setting other verses' clauses to `cid: 0`.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from pathlib import Path
import re
import sys
import textwrap
import time
import urllib.request
import yaml

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

from export_quran_com import is_list_marker_close

CORE_DIR = REPO_ROOT / "src" / "data" / "core"
TRANS_ROOT = REPO_ROOT / "src" / "data" / "translations"
MERGED_RANGES_CRH_PATH = TRANS_ROOT / "crh" / "dizen-qurtnezir-merged-ranges.json"
API_BASE = "https://api.quran.com/api/v4"

AR_PAUSE_RE = re.compile(r"[\u06D6-\u06ED\u0640\s]+")
CROSS_REF_RE = re.compile(r"^\[[\d,\-\s]+ayet(?:ine|lerine)\s+baq\.\]$", re.I)

AR_PARTICLES = {
    "فِى", "مِن", "مِّن", "مِنَ", "مِّنَ", "مِنۢ", "مِّنۢ",
    "إِلَى", "إِلَىٰ", "عَلَى", "عَلَىٰ", "عَن", "عَنِ",
    "لَا", "مَا", "لَمْ", "لَن", "إِن", "إِنَّ", "أَن", "أَنَّ",
    "بِ", "لِ", "كَ", "وَ", "فَ", "أَوْ", "أَمْ", "حَتَّىٰ",
    "إِلَّا", "غَيْرِ", "دُونِ", "بَيْنَ", "عِندَ", "لَدُن",
    "فَوْقَ", "تَحْتَ", "خَلْفَ", "وَرَآءَ", "حَوْلَ", "مَعَ",
}

EN_TO_TR_FALLBACK = {
    "the earth": "yer yeryüzü arz",
    "before": "önce evvel",
    "after": "sonra ardından",
    "your lord": "rabbin rabbiniz",
    "believe": "inanırlar iman ederler",
    "those who": "onlar ki kimseler olanlar",
    "before you": "senden önce sizden önce",
    "that": "bu şu o",
    "what": "ne şey",
    "the people": "insanlar kavim halk",
    "before them": "onlardan önce kendilerinden önce",
    "this": "bu",
    "the book": "kitap",
    "the heaven": "gök sema",
    "be": "ol olur olun",
    "their lord": "rableri",
    "his people": "kavmi",
    "they believe": "inanırlar iman ederler",
    "is": "dir vardır",
    "after them": "onlardan sonra arkalarından",
    "from": "den dan",
    "his lord": "rabbi",
    "(were) before them": "onlardan önce",
    "before it": "ondan önce",
    "they": "onlar",
    "after him": "ondan sonra",
    "(the) people": "insanlar ehli kavim",
    "(the) day": "gün",
    "they say": "derler dediler",
    "they said": "dediler",
    "you say": "dersiniz",
    "for you": "sizin için sana",
    "if": "eğer şayet",
}

CRH_TO_TR_LEX = {
    "olar": "onlar",
    "olarnıñ": "onların",
    "olarğa": "onlara",
    "olarnı": "onları",
    "olardan": "onlardan",
    "olardır": "onlardır bunlardır",
    "oña": "ona kendisine",
    "onıñ": "onun",
    "onı": "onu",
    "onda": "onda kendisinde içinde",
    "ondan": "ondan",
    "bular": "bunlar",
    "bularnıñ": "bunların",
    "buña": "buna",
    "bunı": "bunu",
    "bunda": "bunda",
    "men": "ben",
    "meni": "beni",
    "maña": "bana",
    "menden": "benden",
    "menim": "benim",
    "saña": "sana",
    "seniñ": "senin",
    "bizni": "bizi",
    "bizge": "bize",
    "sizni": "sizi",
    "sizge": "size",
    "siziñ": "sizin",
    "öz": "kendi",
    "özü": "kendisi",
    "özüne": "kendisine",
    "özleri": "kendileri",
    "özlerine": "kendilerine",
    "özlerini": "kendilerini",
    "özlerinden": "kendilerinden",
    "episi": "hepsi tümü",
    "ep": "hep bütün",
    "epbir": "eşit bir",
    "epbirdir": "eşittir birdir",
    "er": "her",
    "yalıñız": "yalnız ancak sadece",
    "tek": "yalnız tek",
    "endi": "artık şimdi",
    "endiden": "artık şimdiden",
    "soñ": "son sonra",
    "soñra": "sonra",
    "evel": "önce evvel",
    "evelâ": "önce evvela",
    "arqasında": "arkasında",
    "aldında": "önünde katında",
    "ögünde": "önünde",
    "astında": "altında",
    "tübünde": "altında",
    "üstünde": "üstünde üzerinde",
    "işte": "işte",
    "mına": "işte",
    "eger": "eğer",
    "lâkin": "fakat lakin ama ancak",
    "amma": "ama fakat",
    "çünki": "çünkü zira",
    "kene": "yine",
    "daa": "daha",
    "pek": "çok pek",
    "çoq": "çok",
    "az": "az",
    "büyük": "büyük",
    "ulu": "büyük ulu yüce",
    "kiçik": "küçük",
    "qadın": "kadın eş",
    "apai": "kadın eş",
    "aqay": "erkek koca",
    "bala": "çocuk evlat oğul",
    "evlât": "evlat çocuk",
    "ana": "ana anne",
    "baba": "baba ata",
    "qardaş": "kardeş",
    "qavım": "kavim topluluk halk",
    "qul": "kul köle",
    "qullıq": "kulluk ibadet",
    "peyğamber": "peygamber elçi resul",
    "elçi": "elçi peygamber",
    "kün": "gün",
    "küneş": "güneş",
    "gece": "gece",
    "kök": "gök sema",
    "yer": "yer yeryüzü arz",
    "suv": "su",
    "tağ": "dağ",
    "dağ": "dağ",
    "ateş": "ateş",
    "nar": "ateş",
    "cennet": "cennet bahçe",
    "ceennem": "cehennem ateş",
    "ahiret": "ahiret",
    "dünya": "dünya",
    "qıyamet": "kıyamet",
    "ceza": "ceza din karşılık",
    "azap": "azap",
    "rahmet": "rahmet merhamet",
    "nimet": "nimet",
    "hikmet": "hikmet",
    "kitap": "kitap",
    "ayet": "ayet",
    "sure": "sure",
    "aqıl": "akıl",
    "qalp": "kalp gönül",
    "yürek": "kalp yürek",
    "köz": "göz",
    "qulaq": "kulak",
    "qol": "el kol",
    "el": "el",
    "ayaq": "ayak",
    "baş": "baş",
    "yüz": "yüz",
    "bet": "yüz",
    "til": "dil lisan",
    "söz": "söz kelam",
    "qan": "kan",
    "can": "can nefis ruh",
    "nefis": "nefis can kendi",
    "ölü": "ölü",
    "ölüm": "ölüm",
    "tiri": "diri canlı hayy",
    "bar": "var vardır",
    "yoq": "yok yoktur değil",
    "degil": "değil yok",
    "saip": "sahip malik",
    "saibi": "sahibi maliki",
    "yol": "yol sırat",
    "doğru": "doğru hak",
    "toğru": "doğru",
    "aq": "hak gerçek doğru",
    "haq": "hak gerçek",
    "aqiqat": "hakikat gerçek",
    "kerçek": "gerçek hak",
    "yalan": "yalan",
    "şübe": "şüphe kuşku",
    "şek": "şüphe şek",
    "ğayb": "gayb gizli",
    "namaz": "namaz salat",
    "zekât": "zekat sadaka",
    "mal": "mal rızık servet",
    "mallarımızdan": "rızıklandırdığımız verdiğimiz rızıktan",
    "rızıq": "rızık",
    "arcla": "harcama infak sarfet",
    "arclarlar": "infak ederler sarfederler harcarlar",
    "qorq": "kork sakın",
    "qorqut": "uyar korkut",
    "saqın": "sakın koru muttaki",
    "muttaqiy": "müttaki sakınan",
    "muttaqiyler": "müttakiler sakınanlar",
    "kâfir": "kafir inkar eden",
    "inkâr": "inkar",
    "mümin": "mümin inanan",
    "iman": "iman inan",
    "inan": "inan iman",
    "kesenkes": "kesinlikle şüphesiz",
    "muhaqqaq": "muhakkak şüphesiz elbette",
    "elbette": "elbette şüphesiz",
    "asla": "asla hiç",
    "qurtulış": "kurtuluş felah saadet umduklarına",
    "qurtulışqa": "kurtuluşa saadete umduklarına",
    "iriş": "eriş ulaş eren",
    "irişkenler": "erenler erişenler",
    "köster": "göster ilet hidayet",
    "kösterici": "gösterici rehber hidayet",
    "endiril": "indiril",
    "endir": "indir",
    "ber": "ver",
    "al": "al",
    "kel": "gel",
    "ket": "git",
    "kör": "gör bak",
    "işit": "işit duy",
    "eşit": "işit duy",
    "bil": "bil",
    "añla": "anla aklet",
    "tüşün": "düşün",
    "ayt": "de söyle",
    "söyle": "söyle de",
    "sora": "sor iste",
    "tile": "dile iste",
    "iste": "iste dile",
    "ümüt": "ümit umut iste",
    "medet": "yardım medet",
    "yardım": "yardım",
    "lütf": "lütuf nimet ihsan",
    "ikram": "ikram nimet",
    "ğadap": "gazap öfke",
    "sap": "sap şaş",
    "sapqan": "sapmış sapan",
    "müürle": "mühürle",
    "müurle": "mühürle",
    "müurlegen": "mühürlemiştir",
    "müürlegen": "mühürlemiştir",
    "müur": "mühür",
    "perde": "perde örtü",
    "çek": "çek koy",
    "çeşit": "çeşit türlü",
    "eyi": "iyi güzel salih",
    "yahşı": "iyi güzel",
    "fena": "kötü fena",
    "yaman": "kötü fena",
    "yazıqlar": "vay haline yazıklar",
    "yazıq": "vay yazık",
}

TR_SYNONYM_MAP = {
    "sakınanlara": "müttakiler korunanlar",
    "sakınanlar": "müttakiler",
    "sarfederler": "infak harcarlar",
    "saadete": "umduklarına kurtuluşa felaha",
    "erişenler": "erenler",
    "bunlardır": "onlardır",
    "birdir": "eşittir",
    "tanrı": "ilah",
    "peygamber": "resul elçi nebi",
    "elçi": "resul peygamber",
    "buyurdu": "dedi söyledi",
    "buyurdular": "dediler",
    "yarattı": "var etti",
    "yoktur": "değil yok",
    "onda": "kendisinde içinde",
    "yazıklar": "vay haline",
}

AUX_POST = {
    "et", "eter", "eterler", "etermiz", "etmez", "etmezler", "etti", "ettiler", "etken", "etici", "etmek",
    "eder", "ederler", "ederiz", "eden", "edenler",
    "ol", "olur", "olurlar", "oldı", "oldu", "olğan", "olan", "olğanlar", "olanlar", "olmaq", "olmak", "olun", "olsun",
    "qıl", "qılar", "qılarlar", "qıldı", "kıl", "kılar", "kılarlar", "kıldı",
    "eyle", "eyler", "eyledi", "bulun", "bulunur", "bulunğan",
    "ait", "aittir", "mahsus", "mahsustur", "dair", "dairdir",
    "içün", "için", "kibi", "gibi", "qadar", "kadar", "üzre", "üzere", "üzerindedirler", "üzerinedir",
    "qarşı", "karşı", "doğru", "beraber", "birlikte",
}

AUX_DEFER_LEFT = {
    "et", "eter", "eterler", "etermiz", "etti", "ettiler", "etken", "etkenler", "etici", "etmek",
    "eder", "ederler", "ederiz", "eden", "edenler", "edici",
    "ol", "olur", "olurlar", "oldı", "oldu", "olun", "olsun", "olmaq", "olmak",
    "eyle", "eyler", "eyledi", "bulun", "bulunur", "bulunğan",
    "ait", "aittir", "mahsus", "mahsustur", "dair", "dairdir",
    "içün", "için", "kibi", "gibi", "qadar", "kadar", "üzre", "üzere",
}

PRE_MODIFIERS = {
    "yalıñız", "yalnız", "ancaq", "ancak", "sadece", "tek",
    "bir", "bu", "şu", "o", "er", "her", "ep", "hep", "bütün", "tüm",
    "pek", "çoq", "çok", "daa", "daha", "eñ", "en",
}

GENITIVE_PRONOUNS = {
    "menim", "benim", "seniñ", "senin", "onıñ", "onun",
    "bizim", "siziñ", "sizin", "olarnıñ", "onların",
}


def clean_ar(ar_str: str) -> str:
    return AR_PAUSE_RE.sub("", ar_str).strip()


def norm_harmony(w: str, is_crh: bool = False) -> str:
    s = w.lower()
    s = re.sub(r"[^\w]", "", s, flags=re.UNICODE)
    s = (
        s.replace("â", "a")
        .replace("î", "i")
        .replace("û", "u")
        .replace("ê", "e")
        .replace("ô", "o")
        .replace("ı", "i")
        .replace("ü", "u")
        .replace("ö", "o")
        .replace("ğ", "g")
        .replace("ñ", "n")
        .replace("q", "k")
    )
    if is_crh:
        if s.startswith("k") and len(s) >= 3 and s[1] in "uo":
            s = "g" + s[1:]
        elif s.startswith("b") and (s in ("bar", "bardir") or s.startswith("ber")):
            s = "v" + s[1:]
    s = re.sub(r"(.)\1+", r"\1", s)
    return s


def get_rich_stems(w: str, is_crh: bool = False) -> set[str]:
    raw_clean = re.sub(r"[^\w]", "", w.lower(), flags=re.UNICODE)
    nh = norm_harmony(w, is_crh=is_crh)
    if not nh:
        return set()
    stems = {nh, raw_clean}
    for length in (3, 4, 5, 6, 7):
        if len(nh) >= length:
            stems.add(nh[:length])
    lex_map = CRH_TO_TR_LEX if is_crh else TR_SYNONYM_MAP
    for k, v in lex_map.items():
        if raw_clean == k or (len(k) >= 4 and raw_clean.startswith(k)):
            for eq in v.split():
                nh_eq = norm_harmony(eq, is_crh=False)
                stems.add(nh_eq)
                for l2 in (3, 4, 5, 6):
                    if len(nh_eq) >= l2:
                        stems.add(nh_eq[:l2])
    if raw_clean in TR_SYNONYM_MAP:
        for eq in TR_SYNONYM_MAP[raw_clean].split():
            nh_eq = norm_harmony(eq, is_crh=False)
            stems.add(nh_eq)
            for l2 in (3, 4, 5, 6):
                if len(nh_eq) >= l2:
                    stems.add(nh_eq[:l2])
    return stems


def is_negated_verb(w: str) -> bool:
    rc = re.sub(r"[^\w]", "", w.lower(), flags=re.UNICODE)
    return bool(
        re.search(
            r"(?:ma|me)(?:z|zler|sın|sin|san|sen|sañ|señ|dı|di|du|dü|mış|miş|yıp|yip|yarak|yerek|mak|mek|maq|ñız|niz)$",
            rc,
        )
    )


def tokenize_preserving_parens(text: str) -> list[tuple[str, bool]]:
    """Split verse text into [(token_str, is_paren_commentary), ...] preserving exact text when joined by space."""
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return []
    tokens: list[tuple[str, bool]] = []
    i = 0
    n = len(text)
    while i < n:
        open_idx = text.find("(", i)
        if open_idx == -1:
            for w in text[i:].split():
                tokens.append((w, False))
            break
        if open_idx > i:
            prefix = text[i:open_idx]
            if not prefix[-1].isspace():
                # Word directly attached before '(' — find preceding space
                last_space = prefix.rfind(" ")
                if last_space != -1:
                    for w in prefix[:last_space].split():
                        tokens.append((w, False))
                    open_idx = i + last_space + 1
                else:
                    open_idx = i
            else:
                for w in prefix.split():
                    tokens.append((w, False))
        # Find balanced ')' respecting list markers
        start_paren = text.find("(", open_idx)
        depth = 1
        close_idx = start_paren + 1
        while close_idx < n and depth > 0:
            ch = text[close_idx]
            if ch == "(":
                depth += 1
            elif ch == ")" and not is_list_marker_close(text, start_paren, close_idx):
                depth -= 1
            close_idx += 1
        while close_idx < n and not text[close_idx].isspace():
            close_idx += 1
        paren_block = text[open_idx:close_idx].strip()
        tokens.append((paren_block, True))
        i = close_idx
    return tokens


def coalesce_segments(segs: list[dict]) -> list[dict]:
    if not segs:
        return []
    out = [dict(segs[0])]
    for s in segs[1:]:
        if s["cid"] == out[-1]["cid"]:
            out[-1]["text"] = f"{out[-1]['text']} {s['text']}"
        else:
            out.append(dict(s))
    return out


def fetch_or_load_wbw(cache_path: Path | None) -> dict[str, dict[str, list[dict]]]:
    if cache_path and cache_path.exists():
        return json.loads(cache_path.read_text(encoding="utf-8"))

    print("Fetching Turkish Word-by-Word (WBW) glosses from Quran.com API v4...")

    def _fetch_json(url: str) -> dict:
        for attempt in range(5):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=20) as resp:
                    return json.load(resp)
            except Exception:
                if attempt == 4:
                    raise
                time.sleep(0.5 * (attempt + 1))
        return {}

    def _fetch_surah(cid: int) -> tuple[int, dict[str, list[dict]]]:
        base_url = f"{API_BASE}/verses/by_chapter/{cid}?language=tr&words=true&word_fields=text_uthmani,translation&per_page=50"
        first = _fetch_json(base_url)
        verses = list(first.get("verses", []))
        total_pages = first.get("pagination", {}).get("total_pages", 1)
        for p in range(2, total_pages + 1):
            verses.extend(_fetch_json(f"{base_url}&page={p}").get("verses", []))
        vmap: dict[str, list[dict]] = {}
        for v in verses:
            vnum = v["verse_key"].split(":")[1]
            words = [w for w in v.get("words", []) if w.get("char_type_name") != "end"]
            vmap[vnum] = [
                {
                    "cid": idx,
                    "ar": w.get("text_uthmani", ""),
                    "tr": (w.get("translation") or {}).get("text") or "",
                }
                for idx, w in enumerate(words, 1)
            ]
        return cid, vmap

    all_wbw: dict[str, dict[str, list[dict]]] = {}
    with ThreadPoolExecutor(max_workers=8) as pool:
        futs = [pool.submit(_fetch_surah, c) for c in range(1, 115)]
        for fut in as_completed(futs):
            sid, vmap = fut.result()
            all_wbw[str(sid)] = vmap

    if cache_path:
        cache_path.write_text(json.dumps(all_wbw, ensure_ascii=False), encoding="utf-8")
    return all_wbw


class TurkicCidAligner:
    def __init__(self, wbw_data: dict[str, dict[str, list[dict]]]) -> None:
        self.wbw_data = wbw_data
        self.ar_tr_dict: dict[str, Counter] = defaultdict(Counter)
        common_en = set(EN_TO_TR_FALLBACK.keys()) | {
            "the", "and", "you", "they", "from", "to", "in", "of", "is", "are", "was", "were"
        }
        for vmap in wbw_data.values():
            for wlist in vmap.values():
                for w in wlist:
                    ar_c = clean_ar(w["ar"])
                    tr_c = w["tr"].strip()
                    if tr_c.lower() not in common_en:
                        self.ar_tr_dict[ar_c][tr_c] += 1

    def get_repaired_wbw(self, sid: int, vnum: int) -> list[dict]:
        raw_list = self.wbw_data[str(sid)][str(vnum)]
        wlist = [dict(w) for w in raw_list]
        for i, w in enumerate(wlist):
            t_low = w["tr"].strip().lower()
            is_en = t_low in EN_TO_TR_FALLBACK or (
                bool(re.findall(r"^[a-z\s\(\)']+$", t_low))
                and t_low
                not in (
                    "allah", "rahman", "rahim", "amin", "el", "hak", "nur", "tur",
                    "hud", "nuh", "lut", "ad", "rem", "kaf", "sad", "ta", "ha", "ya", "sin",
                )
                and any(
                    ew in t_low.split()
                    for ew in (
                        "the", "you", "they", "their", "before", "after", "from", "who",
                        "what", "those", "lord", "earth", "heaven", "book", "people",
                        "believe", "say", "said", "were", "was", "be", "is", "not", "in",
                        "for", "his", "him", "them",
                    )
                )
            )
            if is_en:
                ar_c = clean_ar(w["ar"])
                best_tr = ""
                if ar_c in self.ar_tr_dict and self.ar_tr_dict[ar_c]:
                    best_tr = self.ar_tr_dict[ar_c].most_common(1)[0][0]
                elif t_low in EN_TO_TR_FALLBACK:
                    best_tr = EN_TO_TR_FALLBACK[t_low]
                if i > 0:
                    prev_ar = clean_ar(wlist[i - 1]["ar"])
                    prev_tr = wlist[i - 1]["tr"].strip()
                    prev_words = prev_tr.split()
                    if len(prev_words) >= 2 and prev_ar in AR_PARTICLES:
                        wlist[i - 1]["tr"] = prev_words[0]
                        w["tr"] = " ".join(prev_words[1:]) + (" " + best_tr if best_tr else "")
                        continue
                    elif len(prev_words) == 1 and prev_ar in AR_PARTICLES:
                        w["tr"] = prev_tr + (" " + best_tr if best_tr else "")
                        continue
                if best_tr:
                    w["tr"] = best_tr
        return wlist

    def train_corpus_ibm1(self, trans_dir: Path, is_crh: bool = False) -> dict[tuple[str, str], float]:
        ar_counts: Counter = Counter()
        stem_counts: Counter = Counter()
        pair_counts: Counter = Counter()

        for yf in sorted(trans_dir.glob("*.yaml")):
            sid = int(yf.name.split("-")[0])
            txt = yf.read_text(encoding="utf-8")
            blocks = txt.split("\n  - verse: ")
            for b in blocks[1:]:
                lines = b.splitlines()
                vnum = int(lines[0].strip())
                raw_t = " ".join(
                    ln.strip().lstrip("- text:").strip().strip("'\"")
                    for ln in lines[1:]
                    if not ln.lstrip().startswith(("cid:", "segments:", "merged_into:", "- text: >"))
                )
                clean_t = re.sub(r"\([^()]*\)", " ", raw_t)
                words = set()
                for w in clean_t.split():
                    nh = norm_harmony(w, is_crh=is_crh)
                    if len(nh) >= 3:
                        words.add(nh[:5])
                ar_words = {clean_ar(w["ar"]) for w in self.wbw_data[str(sid)][str(vnum)]}
                for aw in ar_words:
                    ar_counts[aw] += 1
                for sw in words:
                    stem_counts[sw] += 1
                for aw in ar_words:
                    for sw in words:
                        pair_counts[(aw, sw)] += 1

        assoc: dict[tuple[str, str], float] = {}
        for (aw, sw), cnt in pair_counts.items():
            if cnt < 2:
                continue
            dice = (2.0 * cnt) / (ar_counts[aw] + stem_counts[sw] + 2.0)
            cond = cnt / (ar_counts[aw] + 1.0)
            score = max(dice, cond * 0.7)
            if score >= 0.08:
                assoc[(aw, sw)] = score
        return assoc

    def align_verse(
        self,
        text: str,
        sid: int,
        vnum: int,
        range_verses: list[int],
        is_crh: bool = False,
        assoc_ar: dict[tuple[str, str], float] | None = None,
    ) -> list[dict]:
        if CROSS_REF_RE.match(text.strip()):
            return [{"text": text.strip(), "cid": 0}]

        tokens = tokenize_preserving_parens(text)
        if not tokens:
            return [{"text": text, "cid": 0}]

        concepts: list[tuple[int, int, dict]] = []
        for u in range_verses:
            for w in self.get_repaired_wbw(sid, u):
                concepts.append((u, w["cid"], w))

        K_total = len(concepts)
        if K_total == 0:
            return [{"text": text, "cid": 0}]
        if K_total == 1:
            u0, c0, _ = concepts[0]
            target_cid = c0 if u0 == vnum else 0
            segs = [{"text": tok, "cid": 0 if is_p else target_cid} for tok, is_p in tokens]
            return coalesce_segments(segs)

        cid_stems: dict[tuple[int, int], set[str]] = {}
        cid_norm_words: dict[tuple[int, int], set[str]] = {}
        cid_has_wa: dict[tuple[int, int], bool] = {}
        cid_ar_clean: dict[tuple[int, int], str] = {}
        cid_is_neg: dict[tuple[int, int], bool] = {}
        cid_has_neg_verb: dict[tuple[int, int], bool] = {}
        cid_global_pos: dict[tuple[int, int], int] = {}

        for g_idx, (u, c, w) in enumerate(concepts):
            g = (u, c)
            cid_global_pos[g] = g_idx
            ar_c = clean_ar(w["ar"])
            cid_ar_clean[g] = ar_c
            tr_text = w["tr"]
            cid_has_wa[g] = ar_c.startswith("و") or tr_text.lower().startswith("ve ")
            prev_ar = clean_ar(concepts[g_idx - 1][2]["ar"]) if g_idx > 0 and concepts[g_idx - 1][0] == u else ""
            cid_is_neg[g] = ar_c in ("غَيْرِ", "لَا", "وَلَا", "مَا", "لَمْ", "لَن", "لَيْسَ", "إِلَّا") or any(
                nw in tr_text.lower().split() for nw in ("değil", "yok", "yoktur", "asla")
            )
            cid_has_neg_verb[g] = (
                cid_is_neg[g]
                or prev_ar in ("لَا", "وَلَا", "مَا", "لَمْ", "لَن")
                or any(is_negated_verb(tw) for tw in re.findall(r"[\w']+", tr_text, flags=re.UNICODE))
            )

            stems = set()
            nwords = set()
            for tw in re.findall(r"[\w']+", tr_text, flags=re.UNICODE):
                nh = norm_harmony(tw, is_crh=False)
                if nh and nh not in ("ve", "ile", "bir", "ki", "mi", "olan"):
                    nwords.add(nh)
                    stems.update(get_rich_stems(tw, is_crh=False))
            cid_stems[g] = stems
            cid_norm_words[g] = nwords

        word_indices = [idx for idx, (_, is_p) in enumerate(tokens) if not is_p]
        if not word_indices and tokens:
            # Edge case (e.g. 13:30 where opening vocative '(Ey, Muhammed!' was closed at end of verse):
            # Tokenize by whitespace so the verse is mapped rather than collapsed.
            tokens = [(w, w.startswith("(") and w.endswith(")")) for w in text.split()]
            word_indices = [idx for idx, (_, is_p) in enumerate(tokens) if not is_p]
        M = len(word_indices)
        if M == 0:
            return [{"text": text, "cid": 0}]

        assigned_g: list[tuple[int, int] | None] = [None] * len(tokens)
        raw_scores: dict[int, dict[tuple[int, int], float]] = {}

        for pos_m, idx in enumerate(word_indices):
            tok = tokens[idx][0]
            raw_clean = re.sub(r"[^\w]", "", tok.lower(), flags=re.UNICODE)
            nh = norm_harmony(tok, is_crh=is_crh)
            tok_stems = get_rich_stems(tok, is_crh=is_crh)
            tok_neg = is_negated_verb(tok)
            raw_scores[idx] = {}

            next_clean = (
                re.sub(r"[^\w]", "", tokens[word_indices[pos_m + 1]][0].lower(), flags=re.UNICODE)
                if pos_m + 1 < M
                else ""
            )
            is_de_imperative = raw_clean == "de" and (next_clean == "ki" or tok.endswith(":"))

            if not is_de_imperative:
                if raw_clean in ("ve", "olğan", "olan", "bir", "de", "da", "ki"):
                    continue
                if raw_clean in GENITIVE_PRONOUNS and not tok.endswith((".", ",", ";", ":", "!", "?")) and pos_m + 1 < M:
                    continue
                if (
                    raw_clean in AUX_DEFER_LEFT
                    and pos_m > 0
                    and not tokens[word_indices[pos_m - 1]][0].endswith((".", ",", ";", ":", "!", "?"))
                ):
                    continue

            for u, c, _ in concepts:
                g = (u, c)
                sc = 0.0
                if is_de_imperative and cid_ar_clean[g] in ("قُلْ", "قُل", "فَقُلْ", "وَقُلْ", "قُولُوا۟"):
                    sc += 14.0
                elif nh and nh in cid_norm_words[g]:
                    sc += 12.0
                else:
                    shared = tok_stems & cid_stems[g]
                    if shared:
                        max_len = max(len(s) for s in shared)
                        if max_len >= 6:
                            sc += 9.5
                        elif max_len == 5:
                            sc += 8.0
                        elif max_len == 4:
                            sc += 6.2
                        elif max_len == 3:
                            sc += 3.8
                    for cnw in cid_norm_words[g]:
                        if len(nh) >= 4 and len(cnw) >= 4 and (nh in cnw or cnw in nh):
                            sc = max(sc, 7.5)

                if raw_clean in ("degil", "değil", "yoq", "yok", "yoktur", "yoqtır") and cid_is_neg[g]:
                    sc += 10.0

                if assoc_ar and len(nh) >= 3:
                    ar_c = cid_ar_clean[g]
                    assoc_val = assoc_ar.get((ar_c, nh[:5]), 0.0)
                    if assoc_val >= 0.14:
                        sc += assoc_val * 9.0

                if sc >= 3.2:
                    if tok_neg == cid_has_neg_verb[g]:
                        sc += 1.8
                    else:
                        sc -= 1.8
                    rel_m = pos_m / max(1, M - 1)
                    rel_c = cid_global_pos[g] / max(1, K_total - 1)
                    dist = min(abs(rel_m - rel_c), abs(rel_m - (1.0 - rel_c)) * 0.9 + 0.05)
                    sc += max(0.0, 1.0 - dist) * 0.8
                    raw_scores[idx][g] = sc

        covered_g: set[tuple[int, int]] = set()
        unambiguous_order = []
        ambiguous_order = []
        for idx in word_indices:
            if not raw_scores[idx]:
                continue
            vals = sorted(raw_scores[idx].values(), reverse=True)
            if vals[0] >= 4.2:
                if len(vals) == 1 or (vals[0] - vals[1]) >= 1.2:
                    unambiguous_order.append((vals[0], idx))
                else:
                    ambiguous_order.append((vals[0], idx))

        unambiguous_order.sort(reverse=True)
        for _, idx in unambiguous_order:
            best_g = max(
                raw_scores[idx].keys(),
                key=lambda g: raw_scores[idx][g] + (1.5 if g not in covered_g else 0.0),
            )
            assigned_g[idx] = best_g
            covered_g.add(best_g)

        idx_to_pos = {idx: pos_m for pos_m, idx in enumerate(word_indices)}
        ambiguous_order.sort(reverse=True)
        for _, idx in ambiguous_order:
            pos_m = idx_to_pos[idx]
            next_g = assigned_g[word_indices[pos_m + 1]] if pos_m + 1 < M else None
            prev_g = assigned_g[word_indices[pos_m - 1]] if pos_m > 0 else None

            def _score_with_neighbor(g: tuple[int, int]) -> float:
                s = raw_scores[idx][g] + (1.5 if g not in covered_g else 0.0)
                u, c = g
                if next_g is not None and next_g[0] == u and abs(c - next_g[1]) <= 2:
                    s += 3.5
                if prev_g is not None and prev_g[0] == u and abs(c - prev_g[1]) <= 2:
                    s += 2.5
                return s

            best_g = max(raw_scores[idx].keys(), key=_score_with_neighbor)
            assigned_g[idx] = best_g
            covered_g.add(best_g)

        for pos_m, idx in enumerate(word_indices):
            if assigned_g[idx] is not None:
                continue
            tok = tokens[idx][0]
            raw_clean = re.sub(r"[^\w]", "", tok.lower(), flags=re.UNICODE)
            if (
                raw_clean in ("de", "da", "ki", "mi", "mı", "mu", "mü")
                or raw_clean in AUX_POST
                or raw_clean in AUX_DEFER_LEFT
            ):
                if pos_m > 0:
                    prev_idx = word_indices[pos_m - 1]
                    if assigned_g[prev_idx] is not None:
                        assigned_g[idx] = assigned_g[prev_idx]
                        continue

        for pos_m in range(M - 1, -1, -1):
            idx = word_indices[pos_m]
            if assigned_g[idx] is not None:
                continue
            tok = tokens[idx][0]
            raw_clean = re.sub(r"[^\w]", "", tok.lower(), flags=re.UNICODE)
            if (raw_clean in PRE_MODIFIERS or raw_clean in GENITIVE_PRONOUNS) and pos_m + 1 < M:
                next_idx = word_indices[pos_m + 1]
                if assigned_g[next_idx] is not None:
                    assigned_g[idx] = assigned_g[next_idx]
                    continue

        for pos_m, idx in enumerate(word_indices):
            if assigned_g[idx] is not None:
                continue
            tok = tokens[idx][0]
            raw_clean = re.sub(r"[^\w]", "", tok.lower(), flags=re.UNICODE)

            if raw_clean == "ve":
                standalone_wa = [
                    (u, c)
                    for u, c, _ in concepts
                    if cid_ar_clean[(u, c)] in ("وَلَا", "وَ", "أَوْ", "ثُمَّ") and (u, c) not in covered_g
                ]
                if standalone_wa:
                    assigned_g[idx] = standalone_wa[0]
                    covered_g.add(standalone_wa[0])
                elif pos_m + 1 < M:
                    next_idx = word_indices[pos_m + 1]
                    next_g = assigned_g[next_idx]
                    if next_g is not None and cid_has_wa.get(next_g, False):
                        assigned_g[idx] = next_g
                continue

            if raw_clean in ("olğan", "olan"):
                continue

            if raw_scores[idx]:
                best_g = max(
                    raw_scores[idx].keys(),
                    key=lambda g: raw_scores[idx][g] + (1.2 if g not in covered_g else 0.0),
                )
                assigned_g[idx] = best_g
                covered_g.add(best_g)
            else:
                prev_idx = word_indices[pos_m - 1] if pos_m > 0 else None
                next_idx = word_indices[pos_m + 1] if pos_m + 1 < M else None
                if (
                    prev_idx is not None
                    and assigned_g[prev_idx] is not None
                    and not tokens[prev_idx][0].endswith((".", ";", ":", "!", "?"))
                ):
                    assigned_g[idx] = assigned_g[prev_idx]
                elif next_idx is not None and assigned_g[next_idx] is not None:
                    assigned_g[idx] = assigned_g[next_idx]

        # Fallback guarantee: ensure every content verse (u == vnum) has at least one mapped segment
        has_vnum_cid = any(g is not None and g[0] == vnum for g in assigned_g)
        if not has_vnum_cid and M > 0:
            vnum_cids = [c for u, c, _ in concepts if u == vnum]
            if vnum_cids:
                if len(range_verses) == 1:
                    # Single-verse fallback: distribute words across vnum_cids in SOV order
                    # (final predicate word maps to cid 1 if K >= 2, earlier words map across 2..K or 1..K)
                    Kv = len(vnum_cids)
                    for pos_m, idx in enumerate(word_indices):
                        tok_clean = re.sub(r"[^\w]", "", tokens[idx][0].lower(), flags=re.UNICODE)
                        if tok_clean in ("ve", "olğan", "olan"):
                            continue
                        if Kv >= 2 and pos_m == M - 1:
                            c_pick = vnum_cids[0]
                        elif Kv >= 2:
                            rem_pos = pos_m / max(1, M - 1)
                            c_idx = min(Kv - 1, 1 + int(rem_pos * (Kv - 1)))
                            c_pick = vnum_cids[c_idx]
                        else:
                            c_pick = vnum_cids[0]
                        assigned_g[idx] = (vnum, c_pick)
                else:
                    # Multi-verse combined range fallback: assign the proportional slice of tokens for vnum
                    r_idx = range_verses.index(vnum)
                    n_rng = len(range_verses)
                    s_pos = int(round(r_idx * M / n_rng))
                    e_pos = max(s_pos + 1, int(round((r_idx + 1) * M / n_rng)))
                    slice_positions = list(range(min(s_pos, M - 1), min(e_pos, M)))
                    Kv = len(vnum_cids)
                    for k_i, pos_m in enumerate(slice_positions):
                        idx = word_indices[pos_m]
                        c_pick = vnum_cids[min(Kv - 1, int(k_i * Kv / max(1, len(slice_positions))))]
                        assigned_g[idx] = (vnum, c_pick)

        segs = []
        for i, (tok, is_p) in enumerate(tokens):
            g = assigned_g[i]
            if is_p or g is None:
                cid_out = 0
            else:
                u, c = g
                cid_out = c if u == vnum else 0
            segs.append({"text": tok, "cid": cid_out})
        return coalesce_segments(segs)


NEEDS_BLOCK_RE = re.compile(r"(?:^[\[\{\"'!&*|>%@`?\-]|:\s|\s#|['\":]$)")


def fast_read_translation_yaml(yaml_path: Path) -> list[dict]:
    """Fast line-based reader for translation YAML files (50x faster than pure-Python SafeLoader)."""
    txt = yaml_path.read_text(encoding="utf-8")
    blocks = txt.split("\n  - verse: ")
    verses: list[dict] = []
    for b in blocks[1:]:
        lines = b.splitlines()
        vnum = int(lines[0].strip())
        vdict: dict = {"verse": vnum, "segments": []}
        idx = 1
        while idx < len(lines):
            ln = lines[idx]
            m_merged = re.match(r'^\s*merged_into:\s*"?([^"\n]+)"?\s*$', ln)
            if m_merged:
                vdict["merged_into"] = m_merged.group(1).strip()
                idx += 1
                continue
            if re.match(r"^\s*-\s+text:\s*>[+-]?\s*$", ln):
                idx += 1
                chunk = []
                while idx < len(lines) and (
                    (lines[idx].startswith("        ") and not lines[idx].lstrip().startswith("cid:"))
                    or not lines[idx].strip()
                ):
                    if lines[idx].strip():
                        chunk.append(lines[idx].strip())
                    idx += 1
                seg_text = " ".join(chunk)
                cid_val = 0
                if idx < len(lines) and lines[idx].lstrip().startswith("cid:"):
                    cid_val = int(lines[idx].split(":", 1)[1].strip())
                    idx += 1
                vdict["segments"].append({"text": seg_text, "cid": cid_val})
            else:
                m_in = re.match(r"^\s*-\s+text:\s*(.+)$", ln)
                if m_in:
                    raw_val = m_in.group(1).strip()
                    if (raw_val.startswith('"') and raw_val.endswith('"')) or (
                        raw_val.startswith("'") and raw_val.endswith("'")
                    ):
                        raw_val = raw_val[1:-1]
                    cid_val = 0
                    if idx + 1 < len(lines) and lines[idx + 1].lstrip().startswith("cid:"):
                        cid_val = int(lines[idx + 1].split(":", 1)[1].strip())
                        idx += 2
                    else:
                        idx += 1
                    vdict["segments"].append({"text": raw_val, "cid": cid_val})
                else:
                    idx += 1
        verses.append(vdict)
    return verses


def format_segment_yaml(seg_text: str, cid: int) -> list[str]:
    """Serialize a segment into clean YAML matching repository conventions and fast/full parsers."""
    t = seg_text.strip()
    if len(t) <= 74 and not NEEDS_BLOCK_RE.search(t) and t.lower() not in ("true", "false", "null", "yes", "no", "on", "off"):
        return [f"      - text: {t}", f"        cid: {cid}"]
    wrapped = textwrap.wrap(
        t,
        width=84,
        break_long_words=False,
        break_on_hyphens=False,
    )
    lines = ["      - text: >-"]
    for wln in wrapped:
        lines.append(f"          {wln}")
    lines.append(f"        cid: {cid}")
    return lines


def process_translation_corpus(
    aligner: TurkicCidAligner,
    lang: str,
    author: str,
    surah_start: int = 1,
    surah_end: int = 114,
    force_all: bool = False,
) -> tuple[int, int]:
    trans_dir = TRANS_ROOT / lang / author
    is_crh = lang == "crh"
    assoc_ar = aligner.train_corpus_ibm1(trans_dir, is_crh=is_crh)

    crh_merged_map: dict[int, dict[int, list[int]]] = defaultdict(dict)
    if is_crh and MERGED_RANGES_CRH_PATH.exists():
        mdata = json.loads(MERGED_RANGES_CRH_PATH.read_text(encoding="utf-8"))
        for item in mdata.get("merged_ranges", []):
            sid_int = int(item["surah_id"])
            a_int = int(item["start_verse"])
            b_int = int(item["end_verse"])
            rlist = list(range(a_int, b_int + 1))
            for u in rlist:
                crh_merged_map[sid_int][u] = rlist

    surahs_updated = 0
    verses_updated = 0

    for yf in sorted(trans_dir.glob("*.yaml")):
        sid = int(yf.name.split("-")[0])
        if sid < surah_start or sid > surah_end:
            continue

        verses = fast_read_translation_yaml(yf)

        # Preserve hand-curated Surah 1 (Al-Fatiha) in crh/dizen-qurtnezir and tr/elmalili unless --force-all
        if sid == 1 and (is_crh or (lang == "tr" and author == "elmalili")) and not force_all:
            continue

        # Detect combined/merged ranges in Turkish (identical text across consecutive verses)
        verse_texts: dict[int, str] = {}
        for v in verses:
            vnum = int(v["verse"])
            verse_texts[vnum] = " ".join(str(s["text"]).strip() for s in v["segments"]).strip()

        tr_combined_ranges: dict[int, list[int]] = {}
        if not is_crh:
            vnums_sorted = sorted(verse_texts.keys())
            i = 0
            while i < len(vnums_sorted):
                j = i
                while j + 1 < len(vnums_sorted) and verse_texts[vnums_sorted[j + 1]] == verse_texts[vnums_sorted[i]]:
                    j += 1
                if j > i:
                    rlist = vnums_sorted[i : j + 1]
                    for u in rlist:
                        tr_combined_ranges[u] = rlist
                i = j + 1

        out_lines = [
            f"surah_id: {sid}",
            f"language: {lang}",
            f"author: {author}",
            "verses:",
        ]

        file_changed = False
        for v in verses:
            vnum = int(v["verse"])
            out_lines.append(f"  - verse: {vnum}")
            if "merged_into" in v:
                out_lines.append(f'    merged_into: "{v["merged_into"]}"')
            out_lines.append("    segments:")

            full_text = verse_texts[vnum]
            if is_crh:
                rng = crh_merged_map[sid].get(vnum, [vnum])
            else:
                rng = tr_combined_ranges.get(vnum, [vnum])
            new_segs = aligner.align_verse(
                full_text,
                sid=sid,
                vnum=vnum,
                range_verses=rng,
                is_crh=is_crh,
                assoc_ar=assoc_ar,
            )
            file_changed = True
            verses_updated += 1

            for s in new_segs:
                out_lines.extend(format_segment_yaml(str(s["text"]), int(s["cid"])))

        if file_changed:
            yf.write_text("\n".join(out_lines) + "\n", encoding="utf-8")
            surahs_updated += 1

    return surahs_updated, verses_updated


def main() -> int:
    parser = argparse.ArgumentParser(description="Align CRH and TR Quran translations to Core Arabic CIDs.")
    parser.add_argument(
        "--target",
        choices=["all", "crh", "diyanet", "elmalili"],
        default="all",
        help="Which translation corpus to align (default: all)",
    )
    parser.add_argument("--surah-start", type=int, default=1)
    parser.add_argument("--surah-end", type=int, default=114)
    parser.add_argument("--wbw-cache", type=Path, default=None, help="Path to cached quran_tr_wbw.json")
    parser.add_argument("--force-all", action="store_true", help="Re-map even already mapped verses")
    args = parser.parse_args()

    t0 = time.time()
    wbw_data = fetch_or_load_wbw(args.wbw_cache)
    aligner = TurkicCidAligner(wbw_data)

    targets = []
    if args.target in ("all", "crh"):
        targets.append(("crh", "dizen-qurtnezir"))
    if args.target in ("all", "diyanet"):
        targets.append(("tr", "diyanet"))
    if args.target in ("all", "elmalili"):
        targets.append(("tr", "elmalili"))

    for lang, author in targets:
        t_c = time.time()
        s_cnt, v_cnt = process_translation_corpus(
            aligner,
            lang=lang,
            author=author,
            surah_start=args.surah_start,
            surah_end=args.surah_end,
            force_all=args.force_all,
        )
        print(f"✅ [{lang}/{author}] Mapped {s_cnt} surahs ({v_cnt} verses) in {time.time() - t_c:.1f}s")

    print(f"🎉 Completed CID alignment in {time.time() - t0:.1f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
