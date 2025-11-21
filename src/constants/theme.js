export const COLORS = {
    1: "text-blue-600 dark:text-blue-400 bg-blue-100 dark:bg-blue-900/30",
    2: "text-emerald-600 dark:text-emerald-400 bg-emerald-100 dark:bg-emerald-900/30",
    3: "text-purple-600 dark:text-purple-400 bg-purple-100 dark:bg-purple-900/30",
    4: "text-amber-600 dark:text-amber-400 bg-amber-100 dark:bg-amber-900/30",
    5: "text-rose-600 dark:text-rose-400 bg-rose-100 dark:bg-rose-900/30",
    default: "text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800"
};

export const HOVER_STYLES = "cursor-pointer transition-colors duration-150 rounded px-0.5 mx-0.5";

export const THEMES = {
    arabic: "bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 border-slate-300 dark:border-slate-600 hover:bg-slate-200 dark:hover:bg-slate-700",
    translit: "bg-amber-50 dark:bg-amber-900/20 text-amber-700 dark:text-amber-400 border-amber-200 dark:border-amber-800 hover:bg-amber-100 dark:hover:bg-amber-900/30",
    english: "bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-400 border-blue-200 dark:border-blue-800 hover:bg-blue-100 dark:hover:bg-blue-900/30",
    crh: "bg-emerald-50 dark:bg-emerald-900/20 text-emerald-700 dark:text-emerald-400 border-emerald-200 dark:border-emerald-800 hover:bg-emerald-100 dark:hover:bg-emerald-900/30",
    turkish: "bg-rose-50 dark:bg-rose-900/20 text-rose-700 dark:text-rose-400 border-rose-200 dark:border-rose-800 hover:bg-rose-100 dark:hover:bg-rose-900/30",
    neutral: "bg-slate-50 text-slate-500 border-slate-200 hover:bg-slate-100 dark:bg-slate-800 dark:text-slate-400 dark:border-slate-700"
};

export const LAYOUT_STYLES = {
    pageWrapper: "flex flex-col h-screen bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-100 transition-colors duration-300 font-sans overflow-hidden",
    header: "flex flex-col shrink-0 z-30 shadow-sm bg-white dark:bg-slate-900",
    headerContent: "px-6 py-3 flex justify-between items-center",
    controls: "border-t border-slate-100 dark:border-slate-800 bg-white dark:bg-slate-900 px-6 py-4 animate-in fade-in slide-in-from-top-1 duration-200",
    navigation: "bg-slate-50 dark:bg-slate-950 border-b border-slate-200 dark:border-slate-800 px-6 py-3 flex flex-col md:flex-row gap-4 justify-between items-center",
    main: "flex-1 overflow-y-auto bg-slate-50 dark:bg-slate-950 p-0 sm:p-4 scroll-smooth",
    container: "max-w-4xl mx-auto",
    footer: "text-center text-slate-400 text-sm py-8 border-t border-slate-200 dark:border-slate-800 mt-8",

    // VerseCard specific
    card: "bg-white dark:bg-slate-900 rounded-none sm:rounded-xl shadow-sm border-y sm:border border-slate-200 dark:border-slate-800 overflow-hidden transition-colors duration-300 flex flex-col relative",
    // gutter style removed as it is no longer used
};
