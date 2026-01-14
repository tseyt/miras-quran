import React from 'react';

/**
 * CollapsibleCommentary - Renders parenthetical commentary that can be expanded/collapsed
 * 
 * @param {string} text - The commentary text (without parentheses)
 * @param {boolean} isExpanded - Whether the commentary is currently expanded
 * @param {function} onToggle - Callback to toggle expansion state
 */
export default function CollapsibleCommentary({ text, isExpanded, onToggle }) {
    if (isExpanded) {
        return (
            <span
                onClick={onToggle}
                className="cursor-pointer hover:bg-amber-50 dark:hover:bg-amber-900/20 rounded transition-colors"
                title="Click to collapse"
            >
                <span className="text-slate-500 dark:text-slate-400">(</span>
                <span className="text-slate-600 dark:text-slate-300 italic">{text}</span>
                <span className="text-slate-500 dark:text-slate-400">)</span>
                <span className="ml-1 text-amber-600 dark:text-amber-400 text-xs">▲</span>
            </span>
        );
    }

    return (
        <span
            onClick={onToggle}
            className="cursor-pointer px-1 py-0.5 rounded bg-amber-100/50 dark:bg-amber-900/30 hover:bg-amber-200/70 dark:hover:bg-amber-800/40 transition-colors"
            title="Click to expand commentary"
        >
            <span className="text-amber-700 dark:text-amber-400 text-sm font-medium">
                (...)
            </span>
            <span className="ml-1 text-amber-600 dark:text-amber-400 text-xs">▼</span>
        </span>
    );
}
