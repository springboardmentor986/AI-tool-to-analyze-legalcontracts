import React from 'react';
import {
  PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, Legend, ResponsiveContainer, RadialBarChart, RadialBar
} from 'recharts';
import { useTranslation } from '../hooks/useTranslation';
import './Dashboard.css';

const Dashboard = ({ analysisData }) => {
  const { t } = useTranslation();
  
  if (!analysisData) {
    return null;
  }

  const riskScores = analysisData.risk_scores || {};
  const domainScores = riskScores.domain_scores || {};
  const severityBreakdown = riskScores.severity_breakdown || {};
  const riskDistribution = riskScores.risk_distribution || {};
  const missingClauseSummary = analysisData.missing_clause_summary || {};

  // Risk Score Gauge Data
  const overallScore = riskScores.overall_score || 0;
  const overallLevel = riskScores.overall_level || 'LOW RISK';
  
  const gaugeData = [
    {
      name: 'Risk',
      value: overallScore,
      fill: getScoreColor(overallScore)
    }
  ];

  // Domain Scores Bar Chart Data
  const domainData = [
    { domain: t('domains.compliance'), score: domainScores.compliance || 0, fill: '#8b5cf6' },
    { domain: t('domains.financial'), score: domainScores.financial || 0, fill: '#ef4444' },
    { domain: t('domains.legal'), score: domainScores.legal || 0, fill: '#f59e0b' },
    { domain: t('domains.operational'), score: domainScores.operational || 0, fill: '#10b981' }
  ];

  // Severity Breakdown Pie Chart Data
  const severityData = [
    { name: t('risk.critical'), value: severityBreakdown.critical || 0, color: '#dc2626' },
    { name: t('risk.high'), value: severityBreakdown.high || 0, color: '#f59e0b' },
    { name: t('risk.medium'), value: severityBreakdown.medium || 0, color: '#fbbf24' },
    { name: t('risk.low'), value: severityBreakdown.low || 0, color: '#10b981' }
  ].filter(item => item.value > 0);

  // Risk Type Distribution for Bar Chart
  const riskTypeData = Object.entries(riskDistribution).map(([name, value]) => ({
    name: name.length > 20 ? name.substring(0, 20) + '...' : name,
    value,
    fill: '#6366f1'
  })).slice(0, 8); // Top 8 risk types

  // Missing Clauses Data
  const missingClausesData = [
    { name: t('risk.critical'), value: missingClauseSummary.critical_missing || 0, color: '#dc2626' },
    { name: t('risk.high'), value: missingClauseSummary.high_missing || 0, color: '#f59e0b' },
    { name: t('risk.medium'), value: missingClauseSummary.medium_missing || 0, color: '#fbbf24' }
  ].filter(item => item.value > 0);

  // Clause Extraction Stats
  const extractedClauses = analysisData.extracted_clauses || {};
  const clauseStats = Object.entries(extractedClauses).map(([domain, clauses]) => ({
    domain: domain.charAt(0).toUpperCase() + domain.slice(1),
    count: clauses?.length || 0,
    fill: getDomainColor(domain)
  }));

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h2>📊 {t('dashboard.title')}</h2>
        <div className="risk-badge" data-level={overallLevel}>
          {overallLevel}
        </div>
      </div>

      {/* Overall Risk Score - Large Display */}
      <div className="risk-score-hero">
        <div className="score-gauge">
          <ResponsiveContainer width="100%" height={250}>
            <RadialBarChart
              cx="50%"
              cy="50%"
              innerRadius="70%"
              outerRadius="100%"
              data={gaugeData}
              startAngle={180}
              endAngle={0}
            >
              <RadialBar
                background
                dataKey="value"
                cornerRadius={10}
                max={10}
              />
              <text
                x="50%"
                y="50%"
                textAnchor="middle"
                dominantBaseline="middle"
                className="gauge-text"
              >
                <tspan className="gauge-score">{overallScore}</tspan>
                <tspan className="gauge-max" x="50%" dy="25">/ 10</tspan>
              </text>
            </RadialBarChart>
          </ResponsiveContainer>
          <div className="score-label">{t('dashboard.overallRisk')}</div>
        </div>
        
        <div className="score-details">
          <div className="score-metric">
            <span className="metric-label">{t('dashboard.totalRisks')}</span>
            <span className="metric-value">{riskScores.risk_count || 0}</span>
          </div>
          <div className="score-metric">
            <span className="metric-label">{t('dashboard.missingClauses')}</span>
            <span className="metric-value critical">{missingClauseSummary.total_missing || 0}</span>
          </div>
          <div className="score-metric">
            <span className="metric-label">{t('dashboard.completionScore')}</span>
            <span className="metric-value">{missingClauseSummary.completion_score || 100}%</span>
          </div>
          <div className="score-metric">
            <span className="metric-label">{t('dashboard.criticalIssues')}</span>
            <span className="metric-value critical">
              {(severityBreakdown.critical || 0) + (missingClauseSummary.critical_missing || 0)}
            </span>
          </div>
        </div>
      </div>

      {/* Charts Grid */}
      <div className="charts-grid">
        {/* Domain Scores Bar Chart */}
        <div className="chart-card">
          <h3>{t('dashboard.domainRiskScores')}</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={domainData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
              <XAxis dataKey="domain" stroke="#9ca3af" />
              <YAxis domain={[0, 10]} stroke="#9ca3af" />
              <Tooltip
                contentStyle={{ backgroundColor: '#1f2937', border: '1px solid #374151' }}
                labelStyle={{ color: '#f9fafb' }}
              />
              <Bar dataKey="score" radius={[8, 8, 0, 0]}>
                {domainData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.fill} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Risk Severity Pie Chart */}
        <div className="chart-card">
          <h3>{t('dashboard.riskSeverityDistribution')}</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={severityData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={renderCustomLabel}
                outerRadius={100}
                fill="#8884d8"
                dataKey="value"
              >
                {severityData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip
                contentStyle={{ backgroundColor: '#1f2937', border: '1px solid #374151' }}
              />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Risk Type Distribution */}
        <div className="chart-card">
          <h3>{t('dashboard.topRiskTypes')}</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart
              data={riskTypeData}
              layout="horizontal"
              margin={{ top: 5, right: 30, left: 100, bottom: 5 }}
            >
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
              <XAxis type="number" stroke="#9ca3af" />
              <YAxis dataKey="name" type="category" stroke="#9ca3af" />
              <Tooltip
                contentStyle={{ backgroundColor: '#1f2937', border: '1px solid #374151' }}
              />
              <Bar dataKey="value" radius={[0, 8, 8, 0]}>
                {riskTypeData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.fill} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Clause Extraction Stats */}
        <div className="chart-card">
          <h3>{t('dashboard.extractedClauses')}</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={clauseStats} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
              <XAxis dataKey="domain" stroke="#9ca3af" />
              <YAxis stroke="#9ca3af" />
              <Tooltip
                contentStyle={{ backgroundColor: '#1f2937', border: '1px solid #374151' }}
              />
              <Bar dataKey="count" radius={[8, 8, 0, 0]}>
                {clauseStats.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.fill} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Missing Clauses */}
        {missingClausesData.length > 0 && (
          <div className="chart-card">
            <h3>{t('dashboard.missingCriticalClauses')}</h3>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={missingClausesData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={renderCustomLabel}
                  outerRadius={100}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {missingClausesData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{ backgroundColor: '#1f2937', border: '1px solid #374151' }}
                />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
        )}

        {/* Risk Heatmap */}
        <div className="chart-card heatmap-card">
          <h3>{t('dashboard.riskSeverityHeatmap')}</h3>
          <div className="heatmap-grid">
            {[{key: 'compliance', label: t('domains.compliance')}, {key: 'financial', label: t('domains.financial')}, {key: 'legal', label: t('domains.legal')}, {key: 'operational', label: t('domains.operational')}].map(domain => (
              <div key={domain.key} className="heatmap-row">
                <div className="heatmap-label">{domain.label}</div>
                <div
                  className="heatmap-cell"
                  style={{
                    backgroundColor: getHeatmapColor(domainScores[domain.key] || 0),
                    width: `${(domainScores[domain.key] || 0) * 10}%`
                  }}
                >
                  <span className="heatmap-value">
                    {(domainScores[domain.key] || 0).toFixed(1)}
                  </span>
                </div>
              </div>
            ))}
          </div>
          <div className="heatmap-legend">
            <span>{t('dashboard.lowRisk')}</span>
            <div className="legend-gradient"></div>
            <span>{t('dashboard.highRisk')}</span>
          </div>
        </div>
      </div>
    </div>
  );
};

// Helper function to render custom pie chart labels
const renderCustomLabel = ({ name, value, percent }) => {
  return `${name}: ${value} (${(percent * 100).toFixed(0)}%)`;
};

// Helper function to get color based on score
function getScoreColor(score) {
  if (score >= 8) return '#dc2626'; // Red - Critical
  if (score >= 6) return '#f59e0b'; // Orange - High
  if (score >= 4) return '#fbbf24'; // Yellow - Medium
  return '#10b981'; // Green - Low
}

// Helper function to get domain-specific colors
function getDomainColor(domain) {
  const colors = {
    compliance: '#8b5cf6',
    finance: '#ef4444',
    legal: '#f59e0b',
    operations: '#10b981'
  };
  return colors[domain] || '#6366f1';
}

// Helper function for heatmap colors
function getHeatmapColor(score) {
  if (score >= 8) return '#dc2626';
  if (score >= 6) return '#f59e0b';
  if (score >= 4) return '#fbbf24';
  if (score >= 2) return '#84cc16';
  return '#10b981';
}

export default Dashboard;
