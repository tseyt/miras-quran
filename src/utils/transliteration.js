const RU_MAP = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ъ': '', 'ы': 'y', 'ь': "'", 'э': 'e', 'ю': 'yu', 'я': 'ya',
    'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'YO', 'Ж': 'ZH', 'З': 'Z', 'И': 'I', 'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'KH', 'Ц': 'TS', 'Ч': 'CH', 'Ш': 'SH', 'Щ': 'SHCH', 'Ъ': '', 'Ы': 'Y', 'Ь': "'", 'Э': 'E', 'Ю': 'YU', 'Я': 'YA'
};

const UA_MAP = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'h', 'ґ': 'g', 'д': 'd', 'е': 'e', 'є': 'ye', 'ж': 'zh', 'з': 'z', 'и': 'y', 'і': 'i', 'ї': 'yi', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ь': "'", 'ю': 'yu', 'я': 'ya',
    'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'H', 'Ґ': 'G', 'Д': 'D', 'Е': 'E', 'Є': 'YE', 'Ж': 'ZH', 'З': 'Z', 'И': 'Y', 'І': 'I', 'Ї': 'YI', 'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'KH', 'Ц': 'TS', 'Ч': 'CH', 'Ш': 'SH', 'Щ': 'SHCH', 'Ь': "'", 'Ю': 'YU', 'Я': 'YA'
};

// CRH Latin to Cyrillic mapping (based on official 1992/2012/2021 standards)
// Multi-character sequences must be processed first to avoid partial matches
const CRH_LAT_TO_CYR_MULTI = [
    // Digraphs - process longer matches first
    ['Ğ', 'Гъ'], ['ğ', 'гъ'],
    ['Q', 'Къ'], ['q', 'къ'],
    ['Ñ', 'Нъ'], ['ñ', 'нъ'],
    // Şç for щ
    ['Şç', 'Щ'], ['şç', 'щ'],
    // Ts for ц
    ['Ts', 'Ц'], ['ts', 'ц'],
];

const CRH_LAT_TO_CYR_SINGLE = {
    // Vowels
    'a': 'а', 'A': 'А',
    'e': 'е', 'E': 'Е',
    'i': 'и', 'I': 'И', 'İ': 'И', 'ı': 'ы',
    'o': 'о', 'O': 'О',
    'u': 'у', 'U': 'У',
    'ö': 'о', 'Ö': 'О',
    'ü': 'у', 'Ü': 'У',
    'â': 'я', 'Â': 'Я',
    // Consonants
    'b': 'б', 'B': 'Б',
    'c': 'дж', 'C': 'Дж',
    'ç': 'ч', 'Ç': 'Ч',
    'd': 'д', 'D': 'Д',
    'f': 'ф', 'F': 'Ф',
    'g': 'г', 'G': 'Г',
    'h': 'х', 'H': 'Х',
    'j': 'ж', 'J': 'Ж',
    'k': 'к', 'K': 'К',
    'l': 'л', 'L': 'Л',
    'm': 'м', 'M': 'М',
    'n': 'н', 'N': 'Н',
    'p': 'п', 'P': 'П',
    'r': 'р', 'R': 'Р',
    's': 'с', 'S': 'С',
    'ş': 'ш', 'Ş': 'Ш',
    't': 'т', 'T': 'Т',
    'v': 'в', 'V': 'В',
    'y': 'й', 'Y': 'Й',
    'z': 'з', 'Z': 'З',
    "'": 'ь',
};

/**
 * Transliterate CRH Latin text to Cyrillic
 */
function transliterateCrhToCyrillic(text) {
    if (!text) return text;
    let result = text;

    // First, replace multi-character sequences
    for (const [lat, cyr] of CRH_LAT_TO_CYR_MULTI) {
        result = result.split(lat).join(cyr);
    }

    // Then replace single characters
    result = result.split('').map(char => CRH_LAT_TO_CYR_SINGLE[char] || char).join('');

    return result;
}

export function transliterate(text, lang) {
    if (!text) return text;
    const map = lang === 'ru' ? RU_MAP : (lang === 'ua' ? UA_MAP : null);
    if (!map) return text;

    return text.split('').map(char => map[char] || char).join('');
}

/**
 * Convert CRH text between scripts
 * @param {string} text - Input text
 * @param {boolean} toCyrillic - If true, convert Latin to Cyrillic
 */
export function transliterateCrh(text, toCyrillic = false) {
    if (!text) return text;
    if (toCyrillic) {
        return transliterateCrhToCyrillic(text);
    }
    return text;
}
