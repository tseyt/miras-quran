#!/usr/bin/env python3
"""Canonical Crimean Tatar (CRH) PDF errata cleaner and Cyrillic <-> Latin orthography engine.

Designed specifically for the 2005 Simferopol 2nd edition of:
  Sait Dizen & Zakir Qurtnezir, "Qur'an-ı Kerim ve izaatlı manası"
  (Qırım Musulmanları Diniy İdaresi, Decision 15/10/2004).
"""

from __future__ import annotations

import re

# ---------------------------------------------------------------------------
# 1. Verified 2005 PDF Errata (Word-level & Stem-level)
# ---------------------------------------------------------------------------

EXACT_WORD_ERRATA: dict[str, str] = {
    # Transposed / doubled hard sign 'ъ'
    "ёъкса": "ёкъса",
    "ёксъа": "ёкъса",
    "аллаһнныъ": "аллаһнынъ",
    "аллаһннынъ": "аллаһнынъ",
    "аллаһһнынъ": "аллаһнынъ",
    "аллаһт": "аллаһ",
    "инсанныъ": "инсаннынъ",
    "инсаннныъ": "инсаннынъ",
    "куър'ан": "къур'ан",
    "къур'ант": "къур'ан",
    "къу'ан": "къур'ан",
    "куран-ы": "къур'ан-ы",
    "кур'аннынъ": "къур'аннынъ",
    "къур'анынъ": "къур'аннынъ",
    "куърбан": "къурбан",
    "луъкман": "лукъман",
    "мусанныъ": "мусанынъ",
    "пейгаъмберимиз": "пейгъамберимиз",
    "пейгъамберниниъ": "пейгъамбернинъ",
    "рахманныъ": "рахманнынъ",
    "фаъкат": "факъат",
    "авлаъан": "авлагъан",
    "азырлыкъълы": "азырлыкълы",
    "акъсызлыкъъа": "акъсызлыкъкъа",
    "акъъкъан": "акъкъан",
    "араныъзда": "аранъызда",
    "долашъкан": "долашкъан",
    "каъадар": "къадар",
    "къъадар": "къадар",
    "коръку": "къоркъу",
    "къоркунъ": "къоркъунъ",
    "къоркунен": "къоркъунен",
    "куъветли": "къуветли",
    "куветлидир": "къуветлидир",
    "куветлендирильген": "къуветлендирильген",
    "кудрет": "къудрет",
    "куълакъ": "къулакъ",
    "куълларынынъ": "къулларынынъ",
    "куъртулыш": "къуртулыш",
    "къуръанлары": "къургъанлары",
    "къъалырлар": "къалырлар",
    "къъаршы": "къаршы",
    "маналандырылъан": "маналандырылгъан",
    "нефислериниъзде": "нефислеринъизде",
    "ноъктаи": "нокътаи",
    "окуългъанда": "окъулгъанда",
    "оларнныъ": "оларнынъ",
    "оларннынъ": "оларнынъ",
    "рызыък": "рызыкъ",
    "суренниъ": "суренинъ",
    "сурениннъ": "суренинъ",
    "тапъканлар": "тапкъанлар",
    "тартышъмагъа": "тартышмагъа",
    "фаръкына": "фаркъына",
    "чагъыръан": "чагъыргъан",
    "чокуъ": "чокъу",
    "экисинниъ": "экисининъ",
    "япкъанларыныъздан": "япкъанларынъыздан",
    "япъканынен": "япкъанынен",
    "ярышъканларгъа": "ярышкъанларгъа",
    # Dropped / transposed 'д' in 'дж'
    "жеэннем": "джеэннем",
    "сежде": "седжде",
    "мевжют": "мевджут",
    "мевжут": "мевджут",
    "узакълаштыражакъ": "узакълаштыраджакъ",
    "дежнкке": "дженкке",
    "олаждакъмыз": "оладжакъмыз",
    "бежерювлери": "беджерювлери",
    "жинсель": "джинсель",
    "садеже": "садедже",
    "межал": "меджал",
    "месжид": "месджид",
    "инжилер": "инджилер",
    "южедир": "юджедир",
    "южелер": "юджелер",
    "южельтип": "юджельтип",
    "этедежклер": "этеджеклер",
    "къопадажакъ": "къопаджакъ",
    "удюжмлернинъ": "уджумлернинъ",
    "межлисте": "меджлисте",
    "межбуриетини": "меджбуриетини",
    "бильдиреждексинъ": "бильдиреджексинъ",
    "денаб": "дженаб",
    "денаб-ы": "дженаб-ы",
    # Soft sign & velar slips & printed typos
    "юзьь": "юзь",
    "олунаь": "олуна",
    "ёктыр": "ёкътыр",
    "ёкъктыр": "ёкътыр",
    "ёкмы": "ёкъмы",
    "къаранлыклар": "къаранлыкълар",
    "турмакталар": "турмакъталар",
    "токъунылмакта": "токъунылмакъта",
    "ахляк": "ахлякъ",
    "ачыктан": "ачыкътан",
    "аяккъа": "аякъкъа",
    "буюктыр": "буюктир",
    "быкылмадан": "быкъылмадан",
    "демектыр": "демектир",
    "ляйыктыр": "ляйыкътыр",
    "накорьлигинден": "нанкорьлигинден",
    "хактан": "хакътан",
    "якъыладжаклар": "якъыладжакълар",
    "къалмаган": "къалмагъан",
    "къылмаган": "къылмагъан",
    "оладжагыны": "оладжагъыны",
    "сынъырсызлыгыны": "сынъырсызлыгъыны",
    "багыргъанынъыз": "багъыргъанынъыз",
    "багышлайыджы": "багъышлайыджы",
    "багъышлыйыджы": "багъышлайыджы",
    "барлыгынынъ": "барлыгъынынъ",
    "догърулыгыны": "догърулыгъыны",
    "олргъа": "оларгъа",
    "акъкъикъий": "акъикъий",
    "зельзеде": "зельзеле",
    "чыкъкан": "чыкъкъан",
    "онынъен": "онынънен",
    "энгениен": "энгенинен",
    "терджмие": "терджиме",
    "этммек": "этмек",
    "этюёвлерине": "этювлерине",
    "ахкъямнынъ": "ахкямнынъ",
    "ёксельген": "юксельген",
    "ёладыкъ": "ёлладыкъ",
    "ёллараякъ": "ёллаяракъ",
    "ёлламдыкъ": "ёлламадыкъ",
    "ёлланлыгъанына": "ёлланылгъанына",
    "ёуландан": "ёлундан",
    "ёрумалангъан": "ёрумлангъан",
    "инкряджыларгъадыр": "инкярджыларгъадыр",
    "имякнындан": "имкянындан",
    "исялмгъа": "ислямгъа",
    "дюняда": "дюньяда",
    "япайяткъанларынъызны": "япаяткъанларынъызны",
    "бойлдже": "бойледже",
    "ошекленгенген": "ошекленген",
    "мудеттен": "муддеттен",
    "мудетке": "муддетке",
    "мудеткедже": "муддеткедже",
    "мудетти": "муддети",
    "мудетнинъ": "муддетнинъ",
    "умимийдир": "умумийдир",
    "муджизилер": "муджизелер",
    "мукемеллик": "мукеммеллик",
    "мукеммелигини": "мукеммеллигини",
    "мусхинлерден": "мухсинлерден",
    "шубелениджилирден": "шубелениджилерден",
    "шубсиз": "шубесиз",
    "субепнен": "себепнен",
    "мусебетинъиз": "мусибетинъиз",
    "мусебетлерде": "мусибетлерде",
    "мусебетлеримизни": "мусибетлеримизни",
    "мушреклерни": "мушриклерни",
    "уриетке": "урриетке",
    "аетлеириде": "аетлеринде",
    "ирщат": "иршат",
    "иджртте": "иджретте",
    "алемии": "аалемиин",
    "рузьгяр": "рузгяр",
    "сёзьлерини": "сёзлерини",
    "къорчаланырсынъсыз": "къорчаланырсынъыз",
    "шаатларынъзны": "шаатларынъызны",
}

