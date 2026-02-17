"""
Missing Clause Detector Module
Identifies critical clauses that should be present but are missing from contracts.
"""

from typing import List, Dict
from dataclasses import dataclass

@dataclass
class MissingClause:
    """Represents a missing critical clause"""
    clause_name: str
    category: str
    importance: str  # CRITICAL, HIGH, MEDIUM
    reason: str
    recommendation: str

class MissingClauseDetector:
    """Detects missing critical clauses in legal contracts"""
    
    # Define critical clauses that should be present
    CRITICAL_CLAUSES = {
        "compliance": [
            {
                "name": "Data Protection Clause",
                "keywords": ["data protection", "gdpr", "personal data", "privacy", "data security"],
                "importance": "CRITICAL",
                "reason": "Required for GDPR/CCPA compliance and data privacy regulations",
                "recommendation": "Add comprehensive data protection clause covering collection, storage, and processing of personal data"
            },
            {
                "name": "Anti-Corruption Clause",
                "keywords": ["anti-corruption", "bribery", "fcpa", "anti-bribery"],
                "importance": "HIGH",
                "reason": "Required for compliance with FCPA and international anti-corruption laws",
                "recommendation": "Include anti-corruption provisions prohibiting bribes and kickbacks"
            },
            {
                "name": "Regulatory Compliance",
                "keywords": ["regulatory compliance", "laws and regulations", "applicable law", "legal compliance"],
                "importance": "HIGH",
                "reason": "Ensures parties comply with all applicable laws and regulations",
                "recommendation": "Add clause requiring compliance with all relevant industry regulations"
            }
        ],
        "legal": [
            {
                "name": "Dispute Resolution Clause",
                "keywords": ["dispute resolution", "arbitration", "mediation", "litigation"],
                "importance": "CRITICAL",
                "reason": "Defines how conflicts will be resolved, avoiding costly litigation",
                "recommendation": "Specify arbitration or mediation procedures for dispute resolution"
            },
            {
                "name": "Governing Law",
                "keywords": ["governing law", "jurisdiction", "applicable law", "laws of"],
                "importance": "CRITICAL",
                "reason": "Establishes which jurisdiction's laws apply to the contract",
                "recommendation": "Clearly specify the governing law and jurisdiction"
            },
            {
                "name": "Termination for Convenience",
                "keywords": ["termination for convenience", "terminate without cause", "early termination"],
                "importance": "HIGH",
                "reason": "Allows parties to exit the agreement under defined circumstances",
                "recommendation": "Include termination clause with notice period and exit procedures"
            },
            {
                "name": "Force Majeure",
                "keywords": ["force majeure", "act of god", "natural disaster", "unforeseeable circumstances"],
                "importance": "HIGH",
                "reason": "Protects parties from liability due to uncontrollable events",
                "recommendation": "Add force majeure clause covering natural disasters, pandemics, and other unforeseeable events"
            }
        ],
        "financial": [
            {
                "name": "Payment Terms",
                "keywords": ["payment terms", "payment schedule", "invoice", "payment due"],
                "importance": "CRITICAL",
                "reason": "Defines when and how payments will be made",
                "recommendation": "Specify clear payment schedules, methods, and late payment penalties"
            },
            {
                "name": "Limitation of Liability",
                "keywords": ["limitation of liability", "liability cap", "maximum liability", "damages limit"],
                "importance": "CRITICAL",
                "reason": "Caps financial exposure and limits potential damages",
                "recommendation": "Include liability limitations with specific monetary caps"
            },
            {
                "name": "Indemnification",
                "keywords": ["indemnification", "indemnify", "hold harmless", "defend"],
                "importance": "HIGH",
                "reason": "Protects parties from third-party claims and losses",
                "recommendation": "Add mutual indemnification provisions with clear scope and limitations"
            },
            {
                "name": "Price Adjustment Clause",
                "keywords": ["price adjustment", "escalation", "inflation adjustment", "cost increase"],
                "importance": "MEDIUM",
                "reason": "Protects against inflation and cost increases over time",
                "recommendation": "Consider adding price adjustment mechanism tied to inflation index"
            }
        ],
        "operational": [
            {
                "name": "Confidentiality Clause",
                "keywords": ["confidentiality", "non-disclosure", "confidential information", "proprietary"],
                "importance": "CRITICAL",
                "reason": "Protects sensitive business information and trade secrets",
                "recommendation": "Include comprehensive confidentiality obligations with defined term"
            },
            {
                "name": "Intellectual Property Rights",
                "keywords": ["intellectual property", "ip rights", "patent", "copyright", "trademark", "ownership"],
                "importance": "CRITICAL",
                "reason": "Clarifies ownership of IP created during contract term",
                "recommendation": "Define IP ownership, licensing rights, and work-for-hire provisions"
            },
            {
                "name": "Service Level Agreement (SLA)",
                "keywords": ["service level", "sla", "performance metrics", "uptime", "availability"],
                "importance": "HIGH",
                "reason": "Defines expected service quality and performance standards",
                "recommendation": "Add SLA with specific performance metrics and remedies for non-compliance"
            },
            {
                "name": "Change Management",
                "keywords": ["change order", "amendment", "modification", "change request"],
                "importance": "MEDIUM",
                "reason": "Establishes process for making changes to the agreement",
                "recommendation": "Include change management procedures requiring written approval"
            },
            {
                "name": "Insurance Requirements",
                "keywords": ["insurance", "coverage", "liability insurance", "workers compensation"],
                "importance": "HIGH",
                "reason": "Ensures adequate insurance coverage for potential liabilities",
                "recommendation": "Specify required insurance types and minimum coverage amounts"
            }
        ]
    }
    
    def __init__(self):
        """Initialize the missing clause detector"""
        pass
    
    def detect_missing_clauses(self, document_text: str, extracted_clauses: List[Dict]) -> List[MissingClause]:
        """
        Detect missing critical clauses in the contract
        
        Args:
            document_text: Full text of the contract
            extracted_clauses: List of clauses already extracted
            
        Returns:
            List of MissingClause objects
        """
        missing_clauses = []
        document_lower = document_text.lower()
        
        # Get set of extracted clause types
        extracted_types = {clause.get('type', '').lower() for clause in extracted_clauses}
        extracted_text = ' '.join([clause.get('text', '') for clause in extracted_clauses]).lower()
        
        # Check each critical clause category
        for category, clauses in self.CRITICAL_CLAUSES.items():
            for clause_def in clauses:
                # Check if clause is present using keywords
                if not self._is_clause_present(document_lower, extracted_text, clause_def):
                    missing_clauses.append(MissingClause(
                        clause_name=clause_def["name"],
                        category=category,
                        importance=clause_def["importance"],
                        reason=clause_def["reason"],
                        recommendation=clause_def["recommendation"]
                    ))
        
        # Sort by importance (CRITICAL first)
        importance_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2}
        missing_clauses.sort(key=lambda x: importance_order.get(x.importance, 3))
        
        return missing_clauses
    
    def _is_clause_present(self, document_text: str, extracted_text: str, clause_def: Dict) -> bool:
        """Check if a clause is present in the document using keyword matching"""
        keywords = clause_def.get("keywords", [])
        
        # Check if any keyword appears in document
        for keyword in keywords:
            if keyword in document_text or keyword in extracted_text:
                return True
        
        return False
    
    def get_missing_clause_summary(self, missing_clauses: List[MissingClause]) -> Dict:
        """
        Generate summary statistics for missing clauses
        
        Returns:
            Dictionary with summary statistics
        """
        if not missing_clauses:
            return {
                "total_missing": 0,
                "critical_missing": 0,
                "high_missing": 0,
                "medium_missing": 0,
                "by_category": {},
                "completion_score": 100.0
            }
        
        # Count by importance
        critical_count = sum(1 for c in missing_clauses if c.importance == "CRITICAL")
        high_count = sum(1 for c in missing_clauses if c.importance == "HIGH")
        medium_count = sum(1 for c in missing_clauses if c.importance == "MEDIUM")
        
        # Count by category
        by_category = {}
        for clause in missing_clauses:
            category = clause.category
            if category not in by_category:
                by_category[category] = 0
            by_category[category] += 1
        
        # Calculate completion score (inverse of missing clauses)
        total_critical_clauses = sum(
            len([c for c in clauses if c["importance"] == "CRITICAL"])
            for clauses in self.CRITICAL_CLAUSES.values()
        )
        completion_score = max(0, 100 - (critical_count * 10 + high_count * 5 + medium_count * 2))
        
        return {
            "total_missing": len(missing_clauses),
            "critical_missing": critical_count,
            "high_missing": high_count,
            "medium_missing": medium_count,
            "by_category": by_category,
            "completion_score": round(completion_score, 1)
        }
