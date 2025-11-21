// scripts/split_quran_data.js
import fs from 'fs';
import path from 'path';
import yaml from 'js-yaml';
import { fileURLToPath } from 'url';

// Resolve the directory of this script (ESM compatible)
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Resolve project root (assumes this script lives in <project>/scripts)
const ROOT = path.resolve(__dirname, '..');
const SRC_DATA = path.join(ROOT, 'src', 'data');
const ORIGINAL = path.join(SRC_DATA, 'quran_data.yaml');
const BACKUP = path.join(SRC_DATA, 'quran_data.backup.yaml');
const SURAH_DIR = path.join(SRC_DATA, 'surahs');

// Load the original combined YAML file
const raw = fs.readFileSync(ORIGINAL, 'utf8');
const fullData = yaml.load(raw);

// Keep a backup of the original file (just in case)
fs.copyFileSync(ORIGINAL, BACKUP);

// Ensure the target directory exists
fs.mkdirSync(SURAH_DIR, { recursive: true });

// Write each surah to its own YAML file
fullData.surahs.forEach(surah => {
    const safeTitle = surah.title.replace(/\s+/g, '-').replace(/[^a-zA-Z0-9\-]/g, '');
    const fileName = `${String(surah.id).padStart(3, '0')}-${safeTitle}.yaml`;
    const filePath = path.join(SURAH_DIR, fileName);
    const yamlContent = yaml.dump({ ...surah }, { lineWidth: -1 });
    fs.writeFileSync(filePath, yamlContent, 'utf8');
    console.log(`✅ Created ${fileName}`);
});

console.log('✅ All surahs have been split! 🎉');

