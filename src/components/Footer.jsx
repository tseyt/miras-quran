import React from 'react';
import { Github, Flag, Heart } from 'lucide-react';
import { LAYOUT_STYLES } from '../constants/theme';

export default function Footer() {
    return (
        <footer className={LAYOUT_STYLES.footer}>
            <div className="container mx-auto px-4 max-w-4xl py-4 flex flex-col items-center gap-2">
                {/* Heart Message */}
                <div className="flex items-center gap-2 text-slate-600 dark:text-slate-300 font-medium">
                    Made with <Heart className="w-4 h-4 text-rose-500 fill-rose-500" /> for the Ümmet
                </div>

                {/* Description */}
                <div className="text-[10px] text-slate-400 dark:text-slate-500 text-center uppercase tracking-widest leading-tight max-w-lg">
                    A semantic Quran study platform for deep linguistic analysis and language learning.
                </div>

                {/* Actions */}
                <div className="flex items-center gap-4 mt-1">
                    <a
                        href="https://github.com/tseyt/miras-quran"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex items-center gap-2 text-xs text-slate-400 hover:text-emerald-600 dark:hover:text-emerald-400 transition-colors font-bold uppercase tracking-wider"
                    >
                        <Github className="w-4 h-4" />
                        GitHub
                    </a>
                    <a
                        href="https://github.com/tseyt/miras-quran/issues"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex items-center gap-2 text-xs text-slate-400 hover:text-rose-600 dark:hover:text-rose-400 transition-colors font-bold uppercase tracking-wider"
                    >
                        <Flag className="w-4 h-4" />
                        Report Issue
                    </a>
                </div>
            </div>
        </footer>
    );
}


