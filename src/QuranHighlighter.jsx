import React, { useState } from 'react';
import { BookOpen, Settings, Moon, Sun, Type, ChevronDown, Search, Heart } from 'lucide-react';

// --- DATA STRUCTURES ---

const SURAH_LIST = [
  { id: 1, title: "El-Fatiha", english: "The Opening", type: "Meccan", verses: 7 },
  { id: 2, title: "El-Baqarah", english: "The Cow", type: "Medinan", verses: 286 },
  { id: 3, title: "Ali 'Imran", english: "Family of Imran", type: "Medinan", verses: 200 },
  { id: 4, title: "En-Nisa", english: "The Women", type: "Medinan", verses: 176 },
];

const QURAN_CONTENT = {
  1: [
    {
      id: 1,
      verse: 1,
      segments: {
        arabic: [
          { text: "بِسْمِ", cid: 1 },
          { text: " ", cid: 0 },
          { text: "ٱللَّٰهِ", cid: 2 },
          { text: " ", cid: 0 },
          { text: "ٱلرَّحْمَٰنِ", cid: 3 },
          { text: " ", cid: 0 },
          { text: "ٱلرَّحِيمِ", cid: 4 }
        ],
        transliteration: [
          { text: "Bismi", cid: 1 },
          { text: "-llāhi", cid: 2 },
          { text: " ar-Raḥmāni", cid: 3 },
          { text: " ar-Raḥīm", cid: 4 }
        ],
        english: [
          { text: "In the name", cid: 1 },
          { text: " of God,", cid: 2 },
          { text: " the Lord of Mercy,", cid: 3 },
          { text: " the Giver of Mercy!", cid: 4 }
        ],
        crh: [
          { text: "Rahman", cid: 3 },
          { text: " ve ", cid: 0 },
          { text: "rahim", cid: 4 },
          { text: " olğan ", cid: 0 },
          { text: "Allahnıñ", cid: 2 },
          { text: " ", cid: 0 },
          { text: "adınen.", cid: 1 }
        ],
        turkish: [
          { text: "Rahmân", cid: 3 },
          { text: " ve ", cid: 0 },
          { text: "Rahîm", cid: 4 },
          { text: " olan ", cid: 0 },
          { text: "Allah'ın", cid: 2 },
          { text: " ", cid: 0 },
          { text: "ismiyle.", cid: 1 }
        ]
      }
    },
    {
      id: 2,
      verse: 2,
      segments: {
        arabic: [
          { text: "ٱلْحَمْدُ", cid: 1 },
          { text: " ", cid: 0 },
          { text: "لِلَّهِ", cid: 2 },
          { text: " ", cid: 0 },
          { text: "رَبِّ", cid: 3 },
          { text: " ", cid: 0 },
          { text: "ٱلْعَٰلَمِينَ", cid: 4 }
        ],
        transliteration: [
          { text: "Al-ḥamdu", cid: 1 },
          { text: " lillāhi", cid: 2 },
          { text: " rabbi", cid: 3 },
          { text: " al-ʿālamīn", cid: 4 }
        ],
        english: [
          { text: "Praise", cid: 1 },
          { text: " belongs to God,", cid: 2 },
          { text: " Lord", cid: 3 },
          { text: " of the Worlds,", cid: 4 }
        ],
        crh: [
          { text: "Hamd", cid: 1 },
          { text: " (maqtav ve maqtalmaq) ", cid: 0 },
          { text: "alemlerniñ", cid: 4 },
          { text: " ", cid: 0 },
          { text: "Rabbi", cid: 3 },
          { text: " ", cid: 0 },
          { text: "Allahqa aittir.", cid: 2 } 
        ],
        turkish: [
          { text: "Hamd", cid: 1 },
          { text: " o ", cid: 0 },
          { text: "âlemlerin", cid: 4 },
          { text: " ", cid: 0 },
          { text: "Rabbi,", cid: 3 }
        ]
      }
    },
    {
      id: 3,
      verse: 3,
      segments: {
        arabic: [
          { text: "ٱلرَّحْمَٰنِ", cid: 1 },
          { text: " ", cid: 0 },
          { text: "ٱلرَّحِيمِ", cid: 2 }
        ],
        transliteration: [
          { text: "Ar-Raḥmāni", cid: 1 },
          { text: " ar-Raḥīm", cid: 2 }
        ],
        english: [
          { text: "The Lord of Mercy,", cid: 1 },
          { text: " the Giver of Mercy,", cid: 2 }
        ],
        crh: [
          { text: "O ", cid: 0 },
          { text: "rahmandır", cid: 1 },
          { text: " ve ", cid: 0 },
          { text: "rahimdir.", cid: 2 }
        ],
        turkish: [
          { text: "O ", cid: 0 },
          { text: "Rahmân", cid: 1 },
          { text: " ve ", cid: 0 },
          { text: "Rahim,", cid: 2 }
        ]
      }
    },
    {
      id: 4,
      verse: 4,
      segments: {
        arabic: [
          { text: "مَٰلِكِ", cid: 1 },
          { text: " ", cid: 0 },
          { text: "يَوْمِ", cid: 2 },
          { text: " ", cid: 0 },
          { text: "ٱلدِّينِ", cid: 3 }
        ],
        transliteration: [
          { text: "Māliki", cid: 1 },
          { text: " yawmi", cid: 2 },
          { text: "-ddīn", cid: 3 }
        ],
        english: [
          { text: "Master", cid: 1 },
          { text: " of the Day", cid: 2 },
          { text: " of Judgment.", cid: 3 }
        ],
        crh: [
          { text: "Ceza", cid: 3 }, 
          { text: " ", cid: 0 },
          { text: "kunüniñ", cid: 2 }, 
          { text: " ", cid: 0 },
          { text: "saibidir.", cid: 1 }
        ],
        turkish: [
          { text: "O, ", cid: 0 },
          { text: "din", cid: 3 },
          { text: " ", cid: 0 },
          { text: "gününün", cid: 2 },
          { text: " ", cid: 0 },
          { text: "maliki", cid: 1 },
          { text: " ", cid: 0 },
          { text: "Allah'ın.", cid: 4 }
        ]
      }
    },
    {
      id: 5,
      verse: 5,
      segments: {
        arabic: [
          { text: "إِيَّاكَ", cid: 1 },
          { text: " ", cid: 0 },
          { text: "نَعْبُدُ", cid: 2 },
          { text: " ", cid: 0 },
          { text: "وَإِيَّاكَ", cid: 1 },
          { text: " ", cid: 0 },
          { text: "نَسْتَعِينُ", cid: 3 }
        ],
        transliteration: [
          { text: "Iyyāka", cid: 1 },
          { text: " naʿbudu", cid: 2 },
          { text: " wa iyyāka", cid: 1 },
          { text: " nastaʿīn", cid: 3 }
        ],
        english: [
          { text: "It is You", cid: 1 },
          { text: " we worship;", cid: 2 },
          { text: " it is You", cid: 1 },
          { text: " we ask for help.", cid: 3 }
      ],
      crh: [
        { text: "(Rabbimiz!) ", cid: 0 },
        { text: "Yalıñız Saña", cid: 1 },
        { text: " ", cid: 0 },
        { text: "qullıq etermiz", cid: 2 },
        { text: " ve ", cid: 0 },
        { text: "yalıñız Senden", cid: 1 },
        { text: " ", cid: 0 },
        { text: "medet umüt etermiz.", cid: 3 }
      ],
      turkish: [
        { text: "Ancak sana", cid: 1 },
        { text: " ederiz kulluğu, ibadeti", cid: 2 },
        { text: " ve ", cid: 0 },
        { text: "ancak senden", cid: 1 },
        { text: " dileriz yardımı, inayeti.", cid: 3 },
        { text: " (Ya Rab!).", cid: 0 }
      ]
      }
    },
    {
      id: 6,
      verse: 6,
      segments: {
        arabic: [
          { text: "ٱهْدِنَا", cid: 1 },
          { text: " ", cid: 0 },
          { text: "ٱلصِّرَٰطَ", cid: 2 },
          { text: " ", cid: 0 },
          { text: "ٱلْمُسْتَقِيمَ", cid: 3 }
        ],
        transliteration: [
          { text: "Ihdinā", cid: 1 },
          { text: " aṣ-ṣirāṭa", cid: 2 },
          { text: " al-mustaqīm", cid: 3 }
        ],
        english: [
          { text: "Guide us", cid: 1 },
          { text: " to the straight", cid: 3 },
          { text: " path:", cid: 2 }
        ],
        crh: [
          { text: "Bizge", cid: 1 }, 
          { text: " ", cid: 0 },
          { text: "doğru", cid: 3 },
          { text: " ", cid: 0 },
          { text: "yolnı", cid: 2 },
          { text: " ", cid: 0 },
          { text: "koster.", cid: 1 } 
        ],
        turkish: [
          { text: "Hidayet eyle bizi", cid: 1 },
          { text: " ", cid: 0 },
          { text: "doğru", cid: 3 },
          { text: " ", cid: 0 },
          { text: "yola,", cid: 2 }
        ]
      }
    },
    {
      id: 7,
      verse: 7,
      segments: {
        arabic: [
          { text: "صِرَٰطَ", cid: 1 },
          { text: " ", cid: 0 },
          { text: "ٱلَّذِينَ أَنْعَمْتَ عَلَيْهِمْ", cid: 2 },
          { text: " ", cid: 0 },
          { text: "غَيْرِ", cid: 3 }, 
          { text: " ", cid: 0 },
          { text: "ٱلْمَغْضُوبِ عَلَيْهِمْ", cid: 3 },
          { text: " ", cid: 0 },
          { text: "وَلَا", cid: 4 },
          { text: " ", cid: 0 },
          { text: "ٱلضَّآلِّينَ", cid: 4 }
        ],
        transliteration: [
          { text: "Ṣirāṭa", cid: 1 },
          { text: " alladhīna anʿamta ʿalayhim", cid: 2 },
          { text: " ghayri", cid: 3 },
          { text: " l-maghḍūbi ʿalayhim", cid: 3 },
          { text: " wa-lā", cid: 4 },
          { text: " ḍ-ḍāllīn", cid: 4 }
        ],
        english: [
          { text: "the path", cid: 1 },
          { text: " of those You have blessed,", cid: 2 },
          { text: " those who incur no anger", cid: 3 },
          { text: " and who have not gone astray.", cid: 4 }
        ],
        crh: [
          { text: "Ozlerine lütf ve ikram etken kimseleriñniñ", cid: 2 },
          { text: " ", cid: 0 },
          { text: "yolunı;", cid: 1 },
          { text: " ", cid: 0 },
          { text: "ğadapqa oğrağanlarnıñ", cid: 3 },
          { text: " ", cid: 0 },
          { text: "ve", cid: 0 },
          { text: " ", cid: 0 },
          { text: "sapqanlarnıñ", cid: 4 },
          { text: " ", cid: 0 },
          { text: "yolunı degil!", cid: 1 }
        ],
        turkish: [
          { text: "O kendilerine nimet verdiğin mutlu kimselerin", cid: 2 },
          { text: " ", cid: 0 },
          { text: "yoluna;", cid: 1 },
          { text: " ", cid: 0 },
          { text: "o gazaba uğramışların", cid: 3 },
          { text: " ", cid: 0 },
          { text: "ve", cid: 0 },
          { text: " ", cid: 0 },
          { text: "o sapmışların", cid: 4 },
          { text: " ", cid: 0 },
          { text: "yoluna değil.", cid: 1 }
        ]
      }
    }
  ]
};

