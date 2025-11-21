export const SURAH_LIST = [
    { id: 1, title: "El-Fatiha", english: "The Opening", type: "Meccan", verses: 7 },
    { id: 2, title: "El-Baqarah", english: "The Cow", type: "Medinan", verses: 286 },
    { id: 3, title: "Ali 'Imran", english: "Family of Imran", type: "Medinan", verses: 200 },
    { id: 4, title: "En-Nisa", english: "The Women", type: "Medinan", verses: 176 },
];

export const QURAN_CONTENT = {
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