STEM_PREFIX_ERRATA: tuple[tuple[str, str], ...] = (
    ("башъка", "башкъа"),
    ("башка", "башкъа"),
    ("коркъкъан", "къоркъкъан"),
    ("виждан", "видждан"),
    ("ёксул", "ёкъсул"),
    ("мунафык", "мунафыкъ"),
    ("инанмаган", "инанмагъан"),
    ("пейгамбер", "пейгъамбер"),
    ("пейгъмбер", "пейгъамбер"),
    ("рабинъ", "раббинъ"),
    ("уьстю", "усьтю"),
    ("узъре", "узьре"),
)

PAREN_SURGICAL_PATCHES: dict[tuple[int, str], list[tuple[str, str]]] = {
    (2, "197"): [("(Эй, му'минлер! Ахирет", "(Эй, му'минлер!) Ахирет")],
    (2, "227"): [
        ("(муддети ичинде дёнмейип,", "(муддети ичинде дёнмейип),"),
        ("(айрылырлар.", "(айрылырлар)."),
    ],
    (2, "229"): [("залымдырлар).", "залымдырлар.")],
    (2, "243"): [("дикъкъат чеккен.", "дикъкъат чеккен).")],
    (2, "254"): [("залымлардыр).", "залымлардыр.")],
    (3, "12"): [("зафер къазангъанлар.", "зафер къазангъанлар).")],
    (3, "45"): [("«мубарек» манасындадыр.", "«мубарек» манасындадыр).")],
    (3, "73"): [
        ("Кене (олар) озьаралары бойле дедилер:)", "Кене (олар озьаралары бойле дедилер):"),
        ("«(Эй, эхл-и китап!", "«(Эй, эхл-и китап!)"),
    ],
    (3, "79"): [("3/116-117).", "3/116-117)).")],
    (3, "127-128"): [("ярдым этти).", "ярдым этти.")],
    (4, "136"): [("сапыткъандыр).", "сапыткъандыр.")],
    (4, "176"): [("(эркек къардашлары быракъкъанынынъ", "(эркек къардашлары) быракъкъанынынъ")],
    (5, "116"): [("(мени ве анамны, Аллаһтан башкъа эки танъры билинъ, дие", "«Мени ве анамны, Аллаһтан башкъа эки танъры билинъ», дие")],
    (6, "1"): [("(Бу къадар ает ве делиллерден сонъ,", "(Бу къадар ает ве делиллерден сонъ),")],
    (6, "92"): [("Бу (Къур'ан, Умму'ль-къураа", "Бу (Къур'ан), Умму'ль-къураа")],
    (7, "137"): [("аким олгъан эдилер.", "аким олгъан эдилер).")],
    (7, "143"): [("зан эткен эди.", "зан эткен эди).")],
    (7, "172"): [("чешит фикирлер бар.", "чешит фикирлер бар).")],
    (8, "40"): [("Эгер (имандан юзь чевирселер,", "Эгер (имандан) юзь чевирселер,")],
    (9, "32"): [
        ("агъызларынен (уфлеп,", "агъызларынен (уфлеп),"),
        ("«Аллаһнынъ ныры»", "«Аллаһнынъ нуры»"),
    ],
    (9, "70"): [("Луут Пейгъамбернинъ къавмыдыр.", "Луут Пейгъамбернинъ къавмыдыр).")],
    (9, "102"): [("(сеферден къайткъандан сонъ,", "(сеферден къайткъандан сонъ),")],
    (10, "20"): [("истесе, кечиктирир.", "истесе, кечиктирир).")],
    (10, "105"): [("(Аллаһнынъ бирлигини таныйыджы оларакъ,", "(Аллаһнынъ бирлигини таныйыджы) оларакъ,")],
    (11, "14"): [("Эгер (олар сизге", "Эгер (олар) сизге")],
    (11, "27"): [("(«Меле'») келимеси", "(«Меле'» келимеси")],
    (11, "44"): [("(Ниает: «Эй ер,", "(Ниает): «Эй ер,")],
    (12, "31"): [("(Къадынлар мейваларны кескенде,", "(Къадынлар мейваларны кескенде),")],
    (12, "43"): [("Мен (руяда еди", "Мен (руяда) еди")],
    (12, "102"): [("дегиль эдинъ) ки, буларны бильсенъ.", "дегиль эдинъ (ки, буларны бильсенъ).")],
    (13, "32"): [("насыл экен).", "насыл экен.")],
    (13, "34"): [("кимсе де ёкътыр).", "кимсе де ёкътыр.")],
    (14, "23"): [("(бир-бирилеринен расткелишкенде сёйлегенлери", "(бир-бирилеринен расткелишкенде) сёйлегенлери")],
    (15, "71"): [("(Тюшюнгенлеринъизни япаджакъ", "(Тюшюнгенлеринъизни) япаджакъ")],
    (17, "29"): [("отурырсынъ).", "отурырсынъ.")],
    (17, "69"): [("ёллап), узеринъизге", "ёллап, узеринъизге")],
    (17, "94"): [("инсанларнынъ (бунъа инанувларыны", "инсанларнынъ (бунъа) инанувларыны")],
    (17, "95"): [("бешер пейгъамберим) дегендже,", "бешер пейгъамберим» дегендже,")],
    (21, "5"): [("(Эгер ойле олмаса (бизге)", "(Эгер ойле олмаса) (бизге)")],
    (22, "5"): [
        ("(сонъра белли олгъан джанлы эт парчасындан) азалары вакъты иле етильген хамиледен)", "(сонъра белли олгъан) джанлы эт парчасындан (азалары вакъты иле етильген хамиледен)"),
    ],
    (24, "31"): [("аякъларыдыр.", "аякъларыдыр).")],
    (24, "36"): [("Аллаһ (о эвлернинъ юджелювине", "Аллаһ (о эвлернинъ) юджелювине")],
    (24, "47"): [("(Базы инсанлар: «Аллаһкъа", "(Базы инсанлар): «Аллаһкъа")],
    (28, "31"): [
        ("Муса (аткъан таягъы", "Муса (аткъан) таягъы"),
        ("олгъанлардансынъ») буюрылды).", "олгъанлардансынъ» (буюрылды)."),
    ],
    (32, "23"): [("хидает ребери яптыкъ).", "хидает ребери яптыкъ.")],
    (34, "14"): [("къалмаз эдилер.)", "къалмаз эдилер.")],
    (34, "15"): [
        ("(Оларгъа: (Раббинъизнинъ рызкъындан ашанъ ве Онъа шукюр этинъ. Иште, гузель бир мемлекет ве чокъ багъышлайыджы бир Рабб!", "(Оларгъа): «Раббинъизнинъ рызкъындан ашанъ ве Онъа шукюр этинъ. Иште, гузель бир мемлекет ве чокъ багъышлайыджы бир Рабб!»"),
    ],
    (37, "54-55"): [
        ("о ерде олгъанларгъа: «Сиз", "о ерде олгъанларгъа): «Сиз"),
    ],
    (38, "59"): [("юзю корьмесин, дерлер).", "юзю корьмесин», дерлер.")],
    (39, "15"): [("Эй, Аллаһкъа ортакъ къошкъанлар!):", "(Эй, Аллаһкъа ортакъ къошкъанлар!):")],
    (44, "47-50"): [
        ("Тутынъ оны! Джеэннемнинъ ортасына сюйрекленъ! Сонъ башына азап оларакъ, къайнагъан сув тёкюнъ!) ве денъ ки: (Тат, бакъайыкъ. Къана, сен озюнъдже усьтюн эдинъ, шерефли эдинъ! Иште, бу, шубеленип тургъан шейинъиздир.", "«Тутынъ оны! Джеэннемнинъ ортасына сюйрекленъ! Сонъ башына азап оларакъ, къайнагъан сув тёкюнъ!» ве денъ ки: «Тат, бакъайыкъ. Къана, сен озюнъдже усьтюн эдинъ, шерефли эдинъ! Иште, бу, шубеленип тургъан шейинъиздир»."),
    ],
    (52, "23"): [("иляхий бир икрамдыр.", "иляхий бир икрамдыр).")],
}

