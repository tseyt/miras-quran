import React from 'react';
import { ChevronDown } from 'lucide-react';

export default function SurahSelector({ surahList, activeSurahId, setActiveSurahId }) {
    return (
        <div className="relative group w-full md:w-64">
            <select
                value={activeSurahId}
                onChange={(e) => setActiveSurahId(Number(e.target.value))}
                className="w-full appearance-none bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-200 py-2 pl-4 pr-10 rounded-lg font-medium cursor-pointer hover:border-emerald-500/50 transition-colors outline-none focus:ring-2 focus:ring-emerald-500/20 text-sm"
            >
                {surahList.map(surah => (
                    <option key={surah.id} value={surah.id}>
                        {surah.id}. {surah.title} ({surah.english})
                    </option>
                ))}
            </select>
            <ChevronDown className="w-4 h-4 text-slate-400 absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none" />
        </div>
    );
}
