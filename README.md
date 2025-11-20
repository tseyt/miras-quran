# **Miras Quran \- Semantic Syntax Mapping**

**Miras Quran** is a modern, React-based Quranic study tool designed to bridge the linguistic gap between the source Arabic and translations using **Semantic Concept Mapping**.

Unlike traditional word-by-word translations that often break under the weight of different grammar rules (like SVO vs SOV languages), Miras assigns a **Concept ID (CID)** to semantic chunks. This allows us to map "The Master of the Day of Judgment" (English) to "Ceza kunüniñ saibidir" (Crimean Tatar) accurately, even though the word order is completely reversed.

## **Features**

* **Semantic Highlighting:** Hover over a word in any language to see its equivalent concept in all other languages.  
* **Fluid Typography:** A custom density engine that scales padding, gaps, and font sizes together for optimal reading comfort.  
* **Multi-Language Support:** Built-in support for Arabic (Uthmani), English, Crimean Tatar (Latin), and Turkish.  
* **Developer Friendly:** Data is managed in strict YAML and compiled to JSON, making it easy for backend engineers to extend.

## **Getting Started**

### **Prerequisites**

* Node.js & NPM  
* Python 3 (for the data pipeline)

### **Installation**

1. Clone the repository.  
2. Install dependencies:  
   npm install

3. Run the development server:  
   npm run dev

## **Data Pipeline**

The project separates data from logic. The source of truth is data/quran\_data.yaml.

### **1\. Adding a New Surah**

Open data/quran\_data.yaml and add a new entry under surahs:

  \- id: 114  
    title: "An-Nas"  
    english: "Mankind"  
    type: "Meccan"  
    total\_verses: 6  
    content:  
      \- verse: 1  
        segments:  
          arabic: ...  
          english: ...

### **2\. Adding a New Language**

1. Add the language metadata to the meta.languages list in quran\_data.yaml.  
2. Add the segments to every verse in content.  
3. Update src/QuranHighlighter.jsx to render the new language block (look for the THEMES object 
