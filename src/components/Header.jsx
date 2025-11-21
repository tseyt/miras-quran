import React from 'react';
import { BookOpen, Settings, Moon, Sun } from 'lucide-react';
import { LAYOUT_STYLES } from '../constants/theme';

export default function Header({ showControls, setShowControls, isDarkMode, setIsDarkMode }) {
    return (
        <div className={LAYOUT_STYLES.header}>
            <div className={LAYOUT_STYLES.headerContent}>
                <div>
                    <h1 className="text-xl font-bold text-slate-900 dark:text-slate-100 tracking-tight flex items-center gap-2">
                        <BookOpen className="w-6 h-6 text-emerald-600" />
                        Miras Quran
                    </h1>
                    <p className="text-[10px] text-slate-500 dark:text-slate-400 font-medium tracking-wide uppercase ml-8">Semantic Syntax Mapping</p>
                </div>

                <div className="flex items-center gap-2">
                    <button
                        onClick={() => setShowControls(!showControls)}
                        className={`p-2 rounded-full transition-colors ${showControls ? 'bg-slate-100 dark:bg-slate-800 text-emerald-600' : 'hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-400'}`}
                        title="Toggle View Options"
                    >
                        <Settings className="w-5 h-5" />
                    </button>

                    <button
                        onClick={() => setIsDarkMode(!isDarkMode)}
                        className="p-2 rounded-full hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-600 dark:text-slate-400 transition-colors"
                        title="Toggle Dark Mode"
                    >
                        {isDarkMode ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
                    </button>
                </div>
            </div>
        </div>
    );
}