const COLORS = {
  1: "text-blue-600 dark:text-blue-400 bg-blue-100 dark:bg-blue-900/30",
  2: "text-emerald-600 dark:text-emerald-400 bg-emerald-100 dark:bg-emerald-900/30",
  3: "text-purple-600 dark:text-purple-400 bg-purple-100 dark:bg-purple-900/30",
  4: "text-amber-600 dark:text-amber-400 bg-amber-100 dark:bg-amber-900/30",
  5: "text-rose-600 dark:text-rose-400 bg-rose-100 dark:bg-rose-900/30",
  default: "text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800"
};

const HOVER_STYLES = "cursor-pointer transition-colors duration-150 rounded px-0.5 mx-0.5";

const LangBadge = ({ code, colorClass }) => (
  <div className={`w-10 shrink-0 flex justify-center items-center rounded py-1 px-1.5 border ${colorClass}`}>
    <span className="text-[0.65rem] font-bold tracking-wider uppercase">{code}</span>
  </div>
);

const THEMES = {
  arabic: "bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 border-slate-300 dark:border-slate-600 hover:bg-slate-200 dark:hover:bg-slate-700",
  translit: "bg-amber-50 dark:bg-amber-900/20 text-amber-700 dark:text-amber-400 border-amber-200 dark:border-amber-800 hover:bg-amber-100 dark:hover:bg-amber-900/30",
  english: "bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-400 border-blue-200 dark:border-blue-800 hover:bg-blue-100 dark:hover:bg-blue-900/30",
  crh: "bg-emerald-50 dark:bg-emerald-900/20 text-emerald-700 dark:text-emerald-400 border-emerald-200 dark:border-emerald-800 hover:bg-emerald-100 dark:hover:bg-emerald-900/30",
  turkish: "bg-rose-50 dark:bg-rose-900/20 text-rose-700 dark:text-rose-400 border-rose-200 dark:border-rose-800 hover:bg-rose-100 dark:hover:bg-rose-900/30",
  neutral: "bg-slate-50 text-slate-500 border-slate-200 hover:bg-slate-100 dark:bg-slate-800 dark:text-slate-400 dark:border-slate-700"
};

