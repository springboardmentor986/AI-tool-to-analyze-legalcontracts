"""
Risk Analysis Pipelines
Week 3-4 Implementation

Structured pipelines for:
1. Compliance Risk Identification
2. Financial Risk Identification
"""

import re
from typing import Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum


class RiskSeverity(Enum):
    """Risk severity levels"""
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


@dataclass
class IdentifiedRisk:
    """Structure for identified risk"""
    risk_type: str
    category: str
    severity: RiskSeverity
    description: str
    evidence: str
    location: str
    recommendation: str
    score: float  # 0-10 scale


class ComplianceRiskPipeline:
    """
    Structured pipeline for compliance risk identification
    Analyzes regulatory compliance, data protection, audit requirements
    """
    
    def __init__(self):
        self.risk_indicators = self._initialize_compliance_indicators()
        
    def _initialize_compliance_indicators(self) -> Dict:
        """Initialize compliance risk indicators"""
        return {
            'regulatory_gaps': {
                'patterns': [
                    r'(?:without|lacking|absence\s+of)\s+(?:regulatory|compliance)',
                    r'(?:no|not)\s+(?:regulated|compliant)',
                    r'(?:exempt|exemption)\s+from\s+(?:regulation|compliance)',
                    r'non-compliant'
                ],
                'severity': RiskSeverity.CRITICAL,
                'category': 'Regulatory Gap'
            },
            'missing_gdpr': {
                'patterns': [
                    r'(?:without|no)\s+(?:GDPR|data\s+protection)',
                    r'personal\s+data.*(?:without|no)\s+(?:consent|protection)',
                    r'(?:unlimited|unrestricted)\s+data\s+(?:use|processing)'
                ],
                'severity': RiskSeverity.HIGH,
                'category': 'Data Protection Violation'
            },
            'audit_deficiency': {
                'patterns': [
                    r'(?:no|without|prohibit)\s+audit',
                    r'(?:restricted|limited)\s+(?:audit|inspection)',
                    r'(?:no|without)\s+(?:record|documentation)',
                    r'audit\s+(?:not\s+permitted|forbidden)'
                ],
                'severity': RiskSeverity.HIGH,
                'category': 'Audit Deficiency'
            },
            'reporting_gap': {
                'patterns': [
                    r'(?:no|without)\s+(?:reporting|notification)\s+(?:requirement|obligation)',
                    r'(?:exempt|exemption)\s+from\s+reporting',
                    r'(?:no|not)\s+required\s+to\s+(?:report|notify|disclose)'
                ],
                'severity': RiskSeverity.MEDIUM,
                'category': 'Reporting Gap'
            },
            'unclear_obligations': {
                'patterns': [
                    r'(?:may|might|could|should)\s+comply',
                    r'best\s+effort.*compliance',
                    r'(?:attempt|endeavor)\s+to\s+comply',
                    r'compliance.*(?:discretion|optional)'
                ],
                'severity': RiskSeverity.MEDIUM,
                'category': 'Unclear Compliance Obligation'
            },
            'data_breach_risk': {
                'patterns': [
                    r'(?:no|without|lacking)\s+(?:security|encryption)',
                    r'(?:unencrypted|plain\s+text)\s+(?:data|information)',
                    r'(?:no|without)\s+(?:breach|incident)\s+(?:notification|response)',
                    r'security\s+(?:not\s+required|optional)'
                ],
                'severity': RiskSeverity.CRITICAL,
                'category': 'Data Breach Risk'
            }
        }
    
    def analyze(self, contract_text: str, extracted_clauses: List = None) -> List[IdentifiedRisk]:
        """
        Run compliance risk analysis pipeline
        
        Args:
            contract_text: Full contract text
            extracted_clauses: Optional pre-extracted compliance clauses
            
        Returns:
            List of identified compliance risks
        """
        print("🔍 Running Compliance Risk Pipeline...")
        risks = []
        
        # Split into paragraphs for better context
        paragraphs = self._split_paragraphs(contract_text)
        
        # Check for each risk indicator
        for risk_type, config in self.risk_indicators.items():
            for para_idx, paragraph in enumerate(paragraphs):
                for pattern in config['patterns']:
                    matches = re.finditer(pattern, paragraph, re.IGNORECASE)
                    for match in matches:
                        risk = self._create_risk_object(
                            risk_type=risk_type,
                            category=config['category'],
                            severity=config['severity'],
                            match=match,
                            paragraph=paragraph,
                            location=f"Paragraph {para_idx + 1}"
                        )
                        risks.append(risk)
                        break  # One risk per paragraph per type
        
        # Check for missing critical clauses
        missing_risks = self._check_missing_clauses(contract_text)
        risks.extend(missing_risks)
        
        # Sort by severity
        risks.sort(key=lambda r: self._severity_to_score(r.severity), reverse=True)
        
        print(f"✅ Compliance risks identified: {len(risks)}")
        return risks
    
    def _create_risk_object(self, risk_type: str, category: str, severity: RiskSeverity, 
                           match, paragraph: str, location: str) -> IdentifiedRisk:
        """Create a structured risk object"""
        # Extract evidence context
        start = max(0, match.start() - 50)
        end = min(len(paragraph), match.end() + 50)
        evidence = paragraph[start:end].strip()
        
        # Generate description based on risk type
        descriptions = {
            'regulatory_gaps': 'Contract lacks clear regulatory compliance requirements',
            'missing_gdpr': 'Data protection provisions are insufficient or missing',
            'audit_deficiency': 'Audit rights are restricted or not clearly defined',
            'reporting_gap': 'Reporting obligations are unclear or missing',
            'unclear_obligations': 'Compliance obligations use weak or discretionary language',
            'data_breach_risk': 'Security and breach notification provisions are inadequate'
        }
        
        recommendations = {
            'regulatory_gaps': 'Add explicit regulatory compliance requirements and standards',
            'missing_gdpr': 'Include comprehensive GDPR/data protection clauses with consent mechanisms',
            'audit_deficiency': 'Define clear audit rights with access to records and systems',
            'reporting_gap': 'Specify mandatory reporting obligations with timelines',
            'unclear_obligations': 'Change discretionary language to mandatory compliance requirements',
            'data_breach_risk': 'Add security requirements and incident notification procedures'
        }
        
        return IdentifiedRisk(
            risk_type=risk_type,
            category=category,
            severity=severity,
            description=descriptions.get(risk_type, 'Compliance risk identified'),
            evidence=evidence,
            location=location,
            recommendation=recommendations.get(risk_type, 'Review and update clause'),
            score=self._severity_to_score(severity)
        )
    
    def _check_missing_clauses(self, contract_text: str) -> List[IdentifiedRisk]:
        """Check for missing critical compliance clauses"""
        risks = []
        text_lower = contract_text.lower()
        
        critical_clauses = {
            'gdpr': ('GDPR|data protection regulation|personal data processing', 
                    'Missing GDPR/Data Protection compliance', RiskSeverity.CRITICAL),
            'audit': ('audit right|inspection right|right to audit', 
                     'Missing audit rights provision', RiskSeverity.HIGH),
            'confidentiality': ('confidential|non-disclosure|proprietary information', 
                               'Missing confidentiality obligations', RiskSeverity.HIGH),
            'data_breach': ('data breach|security incident|breach notification', 
                           'Missing data breach notification requirements', RiskSeverity.CRITICAL)
        }
        
        for clause_key, (pattern, description, severity) in critical_clauses.items():
            if not re.search(pattern, text_lower):
                risk = IdentifiedRisk(
                    risk_type=f'missing_{clause_key}',
                    category='Missing Critical Clause',
                    severity=severity,
                    description=description,
                    evidence='No relevant clause found in contract',
                    location='Contract-wide',
                    recommendation=f'Add comprehensive {clause_key.replace("_", " ")} provisions',
                    score=self._severity_to_score(severity)
                )
                risks.append(risk)
        
        return risks
    
    def _split_paragraphs(self, text: str) -> List[str]:
        """Split text into paragraphs"""
        paragraphs = re.split(r'\n\n+|---\s*Page\s+\d+\s*---', text)
        return [p.strip() for p in paragraphs if p.strip()]
    
    def _severity_to_score(self, severity: RiskSeverity) -> float:
        """Convert severity to numeric score"""
        scores = {
            RiskSeverity.CRITICAL: 10.0,
            RiskSeverity.HIGH: 7.5,
            RiskSeverity.MEDIUM: 5.0,
            RiskSeverity.LOW: 2.5
        }
        return scores.get(severity, 5.0)


