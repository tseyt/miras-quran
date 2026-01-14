/**
 * CID Concept Mapping Script
 * Maps TR and CRH translation segments to Arabic word-level CIDs using Gemini LLM
 */

import fs from 'fs';
import path from 'path';
import yaml from 'js-yaml';

// Configuration
const GEMINI_API_KEY = process.env.GEMINI_API_KEY || 'AIzaSyAWRmqsY7hPU0Gq0qLf3I8-G_Gg2cUHYsY';
const GEMINI_API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent';

const CORE_DIR = path.resolve('src/data/core');
const TR_DIR = path.resolve('src/data/translations/tr/elmalili');
const CRH_DIR = path.resolve('src/data/translations/crh/dizen-qurtnezir');
const EN_DIR = path.resolve('src/data/translations/en/haleem');

// Rate limiting
const DELAY_MS = 2000; // Delay between API calls to avoid rate limits
const MAX_RETRIES = 3; // Max retries on rate limit

const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

/**
 * Strip parenthetical commentary from text
 */
function stripCommentary(text) {
    // Use balanced parentheses matching
    let result = '';
    let depth = 0;
    for (let i = 0; i < text.length; i++) {
        if (text[i] === '(') {
            depth++;
        } else if (text[i] === ')') {
            depth = Math.max(0, depth - 1);
        } else if (depth === 0) {
            result += text[i];
        }
    }
    return result.replace(/\s+/g, ' ').trim();
}

/**
 * Call Gemini API to segment translation text
 */