export default function QuranHighlighter() {
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
    <div className={`${isDarkMode ? 'dark' : ''} flex flex-col h-screen bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-100 transition-colors duration-300 font-sans overflow-hidden`}>
      
      <div className="flex flex-col shrink-0 z-30 shadow-sm bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800">
        <div className="px-6 py-3 flex justify-between items-center">
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

        {showControls && (
          <div className="border-t border-slate-100 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-900/50 px-6 py-4 animate-in fade-in slide-in-from-top-1 duration-200">
             <div className="flex flex-col md:flex-row md:items-center gap-6 max-w-3xl mx-auto">
                <div className="flex flex-col gap-2 flex-1">
                  <div className="flex items-center gap-2 text-[10px] uppercase tracking-wider font-bold text-slate-400">
                      Visibility
                  </div>
                  <div className="flex gap-2 flex-wrap">
                      <Toggle label="Arabic" active={showArabic} onClick={() => setShowArabic(!showArabic)} colorTheme={THEMES.arabic} />
                      <Toggle label="Transliteration" active={showTranslit} onClick={() => setShowTranslit(!showTranslit)} colorTheme={THEMES.translit} />
                      <Toggle label="English" active={showEnglish} onClick={() => setShowEnglish(!showEnglish)} colorTheme={THEMES.english} />
                      <Toggle label="Crimean Tatar" active={showCrh} onClick={() => setShowCrh(!showCrh)} colorTheme={THEMES.crh} />
                      <Toggle label="Turkish" active={showTurkish} onClick={() => setShowTurkish(!showTurkish)} colorTheme={THEMES.turkish} />
                  </div>
                </div>
                <div className="hidden md:block w-px h-12 bg-slate-200 dark:bg-slate-700"></div>
                <div className="flex flex-col gap-2 w-full md:w-64">
                    <div className="flex items-center justify-between text-[10px] uppercase tracking-wider font-bold text-slate-400">
                      <div className="flex items-center gap-2"><Type className="w-3 h-3" /> Text Size</div>
                      <span>{baseFontSize}px</span>
                    </div>
                    <div className="flex items-center gap-3">
                      <span className="text-xs text-slate-400 font-medium">A</span>
                      <input 
                          type="range" 
                          min="14" 
                          max="32" 
                          step="1" 
                          value={baseFontSize} 
                          onChange={(e) => setBaseFontSize(parseInt(e.target.value))}
                          className="w-full h-2 bg-slate-200 dark:bg-slate-700 rounded-lg appearance-none cursor-pointer accent-emerald-500"
                      />
                      <span className="text-xl text-slate-600 dark:text-slate-300 font-medium">A</span>
                    </div>
                </div>
             </div>
          </div>
        )}

        <div className="bg-slate-50 dark:bg-slate-950 border-t border-slate-200 dark:border-slate-800 px-6 py-3 flex flex-col md:flex-row gap-4 justify-between items-center">
           <div className="relative group w-full md:w-64">
              <select 
                value={activeSurahId}
                onChange={(e) => setActiveSurahId(Number(e.target.value))}
                className="w-full appearance-none bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-200 py-2 pl-4 pr-10 rounded-lg font-medium cursor-pointer hover:border-emerald-500/50 transition-colors outline-none focus:ring-2 focus:ring-emerald-500/20 text-sm"
              >
                {SURAH_LIST.map(surah => (
                  <option key={surah.id} value={surah.id}>
                    {surah.id}. {surah.title} ({surah.english})
                  </option>
                ))}
              </select>
              <ChevronDown className="w-4 h-4 text-slate-400 absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none" />
            </div>

            <div className="relative w-full md:w-64">
              <input 
                type="text" 
                placeholder="Search verses..." 
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-200 py-2 pl-10 pr-4 rounded-lg text-sm focus:outline-none focus:border-emerald-500 transition-colors placeholder:text-slate-400"
              />
              <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
            </div>
        </div>
      </div>

      <main className="flex-1 overflow-y-auto bg-slate-50 dark:bg-slate-950 p-0 sm:p-4 scroll-smooth">
        <div className="max-w-4xl mx-auto">
          
          <div className="flex flex-col py-4 sm:py-8" style={{ gap: `${panelGap}px` }}>
            {surahContent.length > 0 ? (
              surahContent.map((verse) => (
                <div 
                  key={verse.id} 
                  className="bg-white dark:bg-slate-900 rounded-none sm:rounded-xl shadow-sm border-y sm:border border-slate-200 dark:border-slate-800 overflow-hidden transition-colors duration-300 flex flex-row"
                >
                  {/* Left Gutter - Absolute positioned ID to prevent height expansion */}
                  <div 
                    className="w-10 sm:w-12 shrink-0 bg-slate-50 dark:bg-slate-800/50 border-r border-slate-100 dark:border-slate-800 flex flex-col items-center gap-1 relative"
                    style={{ paddingTop: `${spacingUnit}px`, paddingBottom: `${spacingUnit}px` }}
                  >
                     <span className="text-xs font-bold text-slate-400">{verse.verse}</span>
                     <span className="absolute bottom-1 right-1 text-[10px] font-mono text-emerald-500/70">
                        {activeSegment.verseId === verse.id && activeSegment.cid ? activeSegment.cid : ""}
                     </span>
                  </div>

                  <div className="flex-1 min-w-0" style={{ padding: `${spacingUnit}px` }}>
                    
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
                            <span className="text-emerald-600 font-sans mr-2 text-[0.6em] inline-flex items-center justify-center border border-emerald-600 rounded-full w-[1.2em] h-[1.2em] leading-none align-middle select-none opacity-70">
                               {verse.verse}
                            </span>
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
              ))
            ) : (
              <div className="text-center py-20">
                <BookOpen className="w-12 h-12 text-slate-300 dark:text-slate-700 mx-auto mb-4" />
                <p className="text-slate-400 dark:text-slate-500 text-lg font-medium">Content for {currentSurah.title} is coming soon.</p>
                <p className="text-slate-400 dark:text-slate-500 text-sm mt-2">Select another surah from the menu above.</p>
              </div>
            )}
          </div>

          <footer className="text-center text-slate-400 text-sm py-8 border-t border-slate-200 dark:border-slate-800 mt-8">
             <p className="font-medium text-slate-500 dark:text-slate-400 flex items-center justify-center gap-1">
              Made with <Heart className="w-3 h-3 text-rose-500 fill-rose-500" /> for the Ummah
            </p>
            <p className="mt-2 text-xs opacity-75">Credits: Sait Dizen & Zakir Qurtnezir (CRH), Abdel Haleem (EN), Elmalılı (TR)</p>
          </footer>

        </div>
      </main>

    </div>
  );
}

function Toggle({ label, active, onClick, colorTheme }) {
  const activeStyle = colorTheme || "bg-emerald-50 text-emerald-700 border-emerald-200 dark:bg-emerald-900/20 dark:text-emerald-400 dark:border-emerald-800";
  const inactiveStyle = THEMES.neutral;
  return (
    <button onClick={onClick} className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all duration-200 border ${active ? activeStyle : inactiveStyle}`}>
      {label}
    </button>
  );
}
