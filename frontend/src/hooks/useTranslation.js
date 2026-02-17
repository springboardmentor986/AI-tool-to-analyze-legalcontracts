import { useLanguage } from '../contexts/LanguageContext';
import translations from '../translations';

/**
 * Custom hook for translations
 * Usage: const { t } = useTranslation();
 * Then: t('dashboard.title')
 */
export const useTranslation = () => {
  const { language } = useLanguage();

  /**
   * Translate a key to the current language
   * Supports nested keys with dot notation
   * Example: t('dashboard.title')
   */
  const t = (key, fallback = '') => {
    try {
      const keys = key.split('.');
      let value = translations[language];

      for (const k of keys) {
        if (value && typeof value === 'object' && k in value) {
          value = value[k];
        } else {
          // Fallback to English if translation not found
          value = translations.en;
          for (const fk of keys) {
            if (value && typeof value === 'object' && fk in value) {
              value = value[fk];
            } else {
              return fallback || key;
            }
          }
          break;
        }
      }

      return typeof value === 'string' ? value : (fallback || key);
    } catch (error) {
      console.error(`Translation error for key: ${key}`, error);
      return fallback || key;
    }
  };

  /**
   * Get all translations for a given prefix
   * Example: tAll('domains') returns all domain translations
   */
  const tAll = (prefix) => {
    try {
      const keys = prefix.split('.');
      let value = translations[language];

      for (const k of keys) {
        if (value && typeof value === 'object' && k in value) {
          value = value[k];
        } else {
          return {};
        }
      }

      return typeof value === 'object' ? value : {};
    } catch (error) {
      console.error(`Translation error for prefix: ${prefix}`, error);
      return {};
    }
  };

  return { t, tAll, language };
};

export default useTranslation;
