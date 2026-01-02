import fs from 'fs';
import path from 'path';
import yaml from 'js-yaml';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const DATA_DIR = path.resolve(__dirname, '../src/data');
const CORE_DIR = path.join(DATA_DIR, 'core');
const TRANS_DIR = path.join(DATA_DIR, 'translations');

function validate() {
    if (!fs.existsSync(CORE_DIR)) {
        console.error('❌ Core directory not found. Please run migration first.');
        return;
    }

    const coreFiles = fs.readdirSync(CORE_DIR).filter(f => f.endsWith('.yaml'));

    coreFiles.forEach(file => {
        const corePath = path.join(CORE_DIR, file);
        const coreData = yaml.load(fs.readFileSync(corePath, 'utf8'));

        // Build map of CIDs per verse in core
        const coreCidMap = {};
        coreData.verses.forEach(v => {
            coreCidMap[v.verse] = new Set(
                (v.segments.ar || []).map(s => s.cid).filter(cid => cid !== 0)
            );
        });

        // Check translations
        const langDirs = fs.readdirSync(TRANS_DIR);
        langDirs.forEach(lang => {
            const langPath = path.join(TRANS_DIR, lang);
            if (!fs.statSync(langPath).isDirectory()) return;

            const authors = fs.readdirSync(langPath);
            authors.forEach(author => {
                const transFilePath = path.join(langPath, author, file);
                if (!fs.existsSync(transFilePath)) return;

                const transData = yaml.load(fs.readFileSync(transFilePath, 'utf8'));
                let errors = 0;

                transData.verses.forEach(v => {
                    const transCids = (v.segments || []).map(s => s.cid).filter(cid => cid !== 0);
                    const validCids = coreCidMap[v.verse] || new Set();

                    transCids.forEach(cid => {
                        if (!validCids.has(cid)) {
                            console.error(`❌ [${lang}/${author}] ${file} Verse ${v.verse}: CID ${cid} not found in Arabic core.`);
                            errors++;
                        }
                    });
                });

                if (errors === 0) {
                    console.log(`✅ [${lang}/${author}] ${file} mapping is valid.`);
                }
            });
        });
    });
}

validate();
