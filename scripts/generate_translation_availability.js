import fs from 'fs';
import path from 'path';

const TRANSLATIONS_DIR = path.resolve('src/data/translations');
const OUTPUT_FILE = path.resolve('src/data/translationAvailability.json');

const main = () => {
    const availability = {};

    // Initialize for all 114 surahs
    for (let i = 1; i <= 114; i++) {
        availability[i] = [];
    }

    // Scan directories
    if (fs.existsSync(TRANSLATIONS_DIR)) {
        const languages = fs.readdirSync(TRANSLATIONS_DIR).filter(f => fs.statSync(path.join(TRANSLATIONS_DIR, f)).isDirectory());

        for (const lang of languages) {
            const langDir = path.join(TRANSLATIONS_DIR, lang);
            const authors = fs.readdirSync(langDir).filter(f => fs.statSync(path.join(langDir, f)).isDirectory());

            for (const author of authors) {
                const authorDir = path.join(langDir, author);
                const files = fs.readdirSync(authorDir).filter(f => f.endsWith('.yaml'));

                for (const file of files) {
                    // Extract Surah ID from filename "001-Al-Fatiha.yaml" -> 1
                    const match = file.match(/^(\d+)-/);
                    if (match) {
                        const surahId = parseInt(match[1], 10);
                        const key = `${lang}-${author}`;

                        if (availability[surahId]) {
                            availability[surahId].push(key);
                        }
                    }
                }
            }
        }
    }

    // Sort entries
    for (const id in availability) {
        availability[id].sort();
    }

    fs.writeFileSync(OUTPUT_FILE, JSON.stringify(availability, null, 2));
    console.log(`Generated ${OUTPUT_FILE}`);
};

main();