class FinancialRiskPipeline:
    """
    Structured pipeline for financial risk identification
    Analyzes payment risks, hidden costs, unfavorable terms
    """
    
    def __init__(self):
        self.risk_indicators = self._initialize_financial_indicators()
        
    def _initialize_financial_indicators(self) -> Dict:
        """Initialize financial risk indicators"""
        return {
            'payment_risk': {
                'patterns': [
                    r'(?:no|without)\s+(?:payment|invoice)\s+(?:terms|schedule)',
                    r'payment.*(?:discretion|sole\s+discretion)',
                    r'(?:unlimited|unrestricted)\s+(?:payment|fee)',
                    r'payment.*(?:may|might)\s+be'
                ],
                'severity': RiskSeverity.HIGH,
                'category': 'Payment Risk'
            },
            'hidden_costs': {
                'patterns': [
                    r'additional\s+(?:fee|charge|cost|expense)',
                    r'(?:surcharge|markup|premium)',
                    r'plus\s+(?:fee|charge|cost)',
                    r'(?:incidental|miscellaneous)\s+(?:fee|charge|expense)'
                ],
                'severity': RiskSeverity.MEDIUM,
                'category': 'Hidden Costs'
            },
            'penalty_risk': {
                'patterns': [
                    r'penalty.*(?:exceed|unlimited|without\s+limit)',
                    r'late\s+fee.*(?:\d+%|significant|substantial)',
                    r'liquidated\s+damages.*(?:unlimited|discretion)',
                    r'penalty.*(?:discretion|determine)'
                ],
                'severity': RiskSeverity.HIGH,
                'category': 'Excessive Penalty'
            },
            'unfavorable_terms': {
                'patterns': [
                    r'(?:non-refundable|no\s+refund)',
                    r'payment.*(?:advance|upfront).*(?:100%|full|entire)',
                    r'(?:immediate|instant)\s+payment.*(?:required|due)',
                    r'(?:automatic|auto).*(?:renewal|extension).*fee'
                ],
                'severity': RiskSeverity.MEDIUM,
                'category': 'Unfavorable Payment Terms'
            },
            'price_increase': {
                'patterns': [
                    r'(?:increase|raise|adjust).*(?:price|fee|rate).*(?:discretion|without\s+notice)',
                    r'price.*(?:subject\s+to\s+change|variable|fluctuate)',
                    r'(?:annual|periodic).*(?:increase|escalation).*(?:unlimited|uncapped)',
                    r'fee.*(?:may|can)\s+(?:increase|change)'
                ],
                'severity': RiskSeverity.MEDIUM,
                'category': 'Price Increase Risk'
            },
            'cost_allocation': {
                'patterns': [
                    r'(?:all|entire)\s+(?:cost|expense).*(?:borne|paid)\s+by',
                    r'sole\s+(?:cost|expense)',
                    r'(?:reimburse|reimbursement).*(?:no|not\s+required|optional)',
                    r'expense.*(?:discretion|determine)'
                ],
                'severity': RiskSeverity.MEDIUM,
                'category': 'Unfavorable Cost Allocation'
            }
        }
    
    def analyze(self, contract_text: str, extracted_clauses: List = None) -> List[IdentifiedRisk]:
        """
        Run financial risk analysis pipeline
        
        Args:
            contract_text: Full contract text
            extracted_clauses: Optional pre-extracted financial clauses
            
        Returns:
            List of identified financial risks
        """
        print("💰 Running Financial Risk Pipeline...")
        risks = []
        
        paragraphs = self._split_paragraphs(contract_text)
        
        # Check for each risk indicator
        for risk_type, config in self.risk_indicators.items():
            for para_idx, paragraph in enumerate(paragraphs):
                for pattern in config['patterns']:
                    matches = re.finditer(pattern, paragraph, re.IGNORECASE)
                    for match in matches:
                        risk = self._create_risk_object(
                            risk_type=risk_type,
                            category=config['category'],
                            severity=config['severity'],
                            match=match,
                            paragraph=paragraph,
                            location=f"Paragraph {para_idx + 1}"
                        )
                        risks.append(risk)
                        break
        
        # Analyze numeric financial exposure
        exposure_risks = self._analyze_financial_exposure(contract_text)
        risks.extend(exposure_risks)
        
        # Check for missing critical financial terms
        missing_risks = self._check_missing_financial_terms(contract_text)
        risks.extend(missing_risks)
        
        # Sort by severity
        risks.sort(key=lambda r: self._severity_to_score(r.severity), reverse=True)
        
        print(f"✅ Financial risks identified: {len(risks)}")
        return risks
    
    def _create_risk_object(self, risk_type: str, category: str, severity: RiskSeverity,
                           match, paragraph: str, location: str) -> IdentifiedRisk:
        """Create a structured financial risk object"""
        start = max(0, match.start() - 50)
        end = min(len(paragraph), match.end() + 50)
        evidence = paragraph[start:end].strip()
        
        descriptions = {
            'payment_risk': 'Payment terms are unclear or subject to discretion',
            'hidden_costs': 'Additional fees or charges may apply beyond base price',
            'penalty_risk': 'Penalties or late fees appear excessive or unlimited',
            'unfavorable_terms': 'Payment terms favor the other party disproportionately',
            'price_increase': 'Prices may increase without adequate notice or limits',
            'cost_allocation': 'Cost allocation is unfavorable or one-sided'
        }
        
        recommendations = {
            'payment_risk': 'Define clear payment terms with specific amounts and schedules',
            'hidden_costs': 'Request itemized fee schedule and cap on additional charges',
            'penalty_risk': 'Negotiate reasonable penalty caps and grace periods',
            'unfavorable_terms': 'Negotiate more balanced payment terms with refund provisions',
            'price_increase': 'Add price increase caps and advance notice requirements',
            'cost_allocation': 'Negotiate fair cost-sharing arrangements'
        }
        
        return IdentifiedRisk(
            risk_type=risk_type,
            category=category,
            severity=severity,
            description=descriptions.get(risk_type, 'Financial risk identified'),
            evidence=evidence,
            location=location,
            recommendation=recommendations.get(risk_type, 'Review and negotiate terms'),
            score=self._severity_to_score(severity)
        )
    
    def _analyze_financial_exposure(self, contract_text: str) -> List[IdentifiedRisk]:
        """Analyze overall financial exposure and large amounts"""
        risks = []
        
        # Find monetary amounts
        money_patterns = [
            r'(?:USD|EUR|GBP|\$|€|£)\s*(\d+(?:,\d{3})*(?:\.\d{2})?)',
            r'(\d+(?:,\d{3})*(?:\.\d{2})?)\s*(?:USD|EUR|GBP|dollars|euros|pounds)'
        ]
        
        large_amounts = []
        for pattern in money_patterns:
            matches = re.finditer(pattern, contract_text, re.IGNORECASE)
            for match in matches:
                try:
                    amount_str = match.group(1).replace(',', '')
                    amount = float(amount_str)
                    if amount > 100000:  # Flag amounts over $100k
                        large_amounts.append((amount, match.group(0)))
                except:
                    pass
        
        if large_amounts:
            total_exposure = sum(amt for amt, _ in large_amounts)
            risk = IdentifiedRisk(
                risk_type='high_financial_exposure',
                category='Financial Exposure',
                severity=RiskSeverity.HIGH if total_exposure > 500000 else RiskSeverity.MEDIUM,
                description=f'Contract involves significant financial exposure: ${total_exposure:,.2f}',
                evidence=f'Found {len(large_amounts)} large payment amounts',
                location='Contract-wide',
                recommendation='Ensure adequate budget allocation and payment terms protection',
                score=8.0 if total_exposure > 500000 else 6.0
            )
            risks.append(risk)
        
        return risks
    
    def _check_missing_financial_terms(self, contract_text: str) -> List[IdentifiedRisk]:
        """Check for missing critical financial terms"""
        risks = []
        text_lower = contract_text.lower()
        
        critical_terms = {
            'payment_schedule': ('payment.*(?:schedule|due|term)', 
                                'Missing payment schedule or due dates', RiskSeverity.HIGH),
            'pricing': ('(?:price|fee|cost|rate|charge)', 
                       'Missing pricing information', RiskSeverity.CRITICAL),
            'late_payment': ('late.*(?:payment|fee|penalty|interest)', 
                           'Missing late payment terms', RiskSeverity.MEDIUM),
            'currency': ('(?:USD|EUR|GBP|currency|dollar|euro|pound)', 
                        'Missing currency specification', RiskSeverity.MEDIUM)
        }
        
        for term_key, (pattern, description, severity) in critical_terms.items():
            if not re.search(pattern, text_lower):
                risk = IdentifiedRisk(
                    risk_type=f'missing_{term_key}',
                    category='Missing Financial Terms',
                    severity=severity,
                    description=description,
                    evidence='No relevant financial terms found',
                    location='Contract-wide',
                    recommendation=f'Add clear {term_key.replace("_", " ")} provisions',
                    score=self._severity_to_score(severity)
                )
                risks.append(risk)
        
        return risks
    
    def _split_paragraphs(self, text: str) -> List[str]:
        """Split text into paragraphs"""
        paragraphs = re.split(r'\n\n+|---\s*Page\s+\d+\s*---', text)
        return [p.strip() for p in paragraphs if p.strip()]
    
    def _severity_to_score(self, severity: RiskSeverity) -> float:
        """Convert severity to numeric score"""
        scores = {
            RiskSeverity.CRITICAL: 10.0,
            RiskSeverity.HIGH: 7.5,
            RiskSeverity.MEDIUM: 5.0,
            RiskSeverity.LOW: 2.5
        }
        return scores.get(severity, 5.0)


