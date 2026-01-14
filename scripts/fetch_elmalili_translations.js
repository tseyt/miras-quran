import fs from 'fs';
import path from 'path';
import https from 'https';

// Configuration
const TRANSLATION_ID = 52; // Elmalili Hamdi Yazir
const LANGUAGE = 'tr';
const AUTHOR = 'elmalili';
const OUTPUT_DIR = path.resolve('src/data/translations/tr/elmalili');
const CORE_DIR = path.resolve('src/data/core');

// Ensure output directory exists
if (!fs.existsSync(OUTPUT_DIR)) {
    fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

// Helper to fetch data
const fetchJson = (url) => {
    return new Promise((resolve, reject) => {
        https.get(url, (res) => {
            let data = '';
            res.on('data', (chunk) => data += chunk);
            res.on('end', () => {
                try {
                    resolve(JSON.parse(data));
                } catch (e) {
                    reject(e);
                }
            });
        }).on('error', reject);
    });
};

// Helper to get Surah name from core files
const getSurahFilename = (surahId) => {
    const paddedId = String(surahId).padStart(3, '0');
    const files = fs.readdirSync(CORE_DIR);
    const match = files.find(f => f.startsWith(`${paddedId}-`));
    return match ? match : null;
};

// Main function
const main = async () => {
    console.log(`Fetching translations for resource ID ${TRANSLATION_ID}...`);

    // We need to fill Surahs 3 to 114
    // Surah 1 and 2 already exist and should be preserved
    for (let surahId = 3; surahId <= 114; surahId++) {
        const filename = getSurahFilename(surahId);
        if (!filename) {
            console.error(`Could not find core file for Surah ID ${surahId}`);
            continue;
        }

        const outputFilePath = path.join(OUTPUT_DIR, filename);
        if (fs.existsSync(outputFilePath)) {
            console.log(`Skipping existing file: ${filename}`);
            continue;
        }

        console.log(`Processing Surah ${surahId}: ${filename}...`);

        try {
            // Fetch translation from Quran.com API
            const url = `https://api.quran.com/api/v4/quran/translations/${TRANSLATION_ID}?chapter_number=${surahId}`;
            const response = await fetchJson(url);

            if (!response.translations || response.translations.length === 0) {
                console.error(`No translations found for Surah ${surahId}`);
                continue;
            }

            // Read core file to get verse structure (though for unmapped we just do 1 segment)
            // Actually, we just iterate the API response which matches verses.

            const lines = [];
            lines.push(`surah_id: ${surahId}`);
            lines.push(`language: ${LANGUAGE}`);
            lines.push(`author: ${AUTHOR}`);
            lines.push(`verses:`);

            // Process translations
            response.translations.forEach((t, index) => {
                const verseNum = index + 1;

                lines.push(`  - verse: ${verseNum}`);
                lines.push(`    segments:`);
                // Clean text: remove HTML tags if present
                let cleanText = t.text.replace(/<\/?[^>]+(>|$)/g, "");
                cleanText = cleanText.trim();

                // Use JSON.stringify to safely create a double-quoted YAML string
                // This handles quotes, newlines, and other special characters automatically.
                lines.push(`      - text: ${JSON.stringify(cleanText)}`);
                lines.push(`        cid: 0`);
            });

            fs.writeFileSync(outputFilePath, lines.join('\n'));
            console.log(`Generated ${filename}`);

            // Rate limit to be nice to API
            await new Promise(r => setTimeout(r, 200));

        } catch (error) {
            console.error(`Error processing Surah ${surahId}:`, error);
        }
    }

    console.log('Done!');
};

main();