LIST_MARKER_RE = re.compile(r"(?:(?<=^)|(?<=[\s:;«.(]))(?:[абвгдеa-e]|[1-9])\)\.?(?=\s)")

CLAUSE_DASH_WRAPS = (
    ("къадар", "джюнюп"),
    ("дие", "весиле"),
    ("себебинден", "сокътыгъымыз"),
    ("олмадан", "озюнден"),
)

LATIN_HOMOGLYPHS_IN_CYR = str.maketrans({
    "a": "а",
    "c": "с",
    "e": "е",
    "o": "о",
    "A": "А",
    "C": "С",
    "E": "Е",
    "O": "О",
    "h": "һ",
    "H": "Һ",
})

CYR_WORD_TOKEN_RE = re.compile(r"[А-Яа-яЁёҺһA-Za-z]+(?:'[А-Яа-яЁёҺһA-Za-z]+)*")


def _apply_case_template(original: str, corrected_lower: str) -> str:
    if original.isupper():
        return corrected_lower.upper()
    if original[0].isupper() and (len(original) == 1 or not original[1:].isupper()):
        return corrected_lower[0].upper() + corrected_lower[1:]
    return corrected_lower


def _clean_cyrillic_token(token: str) -> str:
    # Keep Roman numerals (I, II, III, IV, V...) untouched!
    if re.match(r"^[IVXLCDM]+$", token):
        return token
    norm = token.translate(LATIN_HOMOGLYPHS_IN_CYR)
    low = norm.lower()
    if low in EXACT_WORD_ERRATA:
        return _apply_case_template(norm, EXACT_WORD_ERRATA[low])
    for bad_pref, good_pref in STEM_PREFIX_ERRATA:
        if low.startswith(bad_pref):
            if bad_pref == "мунафык" and low.startswith("мунафыкъ"):
                continue
            fixed_low = good_pref + low[len(bad_pref) :]
            return _apply_case_template(norm, fixed_low)
    return norm


