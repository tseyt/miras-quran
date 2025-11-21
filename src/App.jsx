import React, { useState } from 'react';
import { BookOpen, Heart } from 'lucide-react';
import Header from './components/Header';
import Controls from './components/Controls';
import Navigation from './components/Navigation';
import VerseCard from './components/VerseCard';
import { SURAH_LIST, QURAN_CONTENT } from './data/quranData';
import { LAYOUT_STYLES } from './constants/theme';

export default function App() {
    const [activeSegment, setActiveSegment] = useState({ verseId: null, cid: null });
    const [isDarkMode, setIsDarkMode] = useState(false);
    const [activeSurahId, setActiveSurahId] = useState(1);
    const [showControls, setShowControls] = useState(true);
    const [searchQuery, setSearchQuery] = useState("");

    const [showArabic, setShowArabic] = useState(true);
    const [showTranslit, setShowTranslit] = useState(true);
    const [showEnglish, setShowEnglish] = useState(true);
    const [showCrh, setShowCrh] = useState(true);
    const [showTurkish, setShowTurkish] = useState(true);

    const [baseFontSize, setBaseFontSize] = useState(18);

    const spacingUnit = Math.max(8, baseFontSize - 6);
    const panelGap = Math.max(0, (baseFontSize - 14) * 2);
    const horizontalGap = Math.max(8, (baseFontSize - 14) + 8);
    const internalVerticalGap = Math.max(0, (baseFontSize - 14) * 1.5);

    const currentSurah = SURAH_LIST.find(s => s.id === activeSurahId) || SURAH_LIST[0];
    const surahContent = QURAN_CONTENT[activeSurahId] || [];

    return (
        <div className={`${isDarkMode ? 'dark' : ''} ${LAYOUT_STYLES.pageWrapper}`}>

            <Header
                showControls={showControls}
                setShowControls={setShowControls}
                isDarkMode={isDarkMode}
                setIsDarkMode={setIsDarkMode}
            />

            {showControls && (
                <Controls
                    showArabic={showArabic} setShowArabic={setShowArabic}
                    showTranslit={showTranslit} setShowTranslit={setShowTranslit}
                    showEnglish={showEnglish} setShowEnglish={setShowEnglish}
                    showCrh={showCrh} setShowCrh={setShowCrh}
                    showTurkish={showTurkish} setShowTurkish={setShowTurkish}
                    baseFontSize={baseFontSize} setBaseFontSize={setBaseFontSize}
                />
            )}

            <Navigation
                activeSurahId={activeSurahId}
                setActiveSurahId={setActiveSurahId}
                searchQuery={searchQuery}
                setSearchQuery={setSearchQuery}
            />

            <main className={LAYOUT_STYLES.main}>
                <div className={LAYOUT_STYLES.container}>

                    <div className="flex flex-col py-4 sm:py-8" style={{ gap: `${panelGap}px` }}>
                        {surahContent.length > 0 ? (
                            surahContent.map((verse) => (
                                <VerseCard
                                    key={verse.id}
                                    verse={verse}
                                    activeSegment={activeSegment}
                                    setActiveSegment={setActiveSegment}
                                    showArabic={showArabic}
                                    showTranslit={showTranslit}
                                    showEnglish={showEnglish}
                                    showCrh={showCrh}
                                    showTurkish={showTurkish}
                                    baseFontSize={baseFontSize}
                                    spacingUnit={spacingUnit}
                                    internalVerticalGap={internalVerticalGap}
                                    horizontalGap={horizontalGap}
                                />
                            ))
                        ) : (
                            <div className="text-center py-20">
                                <BookOpen className="w-12 h-12 text-slate-300 dark:text-slate-700 mx-auto mb-4" />
                                <p className="text-slate-400 dark:text-slate-500 text-lg font-medium">Content for {currentSurah.title} is coming soon.</p>
                                <p className="text-slate-400 dark:text-slate-500 text-sm mt-2">Select another surah from the menu above.</p>
                            </div>
                        )}
                    </div>

                    <footer className={LAYOUT_STYLES.footer}>
                        <p className="font-medium text-slate-500 dark:text-slate-400 flex items-center justify-center gap-1">
                            Made with <Heart className="w-3 h-3 text-rose-500 fill-rose-500" /> for the Ümmet
                        </p>
                        <p className="mt-2 text-xs opacity-75">Credits: Sait Dizen & Zakir Qurtnezir (CRH), Abdel Haleem (EN), Elmalılı (TR)</p>
                    </footer>

                </div>
            </main>

        </div>
    );
}
