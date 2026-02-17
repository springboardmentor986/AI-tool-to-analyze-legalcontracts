"""
Risk Scoring System
Calculates numerical risk scores for contracts and domains
"""

from typing import Dict, List
from enum import Enum


class RiskLevel(Enum):
    """Overall risk level classification"""
    CRITICAL_RISK = "CRITICAL RISK"
    HIGH_RISK = "HIGH RISK"
    MEDIUM_RISK = "MEDIUM RISK"
    LOW_RISK = "LOW RISK"


class RiskScoringSystem:
    """Calculates comprehensive risk scores for contracts"""
    
    # Severity weights for score calculation
    SEVERITY_WEIGHTS = {
        "Critical": 10.0,
        "High": 7.0,
        "Medium": 4.0,
        "Low": 2.0
    }
    
    # Risk type weights (how much each type contributes to domain score)
    RISK_TYPE_WEIGHTS = {
        # Compliance domain
        "compliance": {
            "Regulatory Gap": 1.0,
            "Data Protection Violation": 0.9,
            "Audit Deficiency": 0.8,
            "Reporting Gap": 0.7,
            "Certification Missing": 0.6
        },
        # Financial domain
        "financial": {
            "Unlimited Liability": 1.0,
            "Payment Risk": 0.9,
            "Hidden Costs": 0.8,
            "Currency Risk": 0.7,
            "Penalty Risk": 0.6
        },
        # Legal domain
        "legal": {
            "Unfair Terms": 1.0,
            "Termination Risk": 0.9,
            "Jurisdiction Issue": 0.8,
            "IP Ownership Risk": 0.7,
            "Dispute Resolution Gap": 0.6
        },
        # Operational domain
        "operational": {
            "SLA Violation": 1.0,
            "Resource Constraint": 0.9,
            "Dependency Risk": 0.8,
            "Performance Gap": 0.7,
            "Timeline Risk": 0.6
        }
    }
    
    def __init__(self):
        """Initialize the risk scoring system"""
        pass
    
    def calculate_risk_scores(self, risks: List[Dict], missing_clauses: List = None) -> Dict:
        """
        Calculate comprehensive risk scores
        
        Args:
            risks: List of identified risks from analysis
            missing_clauses: List of missing critical clauses (optional)
            
        Returns:
            Dictionary with overall and domain-specific scores
        """
        if not risks:
            return {
                "overall_score": 0.0,
                "overall_level": RiskLevel.LOW_RISK.value,
                "domain_scores": {
                    "compliance": 0.0,
                    "financial": 0.0,
                    "legal": 0.0,
                    "operational": 0.0
                },
                "severity_breakdown": {
                    "critical": 0,
                    "high": 0,
                    "medium": 0,
                    "low": 0
                },
                "risk_distribution": {},
                "missing_clause_penalty": 0.0
            }
        
        # Calculate domain scores
        domain_scores = self._calculate_domain_scores(risks)
        
        # Calculate severity breakdown
        severity_breakdown = self._calculate_severity_breakdown(risks)
        
        # Calculate risk type distribution
        risk_distribution = self._calculate_risk_distribution(risks)
        
        # Calculate penalty for missing clauses
        missing_clause_penalty = 0.0
        if missing_clauses:
            missing_clause_penalty = self._calculate_missing_clause_penalty(missing_clauses)
        
        # Calculate overall score (weighted average of domains + missing clause penalty)
        overall_score = (
            domain_scores["compliance"] * 0.3 +
            domain_scores["financial"] * 0.25 +
            domain_scores["legal"] * 0.25 +
            domain_scores["operational"] * 0.2
        ) + missing_clause_penalty
        
        # Cap at 10.0
        overall_score = min(10.0, overall_score)
        
        # Determine risk level
        overall_level = self._determine_risk_level(overall_score)
        
        return {
            "overall_score": round(overall_score, 1),
            "overall_level": overall_level,
            "domain_scores": {k: round(v, 1) for k, v in domain_scores.items()},
            "severity_breakdown": severity_breakdown,
            "risk_distribution": risk_distribution,
            "missing_clause_penalty": round(missing_clause_penalty, 1),
            "risk_count": len(risks)
        }
    
    def _calculate_domain_scores(self, risks: List[Dict]) -> Dict[str, float]:
        """Calculate risk scores for each domain"""
        domain_scores = {
            "compliance": 0.0,
            "financial": 0.0,
            "legal": 0.0,
            "operational": 0.0
        }
        
        domain_risk_counts = {domain: 0 for domain in domain_scores.keys()}
        
        for risk in risks:
            category = risk.get('category', '').lower()
            severity = risk.get('severity', 'Low')
            risk_type = risk.get('risk_type', '')
            
            # Map category to domain
            domain = self._map_category_to_domain(category, risk_type)
            
            if domain in domain_scores:
                # Get severity weight
                severity_weight = self.SEVERITY_WEIGHTS.get(severity, 2.0)
                
                # Get risk type weight
                type_weight = self._get_risk_type_weight(domain, risk_type)
                
                # Calculate risk contribution
                risk_contribution = severity_weight * type_weight
                
                domain_scores[domain] += risk_contribution
                domain_risk_counts[domain] += 1
        
        # Average the scores (if any risks present)
        for domain in domain_scores:
            if domain_risk_counts[domain] > 0:
                # Average and normalize to 0-10 scale
                domain_scores[domain] = min(10.0, domain_scores[domain] / domain_risk_counts[domain])
        
        return domain_scores
    
    def _calculate_severity_breakdown(self, risks: List[Dict]) -> Dict[str, int]:
        """Count risks by severity level"""
        breakdown = {
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0
        }
        
        for risk in risks:
            severity = risk.get('severity', 'Low').lower()
            if severity in breakdown:
                breakdown[severity] += 1
        
        return breakdown
    
    def _calculate_risk_distribution(self, risks: List[Dict]) -> Dict[str, int]:
        """Calculate distribution of risks by type"""
        distribution = {}
        
        for risk in risks:
            risk_type = risk.get('risk_type', 'Unknown')
            if risk_type not in distribution:
                distribution[risk_type] = 0
            distribution[risk_type] += 1
        
        return distribution
    
    def _calculate_missing_clause_penalty(self, missing_clauses: List) -> float:
        """Calculate penalty score for missing critical clauses"""
        if not missing_clauses:
            return 0.0
        
        penalty = 0.0
        for clause in missing_clauses:
            importance = getattr(clause, 'importance', 'MEDIUM')
            if importance == "CRITICAL":
                penalty += 0.5
            elif importance == "HIGH":
                penalty += 0.3
            elif importance == "MEDIUM":
                penalty += 0.1
        
        return min(2.0, penalty)  # Cap penalty at 2.0 points
    
    def _map_category_to_domain(self, category: str, risk_type: str) -> str:
        """Map risk category to domain"""
        category_lower = category.lower()
        risk_type_lower = risk_type.lower()
        
        # Compliance domain
        if any(word in category_lower or word in risk_type_lower 
               for word in ['regulatory', 'compliance', 'gdpr', 'audit', 'data protection']):
            return "compliance"
        
        # Financial domain
        if any(word in category_lower or word in risk_type_lower 
               for word in ['payment', 'liability', 'cost', 'currency', 'penalty', 'financial']):
            return "financial"
        
        # Legal domain
        if any(word in category_lower or word in risk_type_lower 
               for word in ['termination', 'jurisdiction', 'ip', 'intellectual property', 'dispute', 'legal']):
            return "legal"
        
        # Operational domain (default)
        return "operational"
    
    def _get_risk_type_weight(self, domain: str, risk_type: str) -> float:
        """Get weight for specific risk type within domain"""
        domain_weights = self.RISK_TYPE_WEIGHTS.get(domain, {})
        return domain_weights.get(risk_type, 0.5)  # Default weight 0.5
    
    def _determine_risk_level(self, score: float) -> str:
        """Determine overall risk level from score"""
        if score >= 8.0:
            return RiskLevel.CRITICAL_RISK.value
        elif score >= 6.0:
            return RiskLevel.HIGH_RISK.value
        elif score >= 4.0:
            return RiskLevel.MEDIUM_RISK.value
        else:
            return RiskLevel.LOW_RISK.value
    
    def get_risk_score_summary(self, risk_scores: Dict) -> str:
        """Generate human-readable summary of risk scores"""
        overall = risk_scores.get('overall_score', 0.0)
        level = risk_scores.get('overall_level', 'LOW RISK')
        domains = risk_scores.get('domain_scores', {})
        
        summary = f"Overall Risk Score: {overall} / 10 ({level})\n\n"
        summary += "Domain Breakdown:\n"
        summary += f"  • Compliance Risk: {domains.get('compliance', 0.0)}\n"
        summary += f"  • Financial Risk: {domains.get('financial', 0.0)}\n"
        summary += f"  • Legal Risk: {domains.get('legal', 0.0)}\n"
        summary += f"  • Operational Risk: {domains.get('operational', 0.0)}\n"
        
        return summary