def join_pdf_lines(lines: list[str]) -> str:
    """Join wrapped PDF lines while preserving true hyphenated compounds and clause dashes."""
    raw = "\n".join(ln.strip() for ln in lines if ln.strip())
    raw = raw.replace("’", "'").replace("‘", "'").replace("–", "-")

    for left_w, right_w in CLAUSE_DASH_WRAPS:
        raw = re.sub(
            rf"\b({re.escape(left_w)})-\n\s*({re.escape(right_w)})\b",
            r"\1 - \2",
            raw,
            flags=re.IGNORECASE,
        )

    raw = re.sub(
        r"([А-Яа-яЁёҺһA-Za-z']+)-\n\s*([А-Яа-яЁёҺһA-Za-z']+)",
        r"\1-\2",
        raw,
    )
    raw = re.sub(r"\s+", " ", raw).strip()
    return raw


def clean_pdf_cyrillic_text(
    text: str,
    *,
    surah_id: int | None = None,
    verse_key: str | None = None,
) -> str:
    """Normalize Cyrillic text from the 2005 PDF and apply verified errata + paren fixes."""
    cleaned = text.replace("’", "'").replace("‘", "'")
    cleaned = CYR_WORD_TOKEN_RE.sub(lambda m: _clean_cyrillic_token(m.group(0)), cleaned)
    cleaned = cleaned.replace("Аллаһнынъ ныры", "Аллаһнынъ нуры")

    if surah_id is not None and verse_key is not None:
        patches = PAREN_SURGICAL_PATCHES.get((surah_id, verse_key), [])
        for target, replacement in patches:
            cleaned = cleaned.replace(target, replacement)

    return cleaned


