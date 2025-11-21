import React from 'react';
import { THEMES } from '../constants/theme';

export default function Toggle({ label, active, onClick, colorTheme }) {
    const activeStyle = colorTheme || "bg-emerald-50 text-emerald-700 border-emerald-200 dark:bg-emerald-900/20 dark:text-emerald-400 dark:border-emerald-800";
    const inactiveStyle = THEMES.neutral;
    return (
        <button onClick={onClick} className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all duration-200 border ${active ? activeStyle : inactiveStyle}`}>
            {label}
        </button>
    );
}
