import React, { useState } from 'react';
import axios from 'axios';
import { FiDownload, FiFileText, FiCode, FiVolume2, FiStopCircle } from 'react-icons/fi';
import { useLanguage } from '../contexts/LanguageContext';

const ReportExport = ({ analysisData }) => {
  const { language } = useLanguage();
  const [generating, setGenerating] = useState(false);
  const [speakingText, setSpeakingText] = useState(false);
  const [selectedTone, setSelectedTone] = useState('professional');
  const [selectedFormat, setSelectedFormat] = useState('pdf');

  const generateReport = async () => {
    if (!analysisData) {
      return;
    }

    setGenerating(true);

    try {
      const response = await axios.post('http://localhost:8000/generate-report', {
        analysis_results: analysisData,
        tone: selectedTone,
        format: selectedFormat,
        include_clauses: true,
        include_risks: true,
        include_discussions: true,
        include_recommendations: true,
        focus_areas: ['compliance', 'finance', 'legal', 'operations']
      }, {
        responseType: selectedFormat === 'pdf' || selectedFormat === 'docx' ? 'blob' : 'json'
      });

      // Download the report
      if (selectedFormat === 'pdf' || selectedFormat === 'docx') {
        // Handle binary formats (PDF, DOCX)
        const blob = new Blob([response.data], {
          type: selectedFormat === 'pdf' ? 'application/pdf' : 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `contract-report-${Date.now()}.${selectedFormat}`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
      } else {
        // Handle text formats (JSON, HTML, Markdown)
        const reportContent = response.data.report;
        const blob = new Blob([reportContent], { 
          type: selectedFormat === 'json' ? 'application/json' : 'text/plain'
        });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `contract-report-${Date.now()}.${selectedFormat === 'json' ? 'json' : selectedFormat === 'html' ? 'html' : 'md'}`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
      }

      // Success - no alert needed
    } catch (error) {
      console.error('Error generating report:', error);
      // Silent error handling - just log to console
    } finally {
      setGenerating(false);
    }
  };

  const speakSummary = () => {
    if (!analysisData || !analysisData.final_summary) {
      return;
    }

    // Check if browser supports speech synthesis
    if (!('speechSynthesis' in window)) {
      console.log('Text-to-speech not supported in this browser');
      return;
    }

    setSpeakingText(true);

    try {
      // Cancel any ongoing speech
      window.speechSynthesis.cancel();

      // Create speech utterance
      const utterance = new SpeechSynthesisUtterance(analysisData.final_summary);
      
      // Configure speech parameters based on selected language
      const langCodes = {
        'en': 'en-US',
        'ta': 'ta-IN',
        'hi': 'hi-IN',
        'te': 'te-IN',
        'ml': 'ml-IN'
      };
      
      utterance.lang = langCodes[language] || 'en-US';
      utterance.rate = 0.9; // Slightly slower for clarity
      utterance.pitch = 1.0;
      utterance.volume = 1.0;

      // Handle speech end
      utterance.onend = () => {
        setSpeakingText(false);
      };

      // Handle errors silently
      utterance.onerror = (event) => {
        console.log('Speech synthesis error:', event.error);
        setSpeakingText(false);
      };

      // Start speaking
      window.speechSynthesis.speak(utterance);
      
    } catch (error) {
      console.log('Error with text-to-speech:', error);
      setSpeakingText(false);
    }
  };

  const stopSpeech = () => {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      setSpeakingText(false);
    }
  };

  return (
    <div className="card" style={{ marginTop: '2rem' }}>
      <div className="card-header">
        <FiDownload className="card-icon" style={{ color: '#8b5cf6' }} />
        <h2>Export Report</h2>
      </div>
      <div className="card-body">
        <p style={{ marginBottom: '1.5rem', color: 'var(--text-secondary)' }}>
          Generate a customized report from the analysis results
        </p>

        <div style={{ display: 'grid', gap: '1rem', gridTemplateColumns: '1fr 1fr', marginBottom: '1.5rem' }}>
          <div>
            <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 600 }}>
              Report Tone
            </label>
            <select 
              value={selectedTone}
              onChange={(e) => setSelectedTone(e.target.value)}
              style={{
                width: '100%',
                padding: '0.75rem',
                background: 'var(--dark-bg)',
                border: '1px solid var(--border-color)',
                borderRadius: '0.5rem',
                color: 'var(--text-primary)',
                fontSize: '1rem'
              }}
            >
              <option value="professional">Professional</option>
              <option value="technical">Technical</option>
              <option value="executive">Executive</option>
              <option value="detailed">Detailed</option>
            </select>
          </div>

          <div>
            <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 600 }}>
              Format
            </label>
            <select 
              value={selectedFormat}
              onChange={(e) => setSelectedFormat(e.target.value)}
              style={{
                width: '100%',
                padding: '0.75rem',
                background: 'var(--dark-bg)',
                border: '1px solid var(--border-color)',
                borderRadius: '0.5rem',
                color: 'var(--text-primary)',
                fontSize: '1rem'
              }}
            >
              <option value="pdf">📄 PDF (.pdf)</option>
              <option value="docx">📝 Word (.docx)</option>
              <option value="markdown">Markdown (.md)</option>
              <option value="html">HTML (.html)</option>
              <option value="json">JSON (.json)</option>
            </select>
          </div>
        </div>

        <div style={{ display: 'grid', gap: '1rem', gridTemplateColumns: '1fr 1fr', marginBottom: '1rem' }}>
          <button
            className="btn btn-primary"
            onClick={generateReport}
            disabled={generating || !analysisData}
            style={{ width: '100%' }}
          >
            {generating ? (
              <>
                <div className="spinner" style={{ width: '20px', height: '20px', borderWidth: '2px' }}></div>
                Generating Report...
              </>
            ) : (
              <>
                <FiDownload /> Download Report
              </>
            )}
          </button>

          <button
            className="btn"
            onClick={speakingText ? stopSpeech : speakSummary}
            disabled={!analysisData || !analysisData.final_summary}
            style={{ 
              width: '100%',
              background: speakingText 
                ? 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)' 
                : 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              color: 'white',
              border: 'none',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '0.5rem'
            }}
          >
            {speakingText ? (
              <>
                <FiStopCircle size={20} /> Stop Speaking
              </>
            ) : (
              <>
                <FiVolume2 size={20} /> Read Summary Aloud
              </>
            )}
          </button>
        </div>

        <div style={{ marginTop: '0.75rem', fontSize: '0.875rem', color: 'var(--text-secondary)', textAlign: 'center' }}>
          <p>💡 <strong>Tip:</strong> Click "Read Summary Aloud" to hear the executive summary in your selected language</p>
        </div>

        <div style={{ marginTop: '1rem', fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
          <p><strong>Report Tones:</strong></p>
          <ul style={{ marginLeft: '1.5rem', marginTop: '0.5rem' }}>
            <li><strong>Professional:</strong> Balanced tone for general business use</li>
            <li><strong>Technical:</strong> Detailed technical analysis</li>
            <li><strong>Executive:</strong> High-level summary for executives</li>
            <li><strong>Detailed:</strong> Comprehensive analysis with all details</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default ReportExport;