def check_balanced_parens(text: str) -> tuple[int, bool]:
    """Return (final_depth, went_negative) after masking list markers like `a).` or `1).`."""
    masked = LIST_MARKER_RE.sub(lambda m: "_" * len(m.group(0)), text)
    depth = 0
    went_neg = False
    for ch in masked:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth < 0:
                went_neg = True
    return depth, went_neg


# ---------------------------------------------------------------------------
# 2. Crimean Tatar Cyrillic -> Latin Orthography Engine
# ---------------------------------------------------------------------------

CYR_VOWELS = set("аэыиоуяеёюАЭЫИОУЯЕЁЮ")

FRONT_YO_PREFIXES = ("ёнел", "ёнет", "ёрюнг")

BACK_YU_PREFIXES = (
    "юкъар",
    "юкъу",
    "юкъла",
    "юрт",
    "юсуф",
    "юнус",
    "ют",
    "юмша",
    "юмуш",
    "юмгъ",
    "юма",
    "юмрукъ",
    "ювгъ",
    "ювун",
    "ювыл",
    "юва",
    "ювув",
)

FRONT_POSTVOWEL_YU_PREFIXES = ("буюк", "буюг", "деюв", "еюв", "кеюв")

FRONT_O_PREFIXES = (
    "коре",
    "корм",
    "корс",
    "кори",
    "корь",
    "бойле",
    "ойле",
    "шойле",
    "кокт",
    "кокл",
    "кокк",
    "кокн",
    "кокс",
    "кокрек",
    "огг",
    "огд",
    "огл",
    "огрет",
    "огрен",
    "огей",
    "оледж",
    "олмей",
    "ози",
    "озл",
    "озек",
    "озен",
    "козет",
    "козин",
    "боден",
    "одер",
    "одем",
    "одеп",
    "оден",
    "одев",
    "одель",
    "одет",
    "одег",
    "одес",
    "кошк",
    "копек",
    "чоккен",
    "котер",
    "гогерджин",
    "коме",
    "комм",
    "комг",
    "комс",
    "костер",
    "коше",
    "окче",
    "опке",
    "ботен",
    "толле",
    "орте",
    "орне",
    "тоше",
    "осер",
    "коче",
    "кочк",
    "бодже",
    "койн",
    "койл",
    "ошек",
    "оксюз",
    "болю",
    "больг",
)
FRONT_O_EXACT = {"кок", "ог", "оз", "коз", "кой", "кочь", "коме", "оде"}

FRONT_U_PREFIXES = (
    "шубе",
    "шукр",
    "шурет",
    "гузель",
    "гузел",
    "гудж",
    "гунях",
    "гунах",
    "узери",
    "узерл",
    "узере",
    "му'мин",
    "мушрик",
    "муддет",
    "мукяфат",
    "мукятеб",
    "муим",
    "мужде",
    "мукеллеф",
    "мукеммел",
    "мукеррем",
    "мунеззех",
    "мутешааби",
    "мутхиш",
    "мудхиш",
    "мундеридж",
    "муэссис",
    "муфессир",
    "мункир",
    "муртед",
    "мусбет",
    "муштерек",
    "муессер",
    "мутедиль",
    "мутевелли",
    "мусриф",
    "муур",
    "уммет",
    "уммий",
    "уммиий",
    "укми",
    "укмин",
    "урриет",
    "уджрет",
    "уджре",
    "уджейре",
    "ушен",
    "уфле",
    "уйле",
    "учер",
    "кунн",
    "куни",
    "кунеш",
    "куреш",
    "купе",
    "куле",
    "кучи",
    "куфр",
    "курси",
    "букк",
    "буке",
    "букм",
    "бугри",
    "сутлер",
    "суннет",
    "сулейман",
    "бунямин",
    "зумер",
    "рузгяр",
    "чурю",
    "сурю",
)


