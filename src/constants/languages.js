export const LANGUAGES = {
    'ar': {
        name: 'Arabic',
        label: 'AR',
        themeKey: 'arabic',
        isCore: true
    },
    'ar-lat': {
        name: 'Transliteration',
        label: 'LAT',
        themeKey: 'translit',
        isCore: true
    },
    'en': {
        name: 'English',
        label: 'EN',
        themeKey: 'english',
        translations: [
            { id: 'haleem', author: 'Abdel Haleem' },
            { id: 'sahih', author: 'Sahih International' }
        ]
    },
    'crh': {
        name: 'Crimean Tatar',
        label: 'CRH',
        themeKey: 'crh',
        hasScriptToggle: true,
        translations: [
            { id: 'dizen-qurtnezir', author: 'Sait Dizen & Zakir Qurtnezir' }
        ]
    },
    'tr': {
        name: 'Turkish',
        label: 'TR',
        themeKey: 'turkish',
        translations: [
            { id: 'elmalili', author: 'Elmalılı Hamdi Yazır' }
        ]
    },
    'ru': {
        name: 'Russian',
        label: 'RU',
        themeKey: 'russian',
        translations: [
            { id: 'kuliev', author: 'Elmir Kuliev' }
        ]
    },
    'ua': {
        name: 'Ukrainian',
        label: 'UA',
        themeKey: 'ukrainian',
        translations: [
            { id: 'yakubovych', author: 'Mykhaylo Yakubovych' }
        ]
    }
};

export const DEFAULT_AUTHORS = {
    'en': ['haleem'],
    'crh': ['dizen-qurtnezir'],
    'tr': ['elmalili'],
    'ru': ['kuliev'],
    'ua': ['yakubovych']
};
