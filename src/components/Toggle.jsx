import React from 'react';
import { ChevronDown } from 'lucide-react';
import { THEMES } from '../constants/theme';

export default function Toggle({ label, active, onClick, colorTheme, hasOptions, onOptionsClick, optionsOpen }) {
    const activeStyle = colorTheme || THEMES.crh;
    const inactiveStyle = THEMES.neutral;

    return (
        <div className="flex items-center group relative h-8">
            <button
                onClick={onClick}
                className={`h-full px-3 rounded-l-lg text-xs font-bold transition-all duration-200 border-y border-l ${active
                        ? `${activeStyle} border-current/20`
                        : `${inactiveStyle} border-slate-200 dark:border-slate-700`
                    } ${!hasOptions ? 'rounded-r-lg border-r' : ''}`}
            >
                {label}
            </button>

            {hasOptions && (
                <button
                    onClick={onOptionsClick}
                    className={`h-full px-1.5 rounded-r-lg border transition-all duration-200 ${active
                            ? `${activeStyle} border-l-current/20 border-current/20`
                            : `${inactiveStyle} border-slate-200 dark:border-slate-700`
                        } ${optionsOpen ? 'bg-slate-200 dark:bg-slate-700' : ''}`}
                >
                    <ChevronDown className={`w-3.5 h-3.5 transition-transform duration-200 ${optionsOpen ? 'rotate-180' : ''}`} />
                </button>
            )}
        </div>
    );
}