def _has_post_consonant_yu_yo(rest: str) -> bool:
    """True only when ю/ё appears after a consonant (representing /ü/ or /ö/), not post-vowel /yu/."""
    for idx, ch in enumerate(rest):
        if ch in ("ю", "ё"):
            if idx > 0 and rest[idx - 1] not in CYR_VOWELS and rest[idx - 1] not in ("ь", "ъ", "'"):
                return True
    return False


def _should_front_first_o(lw: str, onset: str, rest: str) -> bool:
    if onset.endswith(("къ", "гъ")):
        return False
    if re.match(r"^[^аэыиоуяеёю]*ь", rest) or _has_post_consonant_yu_yo(rest):
        return True
    if lw in FRONT_O_EXACT or lw.startswith(FRONT_O_PREFIXES):
        return True
    return False


def _should_front_first_u(lw: str, onset: str, rest: str) -> bool:
    if onset.endswith(("къ", "гъ")) or lw.startswith(("бугун", "мусульман")):
        return False
    if lw.startswith(FRONT_POSTVOWEL_YU_PREFIXES):
        return True
    if re.match(r"^[^аэыиоуяеёю]*ь", rest) or _has_post_consonant_yu_yo(rest):
        return True
    if lw.startswith(FRONT_U_PREFIXES):
        return True
    return False


def _match_digraph_case(first_ch: str, next_chars: str, lower_out: str, title_out: str, upper_out: str) -> str:
    if not first_ch.isupper():
        return lower_out
    has_upper_neighbor = any(c.isupper() for c in next_chars if c.isalpha())
    has_lower_neighbor = any(c.islower() for c in next_chars if c.isalpha())
    if has_upper_neighbor and not has_lower_neighbor:
        return upper_out
    return title_out


