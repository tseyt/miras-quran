import React from 'react';
import LangBadge from './LangBadge';
import { COLORS, THEMES, HOVER_STYLES, LAYOUT_STYLES } from '../constants/theme';
import { LANGUAGES } from '../constants/languages';
import { transliterate } from '../utils/transliteration';

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
    // Standardize gaps based on spacing unit and font size
    // Scales to near-zero at 14px
    const internalVerticalGap = Math.max(0, (baseFontSize - 14) * 1.8) * spacingUnit;
    const horizontalGap = 16;
    const cardPadding = Math.max(2, (baseFontSize - 14) * 1.5 + 4) * spacingUnit;

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
                                                    const text = isLatin && (langCode === 'ru' || langCode === 'ua')
                                                        ? transliterate(seg.text, langCode)
                                                        : seg.text;
                                                    return (
                                                        <span key={idx} onMouseEnter={() => handleMouseEnter(verse.id, seg.cid)} onMouseLeave={handleMouseLeave} className={getSegmentClass(verse.id, seg.cid)}>{text}</span>
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
