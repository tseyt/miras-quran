import React, { useState } from 'react';
import LangBadge from './LangBadge';
import CollapsibleCommentary from './CollapsibleCommentary';
import { COLORS, THEMES, HOVER_STYLES, LAYOUT_STYLES } from '../constants/theme';
import { LANGUAGES } from '../constants/languages';
import { transliterate } from '../utils/transliteration';

// Minimum words for commentary to be collapsible
const MIN_WORDS_FOR_COLLAPSE = 5;

export default function VerseCard({
    verse,
    activeSegment,
    setActiveSegment,
    activeLanguages,
    loadedTranslations,
    selectedAuthors,
    baseFontSize,
    spacingUnit,
    isLatin
}) {
    // Track which commentaries are expanded (key: "verseId-segIdx-parenIdx")
    const [expandedCommentaries, setExpandedCommentaries] = useState({});

    // Standardize gaps based on spacing unit and font size
    // Scales to near-zero at 14px
    const internalVerticalGap = Math.max(0, (baseFontSize - 14) * 1.8) * spacingUnit;
    const horizontalGap = 16;
    const cardPadding = Math.max(2, (baseFontSize - 14) * 1.5 + 4) * spacingUnit;

    const toggleCommentary = (key) => {
        setExpandedCommentaries(prev => ({
            ...prev,
            [key]: !prev[key]
        }));
    };

    // Parse text and render with collapsible parenthetical commentary
    // Uses balanced parentheses matching to handle nested parens like (text (note) more)
    const renderTextWithCommentary = (text, verseId, segIdx) => {
        const parts = [];
        let i = 0;
        let parenIdx = 0;

        while (i < text.length) {
            const openIdx = text.indexOf('(', i);

            if (openIdx === -1) {
                // No more parentheses, add remaining text
                parts.push(text.slice(i));
                break;
            }

            // Add text before the parenthesis
            if (openIdx > i) {
                parts.push(text.slice(i, openIdx));
            }

            // Find matching closing parenthesis with depth tracking
            let depth = 1;
            let closeIdx = openIdx + 1;
            while (closeIdx < text.length && depth > 0) {
                if (text[closeIdx] === '(') depth++;
                else if (text[closeIdx] === ')') depth--;
                closeIdx++;
            }

            if (depth === 0) {
                // Found balanced parentheses
                const commentaryText = text.slice(openIdx + 1, closeIdx - 1);
                const wordCount = commentaryText.trim().split(/\s+/).length;

                if (wordCount > MIN_WORDS_FOR_COLLAPSE) {
                    // Long commentary - make collapsible
                    const key = `${verseId}-${segIdx}-${parenIdx}`;
                    const isExpanded = expandedCommentaries[key] || false;
                    parts.push(
                        <CollapsibleCommentary
                            key={key}
                            text={commentaryText}
                            isExpanded={isExpanded}
                            onToggle={() => toggleCommentary(key)}
                        />
                    );
                } else {
                    // Short commentary - show inline normally
                    parts.push(`(${commentaryText})`);
                }
                i = closeIdx;
                parenIdx++;
            } else {
                // Unbalanced - just add literal text
                parts.push(text.slice(openIdx));
                break;
            }
        }

        return parts.length > 0 ? parts : text;
    };

    const getSegmentClass = (verseId, cid) => {
        if (cid === 0) return "text-slate-400 dark:text-slate-500";
        const isActive = activeSegment && activeSegment.verseId === verseId && activeSegment.cid === cid;
        const colorClass = COLORS[cid % 6] || COLORS.default;
        return `${HOVER_STYLES} ${isActive ? `${colorClass} shadow-sm` : `hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-600 dark:text-slate-300`}`;
    };

    const handleMouseEnter = (verseId, cid) => {
        if (cid !== 0) setActiveSegment({ verseId, cid });
    };

    const handleMouseLeave = () => {
        setActiveSegment({ verseId: null, cid: null });
    };

    const activeLangEntries = Object.entries(LANGUAGES)
        .filter(([code]) => activeLanguages.has(code));

    const isFirstVisible = (langCode) => {
        return activeLangEntries[0]?.[0] === langCode;
    };

    const getStackStyle = (isFirst) => {
        return {
            paddingTop: isFirst ? '0px' : `${internalVerticalGap}px`,
            gap: `${horizontalGap}px`,
            borderTopWidth: isFirst ? '0px' : '1px'
        };
    };

    return (
        <div className={LAYOUT_STYLES.card}>
            <div className="absolute top-2 left-2 z-10 flex items-center gap-1">
                <span className="text-xs font-bold text-slate-400 bg-slate-50 dark:bg-slate-800 px-1.5 py-0.5 rounded">
                    {verse.verse}
                </span>
                {verse.context_mapped && (
                    <span className="w-2 h-2 rounded-full bg-emerald-500" title="Context Mapped"></span>
                )}
            </div>

            <div className="absolute bottom-1 right-1 z-10">
                <span className="text-[10px] font-mono text-emerald-500/70 bg-slate-50/80 dark:bg-slate-800/80 px-1 rounded">
                    {activeSegment && activeSegment.verseId === verse.id && activeSegment.cid ? activeSegment.cid : ""}
                </span>
            </div>

            <div className="flex-1 min-w-0" style={{ padding: `${cardPadding}px` }}>
                <div style={{ display: 'flex', flexDirection: 'column', gap: `${internalVerticalGap}px` }}>
                    {activeLangEntries.map(([langCode, lang]) => {
                        if (lang.isCore) {
                            const segments = verse.segments[langCode];
                            if (!segments) return null;
                            const isFirst = isFirstVisible(langCode);
                            const theme = THEMES[lang.themeKey];

                            if (langCode === 'ar') {
                                return (
                                    <div key={langCode} className="text-right pl-2" dir="rtl" style={{ marginBottom: isFirst && activeLangEntries.length > 1 ? `${internalVerticalGap}px` : '0px' }}>
                                        <p className="font-serif text-slate-800 dark:text-slate-100 break-words" style={{ fontSize: `${baseFontSize * 2.0}px`, lineHeight: '1.7' }}>
                                            {segments.map((seg, idx) => (
                                                <span key={idx} onMouseEnter={() => handleMouseEnter(verse.id, seg.cid)} onMouseLeave={handleMouseLeave} className={getSegmentClass(verse.id, seg.cid)}>{seg.text}</span>
                                            ))}
                                        </p>
                                    </div>
                                );
                            }

                            return (
                                <div key={langCode} className="flex items-start border-slate-50 dark:border-slate-800/50" style={getStackStyle(isFirst)}>
                                    <LangBadge code={lang.label} colorClass={theme} />
                                    <div style={{ fontSize: `${baseFontSize}px` }} className="flex-1 min-w-0">
                                        <p className={`${langCode === 'ar-lat' ? 'font-mono' : 'font-sans'} text-slate-700 dark:text-slate-200 leading-relaxed break-words`}>
                                            {segments.map((seg, idx) => (
                                                <span key={idx} onMouseEnter={() => handleMouseEnter(verse.id, seg.cid)} onMouseLeave={handleMouseLeave} className={getSegmentClass(verse.id, seg.cid)}>{seg.text}</span>
                                            ))}
                                        </p>
                                    </div>
                                </div>
                            );
                        } else {
                            // Non-core translations (multiple authors possible)
                            const authors = selectedAuthors[langCode] || [];
                            const langLoaded = loadedTranslations[langCode] || {};

                            return authors.map((authorId, aIdx) => {
                                const authorVerses = langLoaded[authorId];
                                const segments = authorVerses?.find(v => v.verse === verse.id)?.segments;
                                if (!segments) return null;

                                const isFirst = isFirstVisible(langCode) && aIdx === 0;
                                const theme = THEMES[lang.themeKey];
                                const authorLabel = LANGUAGES[langCode].translations.find(t => t.id === authorId)?.author || authorId;

                                return (
                                    <div key={`${langCode}-${authorId}`} className="flex items-start border-slate-50 dark:border-slate-800/50" style={getStackStyle(isFirst)}>
                                        <LangBadge code={lang.label} colorClass={theme} tooltip={authorLabel} />
                                        <div style={{ fontSize: `${baseFontSize}px` }} className="flex-1 min-w-0">
                                            <p className="font-sans text-slate-700 dark:text-slate-200 leading-relaxed break-words">
                                                {segments.map((seg, idx) => {
                                                    let text = isLatin && (langCode === 'ru' || langCode === 'ua')
                                                        ? transliterate(seg.text, langCode)
                                                        : seg.text;
                                                    // Apply collapsible commentary for applicable languages
                                                    const renderedContent = renderTextWithCommentary(text, verse.id, idx);
                                                    return (
                                                        <span key={idx} onMouseEnter={() => handleMouseEnter(verse.id, seg.cid)} onMouseLeave={handleMouseLeave} className={getSegmentClass(verse.id, seg.cid)}>{renderedContent}</span>
                                                    );
                                                })}
                                            </p>
                                        </div>
                                    </div>
                                );
                            });
                        }
                    })}
                </div>
            </div>
        </div>
    );
}