def _transliterate_cyr_word(word: str) -> str:
    lw = word.lower()

    front_first_vowel = False
    first_vowel_idx = -1
    for idx, ch in enumerate(lw):
        if ch in "аэыиоуяеёю":
            first_vowel_idx = idx
            if ch == "о":
                front_first_vowel = _should_front_first_o(lw, lw[:idx], lw[idx + 1 :])
            elif ch == "у":
                front_first_vowel = _should_front_first_u(lw, lw[:idx], lw[idx + 1 :])
            break

    out: list[str] = []
    i = 0
    n = len(word)
    all_caps = sum(1 for c in word if c.isalpha()) > 1 and all(
        not c.islower() for c in word if c.isalpha()
    )

    while i < n:
        ch = word[i]
        lch = ch.lower()
        nxt = word[i + 1] if i + 1 < n else ""
        lnxt = nxt.lower()
        prev = word[i - 1] if i > 0 else ""
        lprev = prev.lower()

        # 1. Digraphs: гъ, къ, нъ, дж
        if lch == "г" and lnxt == "ъ":
            out.append("Ğ" if ch.isupper() else "ğ")
            i += 2
            continue
        if lch == "к" and lnxt == "ъ":
            out.append("Q" if ch.isupper() else "q")
            i += 2
            continue
        if lch == "н" and lnxt == "ъ":
            out.append("Ñ" if ch.isupper() else "ñ")
            i += 2
            continue
        if lch == "д" and lnxt == "ж":
            out.append("C" if ch.isupper() else "c")
            i += 2
            continue

        prev_is_digraph_consonant = (
            i >= 2 and lw[i - 1] == "ъ" and lw[i - 2] in ("г", "к", "н")
        )
        prev_is_vowel_or_start = (
            i == 0
            or lprev in CYR_VOWELS
            or lprev == "ь"
            or (lprev == "ъ" and not prev_is_digraph_consonant)
            or lprev == "'"
        )

        # 2. Vowels
        if lch == "а":
            out.append("A" if ch.isupper() else "a")
        elif lch == "э":
            out.append("E" if ch.isupper() else "e")
        elif lch == "ы":
            out.append("I" if ch.isupper() else "ı")
        elif lch == "и":
            out.append("İ" if ch.isupper() else "i")
        elif lch == "о":
            is_ö = i == first_vowel_idx and front_first_vowel
            out.append(("Ö" if ch.isupper() else "ö") if is_ö else ("O" if ch.isupper() else "o"))
        elif lch == "у":
            is_ü = (i == first_vowel_idx and front_first_vowel) or (
                lw.startswith("бугун") and i > 2
            )
            out.append(("Ü" if ch.isupper() else "ü") if is_ü else ("U" if ch.isupper() else "u"))
        elif lch == "е":
            if i == 0 or lprev in CYR_VOWELS or lprev == "ь" or (lprev == "ъ" and not prev_is_digraph_consonant):
                out.append(_match_digraph_case(ch, word, "ye", "Ye", "YE"))
            else:
                out.append("E" if ch.isupper() else "e")
        elif lch == "ё":
            if prev_is_vowel_or_start:
                if lw.startswith(FRONT_YO_PREFIXES):
                    out.append(_match_digraph_case(ch, word, "yö", "Yö", "YÖ"))
                else:
                    out.append(_match_digraph_case(ch, word, "yo", "Yo", "YO"))
            else:
                out.append("Ö" if ch.isupper() else "ö")
        elif lch == "ю":
            if i == 0:
                if lw.startswith(BACK_YU_PREFIXES):
                    out.append(_match_digraph_case(ch, word, "yu", "Yu", "YU"))
                else:
                    out.append(_match_digraph_case(ch, word, "yü", "Yü", "YÜ"))
            elif lprev in CYR_VOWELS or lprev == "ь" or (lprev == "ъ" and not prev_is_digraph_consonant):
                if lw.startswith(FRONT_POSTVOWEL_YU_PREFIXES) or lprev in ("е", "и", "ь"):
                    out.append(_match_digraph_case(ch, word, "yü", "Yü", "YÜ"))
                else:
                    out.append(_match_digraph_case(ch, word, "yu", "Yu", "YU"))
            else:
                out.append("Ü" if ch.isupper() else "ü")
        elif lch == "я":
            if prev_is_vowel_or_start:
                out.append(_match_digraph_case(ch, word, "ya", "Ya", "YA"))
            elif lprev in ("л", "к", "г", "х") and not lw.startswith(("бунямин", "феряд", "рия")):
                out.append("Â" if (ch.isupper() or all_caps) else "â")
            else:
                out.append(_match_digraph_case(ch, word, "ya", "Ya", "YA"))

        # 3. Consonants & signs
        elif lch == "б":
            out.append("B" if ch.isupper() else "b")
        elif lch == "в":
            out.append("V" if ch.isupper() else "v")
        elif lch == "г":
            out.append("G" if ch.isupper() else "g")
        elif lch == "д":
            out.append("D" if ch.isupper() else "d")
        elif lch == "ж":
            out.append("J" if ch.isupper() else "j")
        elif lch == "з":
            out.append("Z" if ch.isupper() else "z")
        elif lch == "й":
            out.append("Y" if ch.isupper() else "y")
        elif lch == "к":
            out.append("K" if ch.isupper() else "k")
        elif lch == "л":
            out.append("L" if ch.isupper() else "l")
        elif lch == "м":
            out.append("M" if ch.isupper() else "m")
        elif lch == "н":
            out.append("N" if ch.isupper() else "n")
        elif lch == "п":
            out.append("P" if ch.isupper() else "p")
        elif lch == "р":
            out.append("R" if ch.isupper() else "r")
        elif lch == "с":
            out.append("S" if ch.isupper() else "s")
        elif lch == "т":
            out.append("T" if ch.isupper() else "t")
        elif lch == "ф":
            out.append("F" if ch.isupper() else "f")
        elif lch in ("х", "һ"):
            out.append("H" if ch.isupper() else "h")
        elif lch == "ц":
            out.append(_match_digraph_case(ch, word, "ts", "Ts", "TS"))
        elif lch == "ч":
            out.append("Ç" if ch.isupper() else "ç")
        elif lch == "ш":
            out.append("Ş" if ch.isupper() else "ş")
        elif lch == "щ":
            out.append(_match_digraph_case(ch, word, "şç", "Şç", "ŞÇ"))
        elif lch == "ъ":
            if i + 1 < n and lw[i + 1] not in ("я", "е", "ё", "ю"):
                out.append("'")
        elif lch == "ь":
            pass
        else:
            out.append(ch)

        i += 1

    return "".join(out)


CYR_WORD_FOR_LAT_RE = re.compile(r"[А-Яа-яЁёҺһ]+(?:'[А-Яа-яЁёҺһ]+)*")


def cyrillic_to_latin_crh(text: str) -> str:
    """Convert Crimean Tatar Cyrillic text into standard Qırımtatar Latin orthography."""
    text = text.replace("’", "'").replace("‘", "'")
    return CYR_WORD_FOR_LAT_RE.sub(lambda m: _transliterate_cyr_word(m.group(0)), text)


