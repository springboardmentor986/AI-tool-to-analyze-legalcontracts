import React from 'react';
import { FiAlertTriangle, FiCheckCircle, FiInfo } from 'react-icons/fi';
import { useTranslation } from '../hooks/useTranslation';
import './MissingClauses.css';

const MissingClauses = ({ missingClauses, summary }) => {
  const { t } = useTranslation();
  
  if (!missingClauses || missingClauses.length === 0) {
    return (
      <div className="missing-clauses-container">
        <div className="section-header">
          <h2>
            <FiCheckCircle /> {t('missingClauses.title')}
          </h2>
        </div>
        <div className="all-clear">
          <FiCheckCircle size={48} />
          <h3>{t('missingClauses.allPresent')}</h3>
          <p>{t('missingClauses.allPresentDesc')}</p>
          <div className="completion-badge">
            <span className="completion-score">100%</span>
            <span>{t('missingClauses.completeness')}</span>
          </div>
        </div>
      </div>
    );
  }

  const criticalClauses = missingClauses.filter(c => c.importance === 'CRITICAL');
  const highClauses = missingClauses.filter(c => c.importance === 'HIGH');
  const mediumClauses = missingClauses.filter(c => c.importance === 'MEDIUM');

  const completionScore = summary?.completion_score || 0;

  return (
    <div className="missing-clauses-container">
      <div className="section-header">
        <h2>
          <FiAlertTriangle /> {t('missingClauses.title')}
        </h2>
        <div className="completion-indicator">
          <div className="completion-bar">
            <div 
              className="completion-fill" 
              style={{ width: `${completionScore}%` }}
            ></div>
          </div>
          <span className="completion-text">
            {completionScore.toFixed(0)}% {t('missingClauses.complete')}
          </span>
        </div>
      </div>

      <div className="missing-summary">
        <div className="summary-card critical">
          <div className="summary-icon">
            <FiAlertTriangle />
          </div>
          <div className="summary-content">
            <div className="summary-value">{summary?.critical_missing || 0}</div>
            <div className="summary-label">{t('missingClauses.criticalMissing')}</div>
          </div>
        </div>
        <div className="summary-card high">
          <div className="summary-icon">
            <FiAlertTriangle />
          </div>
          <div className="summary-content">
            <div className="summary-value">{summary?.high_missing || 0}</div>
            <div className="summary-label">{t('missingClauses.highPriority')}</div>
          </div>
        </div>
        <div className="summary-card medium">
          <div className="summary-icon">
            <FiInfo />
          </div>
          <div className="summary-content">
            <div className="summary-value">{summary?.medium_missing || 0}</div>
            <div className="summary-label">{t('missingClauses.mediumPriority')}</div>
          </div>
        </div>
        <div className="summary-card total">
          <div className="summary-icon">
            <FiInfo />
          </div>
          <div className="summary-content">
            <div className="summary-value">{summary?.total_missing || 0}</div>
            <div className="summary-label">{t('missingClauses.totalMissing')}</div>
          </div>
        </div>
      </div>

      {criticalClauses.length > 0 && (
        <div className="clause-group">
          <h3 className="group-title critical">
            <FiAlertTriangle /> Critical Missing Clauses ({criticalClauses.length})
          </h3>
          {criticalClauses.map((clause, index) => (
            <MissingClauseCard key={index} clause={clause} />
          ))}
        </div>
      )}

      {highClauses.length > 0 && (
        <div className="clause-group">
          <h3 className="group-title high">
            <FiAlertTriangle /> High Priority Missing Clauses ({highClauses.length})
          </h3>
          {highClauses.map((clause, index) => (
            <MissingClauseCard key={index} clause={clause} />
          ))}
        </div>
      )}

      {mediumClauses.length > 0 && (
        <div className="clause-group">
          <h3 className="group-title medium">
            <FiInfo /> Medium Priority Missing Clauses ({mediumClauses.length})
          </h3>
          {mediumClauses.map((clause, index) => (
            <MissingClauseCard key={index} clause={clause} />
          ))}
        </div>
      )}
    </div>
  );
};

const MissingClauseCard = ({ clause }) => {
  const { t } = useTranslation();
  const importanceClass = clause.importance.toLowerCase();

  return (
    <div className={`missing-clause-card ${importanceClass}`}>
      <div className="clause-header">
        <div className="clause-title">
          <FiAlertTriangle className="clause-icon" />
          <h4>{clause.clause_name}</h4>
        </div>
        <span className={`importance-badge ${importanceClass}`}>
          {clause.importance}
        </span>
      </div>
      
      <div className="clause-category">
        <strong>{t('missingClauses.category')}:</strong> {clause.category.charAt(0).toUpperCase() + clause.category.slice(1)}
      </div>

      <div className="clause-reason">
        <strong>{t('missingClauses.whyItMatters')}:</strong>
        <p>{clause.reason}</p>
      </div>

      <div className="clause-recommendation">
        <strong>{t('missingClauses.recommendation')}:</strong>
        <p>{clause.recommendation}</p>
      </div>
    </div>
  );
};

export default MissingClauses;
