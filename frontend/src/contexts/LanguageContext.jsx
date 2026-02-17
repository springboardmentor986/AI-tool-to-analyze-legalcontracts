import React, { createContext, useState, useContext, useEffect } from 'react';

// Language Context
const LanguageContext = createContext();

// Supported languages
export const SUPPORTED_LANGUAGES = {
  en: { code: 'en', name: 'English', nativeName: 'English' },
  ta: { code: 'ta', name: 'Tamil', nativeName: 'தமிழ்' },
  hi: { code: 'hi', name: 'Hindi', nativeName: 'हिंदी' },
  te: { code: 'te', name: 'Telugu', nativeName: 'తెలుగు' },
  ml: { code: 'ml', name: 'Malayalam', nativeName: 'മലയാളം' }
};

// Language Provider Component
export const LanguageProvider = ({ children }) => {
  // Get saved language from localStorage or default to 'en'
  const [language, setLanguageState] = useState(() => {
    const savedLanguage = localStorage.getItem('clauseai_language');
    return savedLanguage || 'en';
  });

  // Save language preference to localStorage
  const setLanguage = (newLanguage) => {
    if (SUPPORTED_LANGUAGES[newLanguage]) {
      setLanguageState(newLanguage);
      localStorage.setItem('clauseai_language', newLanguage);
      // Set HTML lang attribute for accessibility
      document.documentElement.lang = newLanguage;
    }
  };

  // Set initial HTML lang attribute
  useEffect(() => {
    document.documentElement.lang = language;
  }, [language]);

  const value = {
    language,
    setLanguage,
    languages: SUPPORTED_LANGUAGES,
    currentLanguage: SUPPORTED_LANGUAGES[language]
  };

  return (
    <LanguageContext.Provider value={value}>
      {children}
    </LanguageContext.Provider>
  );
};

// Custom hook to use language context
export const useLanguage = () => {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error('useLanguage must be used within a LanguageProvider');
  }
  return context;
};

export default LanguageContext;