class RiskAnalyzer:
    """
    Main risk analyzer coordinating compliance and financial risk pipelines
    """
    
    def __init__(self):
        self.compliance_pipeline = ComplianceRiskPipeline()
        self.financial_pipeline = FinancialRiskPipeline()
    
    def analyze_all_risks(self, contract_text: str) -> Dict[str, List[IdentifiedRisk]]:
        """
        Run both compliance and financial risk pipelines
        
        Returns:
            Dictionary with 'compliance' and 'finance' risk lists
        """
        print("\n🔍 Starting Risk Analysis Pipelines...")
        print("=" * 60)
        
        results = {
            'compliance': self.compliance_pipeline.analyze(contract_text),
            'finance': self.financial_pipeline.analyze(contract_text)
        }
        
        print(f"\n📊 Risk Analysis Complete:")
        print(f"   Compliance Risks: {len(results['compliance'])}")
        print(f"   Financial Risks: {len(results['finance'])}")
        
        return results
    
    def get_risk_summary(self, risks: Dict[str, List[IdentifiedRisk]]) -> Dict:
        """Generate risk summary statistics"""
        summary = {
            'total_risks': 0,
            'by_severity': {
                'Critical': 0,
                'High': 0,
                'Medium': 0,
                'Low': 0
            },
            'by_category': {},
            'critical_risks': []
        }
        
        for domain, risk_list in risks.items():
            summary['total_risks'] += len(risk_list)
            
            for risk in risk_list:
                # Count by severity
                summary['by_severity'][risk.severity.value] += 1
                
                # Count by category
                category = risk.category
                summary['by_category'][category] = summary['by_category'].get(category, 0) + 1
                
                # Collect critical risks
                if risk.severity == RiskSeverity.CRITICAL:
                    summary['critical_risks'].append({
                        'domain': domain,
                        'category': risk.category,
                        'description': risk.description
                    })
        
        return summary


