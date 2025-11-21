import React from 'react';
import { Type } from 'lucide-react';
import Toggle from './Toggle';
import { THEMES, LAYOUT_STYLES } from '../constants/theme';

export default function Controls({
    showArabic, setShowArabic,
    showTranslit, setShowTranslit,
    showEnglish, setShowEnglish,
    showCrh, setShowCrh,
    showTurkish, setShowTurkish,
    baseFontSize, setBaseFontSize
}) {
    return (
        <div className={LAYOUT_STYLES.controls}>
            <div className="flex flex-col md:flex-row md:items-center gap-6 max-w-3xl mx-auto">
                <div className="flex flex-col gap-2 flex-1">
                    <div className="flex items-center gap-2 text-[10px] uppercase tracking-wider font-bold text-slate-400">
                        Visibility
                    </div>
                    <div className="flex gap-2 flex-wrap">
                        <Toggle label="Arabic" active={showArabic} onClick={() => setShowArabic(!showArabic)} colorTheme={THEMES.arabic} />
                        <Toggle label="Transliteration" active={showTranslit} onClick={() => setShowTranslit(!showTranslit)} colorTheme={THEMES.translit} />
                        <Toggle label="English" active={showEnglish} onClick={() => setShowEnglish(!showEnglish)} colorTheme={THEMES.english} />
                        <Toggle label="Crimean Tatar" active={showCrh} onClick={() => setShowCrh(!showCrh)} colorTheme={THEMES.crh} />
                        <Toggle label="Turkish" active={showTurkish} onClick={() => setShowTurkish(!showTurkish)} colorTheme={THEMES.turkish} />
                    </div>
                </div>
                <div className="hidden md:block w-px h-12 bg-slate-200 dark:bg-slate-700"></div>
                <div className="flex flex-col gap-2 w-full md:w-64">
                    <div className="flex items-center justify-between text-[10px] uppercase tracking-wider font-bold text-slate-400">
                        <div className="flex items-center gap-2"><Type className="w-3 h-3" /> Text Size</div>
                        <span>{baseFontSize}px</span>
                    </div>
                    <div className="flex items-center gap-3">
                        <span className="text-xs text-slate-400 font-medium">A</span>
                        <input
                            type="range"
                            min="14"
                            max="32"
                            step="1"
                            value={baseFontSize}
                            onChange={(e) => setBaseFontSize(parseInt(e.target.value))}
                            className="w-full h-2 bg-slate-200 dark:bg-slate-700 rounded-lg appearance-none cursor-pointer accent-emerald-500"
                        />
                        <span className="text-xl text-slate-600 dark:text-slate-300 font-medium">A</span>
                    </div>
                </div>
            </div>
        </div>
    );
}
