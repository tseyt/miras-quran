const RU_MAP = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ъ': '', 'ы': 'y', 'ь': "'", 'э': 'e', 'ю': 'yu', 'я': 'ya',
    'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'YO', 'Ж': 'ZH', 'З': 'Z', 'И': 'I', 'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'KH', 'Ц': 'TS', 'Ч': 'CH', 'Ш': 'SH', 'Щ': 'SHCH', 'Ъ': '', 'Ы': 'Y', 'Ь': "'", 'Э': 'E', 'Ю': 'YU', 'Я': 'YA'
};

const UA_MAP = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'h', 'ґ': 'g', 'д': 'd', 'е': 'e', 'є': 'ye', 'ж': 'zh', 'з': 'z', 'и': 'y', 'і': 'i', 'ї': 'yi', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ь': "'", 'ю': 'yu', 'я': 'ya',
    'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'H', 'Ґ': 'G', 'Д': 'D', 'Е': 'E', 'Є': 'YE', 'Ж': 'ZH', 'З': 'Z', 'И': 'Y', 'І': 'I', 'Ї': 'YI', 'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'KH', 'Ц': 'TS', 'Ч': 'CH', 'Ш': 'SH', 'Щ': 'SHCH', 'Ь': "'", 'Ю': 'YU', 'Я': 'YA'
};

const CRH_LAT_VOWELS = new Set(['a', 'e', 'i', 'ı', 'o', 'ö', 'u', 'ü', 'â', 'î', 'û']);
const CRH_FRONT_VOWELS = new Set(['e', 'i', 'ö', 'ü', 'â', 'î']);
const CRH_DENTAL_CONSONANTS = new Set(['d', 't', 's', 'z', 'ç', 'ş', 'l', 'n', 'r']);
const CRH_SOFT_CODA_CONSONANTS = new Set(['z', 'l', 'n', 'r', 's', 'ş', 'ç', 't']);

const CRH_LAT_TO_CYR_CONSONANTS = {
    'b': 'б',
    'c': 'дж',
    'ç': 'ч',
    'd': 'д',
    'f': 'ф',
    'g': 'г',
    'h': 'х',
    'j': 'ж',
    'k': 'к',
    'l': 'л',
    'm': 'м',
    'n': 'н',
    'p': 'п',
    'r': 'р',
    's': 'с',
    'ş': 'ш',
    't': 'т',
    'v': 'в',
    'y': 'й',
    'z': 'з',
};

function trLowerChar(ch) {
    if (ch === 'İ') return 'i';
    if (ch === 'I') return 'ı';
    return ch.toLowerCase();
}

function isUpperChar(ch) {
    const low = trLowerChar(ch);
    return ch !== low;
}

function applyCrhCase(cyrLower, sampleChar, isAllCaps) {
    if (isAllCaps) {
        return cyrLower.toUpperCase();
    }
    if (isUpperChar(sampleChar)) {
        return cyrLower[0].toUpperCase() + cyrLower.slice(1);
    }
    return cyrLower;
}

