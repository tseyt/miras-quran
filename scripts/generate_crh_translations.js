import fs from 'fs';
import path from 'path';

// Configuration
const SOURCE_FILE = path.resolve('translations/quran-crh-dizen-qurtnezir-lat.md');
const OUTPUT_DIR = path.resolve('src/data/translations/crh/dizen-qurtnezir');
const CORE_DIR = path.resolve('src/data/core');
const LANGUAGE = 'crh';
const AUTHOR = 'dizen-qurtnezir';

// Ensure output directory exists
if (!fs.existsSync(OUTPUT_DIR)) {
    fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

// Helper to get surah filename from core directory
const getSurahFilename = (surahId) => {
    const paddedId = String(surahId).padStart(3, '0');
    const files = fs.readdirSync(CORE_DIR);
    const match = files.find(f => f.startsWith(`${paddedId}-`));
    return match || null;
};

// Parse the source markdown file
const parseSourceFile = () => {
    const content = fs.readFileSync(SOURCE_FILE, 'utf-8');
    const lines = content.split('\n');

    const surahs = {};
    let currentSurahId = null;
    let currentVerse = null;
    let currentVerseText = '';

    // Regex patterns
    const surahHeaderPattern = /^#\s*(\d+)\.\s*(.+)$/;
    const mergedVersePattern = /^(\d+)-(\d+)\.\s+(.+)$/;  // Matches "3-4. text"
    const singleVersePattern = /^(\d+)\.\s+(.+)$/;         // Matches "3. text"

    for (let i = 0; i < lines.length; i++) {
        const line = lines[i];

        // Check for surah header
        const surahMatch = line.match(surahHeaderPattern);
        if (surahMatch) {
            // Save previous verse if exists
            if (currentSurahId && currentVerse && currentVerseText.trim()) {
                if (!surahs[currentSurahId]) surahs[currentSurahId] = {};
                surahs[currentSurahId][currentVerse] = currentVerseText.trim();
            }

            currentSurahId = parseInt(surahMatch[1], 10);
            currentVerse = null;
            currentVerseText = '';
            console.log(`Found Surah ${currentSurahId}: ${surahMatch[2].trim()}`);
            continue;
        }

        // Skip if no surah context
        if (!currentSurahId) continue;

        // Check for MERGED verse pattern (e.g., "3-4. text")
        // These are commentaries that combine verses, NOT the actual verses
        // Skip them - the individual verses (3. and 4.) follow after
        const mergedMatch = line.match(mergedVersePattern);
        if (mergedMatch) {
            // Save previous verse if any
            if (currentVerse && currentVerseText.trim()) {
                if (!surahs[currentSurahId]) surahs[currentSurahId] = {};
                surahs[currentSurahId][currentVerse] = currentVerseText.trim();
            }
            currentVerse = null;
            currentVerseText = '';
            // Skip this merged commentary line
            continue;
        }

        // Check for SINGLE verse pattern (e.g., "3. text")
        const singleMatch = line.match(singleVersePattern);
        if (singleMatch) {
            const verseNum = parseInt(singleMatch[1], 10);

            // Save previous verse
            if (currentVerse && currentVerseText.trim()) {
                if (!surahs[currentSurahId]) surahs[currentSurahId] = {};
                surahs[currentSurahId][currentVerse] = currentVerseText.trim();
            }

            currentVerse = verseNum;
            currentVerseText = singleMatch[2];
            continue;
        }

        // Accumulate multi-line verse text
        if (currentVerse && line.trim()) {
            currentVerseText += ' ' + line.trim();
        }
    }

    // Save last verse
    if (currentSurahId && currentVerse && currentVerseText.trim()) {
        if (!surahs[currentSurahId]) surahs[currentSurahId] = {};
        surahs[currentSurahId][currentVerse] = currentVerseText.trim();
    }

    return surahs;
};

// Generate YAML files
const generateYamlFiles = (surahs) => {
    let generatedCount = 0;

    for (const surahIdStr of Object.keys(surahs)) {
        const surahId = parseInt(surahIdStr, 10);

        // Skip surahs 1 and 2 (already exist with granular mapping)
        if (surahId <= 2) {
            console.log(`Skipping Surah ${surahId} (already exists with granular mapping)`);
            continue;
        }

        const filename = getSurahFilename(surahId);
        if (!filename) {
            console.error(`Could not find core file for Surah ${surahId}`);
            continue;
        }

        const outputPath = path.join(OUTPUT_DIR, filename);
        if (fs.existsSync(outputPath)) {
            console.log(`Skipping existing file: ${filename}`);
            continue;
        }

        const verses = surahs[surahId];
        const lines = [];
        lines.push(`surah_id: ${surahId}`);
        lines.push(`language: ${LANGUAGE}`);
        lines.push(`author: ${AUTHOR}`);
        lines.push(`verses:`);

        // Sort verses by number (filter out internal _mergedRanges property)
        const verseNums = Object.keys(verses)
            .filter(k => k !== '_mergedRanges')
            .map(n => parseInt(n, 10))
            .sort((a, b) => a - b);

        for (const verseNum of verseNums) {
            const text = verses[verseNum];
            lines.push(`  - verse: ${verseNum}`);
            lines.push(`    segments:`);
            // Use JSON.stringify for safe YAML escaping
            lines.push(`      - text: ${JSON.stringify(text)}`);
            lines.push(`        cid: 0`);
        }

        fs.writeFileSync(outputPath, lines.join('\n'));
        console.log(`Generated ${filename} with ${verseNums.length} verses`);
        generatedCount++;
    }

    return generatedCount;
};

// Main
const main = () => {
    console.log('Parsing CRH source file...');
    const surahs = parseSourceFile();

    console.log(`\nFound ${Object.keys(surahs).length} surahs in source file`);

    console.log('\nGenerating YAML files...');
    const count = generateYamlFiles(surahs);

    console.log(`\nDone! Generated ${count} new YAML files.`);
};

main();