async function segmentWithGemini(translationText, arabicSegments, englishSegments, language = 'Turkish') {
    const arabicWords = arabicSegments.map(s => s.text).join(' ');
    const maxCid = Math.max(...arabicSegments.map(s => s.cid));

    const englishExample = englishSegments
        .map(s => `CID ${s.cid}: "${s.text}"`)
        .join('\n');

    const prompt = `You are a Quran translation alignment expert. 

Given this Arabic verse (${maxCid} concept segments):
${arabicWords}

English translation alignment for reference:
${englishExample}

Now segment this ${language} translation into exactly ${maxCid} parts, matching the same concept boundaries as the Arabic and English:

${language} text: "${translationText}"

IMPORTANT:
- Return ONLY a JSON array of ${maxCid} strings
- Each string should be a segment of the ${language} translation
- Maintain proper word boundaries
- Cover ALL words from the translation, no words should be omitted
- Do not include any commentary in parentheses

Example output format: ["segment 1", "segment 2", "segment 3"]`;

    for (let attempt = 0; attempt < MAX_RETRIES; attempt++) {
        try {
            const response = await fetch(`${GEMINI_API_URL}?key=${GEMINI_API_KEY}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    contents: [{ parts: [{ text: prompt }] }],
                    generationConfig: {
                        temperature: 0.1,
                        maxOutputTokens: 1024
                    }
                })
            });

            if (response.status === 429) {
                // Rate limited - extract retry delay and wait
                const retryDelay = (attempt + 1) * 30000; // 30s, 60s, 90s
                console.log(`  Rate limited, waiting ${retryDelay / 1000}s...`);
                await sleep(retryDelay);
                continue;
            }

            if (!response.ok) {
                const error = await response.text();
                throw new Error(`Gemini API error: ${response.status} - ${error}`);
            }

            const data = await response.json();
            const text = data.candidates?.[0]?.content?.parts?.[0]?.text;

            if (!text) {
                throw new Error('No response from Gemini');
            }

            // Extract JSON array from response
            const jsonMatch = text.match(/\[[\s\S]*\]/);
            if (!jsonMatch) {
                throw new Error('Could not find JSON array in response');
            }

            const segments = JSON.parse(jsonMatch[0]);

            if (segments.length !== maxCid) {
                console.warn(`  Warning: Expected ${maxCid} segments, got ${segments.length}`);
            }

            return segments;
        } catch (error) {
            console.error(`  Gemini error: ${error.message}`);
            if (attempt === MAX_RETRIES - 1) return null;
            await sleep((attempt + 1) * 10000);
        }
    }
    return null;
}

/**
 * Process a single surah for a language
 */
async function processSurah(surahId, language = 'tr') {
    const paddedId = String(surahId).padStart(3, '0');

    // Find matching files
    const coreFiles = fs.readdirSync(CORE_DIR).filter(f => f.startsWith(paddedId));
    if (coreFiles.length === 0) {
        console.log(`  No core file found for surah ${surahId}`);
        return null;
    }

    const coreFile = path.join(CORE_DIR, coreFiles[0]);
    const coreData = yaml.load(fs.readFileSync(coreFile, 'utf8'));

    // Find translation file
    const transDir = language === 'tr' ? TR_DIR : CRH_DIR;
    const transFiles = fs.readdirSync(transDir).filter(f => f.startsWith(paddedId));
    if (transFiles.length === 0) {
        console.log(`  No ${language} translation file found for surah ${surahId}`);
        return null;
    }

    const transFile = path.join(transDir, transFiles[0]);
    const transData = yaml.load(fs.readFileSync(transFile, 'utf8'));

    // Find English reference (optional)
    let enData = null;
    const enFiles = fs.readdirSync(EN_DIR).filter(f => f.startsWith(paddedId));
    if (enFiles.length > 0) {
        enData = yaml.load(fs.readFileSync(path.join(EN_DIR, enFiles[0]), 'utf8'));
    }

    console.log(`Processing Surah ${surahId} (${language})...`);

    let updatedCount = 0;

    for (const verse of transData.verses) {
        const coreVerse = coreData.verses.find(v => v.verse === verse.verse);
        if (!coreVerse || !coreVerse.segments?.ar) continue;

        const arabicSegments = coreVerse.segments.ar;
        const enSegments = enData?.verses.find(v => v.verse === verse.verse)?.segments || [];

        // Check if already mapped (cid != 0)
        if (verse.segments.length > 1 || verse.segments[0]?.cid !== 0) {
            continue; // Already mapped
        }

        const originalText = verse.segments[0].text;
        const cleanText = stripCommentary(originalText);

        if (!cleanText) continue;

        // Use Gemini to segment
        const langName = language === 'tr' ? 'Turkish' : 'Crimean Tatar';
        const segments = await segmentWithGemini(cleanText, arabicSegments, enSegments, langName);

        if (segments && segments.length > 0) {
            verse.segments = segments.map((text, idx) => ({
                text: text.trim(),
                cid: idx + 1
            }));
            updatedCount++;
        }

        await sleep(DELAY_MS);
    }

    // Write updated file
    if (updatedCount > 0) {
        const yamlContent = yaml.dump(transData, {
            lineWidth: -1,
            quotingType: '"',
            forceQuotes: true
        });
        fs.writeFileSync(transFile, yamlContent);
        console.log(`  Updated ${updatedCount} verses in ${transFiles[0]}`);
    }

    return updatedCount;
}

/**
 * Main function
 */
async function main() {
    const args = process.argv.slice(2);
    const language = args[0] || 'tr';
    const surahStart = parseInt(args[1]) || 1;
    const surahEnd = parseInt(args[2]) || 114;

    console.log(`\nCID Mapping Script`);
    console.log(`Language: ${language}`);
    console.log(`Surahs: ${surahStart} to ${surahEnd}`);
    console.log(`Using Gemini API for intelligent segmentation\n`);

    let totalUpdated = 0;

    for (let i = surahStart; i <= surahEnd; i++) {
        try {
            const count = await processSurah(i, language);
            if (count) totalUpdated += count;
        } catch (error) {
            console.error(`Error processing surah ${i}: ${error.message}`);
        }
    }

    console.log(`\nDone! Updated ${totalUpdated} verses total.`);
}

main().catch(console.error);
