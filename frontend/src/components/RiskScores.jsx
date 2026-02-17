import React from 'react';
import { FiAlertTriangle, FiTrendingUp, FiActivity } from 'react-icons/fi';
import { useTranslation } from '../hooks/useTranslation';
import './RiskScores.css';

const RiskScores = ({ riskScores }) => {
  const { t } = useTranslation();
  
  if (!riskScores) {
    return null;
  }

  const overallScore = riskScores.overall_score || 0;
  const overallLevel = riskScores.overall_level || 'LOW RISK';
  const domainScores = riskScores.domain_scores || {};
  const severityBreakdown = riskScores.severity_breakdown || {};
  const missingClausePenalty = riskScores.missing_clause_penalty || 0;

  const getRiskLevelClass = (level) => {
    if (level.includes('CRITICAL')) return 'critical';
    if (level.includes('HIGH')) return 'high';
    if (level.includes('MEDIUM')) return 'medium';
    return 'low';
  };

  const getScoreColor = (score) => {
    if (score >= 8) return '#dc2626';
    if (score >= 6) return '#f59e0b';
    if (score >= 4) return '#fbbf24';
    return '#10b981';
  };

  return (
    <div className="risk-scores-container">
      <div className="section-header">
        <h2>
          <FiActivity /> Risk Scoring System
        </h2>
      </div>

      {/* Overall Risk Score */}
      <div className={`overall-risk-card ${getRiskLevelClass(overallLevel)}`}>
        <div className="risk-icon">
          <FiAlertTriangle size={48} />
        </div>
        <div className="risk-score-main">
          <div className="score-label">{t('risk.overall')}</div>
          <div className="score-display">
            <span className="score-number">{overallScore}</span>
            <span className="score-max">/ 10</span>
          </div>
          <div className="risk-level-badge">{overallLevel}</div>
        </div>
        <div className="risk-description">
          <p>
            {overallScore >= 8 && 'This contract has critical risk factors that require immediate attention before proceeding.'}
            {overallScore >= 6 && overallScore < 8 && 'This contract has significant risks that should be addressed and negotiated.'}
            {overallScore >= 4 && overallScore < 6 && 'This contract has moderate risks. Review recommendations carefully.'}
            {overallScore < 4 && 'This contract has relatively low risks. Standard review procedures apply.'}
          </p>
        </div>
      </div>

      {/* Domain Breakdown */}
      <div className="domain-scores-section">
        <h3>
          <FiTrendingUp /> {t('risk.domainBreakdown')}
        </h3>
        <div className="domain-scores-grid">
          <DomainScoreCard
            domain={t('domains.compliance')}
            score={domainScores.compliance || 0}
            icon="🔒"
            description={t('risk.complianceRisk')}
            t={t}
          />
          <DomainScoreCard
            domain={t('domains.financial')}
            score={domainScores.financial || 0}
            icon="💰"
            description={t('risk.financialRisk')}
            t={t}
          />
          <DomainScoreCard
            domain={t('domains.legal')}
            score={domainScores.legal || 0}
            icon="⚖️"
            description={t('risk.legalRisk')}
            t={t}
          />
          <DomainScoreCard
            domain={t('domains.operational')}
            score={domainScores.operational || 0}
            icon="⚙️"
            description={t('risk.operationalRisk')}
            t={t}
          />
        </div>
      </div>

      {/* Severity Breakdown */}
      <div className="severity-breakdown-section">
        <h3>{t('risk.severityDistribution')}</h3>
        <div className="severity-grid">
          <div className="severity-stat critical">
            <div className="severity-icon">
              <FiAlertTriangle />
            </div>
            <div className="severity-content">
              <div className="severity-count">{severityBreakdown.critical || 0}</div>
              <div className="severity-label">{t('risk.critical')} {t('risk.riskCount')}</div>
            </div>
          </div>
          <div className="severity-stat high">
            <div className="severity-icon">
              <FiAlertTriangle />
            </div>
            <div className="severity-content">
              <div className="severity-count">{severityBreakdown.high || 0}</div>
              <div className="severity-label">{t('risk.high')} {t('risk.riskCount')}</div>
            </div>
          </div>
          <div className="severity-stat medium">
            <div className="severity-icon">
              <FiAlertTriangle />
            </div>
            <div className="severity-content">
              <div className="severity-count">{severityBreakdown.medium || 0}</div>
              <div className="severity-label">{t('risk.medium')} {t('risk.riskCount')}</div>
            </div>
          </div>
          <div className="severity-stat low">
            <div className="severity-icon">
              <FiAlertTriangle />
            </div>
            <div className="severity-content">
              <div className="severity-count">{severityBreakdown.low || 0}</div>
              <div className="severity-label">{t('risk.low')} {t('risk.riskCount')}</div>
            </div>
          </div>
        </div>
      </div>

      {/* Additional Penalties */}
      {missingClausePenalty > 0 && (
        <div className="penalty-notice">
          <FiAlertTriangle />
          <div>
            <strong>Missing Clause Penalty:</strong> +{missingClausePenalty.toFixed(1)} points added to overall score due to missing critical clauses.
          </div>
        </div>
      )}

      {/* Scoring Methodology */}
      <div className="scoring-info">
        <h4>Scoring Methodology</h4>
        <ul>
          <li><strong>0-3.9:</strong> Low Risk - Standard contract with minimal concerns</li>
          <li><strong>4.0-5.9:</strong> Medium Risk - Requires careful review and consideration</li>
          <li><strong>6.0-7.9:</strong> High Risk - Significant issues that need negotiation</li>
          <li><strong>8.0-10.0:</strong> Critical Risk - Major concerns requiring immediate attention</li>
        </ul>
        <p className="scoring-note">
          Scores are calculated based on identified risks, severity levels, and missing critical clauses. 
          Each domain contributes weighted scores: Compliance (30%), Financial (25%), Legal (25%), Operational (20%).
        </p>
      </div>
    </div>
  );
};

const DomainScoreCard = ({ domain, score, icon, description }) => {
  const getScoreClass = (score) => {
    if (score >= 8) return 'critical';
    if (score >= 6) return 'high';
    if (score >= 4) return 'medium';
    return 'low';
  };

  const getScoreColor = (score) => {
    if (score >= 8) return '#dc2626';
    if (score >= 6) return '#f59e0b';
    if (score >= 4) return '#fbbf24';
    return '#10b981';
  };

  return (
    <div className={`domain-score-card ${getScoreClass(score)}`}>
      <div className="domain-icon">{icon}</div>
      <div className="domain-content">
        <div className="domain-name">{domain}</div>
        <div className="domain-score" style={{ color: getScoreColor(score) }}>
          {score.toFixed(1)}
        </div>
        <div className="domain-description">{description}</div>
      </div>
      <div className="score-bar">
        <div 
          className="score-fill" 
          style={{ 
            width: `${score * 10}%`,
            backgroundColor: getScoreColor(score)
          }}
        ></div>
      </div>
    </div>
  );
};

export default RiskScores;
