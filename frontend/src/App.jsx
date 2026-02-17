import React, { useState } from 'react';
import { LanguageProvider } from './contexts/LanguageContext';
import { useTranslation } from './hooks/useTranslation';
import LanguageSelector from './components/LanguageSelector';
import FileUpload from './components/FileUpload';
import Results from './components/Results';
import './styles/App.css';

function AppContent() {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const { t } = useTranslation();

  const handleAnalysisComplete = (data) => {
    console.log('Analysis complete, received data:', data);
    setResults(data);
    setLoading(false);
    setError(null);
  };

  const handleAnalysisStart = () => {
    console.log('Analysis started');
    setLoading(true);
    setResults(null);
    setError(null);
  };

  return (
    <div className="app">
      <header className="header">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', maxWidth: '1200px', margin: '0 auto', width: '100%' }}>
          <div>
            <h1>⚖️ {t('appName', 'ClauseAI')}</h1>
            <p>{t('tagline', 'AI-Powered Legal Contract Analyzer with Multi-Agent Intelligence')}</p>
          </div>
          <LanguageSelector />
        </div>
      </header>

      <FileUpload 
        onAnalysisStart={handleAnalysisStart}
        onAnalysisComplete={handleAnalysisComplete}
      />

      {loading && (
        <div className="loading-container">
          <div className="spinner"></div>
          <h3>{t('upload.analyzing', 'Analyzing Contract...')}</h3>
          <p>{t('upload.pleaseWait', 'Our AI agents are working on your contract. This may take a moment.')}</p>
        </div>
      )}

      {error && (
        <div className="results-section">
          <div className="card">
            <div className="card-header">
              <h2>❌ {t('messages.error', 'Error')}</h2>
            </div>
            <div className="card-body">
              <p>{error}</p>
            </div>
          </div>
        </div>
      )}

      {results && !loading && !error && <Results data={results} />}
    </div>
  );
}

function App() {
  return (
    <LanguageProvider>
      <AppContent />
    </LanguageProvider>
  );
}

export default App;
