import React from 'react';
import { Check } from 'lucide-react';
import { LANGUAGES } from '../constants/languages';

export default function TranslationSelector({ langCode, selectedAuthors, onToggle }) {
    const lang = LANGUAGES[langCode];
    if (!lang || !lang.translations) return null;

    return (
        <div className="absolute top-full mt-2 left-0 z-50 min-w-[200px] bg-white dark:bg-slate-900 shadow-xl rounded-xl border border-slate-200 dark:border-slate-800 p-2 animate-in fade-in zoom-in-95 duration-200">
            <div className="text-[10px] uppercase tracking-wider font-bold text-slate-400 px-2 py-1 border-b border-slate-100 dark:border-slate-800 mb-1">
                Select Versions
            </div>
            <div className="flex flex-col gap-0.5">
                {lang.translations.map((trans) => {
                    const isSelected = selectedAuthors.includes(trans.id);
                    return (
                        <button
                            key={trans.id}
                            onClick={(e) => {
                                e.stopPropagation();
                                onToggle(langCode, trans.id);
                            }}
                            className={`flex items-center justify-between px-3 py-2 rounded-lg text-xs transition-colors ${isSelected
                                    ? 'bg-emerald-50 text-emerald-600 dark:bg-emerald-500/10 dark:text-emerald-400 font-bold'
                                    : 'hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-600 dark:text-slate-400 font-medium'
                                }`}
                        >
                            <span className="truncate mr-2">{trans.author}</span>
                            {isSelected && <Check className="w-3.5 h-3.5 shrink-0" />}
                        </button>
                    );
                })}
            </div>
        </div>
    );
}
