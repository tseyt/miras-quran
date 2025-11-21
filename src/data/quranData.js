import data from './quran_data.yaml';

export const SURAH_LIST = data.surahs.map(s => ({
    id: s.id,
    title: s.title,
    english: s.english,
    type: s.type,
    verses: s.total_verses
}));

export const QURAN_CONTENT = data.surahs.reduce((acc, surah) => {
    acc[surah.id] = surah.content.map(verse => ({
        id: verse.verse,
        ...verse
    }));
    return acc;
}, {});

export const META = data.meta;