if __name__ == "__main__":
    # Test the risk analyzer
    print("Risk Analysis Pipelines - Week 3")
    print("=" * 60)
    
    sample_contract = """
    SERVICE AGREEMENT
    
    Payment is due at the discretion of the Client. Additional fees and surcharges may apply.
    Late payment penalty of 5% per month will be charged without limit.
    
    All costs and expenses shall be borne by the Contractor. Non-refundable advance payment 
    of $250,000 is required immediately upon signing.
    
    This contract does not include audit rights. Security measures are optional and at
    the discretion of the parties.
    
    Price may increase without notice. The contract automatically renews with additional fees.
    """
    
    analyzer = RiskAnalyzer()
    risks = analyzer.analyze_all_risks(sample_contract)
    
    print("\n" + "=" * 60)
    print("COMPLIANCE RISKS:")
    for risk in risks['compliance'][:5]:
        print(f"\n[{risk.severity.value}] {risk.category}")
        print(f"  Description: {risk.description}")
        print(f"  Evidence: {risk.evidence[:80]}...")
        print(f"  Recommendation: {risk.recommendation}")
    
    print("\n" + "=" * 60)
    print("FINANCIAL RISKS:")
    for risk in risks['finance'][:5]:
        print(f"\n[{risk.severity.value}] {risk.category}")
        print(f"  Description: {risk.description}")
        print(f"  Evidence: {risk.evidence[:80]}...")
        print(f"  Recommendation: {risk.recommendation}")
    
    summary = analyzer.get_risk_summary(risks)
    print(f"\n" + "=" * 60)
    print(f"SUMMARY: {summary['total_risks']} total risks identified")
    print(f"Critical: {summary['by_severity']['Critical']}, High: {summary['by_severity']['High']}")