function transliterateCrhWordLatToCyr(word) {
    const lettersOnly = word.replace(/'/g, '');
    const isAllCaps =
        lettersOnly.length > 1 &&
        [...lettersOnly].every(ch => !isUpperChar(ch) ? false : true);

    const chars = [...word];
    const n = chars.length;
    const out = [];
    let seenVowel = false;
    let lastVowelFront = false;
    let i = 0;

    while (i < n) {
        const ch = chars[i];
        if (ch === "'") {
            out.push("'");
            i++;
            continue;
        }

        const low = trLowerChar(ch);
        const nextLow = i + 1 < n && chars[i + 1] !== "'" ? trLowerChar(chars[i + 1]) : '';

        // 1. Multi-character consonant digraphs: şç -> щ, ts -> ц, ğ -> гъ, q -> къ, ñ -> нъ
        if (low === 'ş' && nextLow === 'ç') {
            out.push(applyCrhCase('щ', ch, isAllCaps));
            i += 2;
            continue;
        }
        if (low === 't' && nextLow === 's') {
            out.push(applyCrhCase('ц', ch, isAllCaps));
            i += 2;
            continue;
        }
        if (low === 'ğ') {
            out.push(applyCrhCase('гъ', ch, isAllCaps));
            i++;
            continue;
        }
        if (low === 'q') {
            out.push(applyCrhCase('къ', ch, isAllCaps));
            i++;
            continue;
        }
        if (low === 'ñ') {
            out.push(applyCrhCase('нъ', ch, isAllCaps));
            i++;
            continue;
        }

        // 2. Iotated sequences: ya/yâ -> я, ye -> е, yo/yö -> ё, yu/yü -> ю
        if (low === 'y' && CRH_LAT_VOWELS.has(nextLow)) {
            if (nextLow === 'a' || nextLow === 'â') {
                out.push(applyCrhCase('я', ch, isAllCaps));
                seenVowel = true;
                lastVowelFront = nextLow === 'â';
                i += 2;
                continue;
            }
            if (nextLow === 'e') {
                out.push(applyCrhCase('е', ch, isAllCaps));
                seenVowel = true;
                lastVowelFront = true;
                i += 2;
                continue;
            }
            if (nextLow === 'o' || nextLow === 'ö') {
                out.push(applyCrhCase('ё', ch, isAllCaps));
                seenVowel = true;
                lastVowelFront = nextLow === 'ö';
                i += 2;
                continue;
            }
            if (nextLow === 'u' || nextLow === 'ü') {
                out.push(applyCrhCase('ю', ch, isAllCaps));
                seenVowel = true;
                lastVowelFront = nextLow === 'ü';
                i += 2;
                continue;
            }
        }

        // 3. Vowels
        if (CRH_LAT_VOWELS.has(low)) {
            const prevChar = i > 0 ? chars[i - 1] : '';
            const prevLow = prevChar && prevChar !== "'" ? trLowerChar(prevChar) : '';

            if (low === 'a') {
                out.push(applyCrhCase('а', ch, isAllCaps));
                seenVowel = true;
                lastVowelFront = false;
                i++;
                continue;
            }
            if (low === 'â') {
                const cyrV = i === 0 || prevChar === "'" ? 'а' : 'я';
                out.push(applyCrhCase(cyrV, ch, isAllCaps));
                seenVowel = true;
                lastVowelFront = true;
                i++;
                continue;
            }
            if (low === 'e') {
                const isInitialOrHiatus = i === 0 || prevChar === "'" || CRH_LAT_VOWELS.has(prevLow);
                out.push(applyCrhCase(isInitialOrHiatus ? 'э' : 'е', ch, isAllCaps));
                seenVowel = true;
                lastVowelFront = true;
                i++;
                continue;
            }
            if (low === 'i' || low === 'î') {
                out.push(applyCrhCase('и', ch, isAllCaps));
                seenVowel = true;
                lastVowelFront = true;
                i++;
                continue;
            }
            if (low === 'ı') {
                out.push(applyCrhCase('ы', ch, isAllCaps));
                seenVowel = true;
                lastVowelFront = false;
                i++;
                continue;
            }
            if (low === 'o') {
                out.push(applyCrhCase('о', ch, isAllCaps));
                seenVowel = true;
                lastVowelFront = false;
                i++;
                continue;
            }
            if (low === 'u' || low === 'û') {
                out.push(applyCrhCase('у', ch, isAllCaps));
                seenVowel = true;
                lastVowelFront = false;
                i++;
                continue;
            }
            if (low === 'ö' || low === 'ü') {
                const isO = low === 'ö';
                const restStr = chars.slice(i + 1).map(trLowerChar).join('');
                const hasLaterRoundedFront = /[öü]/.test(restStr);

                if (seenVowel || CRH_DENTAL_CONSONANTS.has(prevLow)) {
                    out.push(applyCrhCase(isO ? 'ё' : 'ю', ch, isAllCaps));
                    seenVowel = true;
                    lastVowelFront = true;
                    i++;
                    continue;
                }

                // Initial or post-velar/labial first-syllable ö/ü -> о/у (+ coda ь when needed)
                out.push(applyCrhCase(isO ? 'о' : 'у', ch, isAllCaps));
                seenVowel = true;
                lastVowelFront = true;

                // Check if closed syllable coda consonant needs soft sign `ь` (e.g. öz->озь, kün->кунь, köster->косьтер, mülk->мульк)
                const afterCodaLow = i + 2 < n && chars[i + 2] !== "'" ? trLowerChar(chars[i + 2]) : '';
                const codaClosesSyllable =
                    i + 1 < n &&
                    CRH_SOFT_CODA_CONSONANTS.has(nextLow) &&
                    (i + 2 === n || (!CRH_LAT_VOWELS.has(afterCodaLow) && chars[i + 2] !== "'"));

                if (codaClosesSyllable) {
                    const codaCyr = CRH_LAT_TO_CYR_CONSONANTS[nextLow] || nextLow;
                    out.push(applyCrhCase(codaCyr, chars[i + 1], isAllCaps));
                    out.push(isAllCaps ? 'Ь' : 'ь');
                    i += 2;
                    continue;
                }

                i++;
                continue;
            }
        }

        // 4. Consonants (including word-final front `-l` -> `-ль`, e.g., güzel -> гузель, degil -> дегиль)
        const mapped = CRH_LAT_TO_CYR_CONSONANTS[low];
        if (mapped) {
            out.push(applyCrhCase(mapped, ch, isAllCaps));
            if (low === 'l' && i === n - 1 && seenVowel && lastVowelFront) {
                out.push(isAllCaps ? 'Ь' : 'ь');
            }
        } else {
            out.push(ch);
        }
        i++;
    }

    return out.join('');
}

/**
 * Transliterate CRH Latin text to standard CRH Cyrillic
 */
export function transliterateCrhToCyrillic(text) {
    if (text === null || text === undefined || text === '') return '';
    const str = String(text);
    return str.replace(
        /[A-Za-zÇçĞğİıÑñÖöŞşÜüÂâÎîÛû]+(?:'[A-Za-zÇçĞğİıÑñÖöŞşÜüÂâÎîÛû]+)*/g,
        word => transliterateCrhWordLatToCyr(word)
    );
}

/**
 * Transliterate CRH Cyrillic text to standard CRH Latin
 */
export function transliterateCrhToLatin(text) {
    if (text === null || text === undefined || text === '') return '';
    const str = String(text);
    if (!/[\u0400-\u04FF]/.test(str)) return str;
    return str.replace(/[\u0400-\u04FFhH]+(?:'[\u0400-\u04FFhH]+)*/g, word => {
        const wLow = word.toLowerCase();
        const isFront =
            /[еиэь]/.test(wLow) ||
            (/[бвгджзклмнпрстфхцчшщ][ёюя]/.test(wLow) && !/[ыъ]/.test(wLow)) ||
            wLow.startsWith('буюк') ||
            wLow.startsWith('буюг') ||
            wLow.startsWith('бугунь');

        const isAllCaps = word.length > 1 && word === word.toUpperCase() && word !== word.toLowerCase();
        const chars = [...word];
        const out = [];
        let seenVowel = false;

        for (let i = 0; i < chars.length; i++) {
            const ch = chars[i];
            const low = ch.toLowerCase();
            const nextLow = i + 1 < chars.length ? chars[i + 1].toLowerCase() : '';
            const prevLow = i > 0 ? chars[i - 1].toLowerCase() : '';

            if (low === 'г' && nextLow === 'ъ') {
                out.push(ch !== low ? 'Ğ' : 'ğ');
                i++;
                continue;
            }
            if (low === 'к' && nextLow === 'ъ') {
                out.push(ch !== low ? 'Q' : 'q');
                i++;
                continue;
            }
            if (low === 'н' && nextLow === 'ъ') {
                out.push(ch !== low ? 'Ñ' : 'ñ');
                i++;
                continue;
            }
            if (low === 'д' && nextLow === 'ж') {
                out.push(ch !== low ? 'C' : 'c');
                i++;
                continue;
            }
            if (low === 'ь' || low === 'ъ') continue;

            let rep = null;
            if (low === 'а') rep = 'a';
            else if (low === 'э') rep = 'e';
            else if (low === 'ы') rep = 'ı';
            else if (low === 'и') rep = 'i';
            else if (low === 'е') rep = (i === 0 || /[аеёиоуыэюяьъ']/.test(prevLow)) ? 'ye' : 'e';
            else if (low === 'о') rep = (!seenVowel && isFront) ? 'ö' : 'o';
            else if (low === 'у') rep = ((!seenVowel && isFront && !wLow.startsWith('мусульман')) || wLow.startsWith('бугунь')) ? 'ü' : 'u';
            else if (low === 'ё') rep = (i === 0 || /[аеёиоуыэюяьъ']/.test(prevLow)) ? (isFront ? 'yö' : 'yo') : 'ö';
            else if (low === 'ю') rep = (i === 0 || /[аеёиоуыэюяьъ']/.test(prevLow)) ? (isFront ? 'yü' : 'yu') : 'ü';
            else if (low === 'я') rep = (i === 0 || /[аеёиоуыэюя'ъ]/.test(prevLow)) ? 'ya' : (prevLow === 'ь' ? 'ya' : 'â');
            else {
                const cmap = {
                    'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'ж': 'j', 'з': 'z', 'й': 'y',
                    'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'п': 'p', 'р': 'r', 'с': 's',
                    'т': 't', 'ф': 'f', 'х': 'h', 'һ': 'h', 'h': 'h', 'ц': 'ts', 'ч': 'ç',
                    'ш': 'ş', 'щ': 'şç', "'": "'"
                };
                rep = cmap[low] ?? ch;
            }

            if (/[аеёиоуыэюя]/.test(low)) seenVowel = true;

            if (ch !== low) {
                if (rep === 'i') out.push('İ');
                else if (rep === 'ı') out.push('I');
                else if (isAllCaps) out.push(rep.toUpperCase());
                else out.push(rep[0].toUpperCase() + rep.slice(1));
            } else {
                out.push(rep);
            }
        }
        return out.join('');
    });
}

export function transliterate(text, lang) {
    if (text === null || text === undefined || text === '') return '';
    const str = String(text);
    const map = lang === 'ru' ? RU_MAP : (lang === 'ua' ? UA_MAP : null);
    if (!map) return str;

    return str.split('').map(char => map[char] || char).join('');
}

/**
 * Convert CRH text between scripts
 * @param {string} text - Input text
 * @param {boolean} toCyrillic - If true, convert Latin to Cyrillic; if false, convert Cyrillic to Latin
 */
export function transliterateCrh(text, toCyrillic = false) {
    if (text === null || text === undefined || text === '') return '';
    const str = String(text);
    if (toCyrillic) {
        return transliterateCrhToCyrillic(str);
    }
    return transliterateCrhToLatin(str);
}
