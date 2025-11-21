import React from 'react';
import LangBadge from './LangBadge';
import { COLORS, THEMES, HOVER_STYLES, LAYOUT_STYLES } from '../constants/theme';

export default function VerseCard({
    verse,
    activeSegment,
    setActiveSegment,
    showArabic,
    showTranslit,
    showEnglish,
    showCrh,
    showTurkish,
    baseFontSize,
    spacingUnit,
    internalVerticalGap,
    horizontalGap
}) {

    const getSegmentClass = (verseId, cid) => {
        if (cid === 0) return "text-slate-400 dark:text-slate-500";
        const isActive = activeSegment.verseId === verseId && activeSegment.cid === cid;
        const colorClass = COLORS[cid % 6] || COLORS.default;
        return `${HOVER_STYLES} ${isActive ? `${colorClass} shadow-sm` : `hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-600 dark:text-slate-300`}`;
    };

    const handleMouseEnter = (verseId, cid) => {
        if (cid !== 0) setActiveSegment({ verseId, cid });
    };

    const handleMouseLeave = () => {
        setActiveSegment({ verseId: null, cid: null });
    };

    // Helper to determine if a language block is the first visible item
    const isFirstVisible = (lang) => {
        const order = ['arabic', 'translit', 'english', 'crh', 'turkish'];
        const visibility = {
            arabic: showArabic,
            translit: showTranslit,
            english: showEnglish,
            crh: showCrh,
            turkish: showTurkish
        };
        // If arabic is shown, nothing else is "first" in the stacked list below it
        if (showArabic && lang !== 'arabic') return false;

        // Find first visible
        const first = order.find(l => visibility[l]);
        return first === lang;
    };

    const getStackStyle = (isFirst) => {
        return {
            paddingTop: isFirst ? '0px' : `${internalVerticalGap}px`,
            gap: `${horizontalGap}px`,
            borderTopWidth: isFirst ? '0px' : '1px'
        };
    };

    return (
        <div
            className={LAYOUT_STYLES.card}
        >
            {/* Verse ID - Top Left */}
            <div className="absolute top-2 left-2 z-10 flex items-center gap-1">
                <span className="text-xs font-bold text-slate-400 bg-slate-50 dark:bg-slate-800 px-1.5 py-0.5 rounded">
                    {verse.verse}
                </span>
                {verse.context_mapped && (
                    <span className="w-2 h-2 rounded-full bg-emerald-500" title="Context Mapped"></span>
                )}
            </div>

            {/* Concept ID - Bottom Right */}
            <div className="absolute bottom-1 right-1 z-10">
                <span className="text-[10px] font-mono text-emerald-500/70 bg-slate-50/80 dark:bg-slate-800/80 px-1 rounded">
                    {activeSegment.verseId === verse.id && activeSegment.cid ? activeSegment.cid : ""}
                </span>
            </div>

            <div className="flex-1 min-w-0" style={{ padding: `${spacingUnit}px`, paddingTop: `${spacingUnit + 10}px` }}>

                <div style={{ display: 'flex', flexDirection: 'column', gap: `${internalVerticalGap}px` }}>

                    {/* Arabic Script */}
                    {showArabic && (
                        <div
                            className="text-right pl-2"
                            dir="rtl"
                            style={{ marginBottom: isFirstVisible('arabic') && (showTranslit || showEnglish || showCrh || showTurkish) ? `${internalVerticalGap}px` : '0px' }}
                        >
                            <p
                                className="font-serif text-slate-800 dark:text-slate-100"
                                style={{ fontSize: `${baseFontSize * 2.0}px`, lineHeight: '1.7' }}
                            >
                                {verse.segments.arabic.map((seg, idx) => (
                                    <span
                                        key={idx}
                                        onMouseEnter={() => handleMouseEnter(verse.id, seg.cid)}
                                        onMouseLeave={handleMouseLeave}
                                        className={getSegmentClass(verse.id, seg.cid)}
                                    >
                                        {seg.text}
                                    </span>
                                ))}
                            </p>
                        </div>
                    )}

                    {/* Stacked Translations - Logic to remove top border/padding if first visible */}

                    {showTranslit && (
                        <div
                            className="flex items-start border-slate-50 dark:border-slate-800/50"
                            style={getStackStyle(isFirstVisible('translit'))}
                        >
                            <LangBadge code="LAT" colorClass={THEMES.translit} />
                            <p
                                className="font-mono text-slate-600 dark:text-slate-300 leading-relaxed"
                                style={{ fontSize: `${baseFontSize}px` }}
                            >
                                {verse.segments.transliteration.map((seg, idx) => (
                                    <span
                                        key={idx}
                                        onMouseEnter={() => handleMouseEnter(verse.id, seg.cid)}
                                        onMouseLeave={handleMouseLeave}
                                        className={getSegmentClass(verse.id, seg.cid)}
                                    >
                                        {seg.text}
                                    </span>
                                ))}
                            </p>
                        </div>
                    )}

                    {showEnglish && (
                        <div
                            className="flex items-start border-slate-50 dark:border-slate-800/50"
                            style={getStackStyle(isFirstVisible('english'))}
                        >
                            <LangBadge code="EN" colorClass={THEMES.english} />
                            <p
                                className="text-slate-700 dark:text-slate-200 leading-relaxed"
                                style={{ fontSize: `${baseFontSize}px` }}
                            >
                                {verse.segments.english.map((seg, idx) => (
                                    <span
                                        key={idx}
                                        onMouseEnter={() => handleMouseEnter(verse.id, seg.cid)}
                                        onMouseLeave={handleMouseLeave}
                                        className={getSegmentClass(verse.id, seg.cid)}
                                    >
                                        {seg.text}
                                    </span>
                                ))}
                            </p>
                        </div>
                    )}

                    {showCrh && (
                        <div
                            className="flex items-start border-slate-50 dark:border-slate-800/50"
                            style={getStackStyle(isFirstVisible('crh'))}
                        >
                            <LangBadge code="CRH" colorClass={THEMES.crh} />
                            <div style={{ fontSize: `${baseFontSize}px` }}>
                                <p className="font-medium text-slate-800 dark:text-slate-100 leading-relaxed">
                                    {verse.segments.crh.map((seg, idx) => (
                                        <span
                                            key={idx}
                                            onMouseEnter={() => handleMouseEnter(verse.id, seg.cid)}
                                            onMouseLeave={handleMouseLeave}
                                            className={getSegmentClass(verse.id, seg.cid)}
                                        >
                                            {seg.text}
                                        </span>
                                    ))}
                                </p>
                            </div>
                        </div>
                    )}

                    {showTurkish && (
                        <div
                            className="flex items-start border-slate-50 dark:border-slate-800/50"
                            style={getStackStyle(isFirstVisible('turkish'))}
                        >
                            <LangBadge code="TR" colorClass={THEMES.turkish} />
                            <div style={{ fontSize: `${baseFontSize}px` }}>
                                <p className="font-medium text-slate-800 dark:text-slate-100 leading-relaxed">
                                    {verse.segments.turkish.map((seg, idx) => (
                                        <span
                                            key={idx}
                                            onMouseEnter={() => handleMouseEnter(verse.id, seg.cid)}
                                            onMouseLeave={handleMouseLeave}
                                            className={getSegmentClass(verse.id, seg.cid)}
                                        >
                                            {seg.text}
                                        </span>
                                    ))}
                                </p>
                            </div>
                        </div>
                    )}
                </div>

            </div>
        </div>
    );
}
