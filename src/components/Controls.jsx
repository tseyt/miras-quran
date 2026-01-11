import React, { useState, useRef, useEffect } from 'react';
import { Type } from 'lucide-react';
import Toggle from './Toggle';
import TranslationSelector from './TranslationSelector';
import { THEMES } from '../constants/theme';
import { LANGUAGES } from '../constants/languages';

export default function Controls({
    isOpen,
    activeLanguages,
    toggleLanguage,
    selectedAuthors,
    toggleAuthor,
    baseFontSize,
    setBaseFontSize,
    isLatin,
    setIsLatin,
    availableTranslations
}) {
    const [openMenu, setOpenMenu] = useState(null);
    const containerRef = useRef(null);

    useEffect(() => {
        function handleClickOutside(event) {
            if (containerRef.current && !containerRef.current.contains(event.target)) {
                setOpenMenu(null);
            }
        }
        document.addEventListener("mousedown", handleClickOutside);
        return () => document.removeEventListener("mousedown", handleClickOutside);
    }, []);

    if (!isOpen) return null;

    return (
        <div ref={containerRef} className="flex flex-wrap items-center gap-3">
            <div className="flex flex-wrap items-center gap-1.5 p-1 bg-slate-100/50 dark:bg-slate-800/50 rounded-xl border border-slate-200/50 dark:border-slate-700/50">
                {Object.entries(LANGUAGES).map(([code, lang]) => {
                    // Check availability
                    if (!lang.isCore && availableTranslations) {
                        // Check if any author for this language is available
                        const anyAvailable = lang.translations?.some(t =>
                            availableTranslations.includes(`${code}-${t.id}`)
                        );
                        if (!anyAvailable) return null;
                    }

                    // For the selector, we might want to pass only available authors, 
                    // but TranslationSelector doesn't take available list yet.
                    // However, if we only show the toggle if strictly available, that handles the "hide toggles" request.
                    // But if a language has MULTIPLE authors and only ONE is available, we still show the toggle, 
                    // but maybe we should filter the selector options too? 
                    // The user said "hide the toggles for translations that are not available". 
                    // If "Turkish" has "Elmalili" (unavailable) and "Diyanet" (available), we show Turkish toggle.
                    // But inside selector, Elmalili should probably be hidden or disabled.
                    // Let's rely on TranslationSelector receiving filtered options or just pass the availability check.

                    // Actually, let's filter the `hasOptions` prop and maybe pass available list to TranslationSelector later if needed.
                    // For now, hiding the main toggle if NO translations exist is the primary request.

                    return (
                        <div key={code} className="relative">
                            <Toggle
                                label={lang.label}
                                active={activeLanguages.has(code)}
                                onClick={() => toggleLanguage(code)}
                                colorTheme={THEMES[lang.themeKey]}
                                hasOptions={lang.translations && lang.translations.length > 0}
                                onOptionsClick={(e) => {
                                    e.stopPropagation();
                                    setOpenMenu(openMenu === code ? null : code);
                                }}
                                optionsOpen={openMenu === code}
                            />
                            {openMenu === code && (
                                <TranslationSelector
                                    langCode={code}
                                    selectedAuthors={selectedAuthors[code] || []}
                                    onToggle={toggleAuthor}
                                    availableTranslations={availableTranslations}
                                />
                            )}
                        </div>
                    );
                })}
            </div>

            <div className="h-6 w-px bg-slate-200 dark:bg-slate-800 mx-1"></div>

            <div className="flex items-center gap-3 bg-slate-100/50 dark:bg-slate-800/50 px-3 py-1.5 rounded-xl border border-slate-200/50 dark:border-slate-700/50">
                <Type className="w-3.5 h-3.5 text-slate-400" />
                <input
                    type="range"
                    min="14"
                    max="32"
                    step="1"
                    value={baseFontSize}
                    onChange={(e) => setBaseFontSize(parseInt(e.target.value))}
                    className="w-24 h-1 bg-slate-200 dark:bg-slate-700 rounded-lg appearance-none cursor-pointer accent-emerald-500"
                />
                <span className="text-[10px] font-bold text-slate-500 w-6">{baseFontSize}</span>
            </div>

            <div className="flex items-center gap-1.5 p-1 bg-slate-100/50 dark:bg-slate-800/50 rounded-xl border border-slate-200/50 dark:border-slate-700/50">
                <Toggle
                    label="LATIN"
                    active={isLatin}
                    onClick={() => setIsLatin(!isLatin)}
                    colorTheme={THEMES.translit}
                />
            </div>
        </div>
    );
}
