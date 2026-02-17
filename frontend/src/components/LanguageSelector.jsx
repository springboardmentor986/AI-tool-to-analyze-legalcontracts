import React from 'react';
import { useLanguage } from '../contexts/LanguageContext';
import { FiGlobe } from 'react-icons/fi';
import './LanguageSelector.css';

const LanguageSelector = () => {
  const { language, setLanguage, languages } = useLanguage();

  const handleLanguageChange = (e) => {
    setLanguage(e.target.value);
  };

  return (
    <div className="language-selector">
      <FiGlobe className="language-icon" />
      <select 
        value={language} 
        onChange={handleLanguageChange}
        className="language-dropdown"
        aria-label="Select Language"
      >
        {Object.values(languages).map((lang) => (
          <option key={lang.code} value={lang.code}>
            {lang.nativeName}
          </option>
        ))}
      </select>
    </div>
  );
};

export default LanguageSelector;
