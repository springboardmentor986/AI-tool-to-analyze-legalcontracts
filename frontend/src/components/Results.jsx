import React, { useState } from 'react';
import { 
  FiCheckCircle, FiDollarSign, FiBook, FiTool, 
  FiAlertTriangle, FiMessageCircle, FiFileText 
} from 'react-icons/fi';
import { useTranslation } from '../hooks/useTranslation';
import ReportExport from './ReportExport';
import Dashboard from './Dashboard';
import RiskScores from './RiskScores';
import MissingClauses from './MissingClauses';
import ContractChat from './ContractChat';

const Results = ({ data }) => {
  const { t } = useTranslation();
  const [activeClauseTab, setActiveClauseTab] = useState('all');
  const [showChat, setShowChat] = useState(false);

  console.log('Results component received data:', data);

  if (!data) {
    console.log('No data to display');
    return null;
  }

  // Safely handle data structure
  try {
    // Group clauses by type
    const groupedClauses = {};
    if (data.extracted_clauses && Array.isArray(data.extracted_clauses)) {
      data.extracted_clauses.forEach(clause => {
        const type = clause.type || 'other';
        if (!groupedClauses[type]) {
          groupedClauses[type] = [];
        }
        groupedClauses[type].push(clause);
      });
    }

      const clauseTypes = ['all', ...Object.keys(groupedClauses)];

    return (
      <div className="results-section">
        <div className="results-grid">
        
        {/* Error Display - Show if there are errors */}
        {data.errors && data.errors.length > 0 && (
          <div className="card" style={{ borderLeft: '4px solid #ef4444' }}>
            <div className="card-header" style={{ background: '#fef2f2' }}>
              <FiAlertTriangle className="card-icon" style={{ color: '#ef4444' }} />
              <h2 style={{ color: '#dc2626' }}>Analysis Errors ({data.errors.length})</h2>
            </div>
            <div className="card-body" style={{ background: '#fef2f2' }}>
              {data.errors.map((error, index) => (
                <div key={index} style={{ 
                  padding: '10px', 
                  marginBottom: '8px', 
                  background: 'white',
                  borderRadius: '4px',
                  borderLeft: '3px solid #ef4444',
                  fontSize: '0.9rem',
                  color: '#dc2626'
                }}>
                  <strong>Error {index + 1}:</strong> {error}
                </div>
              ))}
              <div style={{ 
                marginTop: '12px', 
                padding: '12px', 
                background: '#fffbeb',
                borderRadius: '4px',
                fontSize: '0.85rem',
                color: '#92400e'
              }}>
                <strong>💡 Tip:</strong> These errors occurred during analysis. Check the backend console for more details. Common causes: API rate limits, network issues, or invalid contract format.
              </div>
            </div>
          </div>
        )}
        
        {/* Dashboard with Visual Analytics */}
        <Dashboard analysisData={data} />
        
        {/* Risk Scoring System */}
        <RiskScores riskScores={data.risk_scores} />
        
        {/* Missing Critical Clauses */}
        <MissingClauses 
          missingClauses={data.missing_clauses} 
          summary={data.missing_clause_summary}
        />
        
        {/* Executive Summary */}
        {data.final_summary && (
          <div className="card">
            <div className="card-header">
              <FiFileText className="card-icon" style={{ color: '#8b5cf6' }} />
              <h2>{t('analysis.executiveSummary')}</h2>
            </div>
            <div className="card-body">
              <p>{data.final_summary}</p>
            </div>
          </div>
        )}

        {/* Extracted Clauses */}
        {data.extracted_clauses && data.extracted_clauses.length > 0 && (
          <div className="card">
            <div className="card-header">
              <FiFileText className="card-icon" style={{ color: '#10b981' }} />
              <h2>{t('analysis.extractedClauses')} ({data.extracted_clauses.length})</h2>
            </div>
            <div className="card-body">
              <div className="tabs">
                {clauseTypes.map(type => (
                  <button
                    key={type}
                    className={`tab ${activeClauseTab === type ? 'active' : ''}`}
                    onClick={() => setActiveClauseTab(type)}
                  >
                    {type.charAt(0).toUpperCase() + type.slice(1)} 
                    {type !== 'all' && ` (${groupedClauses[type]?.length || 0})`}
                    {type === 'all' && ` (${data.extracted_clauses.length})`}
                  </button>
                ))}
              </div>
              <div className="tab-content">
                {(activeClauseTab === 'all' 
                  ? data.extracted_clauses 
                  : groupedClauses[activeClauseTab] || []
                ).map((clause, index) => (
                  <div key={index} className="clause-item">
                    <div className="clause-type">{clause.type || 'General'}</div>
                    <div>{clause.text || clause}</div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Identified Risks */}
        {data.identified_risks && data.identified_risks.length > 0 && (
          <div className="card">
            <div className="card-header">
              <FiAlertTriangle className="card-icon" style={{ color: '#f59e0b' }} />
              <h2>{t('analysis.identifiedRisks')} ({data.identified_risks.length})</h2>
            </div>
            <div className="card-body">
              {data.identified_risks.map((risk, index) => (
                <div 
                  key={index} 
                  className={`risk-item ${(risk.severity || 'medium').toLowerCase()}`}
                >
                  <div className="risk-header">
                    <div className="risk-category">{risk.category || risk.type || 'General Risk'}</div>
                    <span className={`risk-badge ${(risk.severity || 'medium').toLowerCase()}`}>
                      {risk.severity || 'MEDIUM'}
                    </span>
                  </div>
                  <div className="risk-description">
                    {risk.description || risk.text || risk}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Agent Discussions */}
        {data.discussion_summaries && data.discussion_summaries.length > 0 && (
          <div className="card">
            <div className="card-header">
              <FiMessageCircle className="card-icon" style={{ color: '#2563eb' }} />
              <h2>{t('analysis.agentDiscussions')} ({data.discussion_summaries.length})</h2>
            </div>
            <div className="card-body">
              {data.discussion_summaries.map((discussion, index) => (
                <div key={index} className="discussion-item">
                  <div className="discussion-header">
                    <div className="discussion-topic">{t('analysis.discussionTopic')} {index + 1}</div>
                    <div className="discussion-status">
                      <FiCheckCircle /> {t('analysis.completed')}
                    </div>
                  </div>
                  <div className="message-content" style={{ whiteSpace: 'pre-wrap' }}>
                    {discussion}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Compliance Analysis */}
        {data.compliance_analysis && (
          <div className="card">
            <div className="card-header">
              <FiCheckCircle className="card-icon" style={{ color: '#10b981' }} />
              <h2>{t('analysis.complianceAnalysis')}</h2>
            </div>
            <div className="card-body">
              <p style={{ whiteSpace: 'pre-wrap' }}>{data.compliance_analysis}</p>
            </div>
          </div>
        )}

        {/* Finance Analysis */}
        {data.finance_analysis && (
          <div className="card">
            <div className="card-header">
              <FiDollarSign className="card-icon" style={{ color: '#f59e0b' }} />
              <h2>{t('analysis.financeAnalysis')}</h2>
            </div>
            <div className="card-body">
              <p style={{ whiteSpace: 'pre-wrap' }}>{data.finance_analysis}</p>
            </div>
          </div>
        )}

        {/* Legal Analysis */}
        {data.legal_analysis && (
          <div className="card">
            <div className="card-header">
              <FiBook className="card-icon" style={{ color: '#8b5cf6' }} />
              <h2>{t('analysis.legalAnalysis')}</h2>
            </div>
            <div className="card-body">
              <p style={{ whiteSpace: 'pre-wrap' }}>{data.legal_analysis}</p>
            </div>
          </div>
        )}

        {/* Operations Analysis */}
        {data.operations_analysis && (
          <div className="card">
            <div className="card-header">
              <FiTool className="card-icon" style={{ color: '#06b6d4' }} />
              <h2>{t('analysis.operationsAnalysis')}</h2>
            </div>
            <div className="card-body">
              <p style={{ whiteSpace: 'pre-wrap' }}>{data.operations_analysis}</p>
            </div>
          </div>
        )}

        {/* Interactive Contract Chat */}
        <div className="card">
          <div className="card-header" style={{ 
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            color: 'white',
            cursor: 'pointer'
          }}
          onClick={() => setShowChat(!showChat)}
          >
            <FiMessageCircle className="card-icon" />
            <h2>💬 Chat with Contract</h2>
            <span style={{ marginLeft: 'auto', fontSize: '0.875rem', opacity: 0.9 }}>
              {showChat ? '▼ Hide' : '▶ Show'}
            </span>
          </div>
          {showChat && (
            <div className="card-body" style={{ padding: 0 }}>
              <ContractChat 
                contractId={data.contract_id}
                onClose={() => setShowChat(false)}
              />
            </div>
          )}
          {!showChat && (
            <div className="card-body">
              <p>Click to open interactive Q&A chat with your contract assistant</p>
              <div style={{ marginTop: '1rem', display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                <span style={{ 
                  background: '#f0f2f5', 
                  padding: '0.5rem 1rem', 
                  borderRadius: '20px',
                  fontSize: '0.875rem'
                }}>💰 "What is my payment obligation?"</span>
                <span style={{ 
                  background: '#f0f2f5', 
                  padding: '0.5rem 1rem', 
                  borderRadius: '20px',
                  fontSize: '0.875rem'
                }}>⚖️ "When can I terminate?"</span>
                <span style={{ 
                  background: '#f0f2f5', 
                  padding: '0.5rem 1rem', 
                  borderRadius: '20px',
                  fontSize: '0.875rem'
                }}>⚠️ "Is there a penalty clause?"</span>
              </div>
            </div>
          )}
        </div>

        {/* Report Export */}
        <ReportExport analysisData={data} />
      </div>
    </div>
  );
  } catch (error) {
    console.error('Error rendering results:', error);
    return (
      <div className="results-section">
        <div className="card">
          <div className="card-header">
            <FiAlertTriangle className="card-icon" style={{ color: '#ef4444' }} />
            <h2>Error Displaying Results</h2>
          </div>
          <div className="card-body">
            <p>There was an error displaying the analysis results. Please check the console for details.</p>
            <p style={{ marginTop: '1rem', fontSize: '0.875rem', opacity: 0.7 }}>
              Error: {error.message}
            </p>
          </div>
        </div>
      </div>
    );
  }
};

export default Results;
