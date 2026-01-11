import React, { useState, useEffect, useMemo } from 'react';
import Header from './components/Header';
import Controls from './components/Controls';
import VerseCard from './components/VerseCard';
import SurahSelector from './components/SurahSelector';
import Footer from './components/Footer';
import { SURAH_LIST, QURAN_CONTENT, loadTranslations } from './data/quranData';
import { LANGUAGES, DEFAULT_AUTHORS } from './constants/languages';
import translationAvailability from './data/translationAvailability.json';

function App() {
    const [activeSegment, setActiveSegment] = useState({ verseId: null, cid: null });
    const [isDarkMode, setIsDarkMode] = useState(true);
    const [activeSurahId, setActiveSurahId] = useState(1);
    const [showControls, setShowControls] = useState(true); // Default to true as it is inline now
    const [baseFontSize, setBaseFontSize] = useState(20);
    const [spacingUnit, setSpacingUnit] = useState(1);
    const [isLatin, setIsLatin] = useState(false);

    // Modular Translation State
    const [activeLanguages, setActiveLanguages] = useState(new Set(['ar', 'ar-lat', 'en', 'crh']));
    const [selectedAuthors, setSelectedAuthors] = useState(DEFAULT_AUTHORS);
    const [loadedTranslations, setLoadedTranslations] = useState({});

    // Derived availability for current surah
    const availableTranslations = useMemo(() => {
        return translationAvailability[String(activeSurahId)] || [];
    }, [activeSurahId]);

    useEffect(() => {
        if (isDarkMode) {
            document.documentElement.classList.add('dark');
        } else {
            document.documentElement.classList.remove('dark');
        }
    }, [isDarkMode]);

    // Load translations when surah or active languages/authors change
    useEffect(() => {
        const fetchTranslations = async () => {
            const trans = await loadTranslations(activeSurahId, Array.from(activeLanguages), selectedAuthors);
            setLoadedTranslations(trans);
        };
        fetchTranslations();
    }, [activeSurahId, activeLanguages, selectedAuthors]);

    const activeSurah = useMemo(() =>
        SURAH_LIST.find(s => s.id === activeSurahId),
        [activeSurahId]);

    const verses = useMemo(() => {
        return QURAN_CONTENT[activeSurahId] || [];
    }, [activeSurahId]);

    const toggleLanguage = (langCode) => {
        setActiveLanguages(prev => {
            const next = new Set(prev);
            if (next.has(langCode)) {
                if (next.size > 1) next.delete(langCode);
            } else {
                next.add(langCode);
            }
            return next;
        });
    };

    const toggleAuthor = (langCode, authorId) => {
        setSelectedAuthors(prev => {
            const current = prev[langCode] || [];
            let next;
            if (current.includes(authorId)) {
                // Remove, but keep at least one
                if (current.length > 1) {
                    next = current.filter(id => id !== authorId);
                } else {
                    next = current;
                }
            } else {
                next = [...current, authorId];
            }
            return { ...prev, [langCode]: next };
        });
    };

    return (
        <div className="min-h-screen bg-slate-50 dark:bg-slate-950 transition-colors duration-300 poly-grid">
            <header className="sticky top-0 z-40 bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800 shadow-sm">
                <Header
                    showControls={showControls}
                    setShowControls={setShowControls}
                    isDarkMode={isDarkMode}
                    setIsDarkMode={setIsDarkMode}
                />

                <div className="px-6 py-3 border-t border-slate-100 dark:border-slate-800/50 flex flex-col md:flex-row gap-4 items-center justify-between max-w-7xl mx-auto">
                    <SurahSelector
                        surahList={SURAH_LIST}
                        activeSurahId={activeSurahId}
                        setActiveSurahId={setActiveSurahId}
                    />

                    <Controls
                        isOpen={showControls}
                        activeLanguages={activeLanguages}
                        toggleLanguage={toggleLanguage}
                        selectedAuthors={selectedAuthors}
                        toggleAuthor={toggleAuthor}
                        baseFontSize={baseFontSize}
                        setBaseFontSize={setBaseFontSize}
                        spacingUnit={spacingUnit}
                        setSpacingUnit={setSpacingUnit}
                        isLatin={isLatin}
                        setIsLatin={setIsLatin}
                        availableTranslations={availableTranslations}
                    />
                </div>
            </header>

            <main
                className="container mx-auto px-4 py-4 min-h-screen transition-all duration-300"
                style={{ maxWidth: `${Math.max(896, 1200 + (baseFontSize - 14) * 35)}px` }}
            >
                <div
                    className="flex flex-col pb-4"
                    style={{ gap: `${Math.max(0, (baseFontSize - 14) * 2.0) * spacingUnit}px` }}
                >
                    {verses.map(v => (
                        <VerseCard
                            key={v.id}
                            verse={v}
                            activeSegment={activeSegment}
                            setActiveSegment={setActiveSegment}
                            activeLanguages={activeLanguages}
                            selectedAuthors={selectedAuthors}
                            loadedTranslations={loadedTranslations}
                            baseFontSize={baseFontSize}
                            spacingUnit={spacingUnit}
                            isLatin={isLatin}
                        />
                    ))}
                </div>
            </main>

            <Footer />
        </div>
    );
}

export default App;
