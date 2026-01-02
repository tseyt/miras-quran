import { LANGUAGES, DEFAULT_AUTHORS } from '../constants/languages';

// Helper to get all core surah files
const coreModules = import.meta.glob('./core/*.yaml', { eager: true });
const translationModules = import.meta.glob('./translations/**/*.yaml');

export const SURAH_LIST = Object.entries(coreModules)
    .map(([path, data]) => ({
        id: data.default.id,
        title: data.default.title,
        english: data.default.english,
        type: data.default.type,
        verses: data.default.total_verses,
        file: path.split('/').pop()
    }))
    .sort((a, b) => a.id - b.id);

export const QURAN_CONTENT = Object.values(coreModules).reduce((acc, data) => {
    acc[data.default.id] = data.default.verses.map(verse => ({
        id: verse.verse,
        ...verse
    }));
    return acc;
}, {});

// Function to load translations for a specific surah
export const loadTranslations = async (surahId, activeLanguages, selectedAuthors) => {
    const surah = SURAH_LIST.find(s => s.id === surahId);
    if (!surah) return {};

    const translations = {};
    const promises = [];

    for (const langCode of activeLanguages) {
        const langConfig = LANGUAGES[langCode];
        if (!langConfig || langConfig.isCore) continue;

        const authors = selectedAuthors[langCode] || DEFAULT_AUTHORS[langCode] || [];
        translations[langCode] = {}; // Map authorId -> verses

        for (const authorId of authors) {
            const surahFile = surah.file;
            const transPath = `./translations/${langCode}/${authorId}/${surahFile}`;

            const loader = translationModules[transPath];
            if (loader) {
                promises.push(
                    loader().then(module => {
                        translations[langCode][authorId] = module.default.verses;
                    }).catch(err => {
                        console.error(`Failed to load translation: ${transPath}`, err);
                    })
                );
            }
        }
    }

    await Promise.all(promises);
    return translations;
};

export const META = {
    generated_at: new Date().toISOString()
};