# ---------------------------------------------------------------------------
# 3. Crimean Tatar Latin -> Cyrillic Converter
# ---------------------------------------------------------------------------

LAT_VOWELS = set("aAeEiIıİoOuUöÖüÜâÂ")

LAT_SINGLE_MAP: dict[str, str] = {
    "a": "а", "A": "А",
    "e": "е", "E": "Е",
    "i": "и", "İ": "И",
    "ı": "ы", "I": "Ы",
    "o": "о", "O": "О",
    "u": "у", "U": "У",
    "â": "я", "Â": "Я",
    "b": "б", "B": "Б",
    "c": "дж", "C": "Дж",
    "ç": "ч", "Ç": "Ч",
    "d": "д", "D": "Д",
    "f": "ф", "F": "Ф",
    "g": "г", "G": "Г",
    "ğ": "гъ", "Ğ": "Гъ",
    "h": "х", "H": "Х",
    "j": "ж", "J": "Ж",
    "k": "к", "K": "К",
    "l": "л", "L": "Л",
    "m": "м", "M": "М",
    "n": "н", "N": "Н",
    "ñ": "нъ", "Ñ": "Нъ",
    "p": "п", "P": "П",
    "q": "къ", "Q": "Къ",
    "r": "р", "R": "Р",
    "s": "с", "S": "С",
    "ş": "ш", "Ş": "Ш",
    "t": "т", "T": "Т",
    "v": "в", "V": "В",
    "y": "й", "Y": "Й",
    "z": "з", "Z": "З",
}

LAT_WORD_RE = re.compile(r"[A-Za-zÇçĞğİıÑñÖöŞşÜüÂâ]+(?:'[A-Za-zÇçĞğİıÑñÖöŞşÜüÂâ]+)*")


def _transliterate_lat_word_to_cyr(word: str) -> str:
    all_caps = sum(1 for c in word if c.isalpha()) > 1 and all(
        not c.islower() for c in word if c.isalpha()
    )
    out: list[str] = []
    i = 0
    n = len(word)
    later_has_front_rounded = any(c in "öÖüÜ" for c in word[2:])

    while i < n:
        ch = word[i]
        lch = ch.lower()
        nxt = word[i + 1] if i + 1 < n else ""
        lnxt = nxt.lower()
        prev = word[i - 1] if i > 0 else ""

        if lch == "y" and lnxt in ("a", "e", "o", "ö", "u", "ü"):
            if lnxt == "a":
                out.append("Я" if ch.isupper() else "я")
            elif lnxt == "e":
                out.append("Е" if ch.isupper() else "е")
            elif lnxt in ("o", "ö"):
                out.append("Ё" if ch.isupper() else "ё")
            elif lnxt in ("u", "ü"):
                out.append("Ю" if ch.isupper() else "ю")
            i += 2
            continue

        if lch == "e" and (i == 0 or prev in LAT_VOWELS or prev == "'"):
            out.append("Э" if ch.isupper() else "э")
            i += 1
            continue

        if lch in ("ö", "ü"):
            is_first_syllable = not any(c in LAT_VOWELS for c in word[:i])
            if is_first_syllable:
                base = ("О" if ch.isupper() else "о") if lch == "ö" else ("У" if ch.isupper() else "у")
                out.append(base)
                if not later_has_front_rounded and i + 1 < n and word[i + 1] not in LAT_VOWELS:
                    coda = word[i + 1]
                    after_coda = word[i + 2] if i + 2 < n else ""
                    if coda.lower() in ("z", "l", "r", "s", "t", "ç", "k", "p", "n") and (
                        after_coda == "" or after_coda not in LAT_VOWELS
                    ):
                        mapped_coda = LAT_SINGLE_MAP.get(coda, coda)
                        if all_caps:
                            mapped_coda = mapped_coda.upper()
                        out.append(mapped_coda)
                        out.append("Ь" if all_caps else "ь")
                        i += 2
                        continue
            else:
                out.append(("Ё" if ch.isupper() else "ё") if lch == "ö" else ("Ю" if ch.isupper() else "ю"))
            i += 1
            continue

        mapped = LAT_SINGLE_MAP.get(ch, ch)
        if all_caps and len(mapped) > 1:
            mapped = mapped.upper()
        out.append(mapped)
        i += 1

    return "".join(out)


def latin_to_cyrillic_crh(text: str) -> str:
    """Convert Crimean Tatar Latin text into Cyrillic orthography."""
    return LAT_WORD_RE.sub(lambda m: _transliterate_lat_word_to_cyr(m.group(0)), text)
